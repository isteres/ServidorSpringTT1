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
    status: str = Field(default="PENDIENTE")  # PENDIENTE, COMPLETADO, ERROR
    max_segundos: Optional[int] = Field(default=None)
    ancho_tablero: Optional[int] = Field(default=None)
    # Almacenamos el diccionario de puntos como JSON, puede ser nulo mientras está pendiente
    puntos: Optional[Dict[str, List[dict]]] = Field(default=None, sa_column=Column(JSON))
    
    # Clave foránea al usuario (nula por ahora)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

class UserTable(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None)
    hashed_password: str = Field()
    disabled: Optional[bool] = Field(default=False)
