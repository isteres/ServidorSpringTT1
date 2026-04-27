from __future__ import annotations
from typing import Optional, Dict, List
from sqlmodel import SQLModel, Field, Column, JSON
from domain.entities.models import DatosSimulation

class EntityTable(SQLModel, table=True):
    __tablename__ = "entities"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    descripcion: str = Field()
    type: str = Field()  # Para saber si es Estática, MovimientoAdyacente, etc.

class SimulationTable(SQLModel, table=True):
    __tablename__ = "simulations"
    ticket: int = Field(primary_key=True)
    max_segundos: int = Field()
    ancho_tablero: int = Field()
    # Almacenamos el diccionario de puntos como JSON
    puntos: Dict[str, List[dict]] = Field(default_factory=dict, sa_column=Column(JSON))
