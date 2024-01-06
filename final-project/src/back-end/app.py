from flask import Flask
from flask_restful import Api
from resources import RunScenarioResource

app = Flask(__name__)
api = Api(app)

api.add_resource(RunScenarioResource, '/run-scenario')

if __name__ == '__main__':
    app.run(debug=True)
