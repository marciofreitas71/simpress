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
- salva_dados_csv(DateTimeStart, DateTimeEnd): Salva os dados do webservice em arquivos CSV para um intervalo de datas.
- gera_arquivo_csv_compilado(pasta): Gera um arquivo CSV compilado a partir de vários arquivos CSV em uma pasta.
- preenche_dados_csv(caminho_csv, data_inicial, data_final, data_inicial_bi): Preenche os dados de um arquivo CSV com informações de impressoras e datas.
- df_impressoras(): Lê os dados de impressoras de um arquivo CSV específico.
"""

from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import numpy as np
import logging
import sys
import os
import re

# Adicionar o diretório principal do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import webservice

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
        # Recupera dados do webservice para a data especificada
        dados_webservice = webservice.recuperar_dados(data)
        dados_webservice['RealDateCapture'] = data
        
        # Salva os dados em um arquivo CSV se ainda não existir
        if not os.path.isfile(f'temp/dados_diarios/dados-{data}.csv'):
            dados_webservice.to_csv(f'temp/dados_diarios/dados-{data}.csv', index=False)
            print(f'Dados do dia {data} processados e salvos')
        else:
            print(f'O arquivo referente ao dia {data} já foi gerado')
            
        # Move para a data anterior
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
    contagem = 0
    # Lê todos os arquivos CSV na pasta especificada
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            df = pd.read_csv(caminho_arquivo)
            dataframes.append(df)
            print(f'Dados adicionados do arquivo {arquivo}')
        contagem += 1
    print(f'Foram adicionados {contagem} arquivos.')

    # Concatena os dados e salva em um novo arquivo CSV
    df_final = pd.concat(dataframes, ignore_index=True)
    df_final.to_csv(f'temp/dados_compilados/arquivo_final.csv', index=False)

def preenche_dados_csv(caminho_csv, data_inicial, data_final, data_inicial_bi):
    """
    Preenche os dados de um arquivo CSV com informações de impressoras e datas.

    Args:
        caminho_csv (str): Caminho do arquivo CSV de entrada.
        data_inicial (str): Data de início para o preenchimento.
        data_final (str): Data de fim para o preenchimento.
        data_inicial_bi (str): Data inicial para o filtro de registros finais.

    Este procedimento realiza as seguintes etapas:
    1. Carrega o conjunto de dados do arquivo CSV e filtra as linhas com a marca 'HP'.
    2. Converte a coluna 'RealDateCapture' para o formato datetime.
    3. Salva o conjunto de dados original filtrado em um arquivo CSV.
    4. Seleciona impressoras únicas com base na coluna 'SerialNumber' e salva em um arquivo CSV.
    5. Gera um DataFrame com um intervalo de datas e combina com as impressoras únicas.
    6. Realiza um merge com o DataFrame original e preenche valores ausentes.
    7. Filtra registros a partir da data inicial do biênio, preenche valores nulos e salva o resultado final em um arquivo CSV.
    """
    # Carregar o conjunto de dados
    print("Carregando o conjunto de dados...")
    df = pd.read_csv(caminho_csv)
    df = df[df['BrandName'] == 'HP']
    df = df.sort_values(by=['RealDateCapture','SerialNumber'], ascending=[False,True])
    print(f"Conjunto de dados carregado com {len(df)} registros.")

    # Converte a coluna 'RealDateCapture' do df para datetime
    df['RealDateCapture'] = pd.to_datetime(df['RealDateCapture'], format='%d-%m-%Y')

    # Salva o arquivo csv com os dados originais
    df.to_csv('temp/dados_compilados/df_original.csv')
    print("Dados originais salvos.")

    # Selecionar impressoras únicas (linhas únicas com base na coluna 'SerialNumber')
    imp = df.drop_duplicates(subset='SerialNumber')

    # Seleciona as colunas do DataFrame 'imp'
    imp = imp[['EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]

    # Gera arquivo csv com as impressoras do dataframe
    imp.to_csv('temp/dados_compilados/df_impressoras.csv')
    print("Dados das impressoras únicos salvos.")

    # Gera um DataFrame com datas
    date_range = pd.date_range(start=data_inicial, end=data_final, freq='D')
    df_dates = pd.DataFrame({'RealDateCapture': date_range})

    # Adicionar a coluna 'key' para combinação
    imp['key'] = 1
    df_dates['key'] = 1

    # Combinação dos DataFrames
    df_full_datas = pd.merge(imp, df_dates, on='key').drop('key', axis=1)

    # Gera um arquivo csv com as datas mescladas com os dados
    df_full_datas.to_csv("temp/dados_compilados/df_full_datas.csv")
    print("Datas combinadas salvas.")

    # Faz o merge com o DataFrame original
    df_merged = df_full_datas.merge(df, how='left', on=['RealDateCapture','SerialNumber','EnterpriseName','PrinterDeviceID','BrandName','PrinterModelName'])

    # Preenche os valores ausentes com nan
    df_merged.fillna(value=np.nan, inplace=True)

    # ordena os registros pelas colunas 'RealDateCapture' e 'SerialNumber'
    df_merged = df_merged.sort_values(by=['RealDateCapture','SerialNumber'], ascending=False)

    # Gera um arquivo csv com os dados mesclados
    df_merged.to_csv('temp/dados_compilados/df_merged.csv')
    print("Dados mesclados salvos.")

    # Inicializa uma lista vazia para armazenar DataFrames individuais correspondentes a cada número de série
    registros_impressoras = []
    # Itera sobre cada linha do DataFrame 'imp'
    for index, row in imp.iterrows():
        serial_number = row['SerialNumber']
        # Filtra o DataFrame 'df_merged' para obter apenas as linhas com o mesmo número de série e preenche valores nulos usando o método backward fill (bfill)
        df_parcial = df_merged[df_merged['SerialNumber'] == serial_number].bfill()
        # Adiciona o DataFrame filtrado e preenchido à lista 'impressoras'
        registros_impressoras.append(df_parcial)
        print(f"Processando número de série: {serial_number}")

    # Concatena todos os DataFrames na lista 'impressoras' em um único DataFrame, ignorando os índices originais
    df_filled = pd.concat(registros_impressoras, ignore_index=True)

    # Converte a coluna 'RealDateCapture' para o tipo datetime
    df_filled['RealDateCapture'] = pd.to_datetime(df_filled['RealDateCapture'])
    # Filtra o DataFrame para incluir apenas os registros onde 'RealDateCapture' é posterior à data inicial do biênio
    df_filled_final = df_filled[df_filled['RealDateCapture'] > data_inicial_bi]
    # Preenche os valores nulos do DataFrame filtrado com 0
    df_filled_final = df_filled_final.fillna(0)

    # Salvar o DataFrame resultante
    df_filled_final.to_csv('temp/dados_compilados/df_filled_final.csv', index=False)
    print("Dados finais salvos.")

def df_impressoras():
    """
    Lê os dados de impressoras de um arquivo CSV específico.

    Returns:
        pd.DataFrame: DataFrame contendo os dados das impressoras.
    """
    # Lê os dados de impressoras do arquivo CSV
    file = 'data/Impressoras Outsourcing - HP.csv'
    df = pd.read_csv(file)
    return df

if __name__ == "__main__":
    # Configura o registro de logs
    logging.basicConfig(level=logging.INFO)
    data_inicial = '01-01-2022'
    data_final = '31-05-2024'
    data_inicial_bi = '01-01-2024'
    # salva_dados_csv(data_inicial, data_final)
    gera_arquivo_csv_compilado('temp/dados_diarios/')
    preenche_dados_csv('temp/dados_compilados/arquivo_final.csv', data_inicial, data_final, data_inicial_bi)
