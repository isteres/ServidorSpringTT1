import random
from typing import List, Optional, Dict, Set, Tuple
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
        
        # Estado inicial de la simulación
        entidades_en_escena = []
        for ent_id, cantidad in sol.nums.items():
            entidad_base = self.repository.get_entity(ent_id)
            if not entidad_base:
                continue
            for _ in range(cantidad):
                entidades_en_escena.append({
                    "entidad": entidad_base,
                    "x": random.randint(0, ancho - 1),
                    "y": random.randint(0, ancho - 1),
                    "color": self._get_color(ent_id)
                })

        # Generamos la evolución temporal (10 pasos)
        for t in range(max_t):
            lista_puntos_actuales = []
            nuevas_entidades_en_escena = []
            
            # Mezclamos para que el orden sea aleatorio cada turno (FCFS justo)
            random.shuffle(entidades_en_escena)
            
            # Set de ocupación para el PRÓXIMO instante (t+1)
            # Empezamos con el mapa actual, pero lo actualizaremos dinámicamente
            ocupadas_al_inicio = set((e["x"], e["y"]) for e in entidades_en_escena)

            for estado in entidades_en_escena:
                entidad = estado["entidad"]
                eid = entidad.id
                
                # Para decidir movimiento, pasamos el estado actual de ocupación
                # Una entidad PUEDE quedarse en su propia casilla (x,y),
                # por lo que quitamos su casilla actual de 'ocupadas' temporalmente
                # para que el método 'mover' sepa que su sitio está garantizado
                ocupadas_sin_mi = ocupadas_al_inicio - {(estado["x"], estado["y"])}
                
                nuevas_posiciones = entidad.mover(estado["x"], estado["y"], ancho, ocupadas_sin_mi)
                
                # Actualizamos ocupación global basándonos en el resultado del movimiento
                if nuevas_posiciones:
                    # Liberamos la posición antigua y reservamos la(s) nueva(s)
                    ocupadas_al_inicio.discard((estado["x"], estado["y"]))
                    for nx, ny in nuevas_posiciones:
                        ocupadas_al_inicio.add((nx, ny))
                        
                        # Guardamos el estado para el próximo paso temporal
                        nuevas_entidades_en_escena.append({
                            "entidad": entidad,
                            "x": nx,
                            "y": ny,
                            "color": estado["color"]
                        })
                        # Guardamos el punto para la visualización
                        lista_puntos_actuales.append(Punto(x=nx, y=ny, color=estado["color"]))
            
            puntos_por_tiempo[t] = lista_puntos_actuales
            entidades_en_escena = nuevas_entidades_en_escena

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
        colors = {1: "#FF5733", 2: "#33FF57", 3: "#3357FF"}
        return colors.get(ent_id, "#888888")
