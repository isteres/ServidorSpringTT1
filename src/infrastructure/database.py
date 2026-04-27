import os
from sqlmodel import create_engine, SQLModel, Session, select
from dotenv import load_dotenv

load_dotenv()

# Por defecto usamos SQLite, pero si DATABASE_URL está definida en .env se usará esa.
# Ejemplo para MySQL: mysql+pymysql://user:password@localhost:3306/db_name
DEFAULT_DATABASE_URL = "sqlite:///database.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    seed_data()

def seed_data():
    from infrastructure.adapters.sql_models import EntityTable
    with Session(engine) as session:
        statement = select(EntityTable)
        results = session.exec(statement).all()
        if not results:
            entities = [
                EntityTable(id=1, name="Entidad Estática", descripcion="Mantiene sus puntos quietos en todo el tiempo.", type="Estatica"),
                EntityTable(id=2, name="Entidad Movimiento Adyacente", descripcion="Mueve sus puntos únicamente a posiciones adyacentes.", type="MovimientoAdyacente"),
                EntityTable(id=3, name="Entidad Estática Clon", descripcion="Se mantiene quieta pero con probabilidad de clonarse.", type="EstaticaClon"),
            ]
            session.add_all(entities)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session
