from typing import List, Optional, Type

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from crawler.data import GetData
from crawler.networks import Networks
from crawler.parameters import Parameters
from crawler.stations import Stations
from models import DataEntryList, Network, Parameter, Station

from utils import parse_datetime


description = """
💧💧💧 access [SNIRH](https://snirh.apambiente.pt/) data  


[source code](https://github.com/franciscobmacedo/snirhAPI)

"""

app = FastAPI(
    title="snirhAPI",
    description=description,
    version="0.0.1",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/redoc")


@app.get("/networks/", response_model=List[Network])
async def networks():
    bot = Networks()
    networks = bot.get()
    # cache.networks = networks
    return networks


@app.get("/networks/{network_id}", response_model=Network)
async def network(network_id: str):
    bot = Networks()
    networks = bot.get()

    network = [n for n in networks if n.id == network_id]
    if network:
        return network[0]
    raise HTTPException(status_code=404, detail=f"Network {network_id} not found")


@app.get("/networks/{network_id}/stations/", response_model=List[Station])
async def stations(network_id: str):
    bot = Stations(network_id=network_id)
    stations = bot.get()
    return stations


@app.get("/networks/{network_id}/stations/{station_id}", response_model=Station)
async def station(network_id: str, station_id: str):
    bot = Stations(network_id=network_id)
    stations = bot.get()
    station = [s for s in stations if s.id == station_id]
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
    bot = Parameters(network_id=network_id)
    return bot.get(station_id)


@app.get("/data/", response_model=DataEntryList)
async def data(
    station_id: str = "1627758916",
    parameter_id: str = "1849",
    tmin: str = "1980-01-01",
    tmax: str = "2020-12-31",
) -> DataEntryList:
    return GetData().get_data(
        station_id=station_id,
        parameter_id=parameter_id,
        tmin=parse_datetime(tmin, format="%Y-%m-%d"),
        tmax=parse_datetime(tmax, format="%Y-%m-%d"),
    )
