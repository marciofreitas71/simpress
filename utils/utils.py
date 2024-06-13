import sys
import os
import logging
import socket
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

from credenciais import config

# Adiciona o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import webservice, crud

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
    Insere dados do webservice no banco de dados para todos os dias entre a última execução e a data atual.
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
    
    print("Última data no banco de dados:")
    ultima_data_bd = pd.to_datetime(ultima_data_bd)
    print(ultima_data_bd)

    # Define a data de início como o dia seguinte ao último registro no banco de dados
    data_inicio = (ultima_data_bd + timedelta(days=1)).date()

    # Define a data de fim como a data atual
    data_fim = datetime.now().date()   
    data_fim = data_fim - timedelta(days=1)

    # Corrige a data de início se data_inicio for posterior a data_fim
    if data_inicio > data_fim:
        print("A data de início é posterior à data de fim. Ajustando data de início para data de fim.")
        data_inicio = data_fim

    print(f"Data de início ajustada: {data_inicio}")
    print(f"Data de fim ajustada: {data_fim}")

    # Verifica se há novas impressoras no webservice e insere no banco de dados
    verifica_impressoras()
    print("Impressoras verificadas e inseridas no banco de dados.")

    # Iteração para preencher as lacunas entre a última data de registro e a data atual
   
    for data in pd.date_range(start=data_inicio, end=data_fim):
        print(f'Ultima data no banco de dados: {ultima_data_bd}')
        print(f'Data atual: {data}')
       
        print(f"Processando dados para a data {data.strftime('%d-%m-%Y')}...")
        # Cria um dataframe com os dados do webservice para a data especificada
        df_webservice = obter_dados_webservice(data.strftime('%d-%m-%Y'))

        print(data.strftime('%d-%m-%Y'))

        # Cria um dataframe pandas com os dados do último registro no banco de dados
        registros_bd = crud.read_impressoras_data(ultima_data_bd.strftime('%d-%m-%Y'))
        
        colunas = ['ID', 'IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
        df_database = pd.DataFrame(registros_bd, columns=colunas) if registros_bd else pd.DataFrame(columns=colunas)
        
    
        print("Registros do banco de dados:")
        print(len(df_database))
        print("Registros do webservice:")
        print(len(df_webservice))
        df_webservice = df_webservice.rename(columns={'PrinterDeviceID': 'IMPRESSORA_ID', 'DateTimeRead': 'DATA_LEITURA', 'ReferenceMono': 'CONTADOR_PB', 'ReferenceColor': 'CONTADOR_COR', })
        df_webservice = df_webservice[['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'DATA_LEITURA']]

        # Concatena os dataframes do webservice e do banco de dados e identifica as diferenças
        df_concatenado = pd.concat([df_webservice, df_database], axis=0)
        # Ordene por IMPRESSORA_ID e DATA_LEITURA, a primeira crescente e a segunda decrescente
        df_concatenado = df_concatenado.sort_values(by=['IMPRESSORA_ID', 'DATA_LEITURA'], ascending=[True, False])
        
        print(df_concatenado.shape)

        data = data.strftime('%d-%m-%Y')
        df_concatenado.to_csv(f'temp/dados_compilados/df_concatenado-{data}.csv')
        
        df_diff = df_concatenado.drop_duplicates(subset=['IMPRESSORA_ID'], keep='first')
        print(df_diff.shape)

        df_diff.to_csv(f'temp/dados_compilados/df_diff-{data}.csv')
        # df_final = df_diff.dropna(subset=['IMPRESSORA_ID', 'DateTimeRead'])    

        # Iteração para inserir os registros no banco de dados
        for index, row in df_diff.iterrows():
            print(row['IMPRESSORA_ID'], row['DATA_LEITURA'])
            try:
                crud.create_contagem_impressoras(
                    row['IMPRESSORA_ID'],
                    row['CONTADOR_PB'],
                    row['CONTADOR_COR'],
                    row['DATA_LEITURA']
                )
                print(f"Registro ({row['IMPRESSORA_ID']}) inserido com sucesso.")
            except Exception as e:
                print(f"Erro ao inserir registro de contagem para o registro com IMPRESSORA_ID {row['IMPRESSORA_ID']}: {e}")
        ultima_data_bd = ultima_data_bd + timedelta(days=1)

def verifica_impressoras(data_atual=None):
    """
    Compara os dados de impressoras do banco de dados e do webservice, inserindo novas impressoras se necessário.
    """
    # Define a data de fim como a data atual
    data_fim = datetime.now().date()

    recuperando_impressoras = True
    while recuperando_impressoras:
        print('Recuperando impressoras do webservice...')
        # Cria um dataframe com os dados do webservice para a data especificada
        df_webservice = webservice.recuperar_dados(data_fim.strftime('%d-%m-%Y'))
        recuperando_impressoras = False
        print('Impressoras recuperadas com sucesso.')
    
    df_webservice = df_webservice[['EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]
        
    # Cria um dataframe pandas com os dados referentes à última data de registro no banco de dados (RealDataCapture)
    registros_bd = crud.obter_registros_ultima_data()
    df_registros_bd = pd.DataFrame(registros_bd, columns=['ID', 'IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT'])
    df_registros_bd = df_registros_bd.merge(df_webservice, how='outer', left_on='IMPRESSORA_ID', right_on='PrinterDeviceID')
    df_registros_bd = df_registros_bd[['EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]
        
    # Concatena os dataframes do webservice e do banco de dados e identifica as diferenças
    df_diff = pd.concat([df_webservice, df_registros_bd]).drop_duplicates(keep=False)
    print('Dataframe de diferenças: ')
    contagem = 0
    if df_diff.empty:
        print('Nenhuma impressora foi adicionada ao banco de dados.')
    else:
        for index, row in df_diff.iterrows():
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

if __name__ == "__main__":
    pass
    # verifica_impressoras(data_atual='09-05-2024')
    # insere_webservice_banco()
    # dados_webservice = obter_dados_webservice('04-05-2024')
