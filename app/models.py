"""
Este módulo define classes que representam os modelos de dados do banco de dados.

Classes:
- ContagemImpressoras: Representa uma contagem de impressoras.
- Impressoras: Representa uma impressora.
"""

class ContagemImpressoras:
    """
    Representa uma contagem de impressoras.

    Attributes:
        ID (int): O ID da contagem.
        IMPRESSORA_ID (int): O ID da impressora associada à contagem.
        CONTADOR_PB (int): O contador de impressões em preto e branco.
        CONTADOR_COR (int): O contador de impressões coloridas.
        CONTADOR_TOTAL (int): O contador total de impressões.
        DATA_LEITURA (datetime): A data e hora da leitura do contador.
        CREATED_AT (datetime): A data e hora de criação do registro.
    """
    def __init__(self, ID: int, IMPRESSORA_ID: int, CONTADOR_PB: int, CONTADOR_COR: int, CONTADOR_TOTAL: int, DATA_LEITURA, CREATED_AT):
        """
        Inicializa uma nova instância da classe ContagemImpressoras.

        Args:
            ID (int): O ID da contagem.
            IMPRESSORA_ID (int): O ID da impressora associada à contagem.
            CONTADOR_PB (int): O contador de impressões em preto e branco.
            CONTADOR_COR (int): O contador de impressões coloridas.
            CONTADOR_TOTAL (int): O contador total de impressões.
            DATA_LEITURA (datetime): A data e hora da leitura do contador.
            CREATED_AT (datetime): A data e hora de criação do registro.
        """
        self.ID = ID
        self.IMPRESSORA_ID = IMPRESSORA_ID
        self.CONTADOR_PB = CONTADOR_PB
        self.CONTADOR_COR = CONTADOR_COR
        self.CONTADOR_TOTAL = CONTADOR_TOTAL
        self.DATA_LEITURA = DATA_LEITURA
        self.CREATED_AT = CREATED_AT

class Impressoras:
    """
    Representa uma impressora.

    Attributes:
        ID (int): O ID da impressora.
        PRINTERDEVICEID (str): O ID do dispositivo da impressora.
        PRINTERBRANDNAME (str): O nome da marca da impressora.
        PRINTERMODELNAME (str): O nome do modelo da impressora.
        SERIALNUMBER (str): O número de série da impressora.
        CREATED_AT (datetime): A data e hora de criação do registro.
        STATUS (int): O status da impressora.
    """
    def __init__(self, ID: int, PRINTERDEVICEID: str, PRINTERBRANDNAME: str, PRINTERMODELNAME: str, SERIALNUMBER: str, CREATED_AT, STATUS: int):
        """
        Inicializa uma nova instância da classe Impressoras.

        Args:
            ID (int): O ID da impressora.
            PRINTERDEVICEID (str): O ID do dispositivo da impressora.
            PRINTERBRANDNAME (str): O nome da marca da impressora.
            PRINTERMODELNAME (str): O nome do modelo da impressora.
            SERIALNUMBER (str): O número de série da impressora.
            CREATED_AT (datetime): A data e hora de criação do registro.
            STATUS (int): O status da impressora.
        """
        self.ID = ID
        self.PRINTERDEVICEID = PRINTERDEVICEID
        self.PRINTERBRANDNAME = PRINTERBRANDNAME
        self.PRINTERMODELNAME = PRINTERMODELNAME
        self.SERIALNUMBER = SERIALNUMBER
        self.CREATED_AT = CREATED_AT
        self.STATUS = STATUS
