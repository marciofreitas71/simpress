from app import database
from datetime import datetime

def create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER):
    
    """
    Cria uma nova impressora no banco de dados.

    Args:
        PRINTERDEVICEID (str): O ID da impressora.
        PRINTERBRANDNAME (str): O nome da marca da impressora.
        PRINTERMODELNAME (str): O nome do modelo da impressora.
        SERIALNUMBER (str): O número de série da impressora.

    Returns:
        bool: True se a impressora for criada com sucesso, False se ela já existir no banco de dados.

    Esta função cria uma nova entrada na tabela 'impressora' no banco de dados, utilizando os valores
    fornecidos para PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME e SERIALNUMBER. Se a impressora
    já existir no banco de dados, a função imprime uma mensagem informando que a impressora já existe
    e retorna False. Caso contrário, a impressora é inserida no banco de dados e a função retorna True.

    Exemplo:
    >>> create_impressora('123456', 'Epson', 'EcoTank L3150', 'ABC123')
    True
    """

    connection = database.get_connection()
    cursor = connection.cursor()
    
    # Verificar se a impressora já existe no banco de dados
    select_query = """
    SELECT COUNT(*) FROM impressora WHERE PRINTERDEVICEID = :printerdeviceid
    """
    cursor.execute(select_query, {'printerdeviceid': PRINTERDEVICEID})
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("Impressora já existe no banco de dados.")
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
        impressora_id (int): O ID da impressora.
        contador_pb (int): O contador de impressões em preto e branco.
        contador_cor (int): O contador de impressões coloridas.
        data_leitura (datetime): A data e hora da leitura do contador.

    Esta função registra uma contagem de impressoras no banco de dados. Se não houver registros 
    com os mesmos valores de IMPRESSORA_ID e DATA_LEITURA, um novo registro é inserido na tabela 
    'contagem_impressora' com os valores fornecidos. Se já existir um registro com os mesmos 
    valores, nenhum novo registro é inserido.

    Exemplo:
    >>> create_contagem_impressoras(123, 100, 50, datetime.now())
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
        impressora_id (int): O ID da impressora para a qual se deseja ler os registros.

    Returns:
        tuple: Uma tupla contendo os dados do registro de contagem de impressoras correspondente
               ao IMPRESSORA_ID fornecido. Se não houver registros correspondentes, retorna None.

    Esta função lê os registros de contagem de impressoras do banco de dados para uma determinada
    impressora, identificada pelo seu IMPRESSORA_ID. Os registros são retornados como uma tupla,
    onde cada elemento representa uma coluna na tabela 'contagem_impressora'. Se não houver registros
    correspondentes, a função retorna None.

    Exemplo:
    >>> read_contagem_impressoras(123)
    (1, 123, 100, 50, 150, '2024-05-09 15:30:00', '2024-05-09 15:30:00')
    """
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
    """
    Atualiza os registros de contagem de impressoras no banco de dados.

    Args:
        impressora_id (int): O ID da impressora para a qual se deseja atualizar os registros.
        contador_pb (int, optional): O novo valor do contador de impressões em preto e branco.
        contador_cor (int, optional): O novo valor do contador de impressões coloridas.
        contador_total (int, optional): O novo valor do contador total de impressões.
        data_leitura (datetime, optional): A nova data e hora da leitura do contador.

    Esta função atualiza os registros de contagem de impressoras no banco de dados para uma determinada
    impressora, identificada pelo seu IMPRESSORA_ID. Os registros são atualizados de acordo com os novos
    valores fornecidos para os parâmetros opcionais. Se algum parâmetro for None, o valor correspondente
    na tabela 'contagem_impressora' não será alterado.

    Exemplo:
    >>> update_contagem_impressora(123, contador_pb=150, contador_cor=75)
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

    connection.commit()
    cursor.close()
    connection.close()

def delete_contagem_impressora(impressora_id):
    """
    Exclui os registros de contagem de impressoras do banco de dados.

    Args:
        impressora_id (int): O ID da impressora para a qual se deseja excluir os registros.

    Esta função exclui os registros de contagem de impressoras do banco de dados para uma determinada
    impressora, identificada pelo seu IMPRESSORA_ID. Todos os registros associados à impressora são
    removidos da tabela 'contagem_impressora'.

    Exemplo:
    >>> delete_contagem_impressora(123)
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = """
    DELETE FROM contagem_impressoras WHERE IMPRESSORA_ID = :impressora_id
    """
    cursor.execute(delete_query, {'impressora_id': impressora_id})

    connection.commit()
    cursor.close()
    connection.close()

def delete_all_registros():
    """
    Exclui todos os registros de contagem de impressoras do banco de dados.

    Esta função exclui todos os registros de contagem de impressoras da tabela 'contagem_impressora'.
    Todos os registros presentes na tabela são removidos permanentemente.

    Exemplo:
    >>> delete_all_registros()
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = """
    DELETE FROM contagem_impressora
    """
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()


def delete_all_impressoras():
    """
    Exclui todas as impressoras do banco de dados.

    Esta função exclui todas as impressoras da tabela 'impressora'.
    Todos os registros de impressoras presentes na tabela são removidos permanentemente.

    Exemplo:
    >>> delete_all_impressoras()
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    delete_query = """
    DELETE FROM impressora
    """
    cursor.execute(delete_query)

    connection.commit()
    cursor.close()
    connection.close()

