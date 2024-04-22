from datetime import datetime, timedelta
import zeep
import pandas as pd
import repository_gestao_impressoras as repo
import config as config
from dotenv import load_dotenv
import logging

load_dotenv()

def send_soap_request_and_write_to_csv(wsdl_url, service_method, output_csv, payload):
    # Create a SOAP client using the WSDL URL
    client = zeep.Client(wsdl=wsdl_url)

    # Access the service method and send the request with the payload
    service = client.service
    method_to_call = getattr(service, service_method)
    response = method_to_call(**payload)
    
    # Parse the response string into Python objects
    df = pd.read_json(response)
    print(df)
    df.to_csv(output_csv, sep=';', index=False)

def carregar_dados_excel(url, sheet):
    tables = pd.read_excel(url, sheet_name=sheet)
    return tables

def carregar_dados_csv(url):
    tables = pd.read_csv(url, delimiter=';')
    return tables

def insert_printer(input_csv, brand_name):
    df = carregar_dados_csv(input_csv)
    df = df[['PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]
    df = df[df['BrandName'] == brand_name].sort_values(by=['SerialNumber'])
    df = df.rename(columns={"BrandName" : "PRINTERBRANDNAME"})
    df['created_at'] = datetime.now()
    df['status'] = 1
    df = df.fillna(0)
    df.columns = df.columns.str.upper()
    print(df)

    repo.cadastrarDadosImpressoras(df)

def recuperar_dados_webservice(wsdl_url, service_method, payload, dateTimeEnd, timeout=5):
    logging.info("Executando a função recuperar_dados_webservice... ")

    # Atualize o payload com a nova dateTimeEnd
    payload['dateTimeEnd'] = dateTimeEnd

    try:
        # Criar um cliente SOAP usando a URL do WSDL com timeout
        client = zeep.Client(wsdl=wsdl_url, transport=zeep.Transport(timeout=timeout))
        logging.info("Criado um cliente SOAP usando a URL do WSDL com timeout")

        # Acessar o método do serviço e enviar a solicitação com os dados
        service = client.service
        method_to_call = getattr(service, service_method)
        response = method_to_call(**payload)
        logging.info("Acessar o método do serviço e enviar a solicitação com os dados")

        # Analisar a string de resposta em objetos Python
        df = pd.read_json(response)
        return df
    except zeep.exceptions.Fault as e:
        logging.error(f"Erro durante a execução da função: {str(e)}")
        # Você pode decidir levantar a exceção novamente ou retornar um valor padrão, dependendo do caso.
        raise
    except zeep.exceptions.TransportError as e:
        logging.error(f"Erro de transporte durante a execução da função: {str(e)}")
        # Trate o erro de transporte conforme necessário
        raise
   
    # df3 = pd.merge(df_remoto, df_local, on='SERIALNUMBER', how='outer')
def inserir_contagem_impressoras(df_remoto):
    df_remoto = df_remoto.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
    df_remoto.columns = df_remoto.columns.str.upper()
    df_remoto['CONTADOR_TOTAL'] = df_remoto['CONTADOR_PB'] + df_remoto['CONTADOR_COR']
    
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

    # Armazena a data atual
    data_atual = datetime.strptime(dateTimeEnd, "%Y-%m-%d %H:%M:%S")

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
            print(data_anterior)
                        
        #     # Verifica se há valores zero em 'ReferenceMono' ou 'ReferenceColor'
        #     registros_zerados = df_remoto[(df_remoto['ReferenceMono'] == 0) | (df_remoto['ReferenceColor'] == 0)].shape[0]
            
        #     # Imprime o número de registros com valores zerados
        #     print("Número de registros com valores zerados:", registros_zerados)

            

    
        

    # # Converter a data anterior para o formato desejado
    # data_anterior_formatada = data_anterior.strftime('%Y-%m-%d 02:00:00')

    # print(data_anterior_formatada)

     

if __name__ == "__main__":
    
   transforma_df_remoto()