from fastapi import FastAPI, HTTPException, Path
from typing import List
from domain.entities.models import Entidad, DatosSolicitud, DatosSimulation
from application.use_cases.simulation_service import SimulationService
from infrastructure.adapters.in_memory_repository import InMemorySimulationRepository

app = FastAPI(title="Servidor de Simulación Hexagonal (TT1)")

# Inyección de dependencias manual
repository = InMemorySimulationRepository()
service = SimulationService(repository)

@app.post("/simulation/solicitar", response_model=int)
def solicitar_simulacion(sol: DatosSolicitud):
    try:
        return service.solicitar_simulacion(sol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/simulation/descargar/{ticket}", response_model=DatosSimulation, response_model_by_alias=True)
def descargar_datos(ticket: int = Path(..., description="Ticket de simulación")):
    data = service.descargar_datos(ticket)
    if not data:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    return data

@app.get("/entities", response_model=List[Entidad])
def get_entities():
    return service.get_entities()

@app.get("/entities/validate/{entity_id}", response_model=bool)
def is_valid_entity_id(entity_id: int):
    return service.is_valid_entity_id(entity_id)
