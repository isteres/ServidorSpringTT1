from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict

class Punto(BaseModel):
    x: int
    y: int
    color: str

class Entidad(BaseModel):
    id: int
    name: str
    descripcion: str

class DatosSolicitud(BaseModel):
    nums: Dict[int, int]

class DatosSimulation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    max_segundos: int = Field(alias="maxSegundos")
    ancho_tablero: int = Field(alias="anchoTablero")
    # El mapa en Java es Map<Integer, List<Punto>> donde la clave es el tiempo 't'
    puntos: Dict[int, List[Punto]]
