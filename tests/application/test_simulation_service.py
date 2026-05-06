import pytest
import sys
import os
from unittest.mock import MagicMock

# Añadir 'src' al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../../src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from application.use_cases.simulation_service import SimulationService
from domain.entities.models import DatosSolicitud, EntidadEstatica

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    # Mock de entidades existentes (IDs 1, 2)
    repo.get_entity.side_effect = lambda eid: EntidadEstatica(id=eid, name="Test", descripcion="Desc") if eid in [1, 2] else None
    repo.save_simulation.return_value = 1234
    return repo

def test_solicitar_simulacion_generates_points(mock_repo):
    """Prueba que el servicio genera los puntos solicitados dentro de los límites."""
    service = SimulationService(mock_repo)
    solicitud = DatosSolicitud(nums={1: 5}) # Solicitar 5 puntos de la entidad ID 1
    
    ticket = service.solicitar_simulacion(solicitud)
    
    assert isinstance(ticket, int)
    assert 1000 <= ticket <= 9999
    
    # Verificamos que se guardó una simulación (dos llamadas en modo síncrono/sin broker)
    assert mock_repo.save_simulation.call_count == 2
    
    # La primera llamada es para marcar como PENDIENTE
    first_call_args = mock_repo.save_simulation.call_args_list[0][0]
    assert first_call_args[1] is None
    
    # La segunda llamada (fallback síncrono) tiene el resultado
    second_call_args = mock_repo.save_simulation.call_args_list[1][0]
    simulacion = second_call_args[1]
    
    assert simulacion.max_segundos == 10
    assert simulacion.ancho_tablero == 10
    
    # Comprobar que en el tiempo 0 hay exactamente 5 puntos
    puntos_t0 = simulacion.puntos[0]
    assert len(puntos_t0) == 5

def test_solicitar_simulacion_ignores_invalid_entities(mock_repo):
    """Prueba que se ignoran IDs de entidades que no existen en el repositorio."""
    service = SimulationService(mock_repo)
    solicitud = DatosSolicitud(nums={99: 10}) # ID 99 no existe
    
    service.solicitar_simulacion(solicitud)
    
    # Verificamos la segunda llamada (resultado final vacío)
    second_call_args = mock_repo.save_simulation.call_args_list[1][0]
    simulacion = second_call_args[1]
    
    # No debería haber puntos si el ID era inválido
    assert len(simulacion.puntos[0]) == 0
