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
    'dealerName': 'XXXXX',  # Nome do revendedor autorizado
    'dealerUserEmail': 'xxxxx@xxx.com.br',  # E-mail do usuário do revendedor
    'dealerUserPassword': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  # Senha do usuário do revendedor
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
