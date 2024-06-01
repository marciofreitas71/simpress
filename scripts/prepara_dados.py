"""
Este módulo contém funções para manipulação de dados de impressoras e datas utilizando pandas e outras bibliotecas.

Pacotes importados:
- datetime: Para manipulação de datas e horas.
- webservice: Módulo de webservice para recuperar dados.
- tqdm: Para exibir barras de progresso.
- pandas (pd): Para manipulação de dados em estruturas DataFrame.
- numpy (np): Para manipulações numéricas.
- logging: Para registro de eventos e mensagens.
- os: Para interações com o sistema operacional, como manipulação de arquivos e diretórios.
- re: Para operações com expressões regulares.

Funções:
- preenche_dados_csv(caminho_csv): Preenche os dados de um arquivo CSV com informações de impressoras e datas.
- salva_dados_csv(DateTimeStart, DateTimeEnd): Salva os dados do webservice em arquivos CSV para um intervalo de datas.
- gera_arquivo_csv_compilado(pasta): Gera um arquivo CSV compilado a partir de vários arquivos CSV em uma pasta.
- df_impressoras(): Lê os dados de impressoras de um arquivo CSV específico.
- extrair_id_zona(ip): Extrai o número da zona a partir de um endereço IP.
"""


from datetime import datetime, timedelta
from app import webservice
from tqdm import tqdm
import pandas as pd
import numpy as np
import logging
import os
import re

