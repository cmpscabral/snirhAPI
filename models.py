from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator
import datetime


class StationState:
    ativa = "ATIVA"
    extinta = "EXTINTA"
    desativada = "DESATIVADA"
    reativada = "REATIVADA"
    suspensa = "SUSPENSA"
    convencional = "INSTALAÇÃO CONVENCIONAL"
    automatica = "INSTALAÇÃO AUTOMÁTICA"
    em_servico = "EM SERVIÇO"
    entulhado = "ENTULHADO"
    abandonado = "ABANDONADO"
    em_reserva = "EM RESERVA"
    destruido = "DESTRUÍDO"
    selado = "SELADO"
    cimentado = "CIMENTADO"
    assoreado = "ASSOREADO"


class Network(BaseModel):
    id: str
    name: str

    @validator("name")
    def validate_optional_str_fields(cls, name: str) -> str:
        return name.strip("*").strip(" ")

    class Config:
        schema_extra = {"example": {"id": "920123705", "name": "Hidrométrica"}}


class Station(BaseModel):
    id: str
    codigo: str
    nome: str
    altitude: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    coord_x: Optional[str]
    coord_y: Optional[str]
    bacia: Optional[str]
    distrito: Optional[str]
    concelho: Optional[str]
    freguesia: Optional[str]
    entidade_responsavel_automatica: Optional[str]
    entidade_responsavel_convencional: Optional[str]
    tipo_estacao_automatica: Optional[str]
    tipo_estacao_convencional: Optional[str]
    entrada_funcionamento_convencional: Optional[str]
    entrada_funcionamento_automatica: Optional[str]
    encerramento_convencional: Optional[str]
    encerramento_automatica: Optional[str]
    telemetria: bool
    estado: Optional[str]
    indice_qualidade: Optional[str]

    @validator(
        "entidade_responsavel_automatica",
        "tipo_estacao_automatica",
        "entrada_funcionamento_convencional",
        "entrada_funcionamento_automatica",
        "encerramento_convencional",
        "encerramento_automatica",
        "estado",
    )
    def validate_optional_str_fields(cls, field: str) -> Optional[str]:
        if field == "-" or field == "":
            return None
        return field

    class Config:
        schema_extra = {
            "example": {
                "id": "1627743378",
                "codigo": "19B/01H",
                "nome": "A-DOS-CUNHADOS",
                "altitude": "14",
                "latitude": "39.152",
                "longitude": "-9.302",
                "coord_x": "98984.104",
                "coord_y": "243387.146",
                "bacia": "RIBEIRAS DO OESTE",
                "distrito": "LISBOA",
                "concelho": "TORRES VEDRAS",
                "freguesia": "A DOS CUNHADOS",
                "entidade_responsavel_automatica": "Autoridade Nacional da Água",
                "entidade_responsavel_convencional": "-",
                "tipo_estacao_automatica": "SENSOR DE NÍVEL",
                "tipo_estacao_convencional": "-",
                "entrada_funcionamento_convencional": None,
                "entrada_funcionamento_automatica": "15-02-2002",
                "encerramento_convencional": None,
                "encerramento_automatica": None,
                "telemetria": False,
                "estado": "SUSPENSA",
                "indice_qualidade": None,
            }
        }


class Parameter(BaseModel):
    id: str
    name: str

    @validator("name")
    def validate_optional_str_fields(cls, name: str) -> str:
        return name.strip("*").strip(" ")

    class Config:
        schema_extra = {"example": {"id": "1849", "name": "Escoamento mensal"}}


class DataEntry(BaseModel):
    timestamp: datetime.datetime
    value: float

    @validator("value")
    def validate_value(cls, value: str) -> float:
        return float(value)

    class Config:
        schema_extra = {
            "example": {"timestamp": "1980-01-01T00:00:00", "value": 851030}
        }


class DataEntryList(BaseModel):
    __root__: list[DataEntry]

    class Config:
        schema_extra = {
            "example": [
                {"timestamp": "1980-01-01T00:00:00", "value": 851030},
                {"timestamp": "1980-01-02T00:00:00", "value": 631010},
                {"timestamp": "1980-01-03T00:00:00", "value": 231010},
            ]
        }
