from app.database import create_database, getConnection
from app.models import Base, ContagemImpressoras, Impressoras
from app.crud import CRUD
from datetime import datetime, timedelta
import pandas as pd
import config as config
import repository_gestao_impressoras as repo
import os

  
def transforma_dados_webservice():
    
    # Definição da data
    dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"
 
    # Chame a função recuperar_dados_webservice() com dateTimeEnd como argumento adicional
    dados_webservice = repo.recuperar_dados_webservice(wsdl_url, service_method, payload, timeout=5)
    dados_webservice.to_csv(f'arquivos/dados_webservice.csv')

    # Armazena a data final
    data_final = datetime.strptime('2024-04-24 02:00:00', '%Y-%m-%d %H:%M:%S')

    # Inicializa dados_dia_anterior como None
    dados_dia_anterior = None

    # Armazena a data do dia anterior
    data_anterior = data_final - timedelta(days=1)

    # Continua buscando em dias anteriores até que os valores sejam preenchidos
    while dados_dia_anterior is None or dados_dia_anterior[(dados_dia_anterior['ReferenceMono'] == 0) | (dados_dia_anterior['ReferenceColor'] == 0)].any(axis=None):        
        print(f'----------------------------------------------------')
        print(f'Pesquisando em {data_anterior}...')
        print(f'----------------------------------------------------')
        
        # Verifica se dados_dia_anterior já foi buscado, se não, busca
        dados_dia_anterior = repo.recuperar_dados_webservice(data_anterior.strftime("%Y-%m-%d %H:%M:%S"))

        # Substituição dos valores no dataframe
        for index, row in dados_webservice[(dados_webservice['ReferenceMono'] == 0) | (dados_webservice['ReferenceColor'] == 0)].iterrows():
            PrinterDeviceID = row['PrinterDeviceID']
            ReferenceMono = row['ReferenceMono']
            ReferenceColor = row['ReferenceColor']
  
            # Verifica se o valor de ReferenceMono é igual a 0
            if ReferenceMono == 0:
                # Busca a impressora no dados_dia_anterior
                printer_data = dados_dia_anterior[dados_dia_anterior['PrinterDeviceID'] == PrinterDeviceID]
                if not printer_data.empty:
                    # Obtém o valor de ReferenceMono do registro correspondente no dia anterior
                    ReferenceMono_anterior = printer_data.iloc[0]['ReferenceMono']
                    # Se o valor for diferente de 0, substitui
                    if ReferenceMono_anterior != 0:
                        dados_webservice.at[index, 'ReferenceMono'] = ReferenceMono_anterior
                        print("O valor da impressão em preto e branco foi substituido")
                        print(f'Valor anterior: {PrinterDeviceID}')
                        print(f'Valor atual: {ReferenceMono_anterior}')

            # Verifica se o valor de ReferenceColor é igual a 0
            if ReferenceColor == 0:
                # Busca a impressora no dados_dia_anterior
                printer_data = dados_dia_anterior[dados_dia_anterior['PrinterDeviceID'] == PrinterDeviceID]
                if not printer_data.empty:
                    # Obtém o valor de ReferenceColor do registro correspondente no dia anterior
                    ReferenceColor_anterior = printer_data.iloc[0]['ReferenceColor']
                    # Se o valor for diferente de 0, substitui
                    if ReferenceColor_anterior != 0:
                        dados_webservice.at[index, 'ReferenceColor'] = ReferenceColor_anterior                        
                        print(f'Valor anterior: {PrinterDeviceID}')
                        print(f'Valor atual: {ReferenceColor_anterior}')
            
            

        # Atualiza a data atual para o dia anterior se os valores ainda estiverem vazios
        if dados_webservice[(dados_webservice['ReferenceMono'] == 0) | (dados_webservice['ReferenceColor'] == 0)].any(axis=None):
            data_anterior -= timedelta(days=1)
            print()
                        
            # Supondo que data_anterior seja seu carimbo de data e hora
            formatted_timestamp = data_anterior.strftime("%Y-%m-%d_%H-%M-%S")
            dados_dia_anterior.to_csv(f"arquivos/dados_dia_anterior-{formatted_timestamp}.csv")
            print(f'Arquivo salvo com os dados do dia {(data_anterior).strftime('%d/%m/%Y')}')
            # Limpa o console
            os.system('cls')
                        
        
        #     # Verifica se há valores zero em 'ReferenceMono' ou 'ReferenceColor'
        #     registros_zerados = dados_webservice[(dados_webservice['ReferenceMono'] == 0) | (dados_webservice['ReferenceColor'] == 0)].shape[0]
            
        #     # Imprime o número de registros com valores zerados
        #     print("Número de registros com valores zerados:", registros_zerados)

            
    # # Converter a data anterior para o formato desejado
    # data_anterior_formatada = data_anterior.strftime('%Y-%m-%d 02:00:00')

    # print(data_anterior_formatada)


if __name__ == "__main__":
    
    wsdl_url = config.wsdl_url
    service_method = config.service_method
    payload = config.payload
    timeout = 5
    
      # Criar a instância CRUD
    crud = CRUD()

    # Criar o banco de dados, se ainda não existir
    crud.create_database()

    # Exemplo de uso do CRUD
    # Ler uma impressora pelo ID
    impressora_lida = crud.read_impressora(printer_device_id=1)
    if impressora_lida:
        print("Impressora encontrada:")
        print("ID:", impressora_lida.PRINTERDEVICEID)
        print("Marca:", impressora_lida.PRINTERBRANDNAME)
        print("Modelo:", impressora_lida.PRINTERMODELNAME)
        print("Número de Série:", impressora_lida.SERIALNUMBER)
        print("Status:", impressora_lida.STATUS)
    else:
        print("Impressora não encontrada.")