import os
import oracledb

"""
Este script define variáveis para acessar um serviço da web SOAP e configurar sua chamada.
"""

wsdl_url = 'https://api-counters.nddprint.com/CountersWS/CountersData.asmx?WSDL'
service_method = 'GetReferenceCountersData' #'GetPlainCountersData'
output_csv = 'output-reference-2023-10-27.csv' #'output-plain-2023-10-15.csv'
payload = {
    'dealerName': 'SIMPRESS',
    'dealerUserEmail': 'ruguedes@tre-ba.jus.br',
    'dealerUserPassword': '8lYKAfLbl2FKqAJgWWRA5Q==',
    #'dateTimeStart': '2023-10-17 00:00:00',
    'dateTimeEnd': '2023-11-30 02:00:00',
    'maxLimitDaysEarlier': 1,
    'enterpriseName': '9853_TRE_BA',
    'serialNumber': '',
    'siteName': '',
    'siteDivisionName': '',
    'engaged': False,
    'fieldsList': 'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #'EnterpriseName;PrinterDeviceID;SerialNumber;AddressName;siteName;EnabledCounters;CounterTypeName;FirstCounterTotal;LatestCounterTotal;FirstCounterMono;LatestCounterMono;FirstCounterColor;LatestCounterColor' #'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #
    # Lista de campos a serem incluídos na resposta do serviço
}

def get_connection():
    """
    Estabelece uma conexão com o banco de dados Oracle.

    Esta função cria e retorna uma conexão ativa com o banco de dados Oracle, utilizando as credenciais
    e informações de conexão fornecidas no arquivo de ambiente (.env). As seguintes variáveis de ambiente 
    são esperadas no arquivo .env:

    - 'user_name': Nome de usuário do banco de dados Oracle.
    - 'password': Senha do banco de dados Oracle.
    - 'host': Endereço do host do banco de dados Oracle.
    - 'port': Porta de conexão do banco de dados Oracle.
    - 'service_name': Nome do serviço do banco de dados Oracle.

    Raises:
        ValueError: Se algum valor necessário estiver ausente no arquivo de ambiente.

    Returns:
        oracledb.Connection: Uma conexão ativa com o banco de dados Oracle.

    Exemplo:
    >>> connection = get_connection()
    """
    
    user_name='GESTAO_IMPRESSAO'
    password='je8u_asdfa'
    host='ba1linha.tre-ba.jus.br'
    port=1523
    service_name='dese'

    if None in [user_name, password, host, port, service_name]:
        raise ValueError("Erro: Algum valor necessário está ausente no arquivo de ambiente (.env).")

    connection = oracledb.connect(user=user_name, password=password, host=host, port=port, service_name=service_name)
    return connection