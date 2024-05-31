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
    # Carregar o conjunto de dados
    print("Carregando o conjunto de dados...")
    df = pd.read_csv(caminho_csv)
    df = df[df['BrandName'] == 'HP']
    df = df.sort_values(by=['RealDateCapture','SerialNumber'], ascending=[False,True])

    # Converte a coluna 'RealDateCapture' do df para datetime
    df['RealDateCapture'] = pd.to_datetime(df['RealDateCapture'], format='%d-%m-%Y')

    # Salva o arquivo csv com os dados originais
    df.to_csv('df_original.csv')
    print(f"Conjunto de dados carregado com {len(df)} registros.")

  # Selecionar impressoras únicas (linhas únicas com base na coluna 'SerialNumber')
    imp = df.drop_duplicates(subset='SerialNumber')

    # Seleciona as colunas do DataFrame 'imp'
    imp = imp[['EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]

    # Gera arquivo csv com as impressoras do dataframe
    imp.to_csv('testes/data/df_impressoras.csv')

    # Gera um DataFrame com datas
    date_range = pd.date_range(start='01-01-2022', end='28-05-2024', freq='D')
    df_dates = pd.DataFrame({'RealDateCapture': date_range})

    # Adicionar a coluna 'key' para combinação
    imp['key'] = 1
    df_dates['key'] = 1

    # Combinação dos DataFrames
    df_full_datas = pd.merge(imp, df_dates, on='key').drop('key', axis=1)

    # Gera um arquivo csv com as datas mescladas com os dados
    df_full_datas.to_csv("df_full_datas.csv")

    # Faz o merge com o DataFrame original
    df_merged = df_full_datas.merge(df, how='left', on=['RealDateCapture','SerialNumber','EnterpriseName','PrinterDeviceID','BrandName','PrinterModelName'])

    # Preenche os valores ausentes com nan
    df_merged.fillna(value=np.nan, inplace=True)

    # ordena os registros pelas colunas 'RealDateCapture' e 'SerialNumber'
    df_merged = df_merged.sort_values(by=['RealDateCapture','SerialNumber'], ascending=False)

    # Gera um arquivo csv com os dados mescladas
    df_merged.to_csv('df_merged.csv')

    # Inicializa uma lista vazia para armazenar DataFrames individuais correspondentes a cada número de série
    registros_impressoras = []
    # Itera sobre cada linha do DataFrame 'imp'
    for index, row in imp.iterrows():
        serial_number = row['SerialNumber']
        # Filtra o DataFrame 'df_merged' para obter apenas as linhas com o mesmo número de série e preenche valores nulos usando o método backward fill (bfill)
        df_parcial = df_merged[df_merged['SerialNumber'] == serial_number].bfill()
        # Adiciona o DataFrame filtrado e preenchido à lista 'impressoras'
        registros_impressoras.append(df_parcial)

    # Concatena todos os DataFrames na lista 'impressoras' em um único DataFrame, ignorando os índices originais
    df_filled = pd.concat(registros_impressoras, ignore_index=True)

    # Converte a coluna 'RealDateCapture' para o tipo datetime
    df_filled['RealDateCapture'] = pd.to_datetime(df_filled['RealDateCapture'])
    # Filtra o DataFrame para incluir apenas os registros onde 'RealDateCapture' é posterior à data de 01/01/2024
    df_filled_2024 = df_filled[df_filled['RealDateCapture'] >= '2024-01-01']
    # Preenche os valores nulos do DataFrame filtrado com 0
    df_filled_2024 = df_filled_2024.fillna(0)
    # Salvar o DataFrame resultante
    df_filled_2024.to_csv('D:/projetos/simpress/testes/df_filled_2024.csv', index=False)

def insere_dados_csv_to_bd():
    """
    Insere registros do webservice a partir de um arquivo csv.

    Lê um arquivo CSV contendo dados do webservice e insere esses registros em um banco de dados.
    
    Arquivo CSV esperado: 'D:/projetos/simpress/testes/df_merged.csv'
    O arquivo deve conter as seguintes colunas:
    - 'RealDateCapture': Data de captura no formato 'YYYY-MM-DD'
    - 'PrinterDeviceID': ID da impressora
    - 'ReferenceMono': Referência de impressões monocromáticas
    - 'ReferenceColor': Referência de impressões coloridas
    
    Cada registro é inserido no banco de dados utilizando a função 'create_contagem_impressoras'
    do módulo 'crud'.

    Se ocorrer algum erro durante a inserção, uma mensagem de erro é impressa, e o programa continua a execução.
    """
    # Configurar logging
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    contagem = 0

    # Abrir o arquivo CSV e o arquivo de log de erros
    with open('D:/projetos/simpress/testes/df_filled_2024.csv', mode='r', encoding='utf-8') as csvfile, \
         open('erros_log.csv', mode='w', newline='', encoding='utf-8') as errorfile:
        
        # Criar um leitor CSV em modo iterador
        reader = pd.read_csv(csvfile, iterator=True, chunksize=1)
        error_writer = csv.writer(errorfile)
        error_writer.writerow(['PrinterDeviceID', 'SerialNumber', 'ErrorType', 'ErrorMessage'])
        
        for chunk in reader:
            for index, row in chunk.iterrows():
                try:
                    # String com a data no formato '2024-01-01'
                    data_string = row['RealDateCapture']
                    
                    # Converter a string em um objeto datetime
                    data_datetime = datetime.strptime(data_string, '%Y-%m-%d')
                    
                    print(f'{row["SerialNumber"]}')
                    
                    # Tentar inserir os dados
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

def salva_dados_csv(DateTimeStart, DateTimeEnd):
    """
    Insere registros de impressoras a partir de um arquivo CSV no banco de dados.

    Args:
        nome_arquivo (str): O caminho do arquivo CSV contendo os dados das impressoras.

    Esta função lê um arquivo CSV contendo informações sobre impressoras e as insere no banco de dados.
    O arquivo CSV deve ter as seguintes colunas:
    - 'PrinterDeviceID': ID da impressora
    - 'BrandName': Nome da marca da impressora
    - 'PrinterModelName': Nome do modelo da impressora
    - 'SerialNumber': Número de série da impressora

    As impressoras são inseridas no banco de dados utilizando a função 'create_impressora' do módulo 'repo'.

    Se uma impressora com o mesmo 'PrinterDeviceID' já existe no banco de dados, a inserção é ignorada.

    Exemplo:
    >>> inserir_impressoras_from_csv('caminho/do/arquivo.csv')
    """
    
    # Quantidade de dias anteriores à data final    
    
    data = DateTimeEnd
    while data != DateTimeStart:
        # Recupera dados do webservice
        dados_webservice = webservice.recuperar_dados(data)
        
        # Adiciona a nova coluna com a DateTimeEnd
        dados_webservice['RealDateCapture'] = data
        
        # Verifica se o arquivo existe
        if not os.path.isfile(f'testes/arquivos_final/dados-{data}.csv'):

            # Salva os dados em um arquivo CSV
            dados_webservice.to_csv(f'testes/arquivos_final/dados-{data}.csv', index=False)
            
            print(f'Dados do dia {data} processados e salvos')
        else:
            print(f'O arquivo referente ao dia {data} já foi gerado')
            
             
        # Atualiza a data para o dia anterior
        
        data = datetime.strptime(data, '%d-%m-%Y')
        data -= timedelta(days=1)
        # Converter o datetime em uma string
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

    Exemplos:
    >>> obter_hostname_por_ip('192.168.1.1')
    'router.example.com'
    >>> obter_hostname_por_ip('256.0.0.1')
    'Endereço IP inválido'
    >>> obter_hostname_por_ip('invalid_ip')
    'Endereço IP inválido'
    """
    try:
        hostname = socket.gethostbyaddr(ip[:-10])
        return hostname[0]  # O nome do host está na primeira posição da tupla retornada
    except socket.herror:
        return "Hostname não encontrado"
    except socket.gaierror:
        return "Endereço IP inválido"

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
    df_final.to_csv('testes/arquivos_final/arquivo_final-06-04-2024.csv', index=False)

# Impressoras informadas por bruno
def df_impressoras():
    file = 'data/Impressoras Outsourcing - HP.csv'
    df = pd.read_csv(file)
    return df

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


def insere_websersvice_banco(data):
    """
    Insere os dados do webservice no banco de dados após verificar e comparar com os dados existentes.
    """
    # Recuperar a data do dia anterior
    data_bd = datetime.strptime(data, '%d-%m-%Y') - timedelta(days=1)
    data_bd_str = data_bd.strftime('%d-%m-%Y')

    # Recuperar dados do webservice
    df_webservice = webservice.recuperar_dados(data)
    
    # Converter 'DateTimeRead' para datetime
    df_webservice['DateTimeRead'] = pd.to_datetime(df_webservice['DateTimeRead'])

    # Obter dados do banco de dados para a data do dia anterior
    registros_bd = crud.read_impressoras_data(data_bd_str)

    # Criar um DataFrame com os dados do banco de dados
    if registros_bd:
        colunas = ['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT']
        df_database = pd.DataFrame(registros_bd, columns=colunas)
    else:
        df_database = pd.DataFrame(columns=['IMPRESSORA_ID', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL', 'DATA_LEITURA', 'CREATED_AT'])

    # Comparar os dois DataFrames para saber quais impressoras do df_database estão no df_webservice
    df_diff = pd.concat([df_webservice, df_database]).drop_duplicates(subset=['IMPRESSORA_ID', 'DateTimeRead'], keep=False)

    # Criar um DataFrame final concatenando o df_diff ao df_webservice
    df_final = pd.concat([df_webservice, df_diff])

    # Inserir no banco de dados os dados do DataFrame final
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

    data = datetime.now().strftime('%d-%m-%Y')
    
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
    df_final.to_csv(f'testes/arquivo_final-{data}.csv', index=False)

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

