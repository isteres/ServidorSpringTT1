import random
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Tuple, Set


class Punto(BaseModel):
    x: int
    y: int
    color: str


class Entidad(BaseModel, ABC):
    id: int
    name: str
    descripcion: str


class EntidadEstatica(Entidad):
    pass


class EntidadMovimientoAdyacente(Entidad):
    pass


class EntidadEstáticaClon(EntidadEstatica):
    pass


class DatosSolicitud(BaseModel):
    nums: Dict[int, int]


class DatosSimulation(BaseModel):
    max_segundos: int = Field(alias="maxSegundos")
    ancho_tablero: int = Field(alias="anchoTablero")
    puntos: Dict[int, List[Punto]]
