import sys
import os

# Adiciona o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


"""
Este módulo contém consultas SQL para operações CRUD no banco de dados.

Consultas:
- SELECT_CONTAGEM_IMPRESSORAS: Consulta para selecionar todas as contagens de impressoras associadas a uma impressora específica.
- INSERT_IMPRESSORA: Consulta para inserir uma nova impressora no banco de dados.
- SELECT_IMPRESSORA: Consulta para selecionar uma impressora com base no ID do dispositivo da impressora.
- UPDATE_IMPRESSORA: Consulta para atualizar os detalhes de uma impressora no banco de dados.
- DELETE_IMPRESSORA: Consulta para excluir uma impressora do banco de dados com base no ID do dispositivo da impressora.
"""

# Consulta para selecionar todas as contagens de impressoras associadas a uma impressora específica.
# Parâmetros:
# - impressora_id (int): O ID da impressora cujas contagens devem ser selecionadas.
# Retorna:
# - Um conjunto de resultados contendo todas as contagens associadas à impressora especificada.
SELECT_CONTAGEM_IMPRESSORAS = """
SELECT * FROM contagem_impressoras WHERE IMPRESSORA_ID = :impressora_id
"""

# Consulta para inserir uma nova impressora no banco de dados.
# Parâmetros:
# - printer_device_id (str): O ID do dispositivo da impressora.
# - brand_name (str): O nome da marca da impressora.
# - model_name (str): O nome do modelo da impressora.
# - serial_number (str): O número de série da impressora.
# - created_at (datetime): A data e hora de criação do registro.
# - status (int): O status da impressora.
# Efeito:
# - Insere um novo registro de impressora no banco de dados.
INSERT_IMPRESSORA = """
INSERT INTO impressoras (PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)
VALUES (:printer_device_id, :brand_name, :model_name, :serial_number, :created_at, :status)
"""

# Consulta para selecionar uma impressora com base no ID do dispositivo da impressora.
# Parâmetros:
# - printer_device_id (str): O ID do dispositivo da impressora a ser selecionada.
# Retorna:
# - Um conjunto de resultados contendo os detalhes da impressora especificada.
SELECT_IMPRESSORA = """
SELECT * FROM impressoras WHERE PRINTERDEVICEID = :printer_device_id
"""

# Consulta para atualizar os detalhes de uma impressora no banco de dados.
# Parâmetros:
# - printer_device_id (str): O ID do dispositivo da impressora a ser atualizada.
# - brand_name (str): O novo nome da marca da impressora.
# - model_name (str): O novo nome do modelo da impressora.
# - serial_number (str): O novo número de série da impressora.
# - created_at (datetime): A nova data e hora de criação do registro.
# - status (int): O novo status da impressora.
# Efeito:
# - Atualiza os detalhes da impressora especificada no banco de dados.
UPDATE_IMPRESSORA = """
UPDATE impressoras
SET PRINTERBRANDNAME = :brand_name,
    PRINTERMODELNAME = :model_name,
    SERIALNUMBER = :serial_number,
    CREATED_AT = :created_at,
    STATUS = :status
WHERE PRINTERDEVICEID = :printer_device_id
"""

# Consulta para excluir uma impressora do banco de dados com base no ID do dispositivo da impressora.
# Parâmetros:
# - printer_device_id (str): O ID do dispositivo da impressora a ser excluída.
# Efeito:
# - Remove o registro da impressora especificada do banco de dados.
DELETE_IMPRESSORA = """
DELETE FROM impressoras WHERE PRINTERDEVICEID = :printer_device_id
"""

# Consulta para recuperar a última data de leitura no banco de dados.
# Retorna:
# - A data e hora do último registro no banco de dados.
SELECT_LAST_READING_DATE = """
SELECT MAX(DATA_LEITURA) FROM contagem_impressoras
"""

