import pytest
from application.use_cases.simulation_service import SimulationService
from infrastructure.adapters.in_memory_repository import InMemorySimulationRepository
from domain.entities.models import (
    DatosSolicitud, Punto, EntidadEstatica, EntidadMovimientoAdyacente, EntidadEstáticaClon
)

@pytest.fixture
def service():
    repo = InMemorySimulationRepository()
    return SimulationService(repo)

def test_movement_is_strictly_adjacent_von_neumann(service):
    """
    Verifica que las entidades de movimiento adyacente NUNCA se muevan en diagonal
    ni a más de una casilla de distancia. Usamos solo una entidad para evitar
    problemas con el barajado (shuffle).
    """
    solicitud = DatosSolicitud(nums={2: 1}) # 1 entidad móvil
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    for t in range(datos.max_segundos - 1):
        p1 = datos.puntos[t][0]
        p2 = datos.puntos[t+1][0]
        
        dist_x = abs(p1.x - p2.x)
        dist_y = abs(p1.y - p2.y)
        dist_manhattan = dist_x + dist_y
        
        # 0 si se quedó quieto, 1 si se movió H/V
        assert dist_manhattan <= 1, f"Movimiento ilegal detectado en t={t}: de ({p1.x},{p1.y}) a ({p2.x},{p2.y})"
        if dist_manhattan == 1:
            assert dist_x == 0 or dist_y == 0

def test_cloning_is_strictly_adjacent_von_neumann(service):
    """
    Verifica que cada nueva entidad en t+1 sea un clon válido de alguna entidad en t.
    Un clon es válido si está en la misma posición que un progenitor (es el progenitor)
    o en una casilla adyacente H/V a uno.
    """
    solicitud = DatosSolicitud(nums={3: 5}) # Varias clonadoras
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    for t in range(datos.max_segundos - 1):
        progenitores = datos.puntos[t]
        puntos_next = datos.puntos[t+1]
        
        posiciones_progenitores = set((p.x, p.y) for p in progenitores)
        
        for p_next in puntos_next:
            # Para cada punto en t+1, debe existir un "padre" en t
            # que esté en su misma posición o sea adyacente H/V.
            valido = False
            for p_prev in progenitores:
                dist_x = abs(p_next.x - p_prev.x)
                dist_y = abs(p_next.y - p_prev.y)
                dist_manhattan = dist_x + dist_y
                
                # Es el mismo o es un clon adyacente
                if dist_manhattan == 0 or (dist_manhattan == 1 and (dist_x == 0 or dist_y == 0)):
                    valido = True
                    break
            
            assert valido, f"Punto en t={t+1} en ({p_next.x},{p_next.y}) no tiene un progenitor válido en t={t}"


def test_no_cloning_when_surrounded(service):
    """
    Verifica que si una clonadora está rodeada de entidades estáticas, no puede clonar.
    """
    # En un tablero pequeño, llenamos casi todo con estáticas (ID 1)
    # y ponemos una clonadora (ID 3)
    solicitud = DatosSolicitud(nums={3: 1, 1: 99}) # Total 100 entidades en tablero 10x10 (calculado por densidad)
    
    # El servicio ajusta el ancho. Para 100 entidades con 10% densidad, el área sería 1000 -> ancho ~31
    # Pero queremos forzar el bloqueo. Vamos a usar un truco: pedir MUCHAS entidades.
    # Si pedimos 2500 entidades, el ancho máximo es 50 (50x50 = 2500). El tablero estará lleno.
    
    solicitud_bloqueo = DatosSolicitud(nums={3: 10, 1: 2490}) 
    ticket = service.solicitar_simulacion(solicitud_bloqueo)
    datos = service.descargar_datos(ticket)
    
    # Si el tablero está lleno al 100%, nadie puede clonar ni moverse.
    poblacion_inicial = len(datos.puntos[0])
    for t in range(datos.max_segundos):
        assert len(datos.puntos[t]) == poblacion_inicial, f"Hubo clonación en un tablero lleno en t={t}"

def test_movement_blocked_by_others(service):
    """
    Verifica que las entidades móviles respeten el espacio ocupado por otros.
    """
    # Escenario: 2 entidades en un tablero muy pequeño o muy denso
    solicitud = DatosSolicitud(nums={2: 1, 1: 2499}) # Tablero 50x50 totalmente lleno
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    # La entidad móvil (ID 2) no debería poder moverse nunca
    puntos_t0 = datos.puntos[0]
    # Buscamos el punto de la entidad móvil (usando el color si es posible, o asumiendo que es el único que podría moverse)
    # En este caso, simplemente verificamos que NINGÚN punto cambie de posición
    posiciones_t0 = set((p.x, p.y) for p in puntos_t0)
    
    for t in range(1, datos.max_segundos):
        posiciones_t = set((p.x, p.y) for p in datos.puntos[t])
        assert posiciones_t == posiciones_t0, f"Una entidad se movió a pesar de estar el tablero lleno en t={t}"

def test_board_width_calculation(service):
    """
    Verifica que el ancho del tablero se calcule dinámicamente según la cantidad de entidades.
    """
    # Para 10 entidades: sqrt(10*10) + 1 = 11
    datos10 = service.descargar_datos(service.solicitar_simulacion(DatosSolicitud(nums={1: 10})))
    assert datos10.ancho_tablero == 11
    
    # Para 400 entidades, el área para 10% densidad es 4000. sqrt(4000) ~ 63.
    # Pero tenemos un máximo de 50.
    datos400 = service.descargar_datos(service.solicitar_simulacion(DatosSolicitud(nums={1: 400})))
    assert datos400.ancho_tablero == 50

def test_entity_colors(service):
    """
    Verifica que se asignen los colores correctos según el ID de la entidad.
    """
    solicitud = DatosSolicitud(nums={1: 1, 2: 1, 3: 1})
    ticket = service.solicitar_simulacion(solicitud)
    datos = service.descargar_datos(ticket)
    
    colores = [p.color for p in datos.puntos[0]]
    assert "#FF5733" in colores # ID 1
    assert "#33FF57" in colores # ID 2
    assert "#3357FF" in colores # ID 3

def test_ticket_format_is_4_digits_numeric(service):
    """
    Verifica que el ticket generado tenga exactamente 4 dígitos y sea un entero.
    """
    solicitud = DatosSolicitud(nums={1: 1})
    ticket = service.solicitar_simulacion(solicitud)
    
    assert isinstance(ticket, int)
    assert 1000 <= ticket <= 9999

