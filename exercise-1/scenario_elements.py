import scipy.spatial.distance
from PIL import Image, ImageTk
import numpy as np

from util import read_scenario


class Pedestrian:
    """
    Defines a single pedestrian.
    """

    def __init__(self, position, desired_speed):
        self._position = position
        self._desired_speed = desired_speed

    @property
    def position(self):
        return self._position

    @property
    def desired_speed(self):
        return self._desired_speed

    def get_neighbors(self, scenario):
        """
        Compute all neighbors in a 9 cell neighborhood of the current position.
        :param scenario: The scenario instance.
        :return: A list of neighbor cell indices (x,y) around the current position.
        """
        return [
            (int(x + self._position[0]), int(y + self._position[1]))
            for x in [-1, 0, 1]
            for y in [-1, 0, 1]
            if 0 <= x + self._position[0] < scenario.width and 0 <= y + self._position[1] < scenario.height and np.abs(x) + np.abs(y) > 0
        ]

    def update_step(self, scenario):
        """
        Moves to the cell with the lowest distance to the target.
        This does not take obstacles or other pedestrians into account.
        Pedestrians can occupy the same cell.

        :param scenario: The current scenario instance.
        """
        neighbors = self.get_neighbors(scenario)
        next_cell_distance = scenario.target_distance_grids[self._position[0]
                                                            ][self._position[1]]
        next_pos = self._position
        for (n_x, n_y) in neighbors:
            if next_cell_distance > scenario.target_distance_grids[n_x, n_y] and not self.encounter_obstacle(n_x, n_y, scenario.obstacles):
                next_pos = (n_x, n_y)
                next_cell_distance = scenario.target_distance_grids[n_x, n_y]
        self._position = next_pos

    def encounter_obstacle(self, next_cellX, next_cellY, obstacle_list):
        """
        Determine if the next cell at coordinates (next_cellX, next_cellY) contains an obstacle.

        This method checks if the given coordinates (next_cellX, next_cellY) match any of the obstacles
        stored in the `obstacle_list`.

        Parameters:
        - self: The instance of the class this method belongs to.
        - next_cellX (int): The X-coordinate of the next cell to check.
        - next_cellY (int): The Y-coordinate of the next cell to check.
        - obstacle_list (list of array): A list of obstacle coordinates, where each element is a list
        containing the X and Y coordinates of an obstacle cell.

        Returns:
        - bool: True if an obstacle is found at the specified coordinates; otherwise, False.

        Example:
        ```python
        obstacle_list = [(2, 3), (4, 5), (6, 7)]
        result = pedestrian.encounter_obstacle(4, 5, obstacle_list)
        print(result)  # Output: True
        ```
        In this example, the method checks if an obstacle exists at coordinates (4, 5) in the `obstacle_list`.

        Note:
        The method compares the provided `next_cellX` and `next_cellY` with the X and Y coordinates of each
        obstacle in `obstacle_list`. If a matching obstacle is found, the method returns True; otherwise, it
        returns False.
        """
        for obstacle in obstacle_list:
            if (next_cellX == obstacle[0] and next_cellY == obstacle[1]):
                return True
        return False


