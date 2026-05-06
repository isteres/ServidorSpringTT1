from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.models import Entidad, DatosSolicitud, DatosSimulation

class SimulationUseCase(ABC):
    @abstractmethod
    def solicitar_simulacion(self, sol: DatosSolicitud) -> int:
        pass

    @abstractmethod
    def descargar_datos(self, ticket: int) -> Optional[DatosSimulation]:
        pass

    @abstractmethod
    def get_entities(self) -> List[Entidad]:
        pass

    @abstractmethod
    def is_valid_entity_id(self, entity_id: int) -> bool:
        pass
