from app import database
from datetime import datetime

def create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER):
    """
    Cria uma nova impressora no banco de dados.

    Args:
        PRINTERDEVICEID (str): ID do dispositivo da impressora.
        PRINTERBRANDNAME (str): Nome da marca da impressora.
        PRINTERMODELNAME (str): Nome do modelo da impressora.
        SERIALNUMBER (str): Número de série da impressora.

    Returns:
        bool: True se a impressora foi criada com sucesso, False se a impressora já existe.
    """
    connection = database.get_connection()
    cursor = connection.cursor()
    
    # Verificar se a impressora já existe no banco de dados
    select_query = "SELECT COUNT(*) FROM impressora WHERE PRINTERDEVICEID = :printerdeviceid"
    cursor.execute(select_query, {'printerdeviceid': PRINTERDEVICEID})
    count = cursor.fetchone()[0]
    
    if count > 0:
        # Impressora já existe no banco de dados
        print("Impressora já existe no banco de dados.")
        return False

    created_at = datetime.now()
    status = 1
    
    # Inserir nova impressora no banco de dados
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

    # Commit e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()
    return True

def create_contagem_impressoras(impressora_id, contador_pb, contador_cor, data_leitura):
    """
    Registra uma contagem de impressoras no banco de dados.

    Args:
        impressora_id (int): ID da impressora.
        contador_pb (int): Contador de páginas preto e branco.
        contador_cor (int): Contador de páginas coloridas.
        data_leitura (datetime): Data da leitura do contador.
    """
    connection = database.get_connection()
    cursor = connection.cursor()
    
    contador_total = contador_pb + contador_cor
    created_at = datetime.now()
    
    # Verifica se já existe um registro com os mesmos valores de IMPRESSORA_ID e DATA_LEITURA
    select_query = """
    SELECT COUNT(*)
    FROM contagem_impressora
    WHERE IMPRESSORA_ID = :impressora_id
    AND DATA_LEITURA = :data_leitura
    """
    cursor.execute(select_query, {'impressora_id': impressora_id, 'data_leitura': data_leitura})
    count = cursor.fetchone()[0]
    
    if count == 0:  # Se não houver registros, insere um novo
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
        # Commit e fechamento da conexão
        connection.commit()
    
    cursor.close()
    connection.close()

def read_contagem_impressoras(impressora_id):
    """
    Lê os registros de contagem de impressoras do banco de dados.

    Args:
        impressora_id (int): ID da impressora.

    Returns:
        tuple: Registro de contagem da impressora.
    """
    connection = database.get_connection()
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
        impressora_id (int): ID da impressora.
        contador_pb (int, optional): Novo contador de páginas preto e branco.
        contador_cor (int, optional): Novo contador de páginas coloridas.
        contador_total (int, optional): Novo contador total de páginas.
        data_leitura (datetime, optional): Nova data de leitura do contador.
    """
    connection = database.get_connection()
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

    # Commit e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()

def delete_contagem_impressora(impressora_id):
    """
    Exclui os registros de contagem de impressoras do banco de dados.

    Args:
        impressora_id (int): ID da impressora.
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM contagem_impressoras WHERE IMPRESSORA_ID = :impressora_id"
    cursor.execute(delete_query, {'impressora_id': impressora_id})

    # Commit e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()

def delete_all_registros():
    """
    Exclui todos os registros de contagem de impressoras do banco de dados.
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM contagem_impressora"
    cursor.execute(delete_query)

    # Commit e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()

def delete_all_impressoras():
    """
    Exclui todas as impressoras do banco de dados.
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM impressora"
    cursor.execute(delete_query)

    # Commit e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()

def read_impressoras_data(data):
    """
    Lê os registros de contagem de impressoras do banco de dados para uma determinada data.

    Args:
        data (datetime): Data de leitura do contador.

    Returns:
        list: Lista de registros de contagem de impressoras para a data especificada.
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM contagem_impressora WHERE DATA_LEITURA = :data"
    cursor.execute(select_query, {'data': data})
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results
