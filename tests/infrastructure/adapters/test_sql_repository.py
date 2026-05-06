import pytest
import sys
import os

# Añadir 'src' al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../../../src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from sqlmodel import SQLModel, Session, create_engine, select
from infrastructure.adapters.sql_repository import SQLSimulationRepository
from infrastructure.adapters.sql_models import EntityTable, SimulationTable
from domain.entities.models import DatosSimulation, Punto, EntidadEstatica
import os

# Configuramos una base de datos SQLite en memoria para los tests
DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_save_and_get_simulation(session):
    # Preparar datos
    repository = SQLSimulationRepository(session)
    ticket = 12345
    puntos = {
        0: [Punto(x=1, y=1, color="#FFFFFF"), Punto(x=2, y=2, color="#000000")],
        1: [Punto(x=1, y=2, color="#FFFFFF"), Punto(x=2, y=3, color="#000000")]
    }
    datos_sim = DatosSimulation(maxSegundos=2, anchoTablero=10, puntos=puntos)

    # Act: Guardar
    saved_ticket = repository.save_simulation(ticket, datos_sim)
    
    # Assert: El ticket devuelto es correcto
    assert saved_ticket == ticket

    # Act: Recuperar
    retrieved_sim = repository.get_simulation(ticket)

    # Assert: Los datos recuperados coinciden con los guardados
    assert retrieved_sim is not None
    assert retrieved_sim.max_segundos == 2
    assert retrieved_sim.ancho_tablero == 10
    assert len(retrieved_sim.puntos) == 2
    assert retrieved_sim.puntos[0][0].x == 1
    assert retrieved_sim.puntos[1][1].y == 3
    assert retrieved_sim.puntos[0][0].color == "#FFFFFF"

def test_get_simulation_not_found(session):
    repository = SQLSimulationRepository(session)
    retrieved_sim = repository.get_simulation(99999)
    assert retrieved_sim is None

def test_get_entities(session):
    # Preparar: Insertar algunas entidades directamente
    e1 = EntityTable(id=1, name="E1", descripcion="D1", type="Estatica")
    e2 = EntityTable(id=2, name="E2", descripcion="D2", type="MovimientoAdyacente")
    session.add(e1)
    session.add(e2)
    session.commit()

    repository = SQLSimulationRepository(session)
    entities = repository.get_entities()

    assert len(entities) == 2
    assert any(e.id == 1 and e.name == "E1" for e in entities)
    assert any(e.id == 2 and isinstance(e, EntidadEstatica) == False for e in entities) # MovimientoAdyacente no hereda de Estatica en models.py

def test_get_entity_by_id(session):
    e1 = EntityTable(id=1, name="E1", descripcion="D1", type="Estatica")
    session.add(e1)
    session.commit()

    repository = SQLSimulationRepository(session)
    entity = repository.get_entity(1)

    assert entity is not None
    assert entity.id == 1
    assert entity.name == "E1"

def test_map_to_domain_logic(session):
    repository = SQLSimulationRepository(session)
    
    # Probar mapeo de diferentes tipos
    estatica = EntityTable(id=1, name="S", descripcion="D", type="Estatica")
    clon = EntityTable(id=2, name="C", descripcion="D", type="EstaticaClon")
    mov = EntityTable(id=3, name="M", descripcion="D", type="MovimientoAdyacente")
    unknown = EntityTable(id=4, name="U", descripcion="D", type="UnknownType")

    from domain.entities.models import EntidadEstatica, EntidadEstáticaClon, EntidadMovimientoAdyacente

    assert isinstance(repository._map_to_domain(estatica), EntidadEstatica)
    assert isinstance(repository._map_to_domain(clon), EntidadEstáticaClon)
    assert isinstance(repository._map_to_domain(mov), EntidadMovimientoAdyacente)
    # Default fallback
    assert isinstance(repository._map_to_domain(unknown), EntidadEstatica)
