"""
Este módulo contém consultas SQL para operações CRUD no banco de dados.

Consultas:
- SELECT_CONTAGEM_IMPRESSORAS: Consulta para selecionar todas as contagens de impressoras associadas a uma impressora específica.
- INSERT_IMPRESSORA: Consulta para inserir uma nova impressora no banco de dados.
- SELECT_IMPRESSORA: Consulta para selecionar uma impressora com base no ID do dispositivo da impressora.
- UPDATE_IMPRESSORA: Consulta para atualizar os detalhes de uma impressora no banco de dados.
- DELETE_IMPRESSORA: Consulta para excluir uma impressora do banco de dados com base no ID do dispositivo da impressora.
"""

SELECT_CONTAGEM_IMPRESSORAS = """
SELECT * FROM contagem_impressoras WHERE IMPRESSORA_ID = :impressora_id
"""

INSERT_IMPRESSORA = """
INSERT INTO impressoras (PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)
VALUES (:printer_device_id, :brand_name, :model_name, :serial_number, :created_at, :status)
"""

SELECT_IMPRESSORA = """
SELECT * FROM impressoras WHERE PRINTERDEVICEID = :printer_device_id
"""

UPDATE_IMPRESSORA = """
UPDATE impressoras
SET PRINTERBRANDNAME = :brand_name,
    PRINTERMODELNAME = :model_name,
    SERIALNUMBER = :serial_number,
    CREATED_AT = :created_at,
    STATUS = :status
WHERE PRINTERDEVICEID = :printer_device_id
"""

DELETE_IMPRESSORA = """
DELETE FROM impressoras WHERE PRINTERDEVICEID = :printer_device_id
"""
