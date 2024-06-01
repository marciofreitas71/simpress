"""
Módulo webservice

Este módulo fornece funcionalidades para recuperar dados de um serviço da web SOAP,
utilizando as bibliotecas SQLAlchemy, dotenv, pandas e zeep. Ele inclui a configuração 
do cliente SOAP e o processamento de dados recebidos do serviço.

Importa:
    os: Para interações com o sistema operacional.
    StringIO: Para manipulação de strings como arquivos.
    sessionmaker (sqlalchemy.orm): Para criação de sessões de banco de dados.
    load_dotenv (dotenv): Para carregar variáveis de ambiente de um arquivo .env.
    datetime, timedelta (datetime): Para manipulação de datas e horários.
    pandas as pd: Para manipulação e análise de dados.
    webservice (app): Para funcionalidades adicionais do aplicativo.
    config (app): Para configuração do aplicativo.
    logging: Para registro de eventos e mensagens.
    zeep: Para interações com serviços da web SOAP.
"""

import os
from io import StringIO
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
from app import webservice
from app import config
import logging
import zeep

load_dotenv()

def recuperar_dados(data):
    """
    Recupera dados de um serviço da web SOAP.

    Args:
        data (str): Data da consulta no formato 'dd-mm-yyyy'.

    Returns:
        DataFrame: Um DataFrame Pandas contendo os dados recuperados do serviço da web.

    Raises:
        zeep.exceptions.Fault: Se ocorrer um erro durante a execução do serviço.
        zeep.exceptions.TransportError: Se ocorrer um erro de transporte durante a execução do serviço.
    """
    logging.info("Executando a função recuperar_dados_webservice... ")

    # Converter para objeto datetime
    data_objeto = datetime.strptime(data, "%d-%m-%Y")

    # Adicionar um dia
    data_objeto += timedelta(days=1)

    # Formatar para o novo formato
    dateTimeEnd = data_objeto.strftime("%Y-%m-%d")

    # Atualizar o payload com o dataTimeEnd fornecido
    config.payload['dateTimeEnd'] = f'{dateTimeEnd} 00:00:00'

    try:
        # Criar um cliente SOAP usando a URL do WSDL com timeout
        client = zeep.Client(wsdl=config.wsdl_url, transport=zeep.Transport(timeout=10))
        logging.info("Criado um cliente SOAP usando a URL do WSDL com timeout")

        # Acessar o método do serviço e enviar a solicitação com os dados
        service = client.service
        method_to_call = getattr(service, config.service_method)
        response = method_to_call(**config.payload)
        logging.info("Acessar o método do serviço e enviar a solicitação com os dados")

        # Analisar a string de resposta em objetos Python
        df = pd.read_json(StringIO(response))
        return df
    except zeep.exceptions.Fault as e:
        logging.error(f"Erro durante a execução da função: {str(e)}")
        # Você pode decidir levantar a exceção novamente ou retornar um valor padrão, dependendo do caso.
        raise
    except zeep.exceptions.TransportError as e:
        logging.error(f"Erro de transporte durante a execução da função: {str(e)}")
        # Trate o erro de transporte conforme necessário
        raise
