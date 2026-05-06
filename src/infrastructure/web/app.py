from fastapi import FastAPI, HTTPException, Path, Depends
from typing import List
from sqlmodel import Session
from domain.entities.models import Entidad, DatosSolicitud, DatosSimulation
from application.use_cases.simulation_service import SimulationService
from infrastructure.adapters.sql_repository import SQLSimulationRepository
from infrastructure.database import create_db_and_tables, get_session

app = FastAPI(
    title="Servidor de Simulación Evolutiva",
    description="Motor de simulación evolutiva de entidades basado en Arquitectura Hexagonal.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_service(session: Session = Depends(get_session)):
    repository = SQLSimulationRepository(session)
    return SimulationService(repository)


@app.post("/simulation/solicitar", response_model=int)
def solicitar_simulacion(
    sol: DatosSolicitud, 
    service: SimulationService = Depends(get_service)
):
    try:
        return service.solicitar_simulacion(sol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/simulation/descargar/{ticket}",
    response_model=DatosSimulation,
    response_model_by_alias=True,
)
def descargar_datos(
    ticket: int = Path(..., description="Ticket de simulación"),
    service: SimulationService = Depends(get_service)
):
    data = service.descargar_datos(ticket)
    if not data:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
    return data


@app.get("/entities", response_model=List[Entidad])
def get_entities(service: SimulationService = Depends(get_service)):
    return service.get_entities()


@app.get("/entities/validate/{entity_id}", response_model=bool)
def is_valid_entity_id(
    entity_id: int,
    service: SimulationService = Depends(get_service)
):
    return service.is_valid_entity_id(entity_id)
