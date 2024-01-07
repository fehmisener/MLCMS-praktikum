import os
import json
import subprocess
import uuid
import pandas as pd
import shutil

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))


def run_scenario(scenario_name):
    """
    Run a Vadere scenario and return the simulation results.

    Parameters:
    - scenario_name (str): The name of the scenario to be executed.

    Returns:
    - json: A json containing simulation results.

    Raises:
    - subprocess.CalledProcessError: If there is an error during the scenario execution.

    Example:
    >>> run_scenario("example_scenario")
    Json with simulation results.
    """

    output_dir = os.path.join(base_dir, "builds", "resources", scenario_name)
    vadere_dir = os.path.join(base_dir, "builds", "vadere.v2.6")

    java_command = [
        "java",
        "-jar",
        os.path.join(vadere_dir, "vadere-console.jar"),
        "scenario-run",
        "--scenario-file",
        os.path.join(base_dir, "builds", "resources", f"{scenario_name}.scenario"),
        "--output-dir",
        os.path.join(base_dir, "builds", "resources"),
    ]

    try:
        subprocess.run(java_command, check=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    data = pd.read_csv(os.path.join(output_dir, "postvis.traj"), delimiter=" ")
    delete_temp_scenario(scenario_name)

    return data.to_dict(orient="records")


def map_to_vadere_scenario(request_json):
    """
    Map a custom scenario description from a JSON request to a Vadere-compatible scenario.

    Parameters:
    - request_json (dict): JSON object containing the scenario description.

    Returns:
    - str: The name of the saved Vadere scenario.
    """
    temp_scenario = read_scenario(request_json["model_name"])
    temp_scenario = map_to_vadere_source(temp_scenario, request_json)
    temp_scenario = map_to_vadere_target(temp_scenario, request_json)
    temp_scenario = map_to_vadere_obstacles(temp_scenario, request_json)
    return save_scenario(temp_scenario)


def map_to_vadere_source(scenario, request_json):
    """
    Map source details from a JSON request to a Vadere scenario.

    Parameters:
    - scenario (dict): Existing Vadere scenario data.
    - request_json (dict): JSON object containing source details.

    Returns:
    - dict: Updated Vadere scenario data.

    Example:
    >>> map_to_vadere_source({"scenario": {"topography": {"sources": [...]}}}, {"source": {...}})
    {"scenario": {"topography": {"sources": [...]}}}
    """
    scenario["scenario"]["topography"]["sources"][0]["shape"] = {
        "x": request_json["source"]["shape"]["x"],
        "y": request_json["source"]["shape"]["y"],
        "width": 1.0,
        "height": 1.0,
        "type": "RECTANGLE",
    }
    scenario["scenario"]["topography"]["sources"][0]["spawner"][
        "eventElementCount"
    ] = request_json["source"]["event_element_count"]
    return scenario


def map_to_vadere_target(scenario, request_json):
    """
    Map target details from a JSON request to a Vadere scenario.

    Parameters:
    - scenario (dict): Existing Vadere scenario data.
    - request_json (dict): JSON object containing target details.

    Returns:
    - dict: Updated Vadere scenario data.

    Example:
    >>> map_to_vadere_target({"scenario": {"topography": {"targets": [...]}}}, {"target": {...}})
    {"scenario": {"topography": {"targets": [...]}}}
    """
    scenario["scenario"]["topography"]["targets"][0]["shape"] = {
        "x": request_json["target"]["shape"]["x"],
        "y": request_json["target"]["shape"]["y"],
        "width": 1.0,
        "height": 1.0,
        "type": "RECTANGLE",
    }
    return scenario


def map_to_vadere_obstacles(scenario, request_json):
    """
    Map obstacle details from a JSON request to a Vadere scenario.

    Parameters:
    - scenario (dict): Existing Vadere scenario data.
    - request_json (dict): JSON object containing obstacle details.

    Returns:
    - dict: Updated Vadere scenario data.

    Example:
    >>> map_to_vadere_obstacle({"scenario": {"topography": {"obstacles": [...]}}}, {"obstacle": {...}})
    {"scenario": {"topography": {"obstacles": [...]}}}
    """
    obstacles = [
        {
            "id": obstacle["id"],
            "shape": {
                "x": obstacle["shape"]["x"],
                "y": obstacle["shape"]["y"],
                "width": 1.0,
                "height": 1.0,
                "type": "RECTANGLE",
            },
            "visible": "true",
        }
        for obstacle in request_json["obstacles"]
    ]
    scenario["scenario"]["topography"]["obstacles"] = obstacles
    return scenario


def read_scenario(model):
    """
    Load the default scenario file in JSON format.

    Args:
        model (str): The name of the default scenario file.

    Returns:
        dict: A dictionary containing the scenario's data.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    scenario_name = f"default_{model}.scenario"
    scenario_path = os.path.join(base_dir, "builds", "resources", scenario_name)

    with open(scenario_path, "r") as f:
        data = json.load(f)
    return data


def save_scenario(data):
    """
    Save the scenario to the given path in JSON format.

    Args:
        data (dict): The scenario data to be saved.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    temp_scenario_name = str(uuid.uuid4())[:8]
    data["name"] = data["name"] + temp_scenario_name

    with open(
        os.path.join(base_dir, "builds", "resources", f"{data['name']}.scenario"), "w"
    ) as f:
        json.dump(data, f, indent=2)
    return data["name"]


def delete_temp_scenario(scenario_name):
    """
    Delete temporary Vadere scenario files and directory.

    Parameters:
    - scenario_name (str): The name of the scenario to be deleted.

    Raises:
    - FileNotFoundError: If the scenario file or scenario output directory is not found.
    - OSError: If an error occurs during the deletion process.

    Example:
    >>> delete_temp_scenario("scenario_xxxxxxxx")
    Successfully deleted scenario file: /path/to/base_dir/builds/resources/scenario_xxxxxxxx.scenario
    """
    scenario_file_path = os.path.join(
        base_dir, "builds", "resources", f"{scenario_name}.scenario"
    )
    scenario_output_path = os.path.join(base_dir, "builds", "resources", scenario_name)

    try:
        os.remove(scenario_file_path)
        shutil.rmtree(scenario_output_path)
        print(f"Successfully deleted scenario file: {scenario_file_path}")
    except FileNotFoundError:
        print(f"Scenario file not found: {scenario_file_path}")
    except OSError as e:
        print(f"Error deleting scenario file: {e}")
