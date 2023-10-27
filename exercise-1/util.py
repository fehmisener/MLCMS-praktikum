"""
Util program for data read and initialization operations.
"""

import json

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
