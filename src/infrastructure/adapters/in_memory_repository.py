from typing import List, Optional, Dict
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import Entidad, DatosSimulation

class InMemorySimulationRepository(SimulationRepository):
    def __init__(self):
        # Entidades iniciales alineadas con el cliente (ID 1, 2, 3)
        self.entities = {
            1: Entidad(id=1, name="Parámetro 1", descripcion="Controlan la temperatura ambiental."),
            2: Entidad(id=2, name="Parámetro 2", descripcion="Miden el nivel de humedad en el aire."),
            3: Entidad(id=3, name="Parámetro 3", descripcion="Sistemas de vigilancia por video.")
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
