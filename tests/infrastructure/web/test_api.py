from fastapi.testclient import TestClient
import sys
import os

# Añadir la raíz y 'src' al path de Python para evitar errores de importación
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
src_dir = os.path.join(project_root, "src")

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from infrastructure.web.app import app

client = TestClient(app)

def test_get_entities():
    """Prueba que el endpoint de entidades devuelva una lista."""
    response = client.get("/entities")
    assert response.status_code == 200
    entities = response.json()
    assert isinstance(entities, list)

def test_validate_entity_id():
    """Prueba la validación de un ID de entidad."""
    response = client.get("/entities/validate/1")
    assert response.status_code == 200
    assert isinstance(response.json(), bool)

def test_simulation_workflow():
    """Prueba solicitar y descargar una simulación."""
    payload = {"nums": {"1": 10}}
    
    # 1. Solicitar
    response = client.post("/simulation/solicitar", json=payload)
    assert response.status_code == 200
    ticket = response.json()
    
    # 2. Descargar
    response = client.get(f"/simulation/descargar/{ticket}")
    assert response.status_code == 200
    data = response.json()
    assert "maxSegundos" in data or "max_segundos" in data
