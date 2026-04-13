import random
from typing import List, Optional, Dict
from application.ports.input.simulation_use_case import SimulationUseCase
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import Entidad, DatosSolicitud, DatosSimulation, Punto

class SimulationService(SimulationUseCase):
    def __init__(self, repository: SimulationRepository):
        self.repository = repository

    def solicitar_simulacion(self, sol: DatosSolicitud) -> int:
        ancho = 10
        max_t = 10
        puntos_por_tiempo: Dict[int, List[Punto]] = {}
        
        # Inicializamos posiciones para cada entidad solicitada
        # Guardamos el estado actual de las entidades para moverlas en el tiempo
        entidades_estado = []
        for ent_id, cantidad in sol.nums.items():
            if not self.is_valid_entity_id(ent_id):
                continue
            for _ in range(cantidad):
                entidades_estado.append({
                    "id": ent_id,
                    "x": random.randint(0, ancho - 1),
                    "y": random.randint(0, ancho - 1),
                    "color": self._get_color(ent_id)
                })

        # Generamos la evolución temporal (10 pasos)
        for t in range(max_t):
            lista_puntos = []
            for ent in entidades_estado:
                # Movimiento aleatorio simple (-1, 0, 1) manteniéndose en el tablero
                ent["x"] = max(0, min(ancho - 1, ent["x"] + random.randint(-1, 1)))
                ent["y"] = max(0, min(ancho - 1, ent["y"] + random.randint(-1, 1)))
                
                lista_puntos.append(Punto(
                    x=ent["x"],
                    y=ent["y"],
                    color=ent["color"]
                ))
            puntos_por_tiempo[t] = lista_puntos

        ticket = random.randint(1000, 9999)
        resultado = DatosSimulation(
            maxSegundos=max_t,
            anchoTablero=ancho,
            puntos=puntos_por_tiempo
        )
        
        return self.repository.save_simulation(ticket, resultado)

    def descargar_datos(self, ticket: int) -> Optional[DatosSimulation]:
        return self.repository.get_simulation(ticket)

    def get_entities(self) -> List[Entidad]:
        return self.repository.get_entities()

    def is_valid_entity_id(self, entity_id: int) -> bool:
        return self.repository.get_entity(entity_id) is not None

    def _get_color(self, ent_id: int) -> str:
        # Colores básicos para distinguir entidades en el mapa
        colors = {1: "#FF5733", 2: "#33FF57", 3: "#3357FF"}
        return colors.get(ent_id, "#888888")
