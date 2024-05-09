from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app import repository_gestao_impressoras as repo
import pandas as pd
from app import config as config
import csv

def obter_hostname_por_ip(ip):
    try:
        hostname = socket.gethostbyaddr(ip[:-10])
        return hostname[0]  # O nome do host está na primeira posição da tupla retornada
    except socket.herror:
        return "Hostname não encontrado"
    except socket.gaierror:
        return "Endereço IP inválido"


def salva_dados_csv(DateTimeEnd,service_method, payload, timeout, wsdl_url):
    
   # Quantidade de dias anteriores à data final
    dias = 1

    while dias < 800:
        # Recupera dados do webservice
        dados_webservice = repo.recuperar_dados_webservice(wsdl_url, service_method, payload)
        
        # Adiciona a nova coluna com a DateTimeEnd
        dados_webservice['RealDataCapture'] = DateTimeEnd.strftime('%Y-%m-%d')
        
        # Salva os dados em um arquivo CSV
        dados_webservice.to_csv(f'testes/arquivos_final/dados-{DateTimeEnd.strftime("%Y-%m-%d")}.csv', index=False)
        
        print(f'Dados do dia {DateTimeEnd.strftime("%Y-%m-%d")} processados e salvos')
        
        dias += 1       
        # Atualiza a data para o dia anterior
        DateTimeEnd -= timedelta(days=1)

# Função para inserir os dados das impressoras do arquivo CSV no banco de dados
from sqlalchemy import text

def inserir_impressoras_from_csv(nome_arquivo):

    # Cria uma instância do mecanismo de conexão
    engine = repo.getConnection()

    # Cria um objeto de sessão
    Session = sessionmaker(bind=engine)
    session = Session()
    # Ler o arquivo CSV para um DataFrame do Pandas
    df = pd.read_csv(nome_arquivo)

    # Iterar sobre as linhas do DataFrame
    for index, linha in df.iterrows():
        # Extrair os valores dos campos do DataFrame
        PRINTERDEVICEID = linha['PrinterDeviceID']
        PRINTERBRANDNAME = linha['BrandName']
        PRINTERMODELNAME = linha['PrinterModelName']
        SERIALNUMBER = linha['SerialNumber']

        CREATED_AT = datetime.now()
        STATUS = 1  # Definir o status como 1

        # Verificar se já existe uma impressora com o mesmo PRINTERDEVICEID
        exists_query = session.query(PRINTERDEVICEID).filter(CONTAGEM_IMPRESSORA.PRINTERDEVICEID == PRINTERDEVICEID).first()
        if exists_query:
            print(f"Impressora com PRINTERDEVICEID {PRINTERDEVICEID} já existe no banco de dados. Ignorando inserção.")
        else:
            # Se não existe, criar a impressora
            repo.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)
            



# # Chamada da função para inserir os dados do arquivo CSV no banco de dados
# inserir_impressoras_from_csv('data/todas_impressoras.csv')

# DateTimeEnd = datetime.strptime(data, '%Y-%m-%d')
# dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"
dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"
wsdl_url = config.wsdl_url
service_method = config.service_method
output_csv = config.output_csv
payload = config.payload
timeout = 5

repo.recuperar_dados_webservice(wsdl_url, service_method, payload, timeout=5)

