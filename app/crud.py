import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import pandas as pd
from credenciais import config
from app import webservice

"""
Este módulo define operações CRUD (Create, Read, Update, Delete) para manipulação dos dados no banco de dados.

Pacotes importados:
- datetime: Para manipulação de datas e horas.
- config: Para configuração e conexão com o banco de dados.

Funções:
- create_impressora(): Cria uma nova impressora no banco de dados.
- create_contagem_impressoras(): Registra uma contagem de impressoras no banco de dados.
- read_contagem_impressoras(): Lê os registros de contagem de impressoras do banco de dados.
- update_contagem_impressora(): Atualiza os registros de contagem de impressoras no banco de dados.
- delete_contagem_impressora(): Exclui os registros de contagem de impressoras do banco de dados.
- delete_all_registros(): Exclui todos os registros de contagem de impressoras do banco de dados.
- delete_all_impressoras(): Exclui todas as impressoras do banco de dados.
- read_impressoras_data(): Lê os registros de contagem de impressoras do banco de dados para uma determinada data.
- read_all_record_data(): Lê todos os registros da tabela contagem_impressora do banco de dados.
- obter_registros_ultima_data(): Obtém registros da última data de leitura no banco de dados.
- obter_ultima_data_bd(): Obtém a última data de leitura no banco de dados.
"""

def create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER):
    """
    Cria uma nova impressora no banco de dados.

    Args:
        PRINTERDEVICEID (str): O ID do dispositivo da impressora.
        PRINTERBRANDNAME (str): O nome da marca da impressora.
        PRINTERMODELNAME (str): O nome do modelo da impressora.
        SERIALNUMBER (str): O número de série da impressora.

    Returns:
        bool: True se a impressora foi criada com sucesso, False se a impressora já existe.

    Raises:
        Exception: Se ocorrer um erro ao inserir a impressora no banco de dados.
    """
    connection = config.get_connection()
    cursor = connection.cursor()
    
    select_query = "SELECT COUNT(*) FROM impressora WHERE PRINTERDEVICEID = :printerdeviceid"
    cursor.execute(select_query, {'printerdeviceid': PRINTERDEVICEID})
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("Impressora já existe no banco de dados.")
        cursor.close()
        connection.close()
        return False

    created_at = datetime.now()
    status = 1
    
    insert_query = """
    INSERT INTO impressora (PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)
    VALUES(:printerdeviceid, :printerbrandname, :printermodelname, :serialnumber, :created_at, :status)
    """
    
    cursor.execute(insert_query, {
        'printerdeviceid': PRINTERDEVICEID,
        'printerbrandname': PRINTERBRANDNAME,
        'printermodelname': PRINTERMODELNAME,
        'serialnumber': SERIALNUMBER,
        'created_at': created_at,
        'status': status
    })

    connection.commit()
    cursor.close()
    connection.close()
    return True

def create_contagem_impressoras(impressora_id, contador_pb, contador_cor, data_leitura):
    """
    Registra uma contagem de impressoras no banco de dados.

    Args:
        impressora_id (int): O ID da impressora associada à contagem.
        contador_pb (int): O contador de impressões em preto e branco.
        contador_cor (int): O contador de impressões coloridas.
        data_leitura (datetime): A data e hora da leitura do contador.

    Raises:
        Exception: Se ocorrer um erro ao inserir a contagem no banco de dados.
    """
    connection = config.get_connection()
    cursor = connection.cursor()
    
    contador_total = contador_pb + contador_cor
    created_at = datetime.now()
    
    select_query = """
    SELECT COUNT(*)
    FROM contagem_impressora
    WHERE IMPRESSORA_ID = :impressora_id
    AND DATA_LEITURA = :data_leitura
    """
    cursor.execute(select_query, {'impressora_id': impressora_id, 'data_leitura': data_leitura})
    count = cursor.fetchone()[0]
    
    if count == 0:
        insert_query = """
        INSERT INTO contagem_impressora (IMPRESSORA_ID, CONTADOR_PB, CONTADOR_COR, CONTADOR_TOTAL, DATA_LEITURA, CREATED_AT)
        VALUES (:impressora_id, :contador_pb, :contador_cor, :contador_total, :data_leitura, :created_at)
        """
        cursor.execute(insert_query, {
            'impressora_id': impressora_id,
            'contador_pb': contador_pb,
            'contador_cor': contador_cor,
            'contador_total': contador_total,
            'data_leitura': data_leitura,
            'created_at': created_at
        })
        connection.commit()
    
    cursor.close()
    connection.close()

