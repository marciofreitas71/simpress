import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import config
import logging
import zeep

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



def recuperar_dados_webservice(wsdl_url, service_method, payload, timeout=5):
    logging.info("Executando a função recuperar_dados_webservice... ")

    dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"
    wsdl_url = config.wsdl_url
    service_method = config.service_method
    output_csv = config.output_csv
    payload = config.payload
    timeout = 5

    try:
        # Criar um cliente SOAP usando a URL do WSDL com timeout
        client = zeep.Client(wsdl=wsdl_url, transport=zeep.Transport(timeout=timeout))
        logging.info("Criado um cliente SOAP usando a URL do WSDL com timeout")

        # Acessar o método do serviço e enviar a solicitação com os dados
        service = client.service
        method_to_call = getattr(service, service_method)
        response = method_to_call(**payload)
        logging.info("Acessar o método do serviço e enviar a solicitação com os dados")

        # Analisar a string de resposta em objetos Python
        df = pd.read_json(response)
        return df
    except zeep.exceptions.Fault as e:
        logging.error(f"Erro durante a execução da função: {str(e)}")
        # Você pode decidir levantar a exceção novamente ou retornar um valor padrão, dependendo do caso.
        raise
    except zeep.exceptions.TransportError as e:
        logging.error(f"Erro de transporte durante a execução da função: {str(e)}")
        # Trate o erro de transporte conforme necessário
        raise

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


