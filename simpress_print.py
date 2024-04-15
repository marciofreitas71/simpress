from datetime import datetime
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

def recuperar_dados_webservice(wsdl_url, service_method, payload, timeout=5):
    logging.info("Executando a função recuperar_dados_webservice... ")

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
    
       
    # print(df_local)
    # print()
    # print("Dados do banco remoto")
    print(df_remoto)
    df_remoto.to_csv("df_remoto.csv")


    # Iterando sobre o DF_REMOTO até achar uma impressora com dados zerados
    for index, row in df_remoto.iterrows():
        if (row["CONTADOR_PB"] or row["CONTADOR_COR"]) == 0:
            print(row["DATA_LEITURA"], row["PRINTERDEVICEID"], row["PRINTERMODELNAME"], row["CONTADOR_PB"], row["CONTADOR_COR"],)
     

if __name__ == "__main__":
    
    wsdl_url = config.wsdl_url
    service_method = config.service_method
    output_csv = config.output_csv
    payload = config.payload

    df_remoto = recuperar_dados_webservice(wsdl_url, service_method, payload, timeout=5)
    df_local = repo.recuperarDadosLocaisImpressoras()

    inserir_contagem_impressoras(df_remoto)