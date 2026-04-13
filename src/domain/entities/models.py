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
        # Movimiento a posiciones adyacentes (-1, 0, 1)
        nx = max(0, min(ancho - 1, x + random.randint(-1, 1)))
        ny = max(0, min(ancho - 1, y + random.randint(-1, 1)))
        return [(nx, ny)]


class EntidadEstáticaClon(EntidadEstatica):
    def mover(
        self, x: int, y: int, ancho: int, ocupadas: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        posiciones = super().mover(x, y, ancho, ocupadas)
        # Probabilidad de clonar (ej: 10% por paso de tiempo)
        if random.random() < 0.1:
            # Buscar una posición del tablero que no esté ocupada por su misma raza
            posibles_vacias = (
                set((i, j) for i in range(ancho) for j in range(ancho)) - ocupadas
            )
            if posibles_vacias:
                nx, ny = random.choice(list(posibles_vacias))
                posiciones.append((nx, ny))
        return posiciones


class DatosSolicitud(BaseModel):
    nums: Dict[int, int]


class DatosSimulation(BaseModel):
    max_segundos: int = Field(alias="maxSegundos")
    ancho_tablero: int = Field(alias="anchoTablero")
    puntos: Dict[int, List[Punto]]
