from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Caminhos para diferentes diretórios
APP_DIR = os.path.dirname(__file__)

CONFIG_DIR = os.path.join(APP_DIR, 'config')
CRUD_DIR = os.path.join(APP_DIR, 'crud')
DATABASE_DIR = os.path.join(APP_DIR, 'database')
MODELS_DIR = os.path.join(APP_DIR, 'models')
QUERIES_DIR = os.path.join(APP_DIR, 'queries')
WEBSERVICE_DIR = os.path.join(APP_DIR, 'webservice')
CREDENCIAIS_DIR = os.path.join(APP_DIR, 'webservice')

def get_connection():
    """
    Estabelece uma conexão com o banco de dados Oracle.

    Retorna uma conexão ativa com o banco de dados Oracle, utilizando as credenciais e
    informações de conexão fornecidas no arquivo de ambiente (.env) através das variáveis
    de ambiente 'user_name', 'password', 'host', 'port' e 'service_name'.

    Raises:
        ValueError: Se algum valor necessário está ausente no arquivo de ambiente.

    Returns:
        Connection: Uma conexão ativa com o banco de dados Oracle.

    Exemplo:
    >>> connection = get_connection()
    """
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')

    if None in [user_name, password, host, port, service_name]:
        raise ValueError("Erro: Algum valor necessário está ausente.")

    connection = oracledb.connect(user=user_name, password=password, host=host, port=port, service_name=service_name)
    return connection



wsdl_url = 'https://api-counters.nddprint.com/CountersWS/CountersData.asmx?WSDL'
service_method = 'GetReferenceCountersData' #'GetPlainCountersData'
output_csv = 'output-reference-2023-10-27.csv' #'output-plain-2023-10-15.csv'
payload = {
    'dealerName': 'SIMPRESS',
    'dealerUserEmail': 'ruguedes@tre-ba.jus.br',
    'dealerUserPassword': '8lYKAfLbl2FKqAJgWWRA5Q==',
    'dateTimeEnd': "",
    'maxLimitDaysEarlier': 180,
    'enterpriseName': '9853_TRE_BA',
    'serialNumber': '',
    'siteName': '',
    'siteDivisionName': '',
    'engaged': False,
    'fieldsList': 'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #'EnterpriseName;PrinterDeviceID;SerialNumber;AddressName;siteName;EnabledCounters;CounterTypeName;FirstCounterTotal;LatestCounterTotal;FirstCounterMono;LatestCounterMono;FirstCounterColor;LatestCounterColor' #'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #
}