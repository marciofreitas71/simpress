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
    """
    Estabelece uma conexão com o banco de dados Oracle.

    Retorna uma conexão ativa com o banco de dados Oracle, utilizando as credenciais e
    informações de conexão fornecidas no arquivo de ambiente (.env) através das variáveis
    de ambiente 'user_name', 'password', 'host', 'port' e 'service_name'.

    Returns:
        Connection: Uma conexão ativa com o banco de dados Oracle.
    """
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')
    dsn = f"oracle+oracledb://{user_name}:{password}@{host}:{port}/{service_name}"
    return create_engine(dsn)


def recuperar_dados_webservice(wsdl_url, service_method, payload, timeout=5):
    """
    Recupera dados de um serviço da web SOAP.

    Args:
        wsdl_url (str): URL do WSDL do serviço da web.
        service_method (str): Nome do método do serviço a ser chamado.
        payload (dict): Dicionário contendo os parâmetros para o método do serviço.
        timeout (int, optional): Tempo limite da solicitação em segundos. Padrão é 5 segundos.

    Returns:
        DataFrame: Um DataFrame Pandas contendo os dados recuperados do serviço da web.

    Raises:
        zeep.exceptions.Fault: Se ocorrer um erro durante a execução do serviço.
        zeep.exceptions.TransportError: Se ocorrer um erro de transporte durante a execução do serviço.
    """
    logging.info("Executando a função recuperar_dados_webservice... ")

    dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"
    wsdl_url = config.wsdl_url
    service_method = config.service_method
    output_csv = config.output_csv
    payload = config.payload
    timeout = 5

    try:
        client = zeep.Client(wsdl=wsdl_url, transport=zeep.Transport(timeout=timeout))
        logging.info("Criado um cliente SOAP usando a URL do WSDL com timeout")

        service = client.service
        method_to_call = getattr(service, service_method)
        response = method_to_call(**payload)
        logging.info("Acessar o método do serviço e enviar a solicitação com os dados")

        df = pd.read_json(response)
        return df
    except zeep.exceptions.Fault as e:
        logging.error(f"Erro durante a execução da função: {str(e)}")
        raise
    except zeep.exceptions.TransportError as e:
        logging.error(f"Erro de transporte durante a execução da função: {str(e)}")
        raise


def query_impressoras():
    """
    Executa uma consulta para recuperar todas as impressoras do banco de dados.

    Returns:
        Query: Uma consulta que pode ser iterada para recuperar as impressoras do banco de dados.
    """
    engine = getConnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(impressora)
    return query


def create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS):
    """
    Cria uma nova entrada de impressora no banco de dados.

    Args:
        PRINTERDEVICEID (str): ID do dispositivo da impressora.
        PRINTERBRANDNAME (str): Nome da marca da impressora.
        PRINTERMODELNAME (str): Nome do modelo da impressora.
        SERIALNUMBER (str): Número de série da impressora.
        CREATED_AT (datetime): Data e hora de criação do registro.
        STATUS (str): Status da impressora.

    Returns:
        str: Uma mensagem indicando que a impressora foi criada com sucesso.
    """
    engine = getConnection()
    Session = sessionmaker(bind=engine)
    session = Session()

    novo_registro = impressora.insert().values(
        PRINTERDEVICEID=PRINTERDEVICEID,
        PRINTERBRANDNAME=PRINTERBRANDNAME,
        PRINTERMODELNAME=PRINTERMODELNAME,
        SERIALNUMBER=SERIALNUMBER,
        CREATED_AT=CREATED_AT,
        STATUS=STATUS
    )

    session.execute(novo_registro)
    session.commit()
    session.close()
    return f'Impressora {PRINTERDEVICEID} incluída com sucesso.'


def update_impressora(ID, PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS):
    """
    Atualiza os detalhes de uma impressora no banco de dados.

    Args:
        ID (int): ID da impressora a ser atualizada.
        PRINTERDEVICEID (str): ID do dispositivo da impressora.
        PRINTERBRANDNAME (str): Nome da marca da impressora.
        PRINTERMODELNAME (str): Nome do modelo da impressora.
        SERIALNUMBER (str): Número de série da impressora.
        CREATED_AT (datetime): Data e hora de criação do registro.
        STATUS (str): Status da impressora.
    """
    engine = getConnection()
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(impressora).filter_by(ID=ID).update({
        'PRINTERDEVICEID': PRINTERDEVICEID,
        'PRINTERBRANDNAME': PRINTERBRANDNAME,
        'PRINTERMODELNAME': PRINTERMODELNAME,
        'SERIALNUMBER': SERIALNUMBER,
        'CREATED_AT': CREATED_AT,
        'STATUS': STATUS
    })

    session.commit()
    session.close()


def delete_impressora(ID):
    """
    Exclui uma impressora do banco de dados.

    Args:
        ID (int): ID da impressora a ser excluída.
    """
    engine = getConnection()
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(impressora).filter_by(ID=ID).delete()

    session.commit()
    session.close()
