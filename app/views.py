from app import ns, api, session

from flask import abort, request
from flask_restplus import Resource

from app.client.stations import Stations
from app.client.parameters import Parameters
from app.client.networks import Networks
from app.client.data import GetData
from app.models import *
from app.serializers import DataQuerySchema


@ns.route("/networks")
@api.doc(
    description="Endpoint to get a list of networks",
)
class network_list(Resource):
    """Shows a list of all networks"""

    @api.marshal_list_with(listed_networks)
    def get(self):
        bot = Networks(session=session.get("client"))
        session["client"] = bot.session
        return bot.get()


@ns.route("/networks/<network>/stations")
@api.doc(
    params={
        "network": {
            "description": "The network ID",
            "default": DefaultValues.Network.id,
        }
    },
    description="Endpoint to get a list of stations",
)
class stations_list(Resource):
    @api.marshal_list_with(listed_stations)
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


@ns.route("/networks/<network>/stations/<station>")
@api.doc(
    params={
        "station": {
            "description": "The station ID",
            "default": DefaultValues.Station.id,
        },
        "network": {
            "description": "The network ID",
            "default": DefaultValues.Network.id,
        },
    },
    description="Endpoint to get the details of a specific station",
)
class station(Resource):
    @api.marshal_with(station)
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


@ns.route("/networks/<network>/stations/<station>/params")
@api.doc(
    params={
        "station": {
            "description": "The station ID",
            "default": DefaultValues.Station.id,
        },
        "network": {
            "description": "The network ID",
            "default": DefaultValues.Network.id,
        },
    },
    description="Endpoint to get al the parameters available for a station",
)
class parameters_list(Resource):
    @api.marshal_list_with(listed_parameters)
    def get(self, station, network):
        if network == session.get("network"):
            bot = Parameters(session=session.get("client"), new_network=False)
        else:
            bot = Parameters(session=session.get("client"), network=network)
        return bot.get(station)


data_schema = DataQuerySchema()


@ns.route("/data")
@api.doc(
    description="Endpoint to get data for a specific station and parameter",
    params={
        "station": {
            "description": "Station ID",
            "in": "query",
            "type": "int",
            "default": DefaultValues.Station.id,
        },
        "parameter": {
            "description": "parameter ID",
            "in": "query",
            "type": "int",
            "default": DefaultValues.Parameter.id,
        },
        "tmin": {
            "description": "starting date",
            "in": "query",
            "type": "date",
            "default": DefaultValues.tmin,
        },
        "tmax": {
            "description": "last date",
            "in": "query",
            "type": "date",
            "default": DefaultValues.tmax,
        },
    },
)
class data(Resource):
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
