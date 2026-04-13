from pydantic import BaseModel, Field
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
    max_segundos: int = Field(alias="maxSegundos")
    ancho_tablero: int = Field(alias="anchoTablero")
    # El mapa en Java es Map<Integer, List<Punto>> donde la clave es el tiempo 't'
    puntos: Dict[int, List[Punto]]

    class Config:
        populate_by_name = True
        # Esto permite que FastAPI use los nombres de los alias al generar el JSON
        # para que Java (Jackson) los reconozca automáticamente.
        json_encoders = {
            # Opcional: configuraciones adicionales de codificación si fuera necesario
        }
