import os
from io import StringIO
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from app import webservice
from app import config
import logging
import zeep

load_dotenv()

def recuperar_dados(dataTimeEnd):
        """
        Recupera dados de um serviço da web SOAP.

        Args:
            dataTimeEnd (str): Data e hora de término para a consulta.

        Returns:
            DataFrame: Um DataFrame Pandas contendo os dados recuperados do serviço da web.

        Raises:
            zeep.exceptions.Fault: Se ocorrer um erro durante a execução do serviço.
            zeep.exceptions.TransportError: Se ocorrer um erro de transporte durante a execução do serviço.
        """
        logging.info("Executando a função recuperar_dados_webservice... ")

        # Atualizar o payload com o dataTimeEnd fornecido
        config.payload['dateTimeEnd'] = f'{dataTimeEnd} 00:00:00'

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