import sys
import os

# Adiciona o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import webservice, crud, config
import logging
from tqdm import tqdm
from datetime import datetime, timedelta
import pandas as pd
import itertools
import numpy as np
import socket
import glob
import csv


def obter_dados_webservice(data):
        """
        Recupera os dados do webservice para uma data específica.

        Args:
            data (str): Data dos dados a serem recuperados no formato 'dd-mm-YYYY'.

        Returns:
            pd.DataFrame: DataFrame contendo os dados do webservice.
        """
        dados_webservice = webservice.recuperar_dados(data)
        dados_webservice['DateTimeRead'] = pd.to_datetime(dados_webservice['DateTimeRead'])
        return dados_webservice

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

def insere_webservice_banco():
    """
   função 'insere_websersvice_banco' que lida com a inserção de dados do webservice no banco de dados. 
   considerar que a aplicação pode ter ficado alguns dias sem rodar, e portanto, é necessário 
   recuperar os dados de todos os dias entre a última execução e a data atual e preencher as lacunas.
    """

    def obter_ultima_data_bd():
        """
        Recupera a data do último registro no banco de dados.

        Returns:
            datetime: Data do último registro no banco de dados.
        """
        ultima_data_bd = crud.obter_ultima_data_bd()
        return ultima_data_bd

    # Recupera a data do último registro no banco de dados
    ultima_data_bd = obter_ultima_data_bd()
    if not ultima_data_bd:
        print("Não há registros anteriores no banco de dados.")
        return

    # Converte a data do último registro no banco de dados para o formato datetime
    ultima_data_bd = pd.to_datetime(ultima_data_bd)

    # Define a data de início como o dia seguinte ao último registro no banco de dados
    data_inicio = ultima_data_bd + timedelta(days=1)

    # Define a data de fim como o dia anterior à data atual
    data_fim = datetime.now().date() - timedelta(days=1)

    # Verifica se há novas impressoras no webservice e insere no banco de dados
    verifica_impressoras()

    # Iteração para preencher as lacunas entre a última data de registro e a data anterior à data atual
    for data in pd.date_range(start=data_inicio, end=data_fim):
        # Cria um dataframe com os dados do webservice para a data especificada
        df_webservice = obter_dados_webservice(data.strftime('%d-%m-%Y'))


        # # Cria um dataframe pandas com os dados do último registro no banco de dados
        # registros_bd = crud.read_impressoras_data(data.strftime('%d-%m-%Y'))
        # colunas = ['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
        # df_database = pd.DataFrame(registros_bd, columns=colunas) if registros_bd else pd.DataFrame(columns=colunas)
        # print(df_database)

        # # Concatena os dataframes do webservice e do banco de dados e identifica as diferenças
        # df_diff = pd.concat([df_webservice, df_database]).drop_duplicates(subset=['IMPRESSORA_ID', 'DateTimeRead'], keep=False)
        # df_final = pd.concat([df_webservice, df_diff])

        # # Iteração para inserir os registros no banco de dados
        # for index, row in df_final.iterrows():
        #     print(row['IMPRESSORA_ID'], row['DateTimeRead'])
        #     # try:
            #     crud.create_contagem_impressoras(
            #         row['IMPRESSORA_ID'],
            #         row['CONTADOR_PB'],
            #         row['CONTADOR_COR'],
            #         row['DateTimeRead']
            #     )
            #     print(f"Registro ({row['IMPRESSORA_ID']}) inserido com sucesso.")
            # except Exception as e:
            #     print(f"Erro ao inserir registro de contagem para o registro com IMPRESSORA_ID {row['IMPRESSORA_ID']}: {e}")


def verifica_impressoras(data_atual=None):

    """
    Compara os dados de impressoras do banco de dados e do webservice, inserindo novas impressoras se necessário.

    Este método realiza as seguintes etapas:
    
    1. Lê os dados de impressoras do banco de dados referentes ao útimo dia registrado.
    2. Recupera os dados das impressoras do webservice relativos ao dia atual.
    3. Compara os dois DataFrames e identifica as diferenças.
    4. Verifica se as impressoras do DataFrame de diferenças estão presentes no banco de dados.
    5. Insere as impressoras que não estão presentes no banco de dados.
    """
    
    # Define a data de fim como a data atual
    data_fim = datetime.now().date()
    # data_fim = datetime.now().date() if data_atual is None else datetime.strptime(data_atual, '%d-%m-%Y').date()

    recuperando_impressoras = True
    while recuperando_impressoras == True:
        print('Recuperando impressoras do webservice...')
        # Cria um dataframe com os dados do webservice para a data especificada
        df_webservice = webservice.recuperar_dados(data_fim.strftime('%d-%m-%Y'))
        recuperando_impressoras = False
        print('Impressoras recuperadas com sucesso.')
    print('Registros recuperados do webservice:')
    
    df_webservice = df_webservice[['EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName','SerialNumber']]
    print(df_webservice)
    
    # Cria um dataframe pandas com os dados referentes à última data de registro no banco de dados (RealDataCapture)
    registros_bd = crud.obter_registros_ultima_data()
            
    df_registros_bd = pd.DataFrame(registros_bd, columns=['ID','IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT'])
    df_registros_bd = df_registros_bd.merge(df_webservice, how='outer', left_on='IMPRESSORA_ID', right_on='PrinterDeviceID')
    df_registros_bd = df_registros_bd[['EnterpriseName','PrinterDeviceID','BrandName','PrinterModelName','SerialNumber']]
    print('Dataframe registros_bd:')
    print(df_registros_bd)    
   
    # # Concatena os dataframes do webservice e do banco de dados e identifica as diferenças
    df_diff = pd.concat([df_webservice,df_registros_bd]).drop_duplicates(keep=False)
    print('Dataframe de diferenças: ')
    contagem = 0
    if df_diff.empty:
        print('Não há diferenças entre os dataframes.')
    else:
        for index, row in df_diff():
            PRINTERDEVICEID = row['PrinterDeviceID']
            PRINTERBRANDNAME = row['BrandName']
            PRINTERMODELNAME = row['PrinterModelName']
            SERIALNUMBER = row['SerialNumber']
            crud.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)
            contagem += 1
            print(f'{contagem} impressora(s) inserida(s) com sucesso.')

           
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

    

if __name__ == "__main__":
    pass
    # verifica_impressoras(data_atual='04-05-2024')
    # insere_websersvice_banco()
    # dados_webservice = obter_dados_webservice('04-05-2024')
    
