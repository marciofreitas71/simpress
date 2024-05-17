from app import config
from app import webservice
import logging
from app import crud
from datetime import datetime, timedelta
import pandas as pd
import glob
import os

def insere_dados_csv_to_bd():
    """
    Insere registros do webservice a partir de um arquivo csv.

    Lê um arquivo CSV contendo dados do webservice e insere esses registros em um banco de dados.
    
    Arquivo CSV esperado: 'testes/arquivos_final/arquivo_final-06-04-2024.csv'
    O arquivo deve conter as seguintes colunas:
    - 'RealDateCapture': Data de captura no formato 'YYYY-MM-DD'
    - 'PrinterDeviceID': ID da impressora
    - 'ReferenceMono': Referência de impressões monocromáticas
    - 'ReferenceColor': Referência de impressões coloridas
    
    Cada registro é inserido no banco de dados utilizando a função 'create_contagem_impressoras'
    do módulo 'crud'.

    Se ocorrer algum erro durante a inserção, uma mensagem de erro é impressa, e o programa continua a execução.
    """
    df = pd.read_csv('D:/projetos/simpress/testes/df_merged.csv')
    total = len(df)
    
    # Configurar logging
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # Supondo que df é seu DataFrame e crud é o módulo ou objeto que você está usando para criar registros

    contagem = 0

    # print(df.columns)
    for index, row in df.iterrows():
        try:
            # String com a data no formato '2024-01-01'
            data_string = row['RealDateCapture']
            
            # Converter a string em um objeto datetime
            data_datetime = datetime.strptime(data_string, '%Y-%m-%d')
            
            # Formatar a data para o formato aceito pelo Oracle (YYYY-MM-DD HH24:MI:SS)
            data_formatada = data_datetime.strftime('%d/%m/%Y')
            
            print(f'{row["SerialNumber"]}')
            
            # Tentar inserir os dados
            crud.create_contagem_impressoras(row['PrinterDeviceID'], row['ReferenceMono'], row['ReferenceColor'], data_formatada)
            print(f"Registro ({row['PrinterDeviceID']}) inserido com sucesso.")
        
        except ValueError as ve:
            logging.error(f"Erro ao converter data para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {ve}")
        
        except KeyError as ke:
            logging.error(f"Erro ao acessar uma chave inexistente no DataFrame para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {ke}")
        
        except Exception as e:
            logging.error(f"Erro ao inserir registro de contagem para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {e}")
        
        contagem += 1
        
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

def salva_dados_csv(DateTimeEnd):
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
    dias = 1
    while dias < 800:
        # Recupera dados do webservice
        dados_webservice = webservice.recuperar_dados(DateTimeEnd)
        
        # Adiciona a nova coluna com a DateTimeEnd
        dados_webservice['RealDateCapture'] = DateTimeEnd
        
        # Verifica se o arquivo existe
        if not os.path.isfile(f'testes/arquivos_final/dados-{DateTimeEnd}.csv'):

            # Salva os dados em um arquivo CSV
            dados_webservice.to_csv(f'testes/arquivos_final/dados-{DateTimeEnd}.csv', index=False)
            
            print(f'Dados do dia {DateTimeEnd} processados e salvos')
        else:
            print(f'O arquivo referente ao dia {DateTimeEnd} já foi gerado')
            
        dias += 1       
        # Atualiza a data para o dia anterior
        
        DateTimeEnd = datetime.strptime(DateTimeEnd, '%Y-%m-%d')
        DateTimeEnd -= timedelta(days=1)
        # Converter o datetime em uma string
        DateTimeEnd = DateTimeEnd.strftime('%Y-%m-%d')


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


def insere_websersvice_banco():

    # Carregando os dados e convertendo 'DateTimeRead' para datetime
    dados_webservice = pd.read_csv('arquivos/dados-teste.csv')
    dados_webservice['DateTimeRead'] = pd.to_datetime(dados_webservice['DateTimeRead'])

    # Filtrando registros anteriores a 01/01/2024
    registros_anteriores = (dados_webservice[dados_webservice['RealDataCapture'] < '2024-01-01']).sort_values(by='DateTimeRead',ascending=False )

    # Carregando a lista de impressoras
    todas_impressoras = pd.read_csv('data/todas_impressoras.csv')

    # Inicializando variáveis
    data_limite = pd.to_datetime('2024-01-01')
    qtd_impressoras = len(todas_impressoras)
    num_impressora = 1
    lista_dataframes = []  # Lista para armazenar DataFrames temporários

    # Iterando sobre as impressoras
    for impressora in todas_impressoras['SerialNumber']:

        # Lista vazia para armazenar registros da impressora atual
        lista_registros = []

        # Iterando sobre os registros
        for indice, registro in dados_webservice.iterrows():

            # Verificando se o registro pertence à impressora e data limite
            if registro['SerialNumber'] == impressora and registro['DateTimeRead'] < data_limite:

                # Encontrando o último registro da impressora antes de 01/01/2024
                ultimo_registro = registro.copy()

                # Atualizando data para 01/01/2024
                ultimo_registro['DateTimeRead'] = '2024-01-01'
                ultimo_registro['RealDataCapture'] = '2024-01-01'

                # Adicionando o registro à lista temporária
                lista_registros.append(ultimo_registro)

        # Se houver registros para a impressora, cria um DataFrame e concatena na lista
        if lista_registros:
            df_impressora = pd.concat(lista_registros)
            lista_dataframes.append(df_impressora)

        # Atualizando contadores
        num_impressora += 1

    # Salvando o DataFrame final (concatenação final)
    arquivo_final = pd.concat(lista_dataframes)
    arquivo_final.to_csv('arquivo_final2.csv')

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
    df_final.to_csv('testes/arquivo_final-10-05-2024.csv', index=False)

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