def preenche_dados_csv(caminho_csv):
    """
    Preenche os dados de um arquivo CSV com informações de impressoras e datas.

    Args:
        caminho_csv (str): Caminho do arquivo CSV de entrada.

    Este procedimento realiza as seguintes etapas:
    1. Carrega o conjunto de dados do arquivo CSV e filtra as linhas com a marca 'HP'.
    2. Converte a coluna 'RealDateCapture' para o formato datetime.
    3. Salva o conjunto de dados original filtrado em um arquivo CSV.
    4. Seleciona impressoras únicas com base na coluna 'SerialNumber' e salva em um arquivo CSV.
    5. Gera um DataFrame com um intervalo de datas e combina com as impressoras únicas.
    6. Realiza um merge com o DataFrame original e preenche valores ausentes.
    7. Filtra registros a partir de 01/01/2024, preenche valores nulos e salva o resultado final em um arquivo CSV.

    """
    print("Carregando o conjunto de dados...")
    df = pd.read_csv(caminho_csv)
    df = df[df['BrandName'] == 'HP']
    df = df.sort_values(by=['RealDateCapture', 'SerialNumber'], ascending=[False, True])

    df['RealDateCapture'] = pd.to_datetime(df['RealDateCapture'], format='%d-%m-%Y')
    df.to_csv('df_original.csv')
    print(f"Conjunto de dados carregado com {len(df)} registros.")

    imp = df.drop_duplicates(subset='SerialNumber')
    imp = imp[['EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]
    imp.to_csv('testes/data/df_impressoras.csv')

    date_range = pd.date_range(start='01-01-2022', end='28-05-2024', freq='D')
    df_dates = pd.DataFrame({'RealDateCapture': date_range})

    imp['key'] = 1
    df_dates['key'] = 1

    df_full_datas = pd.merge(imp, df_dates, on='key').drop('key', axis=1)
    df_full_datas.to_csv("df_full_datas.csv")

    df_merged = df_full_datas.merge(df, how='left', on=['RealDateCapture', 'SerialNumber', 'EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName'])
    df_merged.fillna(value=np.nan, inplace=True)
    df_merged = df_merged.sort_values(by=['RealDateCapture', 'SerialNumber'], ascending=False)
    df_merged.to_csv('df_merged.csv')

    registros_impressoras = []
    for index, row in imp.iterrows():
        serial_number = row['SerialNumber']
        df_parcial = df_merged[df_merged['SerialNumber'] == serial_number].bfill()
        registros_impressoras.append(df_parcial)

    df_filled = pd.concat(registros_impressoras, ignore_index=True)
    df_filled['RealDateCapture'] = pd.to_datetime(df_filled['RealDateCapture'])
    df_filled_2024 = df_filled[df_filled['RealDateCapture'] >= '2024-01-01']
    df_filled_2024 = df_filled_2024.fillna(0)
    df_filled_2024.to_csv('D:/projetos/simpress/testes/df_filled_2024.csv', index=False)

def salva_dados_csv(DateTimeStart, DateTimeEnd):
    """
    Salva os dados do webservice em arquivos CSV para um intervalo de datas.

    Args:
        DateTimeStart (str): Data de início no formato 'dd-mm-YYYY'.
        DateTimeEnd (str): Data de fim no formato 'dd-mm-YYYY'.

    Recupera dados do webservice para cada dia dentro do intervalo de datas especificado
    e salva esses dados em arquivos CSV. Cada arquivo é nomeado com a data correspondente.
    """
    data = DateTimeEnd
    while data != DateTimeStart:
        dados_webservice = webservice.recuperar_dados(data)
        dados_webservice['RealDateCapture'] = data
        
        if not os.path.isfile(f'testes/arquivos_final/dados-{data}.csv'):
            dados_webservice.to_csv(f'testes/arquivos_final/dados-{data}.csv', index=False)
            print(f'Dados do dia {data} processados e salvos')
        else:
            print(f'O arquivo referente ao dia {data} já foi gerado')
            
        data = datetime.strptime(data, '%d-%m-%Y')
        data -= timedelta(days=1)
        data = data.strftime('%d-%m-%Y')

def gera_arquivo_csv_compilado(pasta):
    """
    Gera um arquivo CSV compilado a partir de vários arquivos CSV em uma pasta.

    Args:
        pasta (str): Caminho da pasta contendo os arquivos CSV.

    Esta função lê todos os arquivos CSV na pasta especificada, concatena seus dados em um único DataFrame,
    e salva o DataFrame resultante em um novo arquivo CSV com a data atual no nome.
    """
    data = datetime.now().strftime('%d-%m-%Y')
    dataframes = []

    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            df = pd.read_csv(caminho_arquivo)
            dataframes.append(df)
            print(f'Dados adicionados do arquivo {arquivo}')

    df_final = pd.concat(dataframes, ignore_index=True)
    df_final.to_csv(f'testes/arquivo_final-{data}.csv', index=False)

def gera_arquivo_csv_compilado(pasta):
    """
    Gera um arquivo CSV compilado a partir de vários arquivos CSV em uma pasta.

    Args:
        pasta (str): Caminho da pasta contendo os arquivos CSV.

    Esta função lê todos os arquivos CSV na pasta especificada, concatena seus dados em um único DataFrame,
    e salva o DataFrame resultante em um novo arquivo CSV.
    """
    dataframes = []

    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            df = pd.read_csv(caminho_arquivo)
            dataframes.append(df)
            print(f'Dados adicionados do arquivo {arquivo}')

    df_final = pd.concat(dataframes, ignore_index=True)
    df_final.to_csv('testes/arquivos_final/arquivo_final-06-04-2024.csv', index=False)

def df_impressoras():
    """
    Lê os dados de impressoras de um arquivo CSV específico.

    Returns:
        pd.DataFrame: DataFrame contendo os dados das impressoras.
    """
    file = 'data/Impressoras Outsourcing - HP.csv'
    df = pd.read_csv(file)
    return df

def extrair_id_zona(ip):
    """
    Extrai o número da zona a partir de um endereço IP.

    Args:
        ip (str): O endereço IP do qual se deseja extrair o número da zona.

    Returns:
        str: O número da zona extraído do endereço IP, ou uma mensagem de erro se o padrão não corresponder.
    """
    padrao = r'10\.171\.(\d+)\.60'
    correspondencia = re.match(padrao, ip)
    if correspondencia:
        return correspondencia.group(1)
    else:
        return "Padrão de IP não corresponde"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    salva_dados_csv('01-01-2022', '30-05-2024')
    #gera_arquivo_csv_compilado('D:/projetos/simpress/testes/arquivos_final')
    #preenche_dados_csv('D:/projetos/simpress/testes/arquivo_final-30-05-2024.csv')