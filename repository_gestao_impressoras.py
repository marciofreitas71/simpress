import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Define e mapeia a tabela 'impressora'
metadata = MetaData()
impressora = Table('impressora', metadata,
                   Column('ID', Integer, primary_key=True),
                   Column('PRINTERDEVICEID', String),
                   Column('PRINTERBRANDNAME', String),
                   Column('PRINTERMODELNAME', String),
                   Column('SERIALNUMBER', String),
                   Column('CREATED_AT', DateTime),
                   Column('STATUS', String)
                   )

def getConnection():
    # Conecta ao banco de dados Oracle
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')
    dsn = f"oracle+oracledb://{user_name}:{password}@{host}:{port}/{service_name}"
    return create_engine(dsn)

def query_impressoras():
    # Cria uma instância do mecanismo de conexão
    engine = getConnection()

    # Cria um objeto de sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Executa a consulta (sem usar all())
    query = session.query(impressora)  # Seleciona a tabela impressora

    # Fecha a sessão (opcional, já que o contexto é gerenciado)
    # session.close()

    return query


def create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS):
    # Cria uma instância do mecanismo de conexão
    engine = getConnection()

    # Cria um objeto de sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Cria um novo registro
    novo_registro = impressora.insert().values(
        PRINTERDEVICEID=PRINTERDEVICEID,
        PRINTERBRANDNAME=PRINTERBRANDNAME,
        PRINTERMODELNAME=PRINTERMODELNAME,
        SERIALNUMBER=SERIALNUMBER,
        CREATED_AT=CREATED_AT,
        STATUS=STATUS
    )

    # Executa o comando SQL
    session.execute(novo_registro)

    # Commit e fecha a sessão
    session.commit()
    session.close()

def update_impressora(ID, PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS):
    # Cria uma instância do mecanismo de conexão
    engine = getConnection()

    # Cria um objeto de sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Atualiza o registro
    session.query(impressora).filter_by(ID=ID).update({
        'PRINTERDEVICEID': PRINTERDEVICEID,
        'PRINTERBRANDNAME': PRINTERBRANDNAME,
        'PRINTERMODELNAME': PRINTERMODELNAME,
        'SERIALNUMBER': SERIALNUMBER,
        'CREATED_AT': CREATED_AT,
        'STATUS': STATUS
    })

    # Commit e fecha a sessão
    session.commit()
    session.close()

def delete_impressora(ID):
    # Cria uma instância do mecanismo de conexão
    engine = getConnection()

    # Cria um objeto de sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Deleta o registro
    session.query(impressora).filter_by(ID=ID).delete()

    # Commit e fecha a sessão
    session.commit()
    session.close()

# # Executa a consulta e imprime os resultados
impressoras = pd.DataFrame(query_impressoras())

print(impressoras)
