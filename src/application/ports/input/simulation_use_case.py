from abc import ABC, abstractmethod
from typing import List
from domain.entities.models import Entity, SimulationRequest, SimulationResult

class SimulationUseCase(ABC):
    @abstractmethod
    def solicitar_simulacion(self, sol: SimulationRequest) -> int:
        pass

    @abstractmethod
    def descargar_datos(self, ticket: int) -> SimulationResult:
        pass

    @abstractmethod
    def get_entities(self) -> List[Entity]:
        pass

    @abstractmethod
    def is_valid_entity_id(self, entity_id: int) -> bool:
        pass
