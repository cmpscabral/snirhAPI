from flask_restplus import fields
from app import api


class DefaultValues:
    class Network:
        id = 920123704
        name = "Meteorológica"

    class Parameter:
        id = 4237
        name = "Precipitação anual"

    class Station:
        id = 920752670

    tmin = "1980-01-01"
    tmax = "2020-12-31"


# default_valies = {
#     "network_id": 920123704,
#     "station_id": 920123704,
#     "tmin": "1980-01-01",
#     "tmax": "2020-12-31",
# }
listed_networks = api.model(
    "NetworksList",
    {
        "id": fields.Integer(
            description="The network ID", example=DefaultValues.Network.id
        ),
        "name": fields.String(
            description="The network name", example=DefaultValues.Network.name
        ),
    },
)

station = api.model(
    "Station",
    {
        "CÓDIGO": fields.String(
            required=True, description="the station code", example="18C/02U"
        ),
        "NOME": fields.String(
            required=True, description="the station name", example="A-DOS-FRANCOS"
        ),
        "ALTITUDE (m)": fields.String(
            required=True, description="the station altitude", example="62"
        ),
        "LATITUDE (ºN)": fields.String(
            required=True, description="the station latitude", example="39.320965"
        ),
        "LONGITUDE (ºW)": fields.String(
            required=True, description="the station longitude", example="-9.04583"
        ),
        "COORD_X (m)": fields.String(
            required=True,
            description="the station horizontal coordinates",
            example="121290.59",
        ),
        "COORD_Y (m)": fields.String(
            required=True,
            description="the station vertical coordinates",
            example="261839.825",
        ),
        "BACIA": fields.String(
            required=True,
            description="the station hydrographic basin",
            example="RIBEIRAS DO OESTE",
        ),
        "DISTRITO": fields.String(
            required=True, description="the station district", example="LEIRIA"
        ),
        "CONCELHO": fields.String(
            required=True, description="the station council", example="CALDAS DA RAINHA"
        ),
        "FREGUESIA": fields.String(
            required=True, description="the station parish", example="A DOS FRANCOS"
        ),
        "ENTIDADE RESPONSÁVEL (AUTOMÁTICA)": fields.String(
            required=True,
            description="the station responsible automatic entity",
            example="Autoridade Nacional da Água",
        ),
        "ENTIDADE RESPONSÁVEL (CONVENCIONAL)": fields.String(
            required=True,
            description="the station responsible conventional entity",
            example="CCDR-LVT",
        ),
        "TIPO ESTAÇÃO (AUTOMÁTICA)": fields.String(
            required=True,
            description="the station automatic type",
            example="UDOMÉTRICA",
        ),
        "TIPO ESTAÇÃO (CONVENCIONAL)": fields.String(
            required=True,
            description="the station conventional type",
            example="UDOMÉTRICA",
        ),
        "ENTRADA FUNCIONAMENTO (CONVENCIONAL)": fields.String(
            required=True,
            description="the station conventional starting date",
            example="01-10-1979",
        ),
        "ENCERRAMENTO (CONVENCIONAL)": fields.String(
            required=True,
            description="the station conventional closing date",
            example="30-09-1983",
        ),
        "ENTRADA FUNCIONAMENTO (AUTOMÁTICA)": fields.String(
            required=True,
            description="the station automatic starting date",
            example="01-10-1979",
        ),
        "ENCERRAMENTO (AUTOMÁTICA)": fields.String(
            required=True,
            description="the station automatic closing date",
            example="30-09-1983",
        ),
        "TELEMETRIA": fields.String(
            required=True, description="the station telemetry", example="NÃO"
        ),
        "ESTADO": fields.String(
            required=True, description="the station state", example="EXTINTA"
        ),
        "ÍNDICE QUALIDADE*": fields.String(
            required=True, description="the station quality index", example="-"
        ),
        "ID": fields.Integer(
            required=True,
            description="the station ID",
            example=DefaultValues.Station.id,
        ),
    },
)

listed_stations = api.model("StationsList", station)


parameter = api.model(
    "Parameter",
    {
        "id": fields.Integer(
            description="The parameter ID", example=DefaultValues.Parameter.id
        ),
        "name": fields.String(
            description="The parameter name", example=DefaultValues.Parameter.name
        ),
    },
)
listed_parameters = api.model("ParametersList", parameter)
