from abc import ABC, abstractmethod
from domain.entities.models import DatosSolicitud

class MessageBrokerPort(ABC):
    @abstractmethod
    def send_simulation_request(self, ticket: int, sol: DatosSolicitud):
        pass
