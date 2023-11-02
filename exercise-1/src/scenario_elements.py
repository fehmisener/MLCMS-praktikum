import scipy.spatial.distance
from PIL import Image, ImageTk
import numpy as np
import skfmm
import math

from euclidean_distance import read_scenario

# +
class Pedestrian:
    """
    Defines a single pedestrian.
    """

    def __init__(self, position, desired_speed):
        self._position = position
        self._desired_speed = desired_speed
        self.accumulated_distance = 0
        self.id = -1
        self.age = -1
        self.distance_walked = 0
        self.ticks = 0
        self.finished = False

    def copy(self):
        return Pedestrian(self._position, self._desired_speed)

    @property
    def position(self):
        return self._position

    @property
    def desired_speed(self):
        return self._desired_speed

    def get_neighbors(self, scenario):
        """
        Compute all neighbors in a 9 cell neighborhood of the current position.

        Parameters:
            scenario: The scenario instance.
        
        Return:
            A list of neighbor cell indices (x,y) around the current position.
        """
        return [
            (int(x + self._position[0]), int(y + self._position[1]))
            for x in [-1, 0, 1]
            for y in [-1, 0, 1]
            if 0 <= x + self._position[0] < scenario.width and 0 <= y + self._position[1] < scenario.height and np.abs(
                x) + np.abs(y) > 0
        ]

    def update_step(self, scenario):
        """
        Moves to the cell with the lowest distance to the target.
        This does not take obstacles or other pedestrians into account.
        Pedestrians can occupy the same cell.

        Parameters:
            scenario: The current scenario instance.
        """

        moved = False
        available_distance = self._desired_speed + self.accumulated_distance
        self.accumulated_distance = 0
        while available_distance > 0:
            neighbors = self.get_neighbors(scenario)
            p_x = self._position[0]
            p_y = self._position[1]
            next_cell_distance = scenario.target_distance_grids[p_x, p_y]
            next_pos = self._position
            # Goes to the neighbor position that minimizes the distance to the nearest target
            for (n_x, n_y) in neighbors:
                if scenario.grid[n_x, n_y] != Scenario.NAME2ID['OBSTACLE'] and scenario.grid[n_x, n_y] != \
                        Scenario.NAME2ID['PEDESTRIAN']:
                    if next_cell_distance > scenario.target_distance_grids[n_x, n_y]:
                        next_pos = (n_x, n_y)
                        next_cell_distance = scenario.target_distance_grids[n_x, n_y]

                    elif next_cell_distance == scenario.target_distance_grids[n_x, n_y]:
                        distance_to_next = euclidean_distance(p_x, p_y, next_pos[0], next_pos[1])
                        distance_to_neighbor = euclidean_distance(p_x, p_y, n_x, n_y)
                        if distance_to_neighbor < distance_to_next:
                            next_pos = (n_x, n_y)
                            next_cell_distance = scenario.target_distance_grids[n_x, n_y]

            if self._position != next_pos:
                '''
                    measuring_points related
                '''
                for x, y, size in scenario.measuring_points:
                    if next_pos[0] >= x and next_pos[0] <= x + size and next_pos[1] >= y and next_pos[1] <= y + size and \
                            self._position[0] < x:
                        scenario.measuring_records[(x, y, size)] += [self.ticks]

                moved = True
                distance_to_travel = euclidean_distance(p_x, p_y, next_pos[0], next_pos[1])
                if distance_to_travel <= available_distance:
                    available_distance -= distance_to_travel
                    self.distance_walked += distance_to_travel
                    if scenario.grid[next_pos] != Scenario.NAME2ID['TARGET']:
                        scenario.grid[next_pos] = Scenario.NAME2ID['PEDESTRIAN']
                    elif scenario.grid[next_pos] == Scenario.NAME2ID['TARGET']:
                        self.finished = True
                    scenario.grid[self._position] = Scenario.NAME2ID['EMPTY']
                    self._position = next_pos
                else:
                    self.accumulated_distance += available_distance
                    available_distance = 0
            else:
                break
        self.ticks += 1
        return moved


