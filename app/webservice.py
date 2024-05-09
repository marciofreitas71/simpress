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
