from flask import request
from flask_restful import Resource
from models import RunScenarioInputSchema
from vadere_helper import map_to_vadere_scenario, run_scenario


class RunScenarioResource(Resource):
    def post(self):
        try:
            data = RunScenarioInputSchema().load(request.get_json())
            temp_simulation_name = map_to_vadere_scenario(data)
            response = run_scenario(temp_simulation_name)
            return {"message": "Scenario executed successfully", "data": response}, 200
        except Exception as e:
            return {"error": str(e)}, 400