class Scenario:
    """
    A scenario for a cellular automaton.
    """
    GRID_SIZE = (500, 500)
    ID2NAME = {
        0: 'EMPTY',
        1: 'TARGET',
        2: 'OBSTACLE',
        3: 'PEDESTRIAN'
    }
    NAME2COLOR = {
        'EMPTY': (255, 255, 255),
        'PEDESTRIAN': (255, 0, 0),
        'TARGET': (0, 0, 255),
        'OBSTACLE': (255, 0, 255)
    }
    NAME2ID = {
        ID2NAME[0]: 0,
        ID2NAME[1]: 1,
        ID2NAME[2]: 2,
        ID2NAME[3]: 3
    }

    def __init__(self, width, height):
        if width < 1 or width > 1024:
            raise ValueError(f"Width {width} must be in [1, 1024].")
        if height < 1 or height > 1024:
            raise ValueError(f"Height {height} must be in [1, 1024].")

        self.width = width
        self.height = height
        self.grid_image = None
        self.grid = np.zeros((width, height))
        self.pedestrians = []
        self.obstacles = []
        self.target_distance_grids = self.recompute_target_distances()

    def init_from_file(self, scenario_name):
        """
        Initialize the GUI with a scenario loaded from a JSON file.

        This method reads a scenario from a JSON file and initializes the graphical user interface (GUI)
        with the elements specified in the scenario.

        Parameters:
        - self: The instance of the class this method belongs to.
        - scenario_name (str): The path to the JSON file containing the scenario data.

        Returns:
        - None

        Example:
        ```python
        sc = Scenario(100, 100)
        scenario_name = "scenario.json"  # Path to the scenario file
        gui.init_from_file(scenario_name)
        ```

        In this example, the method loads a scenario from "scenario.json" and initializes the GUI with the
        specified targets, obstacles, and pedestrians.

        Note:
        - The method uses the `read_scenario` function to read the scenario data from the JSON file.
        - It populates the GUI grid with targets and obstacles as specified in the scenario.
        - Ensure that the JSON file format matches the expected structure for this method to work correctly.
        """
        scenario_elements = read_scenario(scenario_name)

        for target in scenario_elements["targets"]:
            self.grid[target["locationX"], target["locationY"]
                      ] = Scenario.NAME2ID['TARGET']
        self.recompute_target_distances()

        for obstacle in scenario_elements["obstacles"]:
            self.grid[obstacle["locationX"], obstacle["locationY"]
                      ] = Scenario.NAME2ID['OBSTACLE']
            self.obstacles.append(
                [obstacle["locationX"], obstacle["locationY"]])

        for pedestrian in scenario_elements["pedestrians"]:
            self.pedestrians.append(Pedestrian(
                (pedestrian["locationX"], pedestrian["locationY"]), pedestrian["speed"]))

    def recompute_target_distances(self):
        self.target_distance_grids = self.update_target_grid()
        return self.target_distance_grids

    def update_target_grid(self):
        """
        Computes the shortest distance from every grid point to the nearest target cell.
        This does not take obstacles into account.
        :returns: The distance for every grid cell, as a np.ndarray.
        """
        targets = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] == Scenario.NAME2ID['TARGET']:
                    # y and x are flipped because they are in image space.
                    targets.append([y, x])
        if len(targets) == 0:
            return np.zeros((self.width, self.height))

        targets = np.row_stack(targets)
        x_space = np.arange(0, self.width)
        y_space = np.arange(0, self.height)
        xx, yy = np.meshgrid(x_space, y_space)
        positions = np.column_stack([xx.ravel(), yy.ravel()])

        # after the target positions and all grid cell positions are stored,
        # compute the pair-wise distances in one step with scipy.
        distances = scipy.spatial.distance.cdist(targets, positions)

        # now, compute the minimum over all distances to all targets.
        distances = np.min(distances, axis=0)

        return distances.reshape((self.width, self.height))

    def update_step(self):
        """
        Updates the position of all pedestrians.
        This does not take obstacles or other pedestrians into account.
        Pedestrians can occupy the same cell.
        """
        for pedestrian in self.pedestrians:
            pedestrian.update_step(self)

    @staticmethod
    def cell_to_color(_id):
        return Scenario.NAME2COLOR[Scenario.ID2NAME[_id]]

    def target_grid_to_image(self, canvas, old_image_id):
        """
        Creates a colored image based on the distance to the target stored in
        self.target_distance_gids.
        :param canvas: the canvas that holds the image.
        :param old_image_id: the id of the old grid image.
        """
        im = Image.new(mode="RGB", size=(self.width, self.height))
        pix = im.load()
        for x in range(self.width):
            for y in range(self.height):
                target_distance = self.target_distance_grids[x][y]
                pix[x, y] = (max(0, min(255, int(10 * target_distance) - 0 * 255)),
                             max(0, min(255, int(10 * target_distance) - 1 * 255)),
                             max(0, min(255, int(10 * target_distance) - 2 * 255)))
        im = im.resize(Scenario.GRID_SIZE, Image.NONE)
        self.grid_image = ImageTk.PhotoImage(im)
        canvas.itemconfigure(old_image_id, image=self.grid_image)

    def to_image(self, canvas, old_image_id):
        """
        Creates a colored image based on the ids stored in self.grid.
        Pedestrians are drawn afterwards, separately.
        :param canvas: the canvas that holds the image.
        :param old_image_id: the id of the old grid image.
        """
        im = Image.new(mode="RGB", size=(self.width, self.height))
        pix = im.load()
        for x in range(self.width):
            for y in range(self.height):
                pix[x, y] = self.cell_to_color(self.grid[x, y])
        for pedestrian in self.pedestrians:
            x, y = pedestrian.position
            pix[x, y] = Scenario.NAME2COLOR['PEDESTRIAN']
        im = im.resize(Scenario.GRID_SIZE, Image.NONE)
        self.grid_image = ImageTk.PhotoImage(im)
        canvas.itemconfigure(old_image_id, image=self.grid_image)
