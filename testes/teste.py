from datetime import datetime, timedelta
import zeep
import pandas as pd
from dotenv import load_dotenv
import logging
import importlib
import os
import sys
from datetime import datetime
import socket

sys.path.append('D:/projetos/simpress')

# # import repository_gestao_impressoras as repo

# impressoras = repo.recuperarDadosImpressoras()
# import repository_gestao_impressoras as repo

def gera_arquivo_csv_compilado(pasta):

    # Lista para armazenar os DataFrames de cada arquivo CSV
    dataframes = []

    # Itera sobre os arquivos na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.csv'):
            # Caminho completo para o arquivo
            caminho_arquivo = os.path.join(pasta, arquivo)
            # Lê o arquivo CSV e adiciona ao lista de DataFrames
            df = pd.read_csv(caminho_arquivo)
            dataframes.append(df)
            print(f'Dados adicionados do arquivo {arquivo}')

    # Concatena todos os DataFrames em um único DataFrame
    df_final = pd.concat(dataframes, ignore_index=True)

    # Salva o DataFrame final em um arquivo CSV
    df_final.to_csv('testes/arquivo_final-06-04-2024.csv', index=False)

# Impressoras informadas por bruno
def df_impressoras():
    file = 'data/Impressoras Outsourcing - HP.csv'
    df = pd.read_csv(file)
    return df

# Busca no dataset todas as impressoras que geraram dados
def verifica_impressoras_dataset():
    file = 'testes/arquivo_final.csv'
    df = pd.read_csv(file)
    # filtra todos os valores únicos das impressoras
    # tomando como base o SerialNumber
    ids_impressoras = df['SerialNumber'].unique()
    print(len(ids_impressoras))
    

def ler_arquivo_compilado():
    file = 'testes/arquivo_final.csv'
    df = pd.read_csv(file)
    return df

# Transorma arquivo compilado para que as lacunas nas datas sejam preenchidas
def transforma_arquivos():
    file = 'testes/arquivo_final.csv'
    df = pd.read_csv(file)
    
    # for index, rows in df.iterrows():
    #     # armazena a data real do relatório
    #     RealDataCapture = datetime.strptime(rows['RealDataCapture'], '%Y-%m-%d').date()        
    #     # armazena a da que será retornada do webservice
    #     DateTimeRead = datetime.strptime(rows['DateTimeRead'], "%Y-%m-%dT%H:%M:%S").date()      
    #     print(DateTimeRead == RealDataCapture)


# Função para retornar o hostname a partir do ip
def obter_hostname_por_ip(ip):
    try:
        hostname = socket.gethostbyaddr(ip[:-10])
        return hostname[0]  # O nome do host está na primeira posição da tupla retornada
    except socket.herror:
        return "Hostname não encontrado"
    except socket.gaierror:
        return "Endereço IP inválido"

# Funcao para extrair o número de zona do ip
def extrair_id_zona(ip):
    padrao = r'10\.171\.(\d+)\.60'
    correspondencia = re.match(padrao, ip)
    if correspondencia:
        return correspondencia.group(1)
    else:
        return "Padrão de IP não corresponde"

# # Substitua 'endereco_ip' pelo endereço IP real que você deseja verificar
# endereco_ip = "10.5.203.75 (network)"  # Exemplo de endereço IP

# hostname = obter_hostname_por_ip(endereco_ip)
# print(f"O hostname para o IP {endereco_ip} é: {hostname}")

pasta = 'D:/projetos/simpress/testes/arquivos_final'

gera_arquivo_csv_compilado(pasta)