import sys
import os

# Adiciona o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import config, webservice, crud
import logging
from tqdm import tqdm
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import pandas as pd
import itertools
import pandas as pd
import numpy as np
import socket
import glob
import csv


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

def insere_websersvice_banco():
    """
    Variação da função 'insere_websersvice_banco' que lida com a inserção de dados do webservice no banco de dados. 
    Nesta variação, deve-se considerar que a aplicação pode ter ficado alguns dias sem rodar, e portanto, é necessário
    recuperar os dados de todos os dias entre a última execução e a data atual e preencher as lacunas.
    """

    def obter_ultima_data_bd():
        """
        Recupera a data do último registro no banco de dados.

        Returns:
            datetime: Data do último registro no banco de dados.
        """
        query = "SELECT MAX(DATA_LEITURA) FROM CONTAGEM_IMPRESSORAS"
        data = crud.execute_query(query)
        return data

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

        # Cria um dataframe pandas com os dados do último registro no banco de dados
        registros_bd = crud.read_impressoras_data(data.strftime('%d-%m-%Y'))
        colunas = ['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
        df_database = pd.DataFrame(registros_bd, columns=colunas) if registros_bd else pd.DataFrame(columns=colunas)

        # Concatena os dataframes do webservice e do banco de dados e identifica as diferenças
        df_diff = pd.concat([df_webservice, df_database]).drop_duplicates(subset=['IMPRESSORA_ID', 'DateTimeRead'], keep=False)
        df_final = pd.concat([df_webservice, df_diff])

        # Iteração para inserir os registros no banco de dados
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


def verifica_impressoras(data_atual=None):
    """
    Compara os dados de impressoras do banco de dados e do webservice, inserindo novas impressoras se necessário.

    Este método realiza as seguintes etapas:
    
    1. Lê os dados de impressoras do banco de dados referentes ao dia anterior.
    2. Recupera os dados das impressoras do webservice relativos ao dia atual.
    3. Compara os dois DataFrames e identifica as diferenças.
    4. Verifica se as impressoras do DataFrame de diferenças estão presentes no banco de dados.
    5. Insere as impressoras que não estão presentes no banco de dados.

    Parâmetros:
    data_atual (str): Data atual no formato 'dd-mm-yyyy'. Se não fornecido, a data atual será utilizada.

    Retorna:
    None
    """
    if data_atual is None:
        data_atual = datetime.now().strftime('%d-%m-%Y')
    else:
        # Certifica-se de que a data_atual está no formato correto
        try:
            data_atual = datetime.strptime(data_atual, '%d-%m-%Y').strftime('%d-%m-%Y')
        except ValueError:
            raise ValueError("O formato da data deve ser 'dd-mm-yyyy'")

    data_bd = datetime.strptime(data_atual, '%d-%m-%Y') - timedelta(days=1)
    data_bd_str = data_bd.strftime('%d-%m-%Y')

    registros_bd = crud.read_impressoras_data(data_bd_str)
    colunas = ['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
    df_database = pd.DataFrame(registros_bd, columns=colunas)

    df_webservice = webservice.recuperar_dados(data_atual)
    df_webservice['DateTimeRead'] = pd.to_datetime(df_webservice['DateTimeRead'])

    df_diff = pd.concat([df_webservice, df_database]).drop_duplicates(subset=['IMPRESSORA_ID', 'DateTimeRead'], keep=False)

    if df_diff.empty:
        print("Não há diferenças entre os dados do webservice e os dados do banco de dados.")
    else:   
        print("Diferenças encontradas:")
        print(df_diff)
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


if __name__ == "__main__":
    
    verifica_impressoras('01-01-2022')
