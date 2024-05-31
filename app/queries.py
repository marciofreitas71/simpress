# Consulta para selecionar todas as contagens de impressoras associadas a uma impressora específica
SELECT_CONTAGEM_IMPRESSORAS = """
SELECT * FROM contagem_impressoras WHERE IMPRESSORA_ID = :impressora_id
"""

# Consulta para inserir uma nova impressora no banco de dados
INSERT_IMPRESSORA = """
INSERT INTO impressoras (PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)
VALUES (:printer_device_id, :brand_name, :model_name, :serial_number, :created_at, :status)
"""

# Consulta para selecionar uma impressora com base no ID do dispositivo da impressora
SELECT_IMPRESSORA = """
SELECT * FROM impressoras WHERE PRINTERDEVICEID = :printer_device_id
"""

# Consulta para atualizar os detalhes de uma impressora no banco de dados
UPDATE_IMPRESSORA = """
UPDATE impressoras
SET PRINTERBRANDNAME = :brand_name,
    PRINTERMODELNAME = :model_name,
    SERIALNUMBER = :serial_number,
    CREATED_AT = :created_at,
    STATUS = :status
WHERE PRINTERDEVICEID = :printer_device_id
"""

# Consulta para excluir uma impressora do banco de dados com base no ID do dispositivo da impressora
DELETE_IMPRESSORA = """
DELETE FROM impressoras WHERE PRINTERDEVICEID = :printer_device_id
"""
