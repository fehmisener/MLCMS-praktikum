import os
import json
import subprocess
import uuid


def run_scenario(scenario_name):
    """ Run vadere from console and wait until the script finished. After that read postvis.traj file in builds/vadere.v2.6.linux/output/{scenario_name}"""

    delete_temp_scenarip(scenario_name)



def map_to_vadere_scenario(request_json):
    """Map the JSON data from the request to a Vadere scenario JSON file."""

    temp_scenario = read_scenario(request_json["model_name"])
    temp_scenario = map_to_vadere_source(temp_scenario, request_json)
    temp_scenario = map_to_vadere_target(temp_scenario, request_json)
    temp_scenario = map_to_vadere_obstacles(temp_scenario, request_json)
    return save_scenario(temp_scenario)


def map_to_vadere_source(scenario, request_json):
    """Map the JSON data from the request to Vadere obstacles."""

    scenario["scenario"]["topography"]["sources"][0]["shape"] = {
        "x": request_json["source"]["shape"]["x"],
        "y": request_json["source"]["shape"]["y"],
        "width": 1.0,
        "height": 1.0,
        "type": "RECTANGLE"
    }
    scenario["scenario"]["topography"]["sources"][0]["spawner"]["eventElementCount"] = request_json["source"]["event_element_count"]
    return scenario


def map_to_vadere_target(scenario, request_json):
    """Map the JSON data from the request to Vadere obstacles."""

    scenario["scenario"]["topography"]["targets"][0]["shape"] = {
        "x": request_json["target"]["shape"]["x"],
        "y": request_json["target"]["shape"]["y"],
        "width": 1.0,
        "height": 1.0,
        "type": "RECTANGLE"
    }
    return scenario


def map_to_vadere_obstacles(scenario, request_json):
    """Map the JSON data from the request to Vadere obstacles."""

    obstacles = []
    for obstacle in request_json["obstacles"]:
        obstacles.append({
            "id": obstacle["id"],
            "shape": {
                "x": obstacle["shape"]["x"],
                "y": obstacle["shape"]["y"],
                "width": 1.0,
                "height": 1.0,
                "type": "RECTANGLE"
            },
            "visible": "true"
        })
    scenario["scenario"]["topography"]["obstacles"] = obstacles
    return scenario


def read_scenario(model):
    """
    Load a scenario file in JSON format.

    Args:
        path (str): The path to the scenario file.

    Returns:
        dict: A dictionary containing the scenario's data.
    """
    scenario_name = f'default_{model}.scenario'
    with open('/Users/machine/Developer/tum/MLCMS-praktikum/final-project/src/builds/resources/'+scenario_name, 'r') as f:
        data = json.load(f)
        return data

def save_scenario(data):
    """
    Save the scenario to the given path in JSON format.

    Args:
        path (str): The output path for the scenario file.
        data (dict): The scenario data to be saved.
    """
    temp_scenario_name = str(uuid.uuid4())[:8]
    data["name"] = data["name"] + temp_scenario_name
    with open(data["name"]+'.scenario', 'w') as f:
        json.dump(data, f, indent=2)
    return data["name"]

def delete_temp_scenarip(name):
    """ Remove temporarly created simulation scenario after the simulation"""

map_to_vadere_scenario(
    {
        "model_name": "osm",
        "source": {
            "shape": {
                "x": 5,
                "y": 5
            },
            "event_element_count": 2
        },
        "target": {
            "shape": {
                "x": 30,
                "y": 30
            },
        },
        "obstacles": [
            {
                "id": 29,
                "shape": {
                    "x": 25,
                    "y": 15,
                    "width": 1,
                    "height": 5
                }
            },
            {
                "id": 28,
                "shape": {
                    "x": 20,
                    "y": 15,
                    "width": 2,
                    "height": 5
                }
            }
        ]

    }
)
