import sys
import os
import random
import pytest

# Añadir 'src' al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../../src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from domain.entities.models import (
    EntidadEstatica, EntidadMovimientoAdyacente, EntidadEstáticaClon
)

def test_entidad_estatica_stays_put():
    entidad = EntidadEstatica(id=1, name="Estatica", descripcion="Desc")
    posiciones = entidad.mover(5, 5, 10, set())
    assert posiciones == [(5, 5)]

def test_entidad_movimiento_adyacente_moves():
    entidad = EntidadMovimientoAdyacente(id=2, name="Movil", descripcion="Desc")
    x, y = 5, 5
    ancho = 10
    ocupadas = set()
    
    posiciones = entidad.mover(x, y, ancho, ocupadas)
    
    assert len(posiciones) == 1
    nx, ny = posiciones[0]
    
    # Debe ser una posición adyacente (H/V) o la misma si no hay hueco
    distancia = abs(nx - x) + abs(ny - y)
    assert distancia <= 1
    assert 0 <= nx < ancho
    assert 0 <= ny < ancho

def test_entidad_movimiento_adyacente_blocked():
    entidad = EntidadMovimientoAdyacente(id=2, name="Movil", descripcion="Desc")
    x, y = 5, 5
    ancho = 10
    # Bloqueamos todas las adyacentes (solo H/V: (5,6), (5,4), (6,5), (4,5))
    ocupadas = {(5, 6), (5, 4), (6, 5), (4, 5)}
    
    posiciones = entidad.mover(x, y, ancho, ocupadas)
    
    # Debe quedarse en su sitio
    assert posiciones == [(5, 5)]

def test_entidad_movimiento_adyacente_boundaries():
    entidad = EntidadMovimientoAdyacente(id=2, name="Movil", descripcion="Desc")
    x, y = 0, 0
    ancho = 10
    # Solo puede ir a (0,1) o (1,0)
    
    # Hacemos muchos intentos para asegurar que probamos las opciones
    for _ in range(20):
        posiciones = entidad.mover(x, y, ancho, set())
        nx, ny = posiciones[0]
        assert nx >= 0 and ny >= 0
        assert (nx, ny) in [(0, 0), (0, 1), (1, 0)]

def test_entidad_estatica_clon_stays_and_clones():
    entidad = EntidadEstáticaClon(id=3, name="Clonador", descripcion="Desc")
    x, y = 5, 5
    ancho = 10
    
    # Forzamos la probabilidad de clonación si fuera posible, 
    # pero como es random.random(), simplemente probamos que la original se queda
    posiciones = entidad.mover(x, y, ancho, set())
    
    assert (x, y) in posiciones
    assert len(posiciones) <= 2
    if len(posiciones) == 2:
        nx, ny = posiciones[1]
        assert 0 <= nx < ancho
        assert 0 <= ny < ancho
        assert (nx, ny) != (x, y)

def test_entidad_estatica_clon_does_not_clone_to_occupied():
    # Este es difícil de probar determinísticamente sin mocks, 
    # pero podemos probar que SI devuelve una posición, no está en 'ocupadas'
    entidad = EntidadEstáticaClon(id=3, name="Clonador", descripcion="Desc")
    x, y = 5, 5
    ancho = 10
    # Ocupamos casi todo el tablero excepto la posición original
    ocupadas = set()
    for i in range(ancho):
        for j in range(ancho):
            if (i, j) != (x, y):
                ocupadas.add((i, j))
    
    # Con el tablero lleno, no debería poder clonar
    posiciones = entidad.mover(x, y, ancho, ocupadas)
    assert posiciones == [(x, y)]
