import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import oracledb
from dotenv import load_dotenv

load_dotenv()

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
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')

    if None in [user_name, password, host, port, service_name]:
        raise ValueError("Erro: Algum valor necessário está ausente no arquivo de ambiente (.env).")

    connection = oracledb.connect(user=user_name, password=password, host=host, port=port, service_name=service_name)
    return connection
