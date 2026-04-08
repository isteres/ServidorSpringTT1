from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.models import Entity, SimulationResult

class SimulationRepository(ABC):
    @abstractmethod
    def save_simulation(self, result: SimulationResult) -> int:
        pass

    @abstractmethod
    def get_simulation(self, ticket: int) -> Optional[SimulationResult]:
        pass

    @abstractmethod
    def get_entities(self) -> List[Entity]:
        pass

    @abstractmethod
    def get_entity(self, entity_id: int) -> Optional[Entity]:
        pass
