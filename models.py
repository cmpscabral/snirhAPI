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


class Parameter(BaseModel):
    id: str
    name: str

    @validator("name")
    def validate_optional_str_fields(cls, name: str) -> str:
        return name.strip("*").strip(" ")


class DataEntry(BaseModel):
    timestamp: datetime.datetime
    value: float

    @validator("value")
    def validate_value(cls, value: str) -> float:
        return float(value)


class DataEntryList(BaseModel):
    __root__: list[DataEntry]
