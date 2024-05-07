from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date  # Importa o tipo Date
from sqlalchemy.ext.declarative import declarative_base  # Importa a função declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class ContagemImpressoras(Base):
    __tablename__ = 'contagem_impressoras'

    ID = Column(Integer, primary_key=True)
    IMPRESSORA_ID = Column(Integer, ForeignKey('impressoras.PRINTERDEVICEID'))
    CONTADOR_PB = Column(Integer)
    CONTADOR_COR = Column(Integer)
    CONTADOR_TOTAL = Column(Integer)
    DATA_LEITURA = Column(DateTime)
    CREATED_AT = Column(DateTime)

class Impressoras(Base):
    __tablename__ = 'impressoras'

    ID = Column(Integer, primary_key=True)
    PRINTERDEVICEID = Column(Integer)
    PRINTERBRANDNAME = Column(String)
    PRINTERMODELNAME = Column(String)
    SERIALNUMBER = Column(String)
    CREATED_AT = Column(DateTime)  # Corrigido para DateTime
    STATUS = Column(String)

    contagem_impressoras = relationship("ContagemImpressoras", backref="impressoras")