def read_contagem_impressoras(impressora_id):
    """
    Lê os registros de contagem de impressoras do banco de dados.

    Args:
        impressora_id (int): O ID da impressora cujas contagens devem ser selecionadas.

    Returns:
        list: Uma lista de registros de contagem de impressoras.

    Raises:
        Exception: Se ocorrer um erro ao ler os registros de contagem de impressoras.
    """
    connection = config.get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM contagem_impressora WHERE IMPRESSORA_ID = :impressora_id"
    cursor.execute(select_query, {'impressora_id': impressora_id})
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result

def update_contagem_impressora(impressora_id, contador_pb=None, contador_cor=None, contador_total=None, data_leitura=None):
    """
    Atualiza os registros de contagem de impressoras no banco de dados.

    Args:
        impressora_id (int): O ID da impressora associada à contagem.
        contador_pb (int, optional): O novo contador de impressões em preto e branco.
        contador_cor (int, optional): O novo contador de impressões coloridas.
        contador_total (int, optional): O novo contador total de impressões.
        data_leitura (datetime, optional): A nova data e hora da leitura do contador.

    Raises:
        Exception: Se ocorrer um erro ao atualizar os registros de contagem de impressoras.
    """
    connection = config.get_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE contagem_impressora
    SET CONTADOR_PB = :contador_pb,
        CONTADOR_COR = :contador_cor,
        CONTADOR_TOTAL = :contador_total,
        DATA_LEITURA = :data_leitura
    WHERE IMPRESSORA_ID = :impressora_id
    """
    cursor.execute(update_query, {
        'impressora_id': impressora_id,
        'contador_pb': contador_pb,
        'contador_cor': contador_cor,
        'contador_total': contador_total,
        'data_leitura': data_leitura
    })

    connection.commit()
    cursor.close()
    connection.close()

def delete_contagem_impressora(impressora_id):
    """
    Exclui os registros de contagem de impressoras do banco de dados.

    Args:
        impressora_id (int): O ID da impressora cujos registros de contagem devem ser excluídos.

    Raises:
        Exception: Se ocorrer um erro ao excluir os registros de contagem de impressoras.
    """
    connection = config.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM contagem_impressora WHERE IMPRESSORA_ID = :impressora_id"
    cursor.execute(delete_query, {'impressora_id': impressora_id})

    connection.commit()
    cursor.close()
    connection.close()

def delete_all_registros():
    """
    Exclui todos os registros de contagem de impressoras do banco de dados.

    Raises:
        Exception: Se ocorrer um erro ao excluir todos os registros de contagem de impressoras.
    """
    connection = config.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM contagem_impressora"
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()

def delete_all_impressoras():
    """
    Exclui todas as impressoras do banco de dados.

    Raises:
        Exception: Se ocorrer um erro ao excluir todas as impressoras.
    """
    connection = config.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM impressora"
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()

def read_impressoras_data(data):
    """
    Lê os registros de contagem de impressoras do banco de dados para uma determinada data.

    Args:
        data (str): Data da leitura no formato 'dd-mm-YYYY'.

    Returns:
        list: Uma lista de registros de contagem de impressoras para a data especificada.

    Raises:
        Exception: Se ocorrer um erro ao ler os registros de contagem de impressoras para a data especificada.
    """
    # Transforma a data do formato 'dd-mm-YYYY' para 'YYYY-mm-dd'
    data = datetime.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
    
    connection = config.get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM contagem_impressora WHERE TO_CHAR(DATA_LEITURA, 'YYYY-MM-DD') = :data"
    cursor.execute(select_query, {'data': data})
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def read_all_record_data():
    """
    Lê todos os registros da tabela contagem_impressora do banco de dados para a última data de leitura.

    Returns:
        list: Uma lista de todos os registros da tabela contagem_impressora para a última data de leitura.

    Raises:
        Exception: Se ocorrer um erro ao ler todos os registros da tabela contagem_impressora.
    """
    connection = config.get_connection()
    cursor = connection.cursor()

    select_query = """
    SELECT * 
    FROM contagem_impressora
    WHERE DATA_LEITURA = (SELECT MAX(DATA_LEITURA) FROM contagem_impressora)
    """
    cursor.execute(select_query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def read_all_impressoras():
    """
    Lê todos os registros da tabela contagem_impressora do banco de dados.

    Returns:
        list: Uma lista de todos os registros da tabela contagem_impressora.

    Raises:
        Exception: Se ocorrer
