import random
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Tuple, Set


class Punto(BaseModel):
    x: int
    y: int
    color: str


class Entidad(BaseModel, ABC):
    id: int
    name: str
    descripcion: str

    @abstractmethod
    def mover(
        self, x: int, y: int, ancho: int, ocupadas: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Calcula la(s) nueva(s) posición(es) de la entidad."""
        pass


class EntidadEstatica(Entidad):
    def mover(
        self, x: int, y: int, ancho: int, ocupadas: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        # Se queda quieta
        return [(x, y)]


class EntidadMovimientoAdyacente(Entidad):
    def mover(
        self, x: int, y: int, ancho: int, ocupadas: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        # Intentamos movernos a una posición adyacente libre (solo H/V)
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcciones)


        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            # Verificar límites y si está libre
            if 0 <= nx < ancho and 0 <= ny < ancho:
                if (nx, ny) not in ocupadas:
                    return [(nx, ny)]  # Éxito: se mueve a nueva casilla

        # Fallback: Si no puede moverse a ninguna, se queda donde está (garantizado)
        return [(x, y)]


class EntidadEstáticaClon(EntidadEstatica):
    def mover(
        self, x: int, y: int, ancho: int, ocupadas: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        # La entidad original siempre se queda en su sitio (garantizado)
        posiciones = [(x, y)]

        # Intento de clonación
        if random.random() < 0.5:
            # Buscamos una casilla vacía aleatoriamente (máximo 10 intentos para eficiencia)
            for _ in range(10):
                nx, ny = random.randint(0, ancho - 1), random.randint(0, ancho - 1)
                # El clon no puede estar en la misma casilla que el original 
                # ni en una casilla ocupada por otros
                if (nx, ny) != (x, y) and (nx, ny) not in ocupadas:
                    posiciones.append((nx, ny))
                    break
        return posiciones


class DatosSolicitud(BaseModel):
    nums: Dict[int, int]


class DatosSimulation(BaseModel):
    max_segundos: int = Field(alias="maxSegundos")
    ancho_tablero: int = Field(alias="anchoTablero")
    puntos: Dict[int, List[Punto]]
