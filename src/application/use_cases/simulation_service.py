import random
import string
import math
from typing import List, Optional, Dict, Set, Tuple
from application.ports.input.simulation_use_case import SimulationUseCase
from application.ports.output.simulation_repository import SimulationRepository
from application.ports.output.message_broker_port import MessageBrokerPort
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
    def __init__(self, repository: SimulationRepository, broker: Optional[MessageBrokerPort] = None):
        self.repository = repository
        self.broker = broker

    def solicitar_simulacion(self, sol: DatosSolicitud) -> str:
        # Generar un ticket de 4 dígitos numéricos únicamente como entero
        ticket = random.randint(1000, 9999)
        
        # Guardamos la simulación como PENDIENTE
        self.repository.save_simulation(ticket, None)
        
        # Si hay broker configurado, enviamos la tarea de forma asíncrona
        if self.broker:
            self.broker.send_simulation_request(ticket, sol)
        else:
            # Fallback síncrono si no hay broker (útil para tests)
            resultado = self.ejecutar_simulacion(sol)
            self.repository.save_simulation(ticket, resultado)

        return ticket

    def ejecutar_simulacion(self, sol: DatosSolicitud) -> DatosSimulation:
        """Lógica pesada de simulación que ahora puede ejecutarse en un worker."""
        # Calculamos el total de entidades solicitadas
        total_entidades = sum(sol.nums.values())
        
        # Ajustamos el ancho proporcionalmente
        ancho_calculado = int((total_entidades * 10) ** 0.5) + 1
        ancho = max(10, min(ancho_calculado, 50))
        
        # Lógica de tiempo dinámico (ya implementada anteriormente)
        base_t = ancho * 0.8
        entity_bonus = total_entidades // 10
        num_clonadores = sol.nums.get(3, 0)
        
        if num_clonadores > 0:
            ratio_clonadores = num_clonadores / total_entidades
            crecimiento_por_paso = 1 + (0.8 * ratio_clonadores)
            limite_poblacion = 0.75 * (ancho ** 2)
            if limite_poblacion > total_entidades:
                pasos_hasta_saturacion = math.log(limite_poblacion / total_entidades) / math.log(crecimiento_por_paso)
                max_t_sugerido = int(pasos_hasta_saturacion + 5)
                max_t_calculado = min(int(base_t + entity_bonus + 5), max_t_sugerido)
            else:
                max_t_calculado = 10
        else:
            max_t_calculado = int(base_t + entity_bonus)
        
        max_t = max(10, min(max_t_calculado, 60))
        
        puntos_por_tiempo: Dict[int, List[Punto]] = {}

        # Estado inicial (T=0)
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

        puntos_por_tiempo[0] = [
            Punto(x=e["x"], y=e["y"], color=e["color"]) for e in entidades_en_escena
        ]

        # Evolución (T=1 a T=max_t-1)
        for t in range(1, max_t):
            lista_puntos_actuales = []
            nuevas_entidades_en_escena = []
            random.shuffle(entidades_en_escena)
            ocupadas_proximas = set()
            ocupadas_actuales = set((e["x"], e["y"]) for e in entidades_en_escena)

            for estado in entidades_en_escena:
                entidad = estado["entidad"]
                ocupadas_para_mi = (ocupadas_actuales | ocupadas_proximas) - {(estado["x"], estado["y"])}
                nuevas_posiciones = self._ejecutar_movimiento_logica(entidad, estado["x"], estado["y"], ancho, ocupadas_para_mi)

                if nuevas_posiciones:
                    ocupadas_actuales.discard((estado["x"], estado["y"]))
                    for nx, ny in nuevas_posiciones:
                        ocupadas_proximas.add((nx, ny))
                        nuevas_entidades_en_escena.append({"entidad": entidad, "x": nx, "y": ny, "color": estado["color"]})
                        lista_puntos_actuales.append(Punto(x=nx, y=ny, color=estado["color"]))

            puntos_por_tiempo[t] = lista_puntos_actuales
            entidades_en_escena = nuevas_entidades_en_escena

        return DatosSimulation(maxSegundos=max_t, anchoTablero=ancho, puntos=puntos_por_tiempo)

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
