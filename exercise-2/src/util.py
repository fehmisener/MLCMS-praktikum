"""
Scenario Handling Utilities

This module provides functions for reading and saving scenario data in JSON format. It includes functions to load a scenario
from a file and save a scenario to a file.

Contents:
- `read_scenario`: Function for loading a scenario from a JSON file.
- `save_scenario`: Function for saving a scenario to a JSON file.

Usage:
This module can be used to handle scenario data, allowing users to load existing scenarios and save new scenarios in a
structured JSON format.

Example:
```python
# Loading a scenario from a file
scenario_data = read_scenario("example.scenario")

# Modifying the scenario data

# Saving the modified scenario to a new file
save_scenario("modified_scenario.scenario", scenario_data)
"""
import json


def read_scenario(path):
    """
    Load a scenario file in JSON format.

    Args:
        path (str): The path to the scenario file.

    Returns:
        dict: A dictionary containing the scenario's data.
    """
    with open(path, 'r') as f:
        data = json.load(f)
        return data


def save_scenario(path, data):
    """
    Save the scenario to the given path in JSON format.

    Args:
        path (str): The output path for the scenario file.
        data (dict): The scenario data to be saved.
    """
    with open(path+data['name']+'.scenario', 'w') as f:
        json.dump(data, f, indent=2)
