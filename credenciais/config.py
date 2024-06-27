import os
import oracledb

"""
Este script define variáveis para acessar um serviço da web SOAP e configurar sua chamada.
"""

# URL do WSDL do serviço da web
wsdl_url = 'https://api-counters.nddprint.com/CountersWS/CountersData.asmx?WSDL'

# Método do serviço da web a ser chamado
service_method = 'GetReferenceCountersData'  # Alternativamente: 'GetPlainCountersData'

# Nome do arquivo CSV de saída para armazenar os dados recuperados
output_csv = 'output-reference-2023-10-27.csv'  # Alternativamente: 'output-plain-2023-10-15.csv'

# Payload contendo os parâmetros para o método do serviço
payload = {
    'dealerName': 'SIMPRESS',  # Nome do revendedor autorizado
    'dealerUserEmail': 'ruguedes@tre-ba.jus.br',  # E-mail do usuário do revendedor
    'dealerUserPassword': '8lYKAfLbl2FKqAJgWWRA5Q==',  # Senha do usuário do revendedor
     'dateTimeEnd': "",
    # 'dateTimeStart': '2023-10-17 00:00:00',  # Data e hora de início (opcional)
    'maxLimitDaysEarlier': 1,  # Limite máximo de dias anteriores para recuperar os dados
    'enterpriseName': '9853_TRE_BA',  # Nome da empresa ou organização
    'serialNumber': '',  # Número de série da impressora (opcional)
    'siteName': '',  # Nome do local (opcional)
    'siteDivisionName': '',  # Nome da divisão do local (opcional)
    'engaged': False,  # Indicador de se a impressora está engajada ou não
    'fieldsList': 'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged'
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