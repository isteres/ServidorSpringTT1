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
from domain.entities.models import DatosSolicitud

def test_simulation_no_overlap_integration():
    """
    Test de integración que verifica que en ningún paso de tiempo 
    dos entidades ocupan la misma posición, validando la lógica de FCFS.
    """
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    # Solicitamos una mezcla de entidades: 
    # 20 móviles (id 2) y 20 clonadoras (id 3)
    # En un tablero de 10x10, esto debería generar bastantes intentos de ocupación
    solicitud = DatosSolicitud(nums={2: 20, 3: 20})
    
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    assert datos is not None
    
    # Para cada paso de tiempo, verificamos que no hay colisiones
    for t, puntos in datos.puntos.items():
        posiciones = [(p.x, p.y) for p in puntos]
        # Si hay duplicados en 'posiciones', set(posiciones) tendrá menos elementos
        assert len(posiciones) == len(set(posiciones)), f"Colisión detectada en tiempo {t}"

def test_simulation_entity_persistence():
    """Verifica que los datos se guardan y recuperan correctamente del repositorio real."""
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    solicitud = DatosSolicitud(nums={1: 10})
    ticket = service.solicitar_simulacion(solicitud)
    
    datos = service.descargar_datos(ticket)
    assert datos is not None
    assert len(datos.puntos[0]) == 10

def test_fcfs_preference_scenario():
    """
    Intento de forzar un escenario de preferencia.
    Si tenemos muchas entidades en un espacio pequeño, el FCFS asegura que 
    quien se procesa primero reserva el sitio.
    """
    # Como el ancho es 10 (100 casillas), si pedimos 100 entidades estáticas, 
    # y luego algunas intentan clonar o moverse, deberían fallar o quedarse bloqueadas.
    repo = InMemorySimulationRepository()
    service = SimulationService(repo)
    
    # 50 estáticas (id 1), 50 móviles (id 2)
    # El tablero estará casi lleno desde el inicio.
    solicitud = DatosSolicitud(nums={1: 50, 2: 50})
    
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    # Verificamos que no hay colisiones a pesar de la alta densidad
    for t, puntos in datos.puntos.items():
        posiciones = [(p.x, p.y) for p in puntos]
        assert len(posiciones) == len(set(posiciones)), f"Colisión en t={t} con alta densidad"
        # El número total de puntos no debería disminuir (las móviles se quedan quietas si no hay hueco)
        # Pero para las clonadoras (id 3) sí podría aumentar. 
        # En este caso usamos id 1 y 2, así que el número debe ser exactamente 100.
        assert len(posiciones) == 100
