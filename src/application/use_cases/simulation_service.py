from typing import List, Optional
import random
from application.ports.input.simulation_use_case import SimulationUseCase
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import Entity, SimulationRequest, SimulationResult

class SimulationService(SimulationUseCase):
    def __init__(self, repository: SimulationRepository):
        self.repository = repository

    def solicitar_simulacion(self, sol: SimulationRequest) -> int:
        entity = self.repository.get_entity(sol.entity_id)
        if not entity:
            raise ValueError(f"Entidad con ID {sol.entity_id} no encontrada")
        
        # Lógica de simulación: Generamos datos variando según el tiempo (horas)
        # Si es la entidad 3 (id=3), varía en el tiempo. Las otras son estáticas.
        values = []
        current_val = entity.initial_quantity
        
        for t in range(sol.duration_hours):
            if entity.id == 3:
                # Variación aleatoria simple para la entidad 3
                current_val += random.uniform(-5, 10)
            values.append(round(current_val, 2))
            
        ticket = random.randint(1000, 9999)
        result = SimulationResult(
            ticket=ticket,
            entity_id=sol.entity_id,
            values=values,
            status="completed"
        )
        
        return self.repository.save_simulation(result)

    def descargar_datos(self, ticket: int) -> Optional[SimulationResult]:
        return self.repository.get_simulation(ticket)

    def get_entities(self) -> List[Entity]:
        return self.repository.get_entities()

    def is_valid_entity_id(self, entity_id: int) -> bool:
        return self.repository.get_entity(entity_id) is not None