class Scenario:
    """
    A scenario for a cellular automaton.
    """
    GRID_SIZE = (600, 600)
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
    max_target_distance = 1
    measuring_points = []
    measuring_records = {}

    def __init__(self, width, height):
        """
        if width < 1 or width > 1024:
            raise ValueError(f"Width {width} must be in [1, 1024].")
        if height < 1 or height > 1024:
            raise ValueError(f"Height {height} must be in [1, 1024].")
        """
        self.width = width
        self.height = height
        self.grid_image = None
        self.grid = np.zeros((width, height))
        self.pedestrians = []
        self.obstacles = []
        self.recompute_method = 'BASIC'
        self.target_distance_grids = self.recompute_target_distances()
        self.target_grid = False
        self.pedestrian_records = [['id', 'age', 'expected_speed', 'real_speed']]

    def init_from_file(self, scenario_data):
        """
        Initialize the GUI with a scenario loaded from a JSON file.

        This method reads a scenario from a JSON file and initializes the graphical user interface (GUI)
        with the elements specified in the scenario.

        Parameters:
        - self: The instance of the class this method belongs to.
        - scenario_data (dict): The path to the JSON file containing the scenario data.

        Returns:
        - None

        Example:
        ```python
        sc = Scenario(100, 100)
        scenario_data = load_scenario() # Loaded scenario from file
        gui.init_from_file(scenario_data)
        ```

        In this example, the method loads a scenario from scenario json file and initializes the GUI with the
        specified targets, obstacles, and pedestrians.

        Note:
        - The method uses the `load_scenario` function to read and load the scenario data from the JSON file.
        - It populates the GUI grid with targets and obstacles as specified in the scenario.
        - Ensure that the JSON file format matches the expected structure for this method to work correctly.
        """

        for target in scenario_data["targets"]:
            self.grid[
                target["locationX"], target["locationY"]
            ] = Scenario.NAME2ID['TARGET']
        self.recompute_target_distances()

        for obstacle in scenario_data["obstacles"]:
            self.grid[
                obstacle["locationX"], obstacle["locationY"]
            ] = Scenario.NAME2ID['OBSTACLE']
            self.obstacles.append(
                [obstacle["locationX"], obstacle["locationY"]])

        for pedestrian in scenario_data["pedestrians"]:
            self.pedestrians.append(Pedestrian(
                (pedestrian["locationX"], pedestrian["locationY"]), pedestrian["speed"]))

    def copy(self):
        """
        Makes a copy of the scenario instance.

        Return:
            A copy of the scenario instance.
        """
        scenario = Scenario(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                scenario.grid[x, y] = self.grid[x, y]
        for pedestrian in self.pedestrians:
            scenario.pedestrians.append(pedestrian.copy())
        scenario.recompute_method = self.recompute_method
        scenario.target_distance_grids = scenario.recompute_target_distances()
        scenario.target_grid = self.target_grid
        return scenario

    def recompute_target_distances(self):
        """
        Recomputes the target distances with the algorithm specified in the attribute `recompute_method`.
        """
        if self.recompute_method == 'BASIC':
            self.target_distance_grids = self.update_target_grid()
        elif self.recompute_method == 'DIJKSTRA':
            self.target_distance_grids = self.dijkstra_flood_update_target_grid((self.width + self.height) * 10)
        elif self.recompute_method == 'FMM':
            self.target_distance_grids = self.fmm_flood_update_target_grid()
        return self.target_distance_grids

    def update_target_grid(self):
        """
        Computes the shortest distance from every grid point to the nearest target cell.
        This does not take obstacles into account.

        Return:
            The distance for every grid cell, as a np.ndarray.
        """
        targets = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] == Scenario.NAME2ID['TARGET']:
                    targets.append([y, x])  # y and x are flipped because they are in image space.
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

        self.max_target_distance = distances.max()

        return distances.reshape((self.width, self.height))

    def get_open_neighbors(self, closed, position):
        """
        Compute all neighbors in a 9 cell neighborhood of the current position.
        :param closed: 2D binary table marking closed positions
        :param position: A tuple position (x,y)
        :return: A list of neighbor cell indices (x,y) around the current position.
        """
        neighbors = []
        for x in [position[0] - 1, position[0], position[0] + 1]:
            for y in [position[1] - 1, position[1], position[1] + 1]:
                if 0 <= x < self.width and 0 <= y < self.height and closed[x, y] == 0:
                    closed[x, y] = 1
                    neighbors.append((x, y))
        return neighbors

    def get_min_distance(self, distances, position):
        """
        Compute the min distance at current position considering all neighbors in a 9 cell neighborhood of
        the current position on the distance map.
        :param distances: 2D nparray distance table
        :param position: A tuple position (x,y)
        :return: A list of neighbor cell indices (x,y) around the current position.
        """
        new_distance = distances[position[0], position[1]]
        new_position = (position[0], position[1])
        for x in [position[0] - 1, position[0], position[0] + 1]:
            for y in [position[1] - 1, position[1], position[1] + 1]:
                if 0 <= x < self.width and 0 <= y < self.height:
                    temp_distance = distances[x, y] + (1 if x == position[0] or y == position[1] else math.sqrt(2))
                    if temp_distance < new_distance:
                        new_distance = temp_distance
                        new_position = (x, y)
        return new_distance

    def dijkstra_flood_update_target_grid(self, limit):
        """
        Computes the shortest distance from every grid point to the nearest target cell.
        This does not take obstacles into account.
        :param limit: work as max distance, after which flooding will stop.
        :returns: The distance for every grid cell, as a np.ndarray.
        """
        targets = []
        closed = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] == Scenario.NAME2ID['TARGET']:
                    targets.append((x, y))
                elif self.grid[x, y] == Scenario.NAME2ID['OBSTACLE']:
                    closed[x, y] = 1
        if len(targets) == 0:
            return np.zeros((self.width, self.height))

        distances = np.matrix(np.ones((self.width, self.height)) * np.inf)
        open_positions = []
        for x, y in targets:
            distances[x, y] = 0
            closed[x, y] = 1
            open_positions += self.get_open_neighbors(closed, (x, y))

        counter = 1
        while counter < limit and open_positions:
            next_open_positions = []
            for x, y in open_positions:
                distances[x, y] = self.get_min_distance(distances, (x, y))
                next_open_positions += self.get_open_neighbors(closed, (x, y))
            open_positions = next_open_positions
            counter += 1

        for x, y in open_positions:
            distances[x, y] = counter

        distances = distances.reshape((self.width, self.height))

        self.max_target_distance = counter

        return distances

    def fmm_flood_update_target_grid(self):
        """
        Computes the shortest distance from every grid point to the nearest target cell.
        This does not take obstacles into account.
        :returns: The distance for every grid cell, as a np.ndarray.
        """
        distances = np.matrix(np.ones((self.width, self.height)))
        mask = np.matrix(np.zeros((self.width, self.height)))
        targets = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] == Scenario.NAME2ID['TARGET']:
                    targets.append((x, y))
                    distances[x, y] = 0
                elif self.grid[x, y] == Scenario.NAME2ID['OBSTACLE']:
                    mask[x, y] = 1
        if len(targets) == 0:
            return np.zeros((self.width, self.height))

        distances = np.ma.MaskedArray(distances, mask)
        distances = skfmm.distance(distances)
        distances = distances.reshape((self.width, self.height))

        self.max_target_distance = distances.max()

        return distances.data

    def update_step(self):
        """
        Updates the position of all pedestrians.
        This does not take obstacles or other pedestrians into account.
        Pedestrians can occupy the same cell.
        """
        updated = False
        for pedestrian in self.pedestrians:
            moved = pedestrian.update_step(self)
            if moved:
                updated = True
        return updated

    @staticmethod
    def cell_to_color(_id):
        return Scenario.NAME2COLOR[Scenario.ID2NAME[_id]]

    def target_grid_to_image(self, canvas, old_image_id):
        """
        Creates a colored image based on the distance to the target stored in
        self.target_distance_gids.

        Parameters
            canvas: the canvas that holds the image.
            old_image_id: the id of the old grid image.
        """
        im = Image.new(mode="RGB", size=(self.width, self.height))
        pix = im.load()
        for x in range(self.width):
            for y in range(self.height):
                target_distance = self.target_distance_grids[x, y]
                if target_distance == np.inf:
                    target_distance = self.width * self.height
                pix[x, y] = (max(0, min(255, int(1000 * target_distance / self.max_target_distance) - 0 * 255)),
                             max(0, min(255, int(1000 * target_distance / self.max_target_distance) - 1 * 255)),
                             max(0, min(255, int(1000 * target_distance / self.max_target_distance) - 2 * 255)))
        im = im.resize(Scenario.GRID_SIZE, Image.NONE)
        self.grid_image = ImageTk.PhotoImage(im)
        canvas.itemconfigure(old_image_id, image=self.grid_image)

    def to_image(self, canvas, old_image_id):
        """
        Creates a colored image based on the ids stored in self.grid.
        Pedestrians are drawn afterwards, separately.

        Parameters:
            canvas: the canvas that holds the image.
            old_image_id: the id of the old grid image.
        """
        if self.target_grid:
            self.target_grid_to_image(canvas, old_image_id)
        else:
            im = Image.new(mode="RGB", size=(self.width, self.height))
            pix = im.load()
            for x in range(self.width):
                for y in range(self.height):
                    pix[x, y] = self.cell_to_color(self.grid[x, y])
            for pedestrian in self.pedestrians:
                x, y = pedestrian.position
                if self.grid[x, y] != Scenario.NAME2ID['TARGET']:
                    pix[x, y] = Scenario.NAME2COLOR['PEDESTRIAN']
            im = im.resize(Scenario.GRID_SIZE, Image.NONE)
            self.grid_image = ImageTk.PhotoImage(im)
            canvas.itemconfigure(old_image_id, image=self.grid_image)
