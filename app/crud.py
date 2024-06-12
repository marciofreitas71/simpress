import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import pandas as pd
from app import config
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
- read_all_records(): Lê todos os registros da tabela contagem_impressora do banco de dados.
"""

def create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER):
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
    connection = config.get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM contagem_impressora WHERE IMPRESSORA_ID = :impressora_id"
    cursor.execute(select_query, {'impressora_id': impressora_id})
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result

def update_contagem_impressora(impressora_id, contador_pb=None, contador_cor=None, contador_total=None, data_leitura=None):
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
    connection = config.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM contagem_impressora WHERE IMPRESSORA_ID = :impressora_id"
    cursor.execute(delete_query, {'impressora_id': impressora_id})

    connection.commit()
    cursor.close()
    connection.close()

def delete_all_registros():
    connection = config.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM contagem_impressora"
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()

def delete_all_impressoras():
    connection = config.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM impressora"
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()

def read_impressoras_data(data):
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
    connection = config.get_connection()
    cursor = connection.cursor()

    select_query = """
    SELECT * 
    FROM contagem_impressora
    WHERE DATA_LEITURA = (SELECT MAX(REALDATACAPTURE) FROM contagem_impressora)
    """
    cursor.execute(select_query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def read_all_impressoras():
    connection = config.get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM contagem_impressora"
    cursor.execute(select_query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def obter_registros_ultima_data():
    # Primeiro, obtenha a maior data_leitura
    connection = config.get_connection()
    cursor = connection.cursor()

    query_max_date = "SELECT MAX(DATA_LEITURA) FROM contagem_impressora"
    cursor.execute(query_max_date)
    ultima_data = cursor.fetchone()[0]

    if ultima_data is None:
        cursor.close()
        connection.close()
        return []

    # Formate a data como string para uso na consulta
    ultima_data_str = ultima_data.strftime('%Y-%m-%d %H:%M:%S')

    # Em seguida, obtenha todos os registros com essa data_leitura
    query_records = f"SELECT * FROM contagem_impressora WHERE DATA_LEITURA = TO_DATE('{ultima_data_str}', 'YYYY-MM-DD HH24:MI:SS')"
    cursor.execute(query_records)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def obter_ultima_data_bd():
    connection = config.get_connection()
    cursor = connection.cursor()

    query_max_date = "SELECT MAX(DATA_LEITURA) FROM contagem_impressora"
    cursor.execute(query_max_date)
    ultima_data = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return ultima_data

if __name__ == '__main__':
    pass
    print(obter_ultima_data_bd())
    # print(read_all_record_data())
    # print(obter_registros_ultima_data())
