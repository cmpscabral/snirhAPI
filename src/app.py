from typing import List, Optional, Type

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.crawler.data import GetData
from src.crawler.networks import Networks
from src.crawler.parameters import Parameters
from src.crawler.stations import Stations
from src.models import DataEntry, Network, Parameter, Station

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Cache(BaseModel):
    client: Optional[Type[requests.Session]]
    networks: Optional[List[Network]]
    network_id: Optional[str]
    stations: Optional[List[Station]]


cache = Cache()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/networks/", response_model=List[Network])
async def networks():
    if cache.networks:
        return cache.networks
    bot = Networks(session=cache.client)
    cache.client = bot.session
    networks = bot.get()
    cache.networks = networks
    return networks


@app.get("/networks/{network_id}", response_model=Network)
async def network(network_id: str):
    if not cache.networks:
        bot = Networks(session=cache.client)
        cache.client = bot.session
        networks = bot.get()
        cache.networks = networks

    network = [n for n in cache.networks if n.id == network_id]
    if network:
        return network[0]
    raise HTTPException(status_code=404, detail=f"Network {network_id} not found")


@app.get("/networks/{network_id}/stations/", response_model=List[Station])
async def stations(network_id: str):
    print(network_id)
    if network_id == cache.network_id:
        if cache.stations:
            return cache.stations
        bot = Stations(session=cache.client, new_network=False)
    else:
        bot = Stations(session=cache.client, network_id=network_id)

    cache.network_id = network_id
    cache.client = bot.session
    stations = bot.get()
    cache.stations = stations
    return stations


@app.get("/networks/{network_id}/stations/{station_id}", response_model=Station)
async def station(network_id: str, station_id: str):
    print(network_id)
    if network_id == cache.network_id:
        if cache.stations:
            station = [s for s in cache.stations if s.id == station_id]
            if station:
                return station[0]
        bot = Stations(session=cache.client, new_network=False)
    else:
        bot = Stations(session=cache.client, network_id=network_id)

    cache.network_id = network_id
    cache.client = bot.session
    stations = bot.get()
    cache.stations = stations
    station = [s for s in cache.stations if s.id == station_id]
    if station:
        return station[0]
    raise HTTPException(
        status_code=404,
        detail=f"Station {station_id} in network {network_id} not found",
    )


@app.get(
    "/networks/{network_id}/stations/{station_id}/params",
    response_model=List[Parameter],
)
async def params(network_id: str, station_id: str):
    if network_id == cache.network_id:
        bot = Parameters(session=cache.client, new_network=False)
    else:
        bot = Parameters(session=cache.client, network_id=network_id)
    return bot.get(station_id)


@app.get("/data/")
async def data(
    station: str, parameter: str, tmin: str = "1980-01-01", tmax: str = "2020-12-31"
) -> List[DataEntry]:
    bot = GetData()
    return bot.get_data(
        station_id=station, parameter_id=parameter, tmin=tmin, tmax=tmax
    )
