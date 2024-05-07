# Aqui você pode definir todas as consultas SQL utilizadas pela aplicação
# por exemplo:
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
