from app.app import station
from .networks import Networks
from .stations import Stations
from .parameters import Parameters
from .data import GetData
from pprint import pprint
import json
import os

from utils import parse_datetime

DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

NETWORKS_FILE = os.path.join(DATA_DIR, "networks.json")
STATIONS_FILE = os.path.join(DATA_DIR, "stations-network_{network_id}.json")
PARAMETERS_FILE = os.path.join(DATA_DIR, "parameters-station_{station_id}.json")
DATA_FILE = os.path.join(
    DATA_DIR,
    "data-station_{station_id}-parameter_{parameter_id}-tmin_{tmin}-tmax_{tmax}.json",
)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def dump_networks():
    print(f"{bcolors.UNDERLINE}\nFetching networks...\n{bcolors.ENDC}")

    bot = Networks()
    networks = [n.dict() for n in bot.get()]
    pprint(networks)
    with open(NETWORKS_FILE, "w") as f:
        json.dump(networks, f)
    print(f"\nNetworks dumped to  {bcolors.OKGREEN}{NETWORKS_FILE}\n{bcolors.ENDC}")


def dump_stations(network_id: str):
    print(
        f"\nFetching stations for network {bcolors.OKGREEN}{network_id}{bcolors.ENDC}...\n"
    )

    bot = Stations(network_id=network_id)
    stations = [s.dict() for s in bot.get()]
    pprint(stations)
    stations_file = STATIONS_FILE.format(network_id=network_id)
    with open(stations_file, "w") as f:
        json.dump(stations, f)
    print(f"\n Stations dumped to {bcolors.OKGREEN}{stations_file}\n{bcolors.ENDC}")


def dump_parameters(network_id: str, station_id: str):
    print(
        f"\nFetching parameters for station {bcolors.OKGREEN}{station_id}{bcolors.ENDC} (from network {bcolors.OKGREEN}{network_id}{bcolors.ENDC})...\n"
    )

    bot = Parameters(network_id=network_id)
    parameters = [s.dict() for s in bot.get(station_id)]
    parameters_file = PARAMETERS_FILE.format(station_id=station_id)
    pprint(parameters)
    with open(parameters_file, "w") as f:
        json.dump(parameters, f)
    print(f"\n Parameters dumped to {bcolors.OKGREEN}{parameters_file}\n{bcolors.ENDC}")


def dump_data(station_id: str, parameter_id: str, tmin: str, tmax: str):
    print(
        f"""\nFetching data for 
        parameter {bcolors.OKGREEN}{parameter_id}{bcolors.ENDC} 
        station {bcolors.OKGREEN}{station_id}{bcolors.ENDC} 
        between {bcolors.OKGREEN}{tmin}{bcolors.ENDC} and {bcolors.OKGREEN}{tmax}{bcolors.ENDC}\n
        """
    )
    bot = GetData()
    data = bot.get_data(
        station_id=station_id,
        parameter_id=parameter_id,
        tmin=parse_datetime(tmin, format="%Y-%m-%d"),
        tmax=parse_datetime(tmax, format="%Y-%m-%d"),
    )
    data_file = DATA_FILE.format(
        station_id=station_id, parameter_id=parameter_id, tmin=tmin, tmax=tmax
    )

    with open(data_file, "w") as f:
        json.dump(data.json(), f)
    print(f"\n Data dumped to {bcolors.OKGREEN}{data_file}\n{bcolors.ENDC}")
