from pydantic import BaseModel
from typing import List, Optional, Dict

class Entity(BaseModel):
    id: int
    name: str
    initial_quantity: float
    description: Optional[str] = None

class SimulationRequest(BaseModel):
    entity_id: int
    duration_hours: int  # Tiempo de simulación

class SimulationResult(BaseModel):
    ticket: int
    entity_id: int
    values: List[float]  # Variación en el tiempo
    status: str = "completed"
