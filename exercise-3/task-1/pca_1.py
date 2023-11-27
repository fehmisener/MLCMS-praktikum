import numpy as np
import matplotlib.pyplot as plt

# Load the dataset from the file pca_dataset.txt
data = np.loadtxt('../data/pca_dataset.txt')

# Center the data by subtracting the mean
mean_data = np.mean(data, axis=0)
centered_data = data - mean_data

# Perform Singular Value Decomposition (SVD)
U, S, Vt = np.linalg.svd(centered_data, full_matrices=False)

# Calculate the energy (variance) contained in each principal component
total_energy = np.sum(S**2)
energy_in_components = S**2 / total_energy

# Choose the number of components to use for dimensionality reduction
num_components = 2  # You can adjust this based on your requirements

# Project the data onto the selected components
projected_data = np.dot(centered_data, Vt[:num_components, :].T)

# Plot the original data
plt.scatter(data[:, 0], data[:, 1], label='Original Data')

# Plot the principal components with smaller arrows
for i in range(num_components):
    plt.arrow(mean_data[0], mean_data[1], Vt[i, 0], Vt[i, 1], color='r', width=0.01, head_width=0.05)
    plt.text(mean_data[0] + Vt[i, 0], mean_data[1] + Vt[i, 1], f'PC{i + 1}', color='r', fontsize=12)

plt.title('Principal Component Analysis')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()

# Display the energy in each principal component
for i in range(num_components):
    print(f'Energy in Principal Component {i + 1}: {energy_in_components[i] * 100:.2f}%')
