from typing import List, Optional
from sqlmodel import Session, select
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import (
    Entidad, EntidadEstatica, EntidadMovimientoAdyacente, EntidadEstáticaClon, DatosSimulation, Punto
)
from infrastructure.adapters.sql_models import EntityTable, SimulationTable

class SQLSimulationRepository(SimulationRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_simulation(self, ticket: int, result: Optional[DatosSimulation]) -> int:
        # Si no hay resultado, se guarda como PENDIENTE
        if result is None:
            db_sim = SimulationTable(
                ticket=ticket,
                status="PENDIENTE",
                user_id=None
            )
            self.session.add(db_sim)
            self.session.commit()
            return ticket

        # Si hay resultado, se guarda como COMPLETADO o se actualiza
        puntos_json = {
            str(k): [p.model_dump() for p in v] 
            for k, v in result.puntos.items()
        }
        
        # Intentar buscar si ya existe (para actualización por el worker)
        statement = select(SimulationTable).where(SimulationTable.ticket == ticket)
        db_sim = self.session.exec(statement).first()
        
        if db_sim:
            db_sim.status = "COMPLETADO"
            db_sim.max_segundos = result.max_segundos
            db_sim.ancho_tablero = result.ancho_tablero
            db_sim.puntos = puntos_json
        else:
            db_sim = SimulationTable(
                ticket=ticket,
                status="COMPLETADO",
                max_segundos=result.max_segundos,
                ancho_tablero=result.ancho_tablero,
                puntos=puntos_json,
                user_id=None
            )
        
        self.session.add(db_sim)
        self.session.commit()
        return ticket

    def get_simulation(self, ticket: int) -> Optional[DatosSimulation]:
        statement = select(SimulationTable).where(SimulationTable.ticket == ticket)
        db_sim = self.session.exec(statement).first()
        if not db_sim or db_sim.status != "COMPLETADO":
            return None
        
        # Reconstruimos DatosSimulation
        puntos = {
            int(k): [Punto(**p) for p in v] 
            for k, v in db_sim.puntos.items()
        }
        
        return DatosSimulation(
            maxSegundos=db_sim.max_segundos,
            anchoTablero=db_sim.ancho_tablero,
            puntos=puntos
        )

    def get_entities(self) -> List[Entidad]:
        statement = select(EntityTable)
        db_entities = self.session.exec(statement).all()
        return [self._map_to_domain(e) for e in db_entities]

    def get_entity(self, entity_id: int) -> Optional[Entidad]:
        statement = select(EntityTable).where(EntityTable.id == entity_id)
        db_entity = self.session.exec(statement).first()
        if not db_entity:
            return None
        return self._map_to_domain(db_entity)

    def _map_to_domain(self, db_entity: EntityTable) -> Entidad:
        if db_entity.type == "Estatica":
            return EntidadEstatica(id=db_entity.id, name=db_entity.name, descripcion=db_entity.descripcion)
        elif db_entity.type == "MovimientoAdyacente":
            return EntidadMovimientoAdyacente(id=db_entity.id, name=db_entity.name, descripcion=db_entity.descripcion)
        elif db_entity.type == "EstaticaClon":
            return EntidadEstáticaClon(id=db_entity.id, name=db_entity.name, descripcion=db_entity.descripcion)
        return EntidadEstatica(id=db_entity.id, name=db_entity.name, descripcion=db_entity.descripcion)
