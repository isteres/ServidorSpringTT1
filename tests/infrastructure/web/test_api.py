import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os

# Añadir la raíz y 'src' al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from infrastructure.web.app import app, get_service
from domain.entities.models import Entidad, DatosSimulation

# Fixture para mockear el servicio
@pytest.fixture
def mock_service():
    service = MagicMock()
    # Mock de get_entities
    service.get_entities.return_value = [
        Entidad(id=1, name="Test", descripcion="Desc", type="Estatica")
    ]
    # Mock de is_valid_entity_id
    service.is_valid_entity_id.side_effect = lambda eid: eid == 1
    # Mock de solicitar_simulacion
    service.solicitar_simulacion.return_value = 1234
    # Mock de descargar_datos
    service.descargar_datos.return_value = DatosSimulation(
        maxSegundos=10, anchoTablero=10, puntos={0: []}
    )
    return service

@pytest.fixture
def client(mock_service):
    # Sobrescribir la dependencia get_service en la app de FastAPI
    app.dependency_overrides[get_service] = lambda: mock_service
    with TestClient(app) as c:
        yield c
    # Limpiar después del test
    app.dependency_overrides.clear()

def test_get_entities(client):
    """Prueba que el endpoint de entidades devuelva una lista."""
    response = client.get("/entities")
    assert response.status_code == 200
    entities = response.json()
    assert isinstance(entities, list)
    assert entities[0]["name"] == "Test"

def test_validate_entity_id(client):
    """Prueba la validación de un ID de entidad."""
    response = client.get("/entities/validate/1")
    assert response.status_code == 200
    assert response.json() is True
    
    response = client.get("/entities/validate/99")
    assert response.status_code == 200
    assert response.json() is False

def test_simulation_workflow(client):
    """Prueba solicitar y descargar una simulación."""
    payload = {"nums": {"1": 10}}
    
    # 1. Solicitar
    response = client.post("/simulation/solicitar", json=payload)
    assert response.status_code == 200
    ticket = response.json()
    assert 1000 <= ticket <= 9999
    
    # 2. Descargar
    response = client.get(f"/simulation/descargar/{ticket}")
    assert response.status_code == 200
    data = response.json()
    assert "maxSegundos" in data

