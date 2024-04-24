from datetime import datetime, timedelta
import zeep
import pandas as pd
import repository_gestao_impressoras as repo
import config as config
from dotenv import load_dotenv
import logging
import re
import os

load_dotenv()


    
def transforma_df_remoto():
    
    # Definindo as configurações
    dateTimeEnd = f"{datetime.now().strftime('%Y-%m-%d')} 02:00:00"
    wsdl_url = config.wsdl_url
    service_method = config.service_method
    output_csv = config.output_csv
    payload = config.payload
    timeout = 5

    # Chame a função recuperar_dados_webservice() com dateTimeEnd como argumento adicional
    df_remoto = recuperar_dados_webservice(wsdl_url, service_method, payload, dateTimeEnd, timeout=timeout)
    df_remoto.to_csv(f'arquivos/df_remoto.csv')

    # Armazena a data atual
    data_atual = datetime.strptime('2024-04-24 02:00:00', '%Y-%m-%d %H:%M:%S')

    # Inicializa df_remoto_2 como None
    df_remoto_2 = None

    # Armazena a data do dia anterior
    data_anterior = data_atual - timedelta(days=1)

    # Continua buscando em dias anteriores até que os valores sejam preenchidos
    while df_remoto_2 is None or df_remoto_2[(df_remoto_2['ReferenceMono'] == 0) | (df_remoto_2['ReferenceColor'] == 0)].any(axis=None):        
        print(f'----------------------------------------------------')
        print(f'Pesquisando em {data_anterior}...')
        print(f'----------------------------------------------------')
        
        # Verifica se df_remoto_2 já foi buscado, se não, busca
        df_remoto_2 = recuperar_dados_webservice(wsdl_url, service_method, payload, data_anterior.strftime("%Y-%m-%d %H:%M:%S"), timeout=timeout)

        # Substituição dos valores no dataframe
        for index, row in df_remoto[(df_remoto['ReferenceMono'] == 0) | (df_remoto['ReferenceColor'] == 0)].iterrows():
            PrinterDeviceID = row['PrinterDeviceID']
            ReferenceMono = row['ReferenceMono']
            ReferenceColor = row['ReferenceColor']
  
            # Verifica se o valor de ReferenceMono é igual a 0
            if ReferenceMono == 0:
                # Busca a impressora no df_remoto_2
                printer_data = df_remoto_2[df_remoto_2['PrinterDeviceID'] == PrinterDeviceID]
                if not printer_data.empty:
                    # Obtém o valor de ReferenceMono do registro correspondente no dia anterior
                    ReferenceMono_anterior = printer_data.iloc[0]['ReferenceMono']
                    # Se o valor for diferente de 0, substitui
                    if ReferenceMono_anterior != 0:
                        df_remoto.at[index, 'ReferenceMono'] = ReferenceMono_anterior
                        print("O valor da impressão em preto e branco foi substituido")
                        print(f'Valor anterior: {PrinterDeviceID}')
                        print(f'Valor atual: {ReferenceMono_anterior}')

            # Verifica se o valor de ReferenceColor é igual a 0
            if ReferenceColor == 0:
                # Busca a impressora no df_remoto_2
                printer_data = df_remoto_2[df_remoto_2['PrinterDeviceID'] == PrinterDeviceID]
                if not printer_data.empty:
                    # Obtém o valor de ReferenceColor do registro correspondente no dia anterior
                    ReferenceColor_anterior = printer_data.iloc[0]['ReferenceColor']
                    # Se o valor for diferente de 0, substitui
                    if ReferenceColor_anterior != 0:
                        df_remoto.at[index, 'ReferenceColor'] = ReferenceColor_anterior                        
                        print(f'Valor anterior: {PrinterDeviceID}')
                        print(f'Valor atual: {ReferenceColor_anterior}')
            
            

        # Atualiza a data atual para o dia anterior se os valores ainda estiverem vazios
        if df_remoto[(df_remoto['ReferenceMono'] == 0) | (df_remoto['ReferenceColor'] == 0)].any(axis=None):
            data_anterior -= timedelta(days=1)
            print()
                        
            # Supondo que data_anterior seja seu carimbo de data e hora
            formatted_timestamp = data_anterior.strftime("%Y-%m-%d_%H-%M-%S")
            df_remoto_2.to_csv(f"arquivos/df_remoto_2-{formatted_timestamp}.csv")
            print(f'Arquivo salvo com os dados do dia {(data_anterior).strftime('%d/%m/%Y')}')
            # Limpa o console
            os.system('cls')
                        
        
        #     # Verifica se há valores zero em 'ReferenceMono' ou 'ReferenceColor'
        #     registros_zerados = df_remoto[(df_remoto['ReferenceMono'] == 0) | (df_remoto['ReferenceColor'] == 0)].shape[0]
            
        #     # Imprime o número de registros com valores zerados
        #     print("Número de registros com valores zerados:", registros_zerados)

            
    # # Converter a data anterior para o formato desejado
    # data_anterior_formatada = data_anterior.strftime('%Y-%m-%d 02:00:00')

    # print(data_anterior_formatada)

     

if __name__ == "__main__":
    
   transforma_df_remoto()