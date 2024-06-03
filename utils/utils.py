from app import config, webservice, crud
import logging
from tqdm import tqdm
from datetime import datetime, timedelta
import itertools
import pandas as pd
import numpy as np
import socket
import glob
import csv
import os

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



def verifica_impressoras():
    """
    Lê os dados de impressoras do banco de dados relativos ao último dia inserido e
    retorna um DataFrame com esses dados.
    lê os dados recuperados do webservice relativos ao dia atual e retorna um DataFrame com esses dados.
    compara os dois DataFrames e retorna um DataFrame contendo as diferenças entre eles.
    Verifica se as impressoras do dataframe de diferenças estão presentes no dataframe de impressoras.
    caso não estejam, insere as impressoras no banco de dados.
    """
    data = datetime.now().strftime('%d-%m-%Y')
    data_bd = datetime.strptime(data, '%d-%m-%Y') - timedelta(days=1)
    data_bd_str = data_bd.strftime('%d-%m-%Y')

    registros_bd = crud.read_impressoras_data(data_bd_str)
    colunas = ['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
    df_database = pd.DataFrame(registros_bd, columns=colunas)

    df_webservice = webservice.recuperar_dados(data)
    df_webservice['DateTimeRead'] = pd.to_datetime(df_webservice['DateTimeRead'])

    df_diff = pd.concat([df_webservice, df_database]).drop_duplicates(subset=['IMPRESSORA_ID', 'DateTimeRead'], keep=False)

    impressoras = crud.read_impressoras()

    for index, row in df_diff.iterrows():
        if row['IMPRESSORA_ID'] not in impressoras:
            crud.create_impressora(row['IMPRESSORA_ID'])
            print(f"Impressora {row['IMPRESSORA_ID']} inserida com sucesso.")
    
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
