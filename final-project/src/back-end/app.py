from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources import RunScenarioResource

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(RunScenarioResource, '/run-scenario')

if __name__ == '__main__':
    app.run(debug=False)
