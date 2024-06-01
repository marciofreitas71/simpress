from app import config, webservice, crud
import logging
from tqdm import tqdm
from datetime import datetime, timedelta
import itertools
import pandas as pd
import numpy as np
import glob
import csv
import os

def inserir_impressoras_from_csv(nome_arquivo):
    """
    Insere registros de impressoras a partir de um arquivo CSV no banco de dados.

    Args:
        nome_arquivo (str): O caminho do arquivo CSV contendo os dados das impressoras.

    Lê um arquivo CSV contendo informações sobre impressoras e as insere no banco de dados.
    O arquivo CSV deve ter as seguintes colunas:
    - 'PrinterDeviceID': ID da impressora
    - 'BrandName': Nome da marca da impressora
    - 'PrinterModelName': Nome do modelo da impressora
    - 'SerialNumber': Número de série da impressora
    
    As impressoras são inseridas no banco de dados utilizando a função 'create_impressora' do módulo 'repo'.
    Se uma impressora com o mesmo 'PrinterDeviceID' já existe no banco de dados, a inserção é ignorada.
    """
    engine = repo.getConnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    df = pd.read_csv(nome_arquivo)

    for index, linha in df.iterrows():
        PRINTERDEVICEID = linha['PrinterDeviceID']
        PRINTERBRANDNAME = linha['BrandName']
        PRINTERMODELNAME = linha['PrinterModelName']
        SERIALNUMBER = linha['SerialNumber']
        
        CREATED_AT = datetime.now()
        STATUS = 1

        exists_query = session.query(PRINTERDEVICEID).filter(CONTAGEM_IMPRESSORA.PRINTERDEVICEID == PRINTERDEVICEID).first()
        if exists_query:
            print(f"Impressora com PRINTERDEVICEID {PRINTERDEVICEID} já existe no banco de dados. Ignorando inserção.")
        else:
            repo.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)



def obter_hostname_por_ip(ip):
    """
    Obtém o nome do host correspondente a um endereço IP.

    Args:
        ip (str): O endereço IP para o qual se deseja obter o nome do host.

    Returns:
        str: O nome do host correspondente ao endereço IP fornecido.

    Esta função tenta obter o nome do host correspondente a um endereço IP usando a função 
    'gethostbyaddr' do módulo 'socket'. Se o nome do host for encontrado, ele é retornado.
    Se o endereço IP for inválido ou o nome do host não puder ser encontrado, são retornadas
    mensagens correspondentes.
    """
    try:
        hostname = socket.gethostbyaddr(ip[:-10])
        return hostname[0]
    except socket.herror:
        return "Hostname não encontrado"
    except socket.gaierror:
        return "Endereço IP inválido"



def insere_websersvice_banco(data):
    """
    Insere os dados do webservice no banco de dados após verificar e comparar com os dados existentes.

    Args:
        data (str): Data dos dados a serem inseridos no formato 'dd-mm-YYYY'.

    Recupera dados do webservice para a data especificada, compara com os dados existentes no banco
    de dados, e insere os dados novos ou atualizados no banco de dados.
    """
    data_bd = datetime.strptime(data, '%d-%m-%Y') - timedelta(days=1)
    data_bd_str = data_bd.strftime('%d-%m-%Y')

    df_webservice = webservice.recuperar_dados(data)
    df_webservice['DateTimeRead'] = pd.to_datetime(df_webservice['DateTimeRead'])

    registros_bd = crud.read_impressoras_data(data_bd_str)

    if registros_bd:
        colunas = ['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
        df_database = pd.DataFrame(registros_bd, columns=colunas)
    else:
        df_database = pd.DataFrame(columns=['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT'])

    df_diff = pd.concat([df_webservice, df_database]).drop_duplicates(subset=['IMPRESSORA_ID', 'DateTimeRead'], keep=False)
    df_final = pd.concat([df_webservice, df_diff])

    for index, row in df_final.iterrows():
        try:
            crud.create_contagem_impressoras(
                row['IMPRESSORA_ID'],
                row['CONTADOR_PB'],
                row['CONTADOR_COR'],
                row['DateTimeRead']
            )
            print(f"Registro ({row['IMPRESSORA_ID']}) inserido com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir registro de contagem para o registro com IMPRESSORA_ID {row['IMPRESSORA_ID']}: {e}")



def df_impressoras():
    """
    Lê os dados de impressoras de um arquivo CSV específico.

    Returns:
        pd.DataFrame: DataFrame contendo os dados das impressoras.
    """
    file = 'data/Impressoras Outsourcing - HP.csv'
    df = pd.read_csv(file)
    return df

def verifica_impressoras_dataset():
    """
    Verifica e imprime o número de impressoras únicas no dataset compilado.

    Lê o arquivo 'arquivo_final.csv', filtra os números de série únicos das impressoras e imprime a quantidade total.
    """
    file = 'testes/arquivo_final.csv'
    df = pd.read_csv(file)
    ids_impressoras = df['SerialNumber'].unique()
    print(len(ids_impressoras))
    
def ler_arquivo_compilado():
    """
    Lê o arquivo CSV compilado.

    Returns:
        pd.DataFrame: DataFrame contendo os dados do arquivo compilado.
    """
    file = 'testes/arquivo_final.csv'
    df = pd.read_csv(file)
    return df

def transforma_arquivos():
    """
    Transforma o arquivo compilado preenchendo lacunas nas datas.

    Lê o arquivo 'arquivo_final.csv' e processa as linhas para preencher lacunas nas datas,
    comparando as datas reais do relatório e as datas retornadas do webservice.
    """
    file = 'testes/arquivo_final.csv'
    df = pd.read_csv(file)

    # for index, rows in df.iterrows():
    #     # armazena a data real do relatório
    #     RealDataCapture = datetime.strptime(rows['RealDataCapture'], '%Y-%m-%d').date()        
    #     # armazena a da que será retornada do webservice
    #     DateTimeRead = datetime.strptime(rows['DateTimeRead'], "%Y-%m-%dT%H:%M:%S").date()      
    #     print(DateTimeRead == RealDataCapture)
