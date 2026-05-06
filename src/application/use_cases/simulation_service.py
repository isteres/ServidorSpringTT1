import random
import string
from typing import List, Optional, Dict, Set, Tuple
from application.ports.input.simulation_use_case import SimulationUseCase
from application.ports.output.simulation_repository import SimulationRepository
from domain.entities.models import (
    Entidad,
    DatosSolicitud,
    DatosSimulation,
    Punto,
    EntidadEstatica,
    EntidadMovimientoAdyacente,
    EntidadEstáticaClon,
)


class SimulationService(SimulationUseCase):
    def __init__(self, repository: SimulationRepository):
        self.repository = repository

    def solicitar_simulacion(self, sol: DatosSolicitud) -> str:
        # Calculamos el total de entidades solicitadas
        total_entidades = sum(sol.nums.values())
        
        # Ajustamos el ancho proporcionalmente: 
        # Queremos que la densidad sea baja (10%).
        # El área debe ser 10 veces el número de entidades.
        # ancho = raiz_cuadrada(total_entidades * 10)
        ancho_calculado = int((total_entidades * 10) ** 0.5) + 1
        
        # Mantenemos un mínimo de 10 y un máximo de 50 para no saturar el servidor
        ancho = max(10, min(ancho_calculado, 50))
        
        # El tiempo de simulación escala con el tamaño del tablero y el número de entidades.
        # - base_t: Proporcional al ancho para permitir desplazamiento significativo.
        # - entity_bonus: Un pequeño incremento por cada 10 entidades.
        # - cloner_bonus: Si hay entidades que se clonan (ID 3), extendemos el tiempo para ver la expansión.
        base_t = ancho * 0.8
        entity_bonus = total_entidades // 10
        cloner_bonus = 5 if sol.nums.get(3, 0) > 0 else 0
        
        max_t_calculado = int(base_t + entity_bonus + cloner_bonus)
        
        # Ampliamos el rango: mínimo 10 y máximo 60 para simulaciones más ricas
        max_t = max(10, min(max_t_calculado, 60))
        
        puntos_por_tiempo: Dict[int, List[Punto]] = {}

        # Estado inicial de la simulación: obtener todas las posiciones posibles y mezclarlas
        todas_posiciones = [(x, y) for x in range(ancho) for y in range(ancho)]
        random.shuffle(todas_posiciones)
        pos_idx = 0

        entidades_en_escena = []
        for ent_id, cantidad in sol.nums.items():
            entidad_base = self.repository.get_entity(ent_id)
            if not entidad_base:
                continue
            for _ in range(cantidad):
                if pos_idx < len(todas_posiciones):
                    x, y = todas_posiciones[pos_idx]
                    entidades_en_escena.append(
                        {
                            "entidad": entidad_base,
                            "x": x,
                            "y": y,
                            "color": self._get_color(ent_id),
                        }
                    )
                    pos_idx += 1

        # T=0: Guardamos el estado inicial exacto (sin movimientos ni clones)
        puntos_por_tiempo[0] = [
            Punto(x=e["x"], y=e["y"], color=e["color"]) for e in entidades_en_escena
        ]

        # Generamos la evolución temporal para los siguientes pasos (de 1 a max_t-1)
        for t in range(1, max_t):
            lista_puntos_actuales = []
            nuevas_entidades_en_escena = []
            
            # Mezclamos para que el orden sea aleatorio cada turno (FCFS justo)
            random.shuffle(entidades_en_escena)
            
            # Tracking de ocupación
            ocupadas_proximas = set()

            ocupadas_actuales = set((e["x"], e["y"]) for e in entidades_en_escena)

            for estado in entidades_en_escena:
                entidad = estado["entidad"]

                # Para decidir movimiento, pasamos el estado actual de ocupación
                ocupadas_para_mi = (ocupadas_actuales | ocupadas_proximas) - {
                    (estado["x"], estado["y"])
                }

                # Lógica de negocio de movimiento extraída del dominio
                nuevas_posiciones = self._ejecutar_movimiento_logica(
                    entidad, estado["x"], estado["y"], ancho, ocupadas_para_mi
                )

                if nuevas_posiciones:
                    ocupadas_actuales.discard((estado["x"], estado["y"]))
                    for nx, ny in nuevas_posiciones:
                        ocupadas_proximas.add((nx, ny))

                        nuevas_entidades_en_escena.append(
                            {
                                "entidad": entidad,
                                "x": nx,
                                "y": ny,
                                "color": estado["color"],
                            }
                        )
                        lista_puntos_actuales.append(
                            Punto(x=nx, y=ny, color=estado["color"])
                        )

            puntos_por_tiempo[t] = lista_puntos_actuales
            entidades_en_escena = nuevas_entidades_en_escena

        # Generar un ticket de 4 dígitos numéricos únicamente como entero
        ticket = random.randint(1000, 9999)
        resultado = DatosSimulation(
            maxSegundos=max_t, anchoTablero=ancho, puntos=puntos_por_tiempo
        )

        return self.repository.save_simulation(ticket, resultado)

    def _ejecutar_movimiento_logica(
        self,
        entidad: Entidad,
        x: int,
        y: int,
        ancho: int,
        ocupadas: Set[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        """Lógica de negocio que decide cómo se mueve cada tipo de entidad."""

        if isinstance(entidad, EntidadMovimientoAdyacente):
            # Movimiento solo H/V (Von Neumann)
            direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(direcciones)
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if 0 <= nx < ancho and 0 <= ny < ancho:
                    if (nx, ny) not in ocupadas:
                        return [(nx, ny)]
            return [(x, y)]

        elif isinstance(entidad, EntidadEstáticaClon):
            posiciones = [(x, y)]
            if random.random() < 0.8:
                # Buscar adyacente libre H/V (Von Neumann)
                direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(direcciones)
                for dx, dy in direcciones:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < ancho and 0 <= ny < ancho:
                        if (nx, ny) not in ocupadas:
                            posiciones.append((nx, ny))
                            break
            return posiciones

        # Fallback para EntidadEstatica o desconocidas
        return [(x, y)]

    def descargar_datos(self, ticket: int) -> Optional[DatosSimulation]:
        return self.repository.get_simulation(ticket)

    def get_entities(self) -> List[Entidad]:
        return self.repository.get_entities()

    def is_valid_entity_id(self, entity_id: int) -> bool:
        return self.repository.get_entity(entity_id) is not None

    def _get_color(self, ent_id: int) -> str:
        colors = {1: "#FF5733", 2: "#33FF57", 3: "#3357FF"}
        return colors.get(ent_id, "#888888")
