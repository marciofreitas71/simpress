from sqlalchemy.orm import sessionmaker
from .models import Base, ContagemImpressoras, Impressoras
from .database import getConnection

class CRUD:
    def __init__(self):
        self.db_engine = getConnection()
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def create_database(self):
        engine = self.db_engine
        Base.metadata.create_all(engine)

    def create_contagem_impressoras(self, impressora_id, contador_pb, contador_cor, contador_total, data_leitura, created_at):
        contagem = ContagemImpressoras(IMPRESSORA_ID=impressora_id, CONTADOR_PB=contador_pb, CONTADOR_COR=contador_cor, CONTADOR_TOTAL=contador_total, DATA_LEITURA=data_leitura, CREATED_AT=created_at)
        self.session.add(contagem)
        self.session.commit()
        return contagem

    def create_impressora(self, printer_device_id, brand_name, model_name, serial_number, created_at, status):
        impressora = Impressoras(PRINTERDEVICEID=printer_device_id, PRINTERBRANDNAME=brand_name, PRINTERMODELNAME=model_name, SERIALNUMBER=serial_number, CREATED_AT=created_at, STATUS=status)
        self.session.add(impressora)
        self.session.commit()
        return impressora

    def read_contagem_impressoras(self, impressora_id):
        return self.session.query(ContagemImpressoras).filter_by(IMPRESSORA_ID=impressora_id).first()

    def read_impressora(self, printer_device_id):
        return self.session.query(Impressoras).filter_by(PRINTERDEVICEID=printer_device_id).first()

    def update_contagem_impressoras(self, impressora_id, contador_pb=None, contador_cor=None, contador_total=None, data_leitura=None):
        contagem = self.read_contagem_impressoras(impressora_id)
        if contagem:
            if contador_pb is not None:
                contagem.CONTADOR_PB = contador_pb
            if contador_cor is not None:
                contagem.CONTADOR_COR = contador_cor
            if contador_total is not None:
                contagem.CONTADOR_TOTAL = contador_total
            if data_leitura is not None:
                contagem.DATA_LEITURA = data_leitura
            self.session.commit()
        return contagem

    def update_impressora(self, printer_device_id, brand_name=None, model_name=None, serial_number=None, status=None):
        impressora = self.read_impressora(printer_device_id)
        if impressora:
            if brand_name is not None:
                impressora.PRINTERBRANDNAME = brand_name
            if model_name is not None:
                impressora.PRINTERMODELNAME = model_name
            if serial_number is not None:
                impressora.SERIALNUMBER = serial_number
            if status is not None:
                impressora.STATUS = status
            self.session.commit()
        return impressora

    def delete_contagem_impressoras(self, impressora_id):
        contagem = self.read_contagem_impressoras(impressora_id)
        if contagem:
            self.session.delete(contagem)
            self.session.commit()
        return contagem

    def delete_impressora(self, printer_device_id):
        impressora = self.read_impressora(printer_device_id)
        if impressora:
            self.session.delete(impressora)
            self.session.commit()
        return impressora
