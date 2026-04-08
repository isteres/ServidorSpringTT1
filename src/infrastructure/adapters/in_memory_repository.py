from typing import List, Optional, Dict
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import Entity, SimulationResult

class InMemorySimulationRepository(SimulationRepository):
    def __init__(self):
        # Entidades iniciales
        self.entities = {
            1: Entity(id=1, name="Entidad 1 (Estática)", initial_quantity=100.0),
            2: Entity(id=2, name="Entidad 2 (Estática)", initial_quantity=200.0),
            3: Entity(id=3, name="Entidad 3 (Dinámica)", initial_quantity=50.0)
        }
        self.simulations: Dict[int, SimulationResult] = {}

    def save_simulation(self, result: SimulationResult) -> int:
        self.simulations[result.ticket] = result
        return result.ticket

    def get_simulation(self, ticket: int) -> Optional[SimulationResult]:
        return self.simulations.get(ticket)

    def get_entities(self) -> List[Entity]:
        return list(self.entities.values())

    def get_entity(self, entity_id: int) -> Optional[Entity]:
        return self.entities.get(entity_id)
