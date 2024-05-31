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

def insere_dados_csv_to_bd():
    """
    Insere registros do webservice a partir de um arquivo CSV no banco de dados.

    Lê um arquivo CSV contendo dados do webservice e insere esses registros em um banco de dados.
    
    O arquivo CSV esperado deve conter as colunas:
    - 'RealDateCapture': Data de captura no formato 'YYYY-MM-DD'
    - 'PrinterDeviceID': ID da impressora
    - 'ReferenceMono': Referência de impressões monocromáticas
    - 'ReferenceColor': Referência de impressões coloridas
    
    Cada registro é inserido no banco de dados utilizando a função 'create_contagem_impressoras' do módulo 'crud'.
    """
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    contagem = 0

    with open('D:/projetos/simpress/testes/df_filled_2024.csv', mode='r', encoding='utf-8') as csvfile, \
         open('erros_log.csv', mode='w', newline='', encoding='utf-8') as errorfile:
        
        reader = pd.read_csv(csvfile, iterator=True, chunksize=1)
        error_writer = csv.writer(errorfile)
        error_writer.writerow(['PrinterDeviceID', 'SerialNumber', 'ErrorType', 'ErrorMessage'])
        
        for chunk in reader:
            for index, row in chunk.iterrows():
                try:
                    data_string = row['RealDateCapture']
                    data_datetime = datetime.strptime(data_string, '%Y-%m-%d')
                    
                    print(f'{row["SerialNumber"]}')
                    crud.create_contagem_impressoras(row['PrinterDeviceID'], row['ReferenceMono'], row['ReferenceColor'], data_datetime)
                    print(f"Registro ({row['PrinterDeviceID']}) inserido com sucesso.")
                
                except ValueError as ve:
                    logging.error(f"Erro ao converter data para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {ve}")
                    error_writer.writerow([row['PrinterDeviceID'], row['SerialNumber'], 'ValueError', str(ve)])
                
                except KeyError as ke:
                    logging.error(f"Erro ao acessar uma chave inexistente no DataFrame para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {ke}")
                    error_writer.writerow([row['PrinterDeviceID'], row['SerialNumber'], 'KeyError', str(ke)])
                
                except Exception as e:
                    logging.error(f"Erro ao inserir registro de contagem para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {e}")
                    error_writer.writerow([row['PrinterDeviceID'], row['SerialNumber'], 'Exception', str(e)])
                
                contagem += 1
                print(f'Inserido o registro {contagem}')
                os.system('cls')

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
