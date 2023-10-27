import sys
from util import read_scenario

import tkinter
from tkinter import Button, Canvas, Menu
from tkinter import filedialog

from scenario_elements import Scenario, Pedestrian


class MainGUI():
    """
    Defines a simple graphical user interface.
    To start, use the `start_gui` method.
    """

    def __init__(self):
        self.loaded_data = None

    def create_scenario(self, ):
        print('create not implemented yet')

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
        self.sc = Scenario(100, 100)
        self.sc.init_from_file(self.loaded_data)
        self.sc.to_image(self.canvas, self.canvas_image)

    def step_scenario(self, scenario, canvas, canvas_image):
        """
        Moves the simulation forward by one step, and visualizes the result.

        Args:
            scenario (scenario_elements.Scenario): Add _description_
            canvas (tkinter.Canvas): Add _description_
            canvas_image (missing _type_): Add _description_
        """
        scenario.update_step()
        scenario.to_image(canvas, canvas_image)

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
        - It reads the scenario data from the selected file and stores it in the `loaded_data` attribute.
        - The user can cancel the file dialog, in which case the method returns without loading a scenario.
        """
        input_file = filedialog.askopenfilename(filetypes=[("Json", '*.json')])
        if not input_file:
            return

        self.loaded_data = read_scenario(input_file)

        self.sc = Scenario(self.loaded_data["height"], self.loaded_data["width"])
        self.sc.init_from_file(self.loaded_data)

        self.canvas.height = self.loaded_data["height"]
        self.canvas.width = self.loaded_data["width"]

        self.sc.to_image(self.canvas, self.canvas_image)

    def start_gui(self, ):
        """
        Creates and shows a simple user interface with a menu and multiple buttons.
        Only one button works at the moment: "step simulation".
        Also creates a rudimentary, fixed Scenario instance with three Pedestrian instances and multiple targets.
        """
        win = tkinter.Tk()
        win.geometry('800x600')  # setting the size of the window
        win.title('Cellular Automata GUI')

        menu = Menu(win)
        win.config(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label='Simulation', menu=file_menu)
        file_menu.add_command(label='New', command=self.create_scenario)
        file_menu.add_command(label='Restart', command=self.restart_scenario)
        file_menu.add_command(label='Close', command=self.exit_gui)
        file_menu.add_command(label='Load', command=lambda: self.load_scenario)

        self.canvas = Canvas(win, width=Scenario.GRID_SIZE[0], height=Scenario.GRID_SIZE[1])  # creating the canvas
        self.canvas_image = self.canvas.create_image(5, 50, image=None, anchor=tkinter.NW)
        self.canvas.pack()

        self.sc = Scenario(100, 100)
        self.sc.to_image(self.canvas, self.canvas_image)

        # can be used to show the target grid instead
        # sc.target_grid_to_image(canvas, canvas_image)

        btn = Button(win, text='Step simulation', command=lambda: self.step_scenario(
            self.sc, self.canvas, self.canvas_image))
        btn.place(x=20, y=10)
        btn = Button(win, text='Restart simulation',
                     command=self.restart_scenario)
        btn.place(x=200, y=10)
        btn = Button(win, text='Create simulation',
                     command=self.create_scenario)
        btn.place(x=380, y=10)
        btn = Button(win, text='Load simulation', command=self.load_scenario)
        btn.place(x=580, y=10)

        win.mainloop()
