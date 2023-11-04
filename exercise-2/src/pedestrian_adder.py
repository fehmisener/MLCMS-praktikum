"""
Add Pedestrian to Scenario

This script adds a pedestrian to a specified scenario and saves the modified scenario as a JSON file.

Usage:
- Use this script to add a pedestrian to an existing scenario.
- Specify the input path of the scenario and optionally provide an output path for the modified scenario.

Example:
```shell
python pedestrian_adder.py --path ../vadere/scenarios/rimea6.scenario
```
"""
from util import read_scenario, save_scenario
import argparse

parser = argparse.ArgumentParser(
    description='Add a pedestrian to the specifed scenario.')

parser.add_argument('-p', '--path',
                    type=str,
                    required=True,
                    help='the path to the scenario')
parser.add_argument('-o', '--output',
                    type=str,
                    required=False,
                    default='../vadere/scenarios/',
                    help='the output path of new scenario')
args = parser.parse_args()


def add_pedestrian(data):
    """
    Add a pedestrian to the scenario data.

    Args:
        data (dict): The scenario data containing information about the scenario.

    Returns:
        dict: The modified scenario data with the added pedestrian.
    """
    pedestrian = {
        "attributes": {
            "id": 99,
            "shape": {
                "x": 0.0,
                "y": 0.0,
                "width": 1.0,
                "height": 1.0,
                "type": "RECTANGLE"
            },
            "visible": True,
            "radius": 0.2,
            "densityDependentSpeed": False,
            "speedDistributionMean": 1.34,
            "speedDistributionStandardDeviation": 0.26,
            "minimumSpeed": 0.5,
            "maximumSpeed": 2.2,
            "acceleration": 2.0,
            "footstepHistorySize": 4,
            "searchRadius": 1.0,
            "walkingDirectionSameIfAngleLessOrEqual": 45.0,
            "walkingDirectionCalculation": "BY_TARGET_CENTER"
        },
        "source": None,
        "targetIds": find_target_id(data),
        "nextTargetListIndex": 0,
        "isCurrentTargetAnAgent": False,
        "position": {
            "x": 14.0,
            "y": 3.0
        },
        "velocity": {
            "x": 0.0,
            "y": 0.0
        },
        "freeFlowSpeed": 1.33,
        "followers": [],
        "idAsTarget": -1,
        "isChild": False,
        "isLikelyInjured": False,
        "psychologyStatus": {
            "mostImportantStimulus": None,
            "threatMemory": {
                "allThreats": [],
                "latestThreatUnhandled": False
            },
            "selfCategory": "TARGET_ORIENTED",
            "groupMembership": "OUT_GROUP",
            "knowledgeBase": {
                "knowledge": [],
                "informationState": "NO_INFORMATION"
            },
            "perceivedStimuli": [],
            "nextPerceivedStimuli": []
        },
        "healthStatus": None,
        "infectionStatus": None,
        "groupIds": [],
        "groupSizes": [],
        "agentsInGroup": [],
        "trajectory": {
            "footSteps": []
        },
        "modelPedestrianMap": None,
        "type": "PEDESTRIAN"
    }

    data["name"] = data["name"] + '_pedestrian_added'
    data["scenario"]["topography"]["dynamicElements"].append(pedestrian)
    return data


def find_target_id(data):
    """
    Find the id of the target in the scenario data.

    Args:
        data (dict): The scenario data containing information about the scenario.

    Returns:
        int: The ID of the target in the scenario, or None if not found.
    """
    target_id_list = []

    for element in data["scenario"]["topography"]["targets"]:
        target_id_list.append(element["id"])

    return target_id_list


if __name__ == '__main__':

    scenario_data = read_scenario(args.path)
    scenario_data = add_pedestrian(scenario_data)
    save_scenario(args.output, scenario_data)
