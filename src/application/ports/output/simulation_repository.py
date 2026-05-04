from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.models import Entidad, DatosSimulation

class SimulationRepository(ABC):
    @abstractmethod
    def save_simulation(self, ticket: str, result: DatosSimulation) -> str:
        pass

    @abstractmethod
    def get_simulation(self, ticket: str) -> Optional[DatosSimulation]:
        pass

    @abstractmethod
    def get_entities(self) -> List[Entidad]:
        pass

    @abstractmethod
    def get_entity(self, entity_id: int) -> Optional[Entidad]:
        pass
