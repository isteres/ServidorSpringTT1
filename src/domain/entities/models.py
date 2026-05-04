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
    nums: Dict[int, int] = Field(..., description="Diccionario con pares {id_entidad: cantidad} para la simulación")


class DatosSimulation(BaseModel):
    max_segundos: int = Field(alias="maxSegundos", description="Duración total de la simulación en segundos")
    ancho_tablero: int = Field(alias="anchoTablero", description="Ancho del tablero cuadrado (ej. 10 para 10x10)")
    puntos: Dict[int, List[Punto]] = Field(..., description="Evolución temporal de los puntos {segundo: [Puntos]}")


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
