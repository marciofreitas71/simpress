from dotenv import load_dotenv
import oracledb
import os

load_dotenv()

def get_connection():
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')

    if None in [user_name, password, host, port, service_name]:
        raise ValueError("Erro: Algum valor necessário está ausente.")

    connection = oracledb.connect(user=user_name, password=password, host=host, port=port, service_name=service_name)
    return connection
