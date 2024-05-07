from app import database

def create_contagem_impressoras(impressora_id, contador_pb, contador_cor, contador_total, data_leitura, created_at):
    connection = database.get_connection()
    cursor = connection.cursor()

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
    connection = database.get_connection()
    cursor = connection.cursor()

    select_query = """
    SELECT * FROM contagem_impressora WHERE IMPRESSORA_ID = :impressora_id
    """
    cursor.execute(select_query, {'impressora_id': impressora_id})
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result

def update_contagem_impressora(impressora_id, contador_pb=None, contador_cor=None, contador_total=None, data_leitura=None):
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

    connection.commit()
    cursor.close()
    connection.close()

def delete_contagem_impressora(impressora_id):
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = """
    DELETE FROM contagem_impressora WHERE IMPRESSORA_ID = :impressora_id
    """
    cursor.execute(delete_query, {'impressora_id': impressora_id})

    connection.commit()
    cursor.close()
    connection.close()
