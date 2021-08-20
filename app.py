from datetime import timedelta

from flask import Flask, abort, request
from flask_restplus import fields, Api, Resource
from flask_session import Session

import redis

from src.client.stations import Stations
from src.client.parameters import Parameters
from src.client.networks import Networks
from src.client.data import GetData
from src.serializers import DataQuerySchema
import os

app = Flask(__name__)
api = Api(app)

app.secret_key = "BAD_SECRET_KEY"

from dotenv import load_dotenv

load_dotenv()
WITH_REDIS_SESSION = os.environ.get("WITH_REDIS_SESSION")
if WITH_REDIS_SESSION:
    from flask import session

    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_REDIS"] = redis.from_url("redis://localhost:6379")
    server_session = Session(app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)


else:
    session = {}


data_schema = DataQuerySchema()


class network_list(Resource):
    def get(self):
        bot = Networks(session=session.get("client"))
        session["client"] = bot.session
        return bot.get()


@api.doc(
    params={"network": "The ID of the network"},
    description="Endpoint to get a list of stations",
)
class stations_list(Resource):
    def get(self, network):
        if network == session.get("network"):
            if session.get("stations"):
                return session["stations"]
            bot = Stations(session=session.get("client"), new_network=False)
        else:
            bot = Stations(session=session.get("client"), network=network)

        session["network"] = network
        session["client"] = bot.session
        stations = bot.get()
        session["stations"] = stations
        return stations


@api.doc(
    params={"station": "the ID of the station", "network": "The ID of the network"},
    description="Endpoint to get the details of a specific station",
)
class station(Resource):
    def get(self, station, network):
        if network == session.get("network"):
            if session.get("stations"):
                stations = session.get("stations")
            else:
                bot = Stations(session=session.get("client"), new_network=False)
                stations = bot.get()
        else:
            bot = Stations(session=session.get("client"), network=network)
            stations = bot.get()
        session["stations"] = stations
        session["station_data"] = [s for s in stations if s["ID"] == station][0]

        return session["station_data"]


@api.doc(
    params={"station": "the ID of the station", "network": "The ID of the network"},
    description="Endpoint to get al the parameters available for a station",
)
class parameters_list(Resource):
    def get(self, station, network):
        if network == session.get("network"):
            bot = Parameters(session=session.get("client"), new_network=False)
        else:
            bot = Parameters(session=session.get("client"), network=network)
        return bot.get(station)


resource_fields = api.model(
    "Data",
    {
        "station": fields.Integer(required=True),
        "parameter": fields.Integer(required=True),
        "tmin": fields.Date(required=True),
        "tmax": fields.String(required=True),
    },
)


@api.doc(
    params={"station": "the ID of the station", "network": "The ID of the network"},
    description="Endpoint to get al the parameters available for a station",
)
class data(Resource):
    @api.doc(resource_fields)
    def get(self):
        args = request.args
        errors = data_schema.validate(args)
        if errors:
            abort(400, str(errors))

        bot = GetData()
        return bot.get_data(
            sites=args["station"],
            pars=args["parameter"],
            tmin=args["tmin"],
            tmax=args["tmax"],
        )


api.add_resource(network_list, "/api/networks")
api.add_resource(stations_list, "/api/networks/<network>/stations")
api.add_resource(station, "/api/networks/<network>/stations/<station>")
api.add_resource(parameters_list, "/api/networks/<network>/stations/<station>/params")
api.add_resource(data, "/api/data")

if __name__ == "__main__":
    app.run(debug=True)
