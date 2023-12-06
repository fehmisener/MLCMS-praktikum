# +
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def mu(b, I, mu0, mu1):
    """
    Recovery rate.
    
    :param b: number of beds per 10,000 persons
    :param I: number of infective persons
    :param mu0: minimum recovery rate based on the number of available beds
    :param mu1: maximum recovery rate based on the number of available beds
    :returns: recovery rate mu
    """
    # recovery rate, depends on mu0, mu1, b
    mu = mu0 + (mu1 - mu0) * (b/(I+b))
    return mu


# -

def R0(beta, d, nu, mu1):
    """
    Basic reproduction number.
    
    :param beta: average number of adequate contacts per unit time with infectious individuals
    :param d: per capita natural death rate
    :param nu: per capita disease-induced death rate
    :param mu1: maximum recovery rate based on the number of available beds
    :returns: basic reproduction number
    """
    return beta / (d + nu + mu1)

# +


def h(I, mu0, mu1, beta, A, d, nu, b):
    """
    Indicator function for bifurcations.
    
    :param I: number of infective persons
    :param mu0: minimum recovery rate based on the number of available beds
    :param mu1: maximum recovery rate based on the number of available beds
    :param beta: average number of adequate contacts per unit time with infectious individuals
    :param A: “recruitment rate” (or birth rate) of susceptible population
    :param d: per capita natural death rate
    :param nu: per capita disease-induced death rate
    :param b: number of beds per 10,000 persons
    :returns: indicator function for bifurcations
    """
    c0 = b**2 * d * A
    c1 = b * ((mu0-mu1+2*d) * A + (beta-nu)*b*d)
    c2 = (mu1-mu0)*b*nu + 2*b*d*(beta-nu)+d*A
    c3 = d*(beta-nu)
    res = c0 + c1 * I + c2 * I**2 + c3 * I**3
    return res


# -

def model(t, y, mu0, mu1, beta, A, d, nu, b):
    """
    SIR model including hospitalization and natural death.
    
    :param mu0: minimum recovery rate based on the number of available beds
    :param mu1: maximum recovery rate based on the number of available beds
    :param beta: average number of adequate contacts per unit time with infectious individuals
    :param A: “recruitment rate” (or birth rate) of susceptible population
    :param d: per capita natural death rate
    :param nu: per capita disease-induced death rate
    :param b: number of beds per 10,000 persons
    """
    S,I,R = y[:]
    m = mu(b, I, mu0, mu1)
    
    dSdt = A - d * S - (beta * S * I) / (S + I + R)
    dIdt = - (d + nu) * I - m * I + (beta * S * I) / (S + I + R)
    dRdt = m * I - d * R
    
    return [dSdt, dIdt, dRdt]


# +
def plot_SIR_behaviour(sol, b, mu0, mu1, beta, A, d, nu):
    """
    Creates three plots:
        1- evolution of the S, I and R variables over time
        2- compares the recovery rate (mu) with the number of infected persons (I) over time
        3- shows the indicator function for bifurcations 
    
    :param sol: solution of the system 
    :param b: number of beds per 10,000 persons
    :param mu0: minimum recovery rate based on the number of available beds
    :param mu1: maximum recovery rate based on the number of available beds
    :param beta: average number of adequate contacts per unit time with infectious individuals
    :param A: “recruitment rate” (or birth rate) of susceptible population
    :param d: per capita natural death rate
    :param nu: per capita disease-induced death rate
    """
    
    # plot of the evolution of the S, I and R variables over time
    fig,ax = plt.subplots(1,3,figsize=(15,5))
    ax[0].plot(sol.t, sol.y[0]-0*sol.y[0][0], label='1E0*susceptible');
    ax[0].plot(sol.t, 1e3*sol.y[1]-0*sol.y[1][0], label='1E3*infective');
    ax[0].plot(sol.t, 1e1*sol.y[2]-0*sol.y[2][0], label='1E1*removed');
    ax[0].set_xlim([0, 500])
    ax[0].legend();
    ax[0].set_xlabel("time")
    ax[0].set_ylabel(r"$S,I,R$")

    # plot of the comparison between the recovery rate (mu) with the number of infected persons (I) over time
    ax[1].plot(sol.t, mu(b, sol.y[1], mu0, mu1), label='recovery rate')
    ax[1].plot(sol.t, 1e2*sol.y[1], label='1E2*infective');
    ax[1].set_xlim([0, 500])
    ax[1].legend();
    ax[1].set_xlabel("time")
    ax[1].set_ylabel(r"$\mu,I$")

    # plot of the indicator function for bifurcations 
    I_h = np.linspace(-0.,0.05,100)
    ax[2].plot(I_h, h(I_h, mu0, mu1, beta, A, d, nu, b));
    ax[2].plot(I_h, 0*I_h, 'r:')
    #ax[2].set_ylim([-0.1,0.05])
    ax[2].set_title("Indicator function h(I)")
    ax[2].set_xlabel("I")
    ax[2].set_ylabel("h(I)")

    fig.tight_layout()
    
def plot_SIR_trajectories(t_0, b, mu0, mu1, beta, A, d, nu, rtol, atol):
    """
    function to plot trajectories of the three initial points of the point 3 of the task
    
    :param t_0: initial time
    :param b: number of beds per 10,000 persons
    :param mu0: minimum recovery rate in the SIR model
    :param mu1: maximum recovery rate in the SIR model
    :param beta: average number of adequate contacts per unit time with infectious individuals
    :param A: “recruitment rate” (or birth rate) of susceptible population
    :param d: per capita natural death rate
    :param nu: per capita disease-induced death rate
    :param rtol: tolerance to avoid qualitatively wrong results
    :param atol: tolerance to avoid qualitatively wrong results
    """
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111,projection="3d")
    NT = 10000
    time = np.linspace(t_0,15000,NT)
    
    SIM0 = [195.3, 0.052, 4.4] # what happens with this initial condition when b=0.022? -- it progresses VERY slowly. Needs t_end to be super large.
    sol = solve_ivp(model, t_span=[time[0],time[-1]], y0=SIM0, t_eval=time, args=(
        mu0, mu1, beta, A, d, nu, b), method='DOP853', rtol=rtol, atol=atol)
    ax.plot(sol.y[0], sol.y[1], sol.y[2], 'r-');
    ax.scatter(sol.y[0], sol.y[1], sol.y[2], s=1, c="red");
    

    SIM0 = [195.7, 0.03, 3.92] # what happens with this initial condition when b=0.022?
    sol = solve_ivp(model, t_span=[time[0],time[-1]], y0=SIM0, t_eval=time, args=(
        mu0, mu1, beta, A, d, nu, b), method='DOP853', rtol=rtol, atol=atol)
    ax.plot(sol.y[0], sol.y[1], sol.y[2], 'b-');
    ax.scatter(sol.y[0], sol.y[1], sol.y[2], s=1, c="blue");

    SIM0 = [193, 0.08, 6.21] # what happens with this initial condition when b=0.022?
    sol = solve_ivp(model, t_span=[time[0],time[-1]], y0=SIM0, t_eval=time, args=(
        mu0, mu1, beta, A, d, nu, b), method='DOP853', rtol=rtol, atol=atol)
    ax.plot(sol.y[0], sol.y[1], sol.y[2], 'g-');
    ax.scatter(sol.y[0], sol.y[1], sol.y[2], s=1, c="green");

    ax.set_xlabel("S")
    ax.set_ylabel("I")
    ax.set_zlabel("R")

    ax.set_title(f"SIR trajectory with b: {b}")
