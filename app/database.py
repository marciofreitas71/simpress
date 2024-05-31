from dotenv import load_dotenv
import oracledb
import os

load_dotenv()

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
