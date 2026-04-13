from typing import List, Optional, Dict
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import (
    Entidad, EntidadEstatica, EntidadMovimientoAdyacente, EntidadEstáticaClon, DatosSimulation
)

class InMemorySimulationRepository(SimulationRepository):
    def __init__(self):
        # Entidades iniciales instanciadas con sus comportamientos concretos
        self.entities = {
            1: EntidadEstatica(
                id=1, 
                name="Entidad Estática", 
                descripcion="Mantiene sus puntos quietos en todo el tiempo."
            ),
            2: EntidadMovimientoAdyacente(
                id=2, 
                name="Entidad Movimiento Adyacente", 
                descripcion="Mueve sus puntos únicamente a posiciones adyacentes."
            ),
            3: EntidadEstáticaClon(
                id=3, 
                name="Entidad Estática Clon", 
                descripcion="Se mantiene quieta pero con probabilidad de clonarse."
            )
        }
        self.simulations: Dict[int, DatosSimulation] = {}

    def save_simulation(self, ticket: int, result: DatosSimulation) -> int:
        self.simulations[ticket] = result
        return ticket

    def get_simulation(self, ticket: int) -> Optional[DatosSimulation]:
        return self.simulations.get(ticket)

    def get_entities(self) -> List[Entidad]:
        return list(self.entities.values())

    def get_entity(self, entity_id: int) -> Optional[Entidad]:
        return self.entities.get(entity_id)
