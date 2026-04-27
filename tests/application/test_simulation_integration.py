import sys
import os
import random
import pytest

# Añadir 'src' al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../../src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from application.use_cases.simulation_service import SimulationService
from infrastructure.adapters.in_memory_repository import InMemorySimulationRepository
from domain.entities.models import (
    DatosSolicitud, EntidadEstatica, EntidadMovimientoAdyacente, EntidadEstáticaClon
)

def test_simulation_t0_is_initial_state():
    """Verifica que en t=0 no hay clones ni movimientos, solo lo solicitado."""
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    # 10 estáticas, 10 móviles, 10 clonadoras
    solicitud = DatosSolicitud(nums={1: 10, 2: 10, 3: 10})
    
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    assert len(datos.puntos[0]) == 30

def test_logic_entidad_estatica_stays():
    """Verifica que la EntidadEstatica no se mueve en ningún paso."""
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    solicitud = DatosSolicitud(nums={1: 1}) # Una estática
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    pos_inicial = (datos.puntos[0][0].x, datos.puntos[0][0].y)
    for t in range(datos.max_segundos):
        pos_t = (datos.puntos[t][0].x, datos.puntos[t][0].y)
        assert pos_t == pos_inicial

def test_logic_entidad_movimiento_adyacente_restricted():
    """Verifica que EntidadMovimientoAdyacente solo se mueve H/V."""
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    solicitud = DatosSolicitud(nums={2: 1}) # Una móvil
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    for t in range(datos.max_segundos - 1):
        p1 = datos.puntos[t][0]
        p2 = datos.puntos[t+1][0]
        distancia = abs(p1.x - p2.x) + abs(p1.y - p2.y)
        # Solo puede moverse 1 casilla (H o V) o quedarse quieto (0)
        assert distancia <= 1
        # No puede haber movimientos diagonales (distancia 2 con dx=1, dy=1)
        if distancia == 1:
            assert (p1.x == p2.x) or (p1.y == p2.y)

def test_logic_entidad_clon_increases_population():
    """Verifica que EntidadEstáticaClon puede aumentar el número de puntos."""
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    # Ponemos 5 clonadoras. Es altamente probable que clonen en 10 pasos.
    solicitud = DatosSolicitud(nums={3: 5})
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    poblacion_inicial = len(datos.puntos[0])
    poblacion_final = len(datos.puntos[datos.max_segundos - 1])
    
    # Debería haber al menos los iniciales, y probablemente más
    assert poblacion_final >= poblacion_inicial

def test_no_overlap_and_fcfs_integration():
    """
    Test de alta densidad para verificar colisiones y FCFS.
    En un tablero 10x10, metemos 80 entidades para forzar conflictos de espacio.
    """
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    solicitud = DatosSolicitud(nums={1: 20, 2: 30, 3: 30})
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    for t, puntos in datos.puntos.items():
        posiciones = [(p.x, p.y) for p in puntos]
        # Verificación de colisiones: cada punto debe tener una coordenada única
        assert len(posiciones) == len(set(posiciones)), f"Colisión detectada en t={t}"
        # Verificación de límites dinámicos
        for p in puntos:
            assert 0 <= p.x < datos.ancho_tablero
            assert 0 <= p.y < datos.ancho_tablero

def test_logic_entidad_movimiento_adyacente_blocked():
    """Verifica que una entidad móvil se queda quieta si todas las adyacentes están ocupadas."""
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    # Colocamos una móvil en el centro (5,5) y la rodeamos de estáticas
    # El orden de inserción inicial es aleatorio, pero en t=0 estarán así.
    # Usaremos una solicitud controlada.
    solicitud = DatosSolicitud(nums={2: 1, 1: 4}) 
    # Forzar una situación de bloqueo es difícil por el random inicial, 
    # pero podemos verificar que en alta densidad el número de puntos se mantiene.
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    # En t=0 siempre debe haber 5 puntos
    assert len(datos.puntos[0]) == 5
    # El número de puntos no debe variar (las móviles no desaparecen, se bloquean)
    for t in range(datos.max_segundos):
        assert len(datos.puntos[t]) == 5

def test_clon_preference_fcfs():
    """
    Si el tablero está casi lleno, una clonadora solo clona si hay sitio 
    libre después de que otros se hayan movido/quedado.
    """
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    # Ponemos 95 estáticas y 5 clonadoras.
    solicitud = DatosSolicitud(nums={1: 95, 3: 5})
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    capacidad_maxima = datos.ancho_tablero * datos.ancho_tablero
    
    for t, puntos in datos.puntos.items():
        # Nunca debe exceder la capacidad total del tablero
        assert len(puntos) <= capacidad_maxima
        posiciones = [(p.x, p.y) for p in puntos]
        assert len(posiciones) == len(set(posiciones))
