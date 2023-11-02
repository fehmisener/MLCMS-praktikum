"""
Utility Functions for Data Handling and Calculation

This module contains utility functions for reading scenario data from JSON files and performing
calculations such as Euclidean distance in 2D space.

Contents:
- `read_scenario`: A function for safely reading and parsing scenario data from JSON files.
- `euclidean_distance`: A function for calculating the Euclidean distance between two points.

Usage:
This file can be imported to access the provided utility functions for data processing and calculations.
"""

import json
import math

def read_scenario(file_path):
    """
    Read JSON data that stores pedestrians, targets and obstacles from a file for scenarios safely.

    This function reads JSON data from the specified file path, handles potential errors,
    and validates the JSON content.

    Args:
        file_path (str): The path to the JSON file to be read.

    Returns:
        dict: If the JSON data is successfully read and parsed, a dictionary
        containing the pedestrians, targets and obstacles is returned.


    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the JSON data is not well-formed.

    Example:
        file_path = 'data.json'
        data = read_json_file(file_path)

        if data is not None:
            # You can now safely work with the JSON data.
            print(data)
    """

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON from file: {e}")
        raise e

def euclidean_distance(x_1, y_1, x_2, y_2):
    """
    Calculate the Euclidean distance between two points in 2D space.

    Args:
        x_1 (float): The x-coordinate of the first point.
        y_1 (float): The y-coordinate of the first point.
        x_2 (float): The x-coordinate of the second point.
        y_2 (float): The y-coordinate of the second point.

    Returns:
        float: The Euclidean distance between the two points.

    Example:
    ```python
    distance = euclidean_distance(1.0, 2.0, 4.0, 6.0)
    print(distance)  # Output: 5.0
    ```
    In this example, the function calculates the Euclidean distance between two points with coordinates (1.0, 2.0) and (4.0, 6.0).

    Note:
    The Euclidean distance is a measure of the straight-line distance between two points in a 2D space.
    """
    x = x_1 - x_2
    y = y_1 - y_2
    return math.sqrt(x * x + y * y)
