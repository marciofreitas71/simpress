import os
from sqlalchemy import create_engine
from .models import Base

def create_database():
    db_url = get_database_url()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

def get_database_url():
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')

    if None in [user_name, password, host, port, service_name]:
        raise ValueError("Erro: Algum valor necessário está ausente.")

    return f"oracle+oracledb://{user_name}:{password}@{host}:{port}/{service_name}"

def getConnection():
    db_url = get_database_url()
    return create_engine(db_url)
