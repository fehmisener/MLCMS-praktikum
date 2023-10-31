from util import read_scenario

import tkinter
from tkinter import Button, Canvas, Menu, Label, messagebox, Toplevel, StringVar, END
from tkinter import filedialog
from tkinter import ttk

from scenario_elements import Scenario


class MainGUI():
    """
    Defines a simple graphical user interface.
    To start, use the `start_gui` method.
    """

    def __init__(self):
        self.simulation_data = {
            "pedestrians": [],
            "targets": [],
            "obstacles": []
        }
        self.step_count = 0

    def create_scenario(self, ):
        """
        Initialize a new scenario for the GUI.

        This method initializes a new scenario for the graphical user interface (GUI) by resetting the simulation data.
        It sets the step count to zero and updates the corresponding label. Then, it opens the popup window to allow
        the user to create and place objects in the new scenario.

        Note:
        - The method clears any existing simulation data, setting the `pedestrians`, `targets`, and `obstacles` lists
        to empty.
        - It sets the step count to zero and updates the corresponding label to reflect the new scenario.
        - After resetting the scenario, it opens the `popup` window to allow the user to create and place objects in
        the new scenario.
        """
        self.step_count = 0
        self.label.config(
            text='Simulation Step Count: ' + str(self.step_count))
        self.popup()

    def restart_scenario(self, ):
        """
        Restart and display the current scenario.

        This method reinitializes and displays the current scenario, allowing the user to restart the scenario
        as it was originally loaded.

        Parameters:
        - self: The instance of the class this method belongs to.

        Returns:
        - None

        Note:
        - The method only restart latest `Scenario` instance.
        - This method is useful when the user wants to reset the scenario to its original state after making changes.
        """
        self.step_count = 0
        self.label.config(
            text='Simulation Step Count: ' + str(self.step_count))

        self.sc = Scenario(self.simulation_data["height"], self.simulation_data["width"])
        self.sc.init_from_file(self.simulation_data)
        self.sc.to_image(self.canvas, self.canvas_image)

    def step_scenario(self, scenario, canvas, canvas_image):
        """
        Moves the simulation forward by one step, visualizes the result and increments step count.
        It also checks if the simulaiton is loaded to start the game.

        Args:
            scenario (scenario_elements.Scenario): Add _description_
            canvas (tkinter.Canvas): Add _description_
            canvas_image (missing _type_): Add _description_
        """

        if (self.simulation_data is not None and len(self.simulation_data["targets"]) > 0 and len(self.simulation_data["pedestrians"]) > 0):
            self.step_count += 1
            self.label.config(
                text='Simulation Step Count: ' + str(self.step_count))
            scenario.update_step()
            scenario.to_image(canvas, canvas_image)
        else:
            messagebox.showerror(
                'Cellular Automata GUI Warning', 'Warning: Please upload valid (should contain at least one target and pedestrians) simulation first!')

    def exit_gui(self, ):
        """
        Close the GUI.
        """
        sys.exit()

    def load_scenario(self):
        """
        Load and display a scenario from a JSON file using a file dialog.

        This method allows the user to select a JSON file containing a scenario using a file dialog. It reads
        the scenario data from the file, initializes a Scenario instance, and displays it on the canvas.

        Parameters:
        - self: The instance of the class this method belongs to.

        Returns:
        - None

        Note:
        - It reads the scenario data from the selected file and stores it in the `simulation_data` attribute.
        - The user can cancel the file dialog, in which case the method returns without loading a scenario.
        """
        self.simulation_data = {
            "pedestrians": [],
            "targets": [],
            "obstacles": []
        }
        self.step_count = 0

        input_file = filedialog.askopenfilename(filetypes=[("Json", '*.json')])
        if not input_file:
            return

        self.simulation_data = read_scenario(input_file)

        self.sc = Scenario(
            self.simulation_data["height"], self.simulation_data["width"])
        self.sc.init_from_file(self.simulation_data)
        self.sc.to_image(self.canvas, self.canvas_image)

    def popup(self):
        """
        Display a popup window for user input and object placement in the GUI.

        This method creates a popup window that allows the user to input object details such as height, width,
        object type (PEDESTRIAN, TARGET, or OBSTACLE), location coordinates (X and Y), and additional attributes
        such as speed for pedestrians. The user can submit the input, and the entered data is added to the scenario
        being displayed on the canvas.

        Parameters:
        - self: The instance of the class this method belongs to.

        Returns:
        - None

        Note:
        - The popup window allows the user to specify object parameters like height, width, type, location
        coordinates, and additional attributes for pedestrians.
        - When the user selects "PEDESTRIAN" as the object type, an additional input field for "Speed" is displayed.
        - The "Submit" button adds the entered object data to the scenario being displayed on the canvas.
        - The "Start" button initializes the scenario based on the entered height and width and displays it
        on the canvas. The popup window is closed after the scenario is started. Without start, you can not see your
        data on the canvas.
        """
        temp_simulation_data =  {
                "pedestrians": [],
                "targets": [],
                "obstacles": []
            }
        popup_window = Toplevel(self.win)
        popup_window.title("Popup")

        # Height element - input box
        height_label = Label(popup_window, text="Height:")
        height_label.grid(row=0, column=0, padx=5, pady=5)

        height_var = StringVar()
        height_entry = ttk.Entry(popup_window, textvariable=height_var)
        height_entry.grid(row=0, column=1, padx=5, pady=5)

        # Width element - select box
        width_label = Label(popup_window, text="Width:")
        width_label.grid(row=1, column=0, padx=5, pady=5)

        width_var = StringVar()
        width_entry = ttk.Entry(popup_window, textvariable=width_var)
        width_entry.grid(row=1, column=1, padx=5, pady=5)

        separator = ttk.Separator(popup_window, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=2,
                       sticky="ew", padx=5, pady=5)

        # Object Type - select box
        select_label = Label(popup_window, text="Select:")
        select_label.grid(row=3, column=0, padx=5, pady=5)

        select_var = StringVar()
        select_box = ttk.Combobox(popup_window, textvariable=select_var, values=[
                                  "PEDESTRIAN", "TARGET", "OBSTACLE"])
        select_box.grid(row=3, column=1, padx=5, pady=5)

        # Location X - input box
        input1_label = Label(popup_window, text="Location X:")
        input1_label.grid(row=4, column=0, padx=5, pady=5)

        input1_var = StringVar()
        input1_entry = ttk.Entry(popup_window, textvariable=input1_var)
        input1_entry.grid(row=4, column=1, padx=5, pady=5)

        # Location Y - input box
        input2_label = Label(popup_window, text="Location Y:")
        input2_label.grid(row=5, column=0, padx=5, pady=5)

        input2_var = StringVar()
        input2_entry = ttk.Entry(popup_window, textvariable=input2_var)
        input2_entry.grid(row=5, column=1, padx=5, pady=5)

        def show_additional_input():
            if select_var.get() == "PEDESTRIAN":
                additional_input_label.grid(row=6, column=0, padx=5, pady=5)
                additional_input_entry.grid(row=6, column=1, padx=5, pady=5)
            else:
                additional_input_label.grid_remove()
                additional_input_entry.grid_remove()

        additional_input_label = ttk.Label(popup_window, text="Speed:")
        additional_input_var = StringVar()
        additional_input_entry = ttk.Entry(
            popup_window, textvariable=additional_input_var)

        select_box.bind("<<ComboboxSelected>>",
                        lambda event: show_additional_input())

        def submit():
            input1_value = int(input1_var.get())
            input2_value = int(input2_var.get())

            if (select_var.get() == "PEDESTRIAN"):
                additional_input_value = int(additional_input_var.get())
                temp_simulation_data[select_var.get().lower(
                ) + "s"].append({"locationX": input1_value, "locationY": input2_value, "speed": additional_input_value})
            else:
                temp_simulation_data[select_var.get().lower(
                ) + "s"].append({"locationX": input1_value, "locationY": input2_value})

            input1_entry.delete(0, END)
            input2_entry.delete(0, END)
            additional_input_entry.delete(0, END)

        def start():
            self.simulation_data = temp_simulation_data

            self.sc = Scenario(int(height_var.get()), int(width_var.get()))
            self.sc.init_from_file(self.simulation_data)
            self.sc.to_image(self.canvas, self.canvas_image)

            popup_window.protocol("WM_DELETE_WINDOW", popup_window.destroy())

        submit_button = Button(popup_window, text="Submit", command=submit)
        submit_button.grid(row=6, column=3, columnspan=2, padx=5, pady=5)

        submit_button = Button(popup_window, text="Start", command=start)
        submit_button.grid(row=6, column=5, columnspan=2, padx=5, pady=5)

    def start_gui(self, ):
        """
        Creates and shows a simple user interface with a menu and multiple buttons.
        Only one button works at the moment: "step simulation".
        Also creates a rudimentary, fixed Scenario instance with three Pedestrian instances and multiple targets.
        """
        self.win = tkinter.Tk()
        self.win.geometry('800x600')  # setting the size of the window
        self.win.title('Cellular Automata GUI')

        menu = Menu(self.win)
        self.win.config(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label='Simulation', menu=file_menu)
        file_menu.add_command(label='New', command=self.create_scenario)
        file_menu.add_command(label='Restart', command=self.restart_scenario)
        file_menu.add_command(label='Close', command=self.exit_gui)
        file_menu.add_command(label='Load', command=lambda: self.load_scenario)

        # creating the canvas
        self.canvas = Canvas(
            self.win, width=Scenario.GRID_SIZE[0], height=Scenario.GRID_SIZE[1])
        self.canvas_image = self.canvas.create_image(
            5, 50, image=None, anchor=tkinter.NW)
        self.canvas.pack()

        self.sc = Scenario(100, 100)
        self.sc.to_image(self.canvas, self.canvas_image)

        # can be used to show the target grid instead
        # sc.target_grid_to_image(canvas, canvas_image)

        btn = Button(self.win, text='Create simulation',
                     command=self.create_scenario)
        btn.place(x=20, y=10)

        btn = Button(self.win, text='Restart simulation',
                     command=self.restart_scenario)
        btn.place(x=200, y=10)

        btn = Button(self.win, text='Step simulation', command=lambda: self.step_scenario(
            self.sc, self.canvas, self.canvas_image))
        btn.place(x=380, y=10)

        btn = Button(self.win, text='Load simulation',
                     command=self.load_scenario)
        btn.place(x=580, y=10)

        self.label = Label(self.win, text='Simulation Step Count')
        self.label.config(
            text='Simulation Step Count: ' + str(self.step_count))
        self.label.place(x=295, y=510)
        self.win.mainloop()
