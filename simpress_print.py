from datetime import datetime
import zeep
import pandas as pd
import repository_gestao_impressoras as repo
import config
from dotenv import load_dotenv

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

def recuperar_dados_webservice(wsdl_url, service_method, payload):
    # Create a SOAP client using the WSDL URL
    client = zeep.Client(wsdl=wsdl_url)

    # Access the service method and send the request with the payload
    service = client.service
    method_to_call = getattr(service, service_method)
    response = method_to_call(**payload)
    
    # Parse the response string into Python objects
    df = pd.read_json(response)
    #print(df)
    return df
   
    # df3 = pd.merge(df_remoto, df_local, on='SERIALNUMBER', how='outer')
def inserir_contagem_impressoras(df_remoto):
    df_remoto = df_remoto.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
    df_remoto.columns = df_remoto.columns.str.upper()
    df_remoto = df_remoto[['SERIALNUMBER', 'DATA_LEITURA', 'CONTADOR_PB', 'CONTADOR_COR']]
    df_remoto['CONTADOR_TOTAL'] = df_remoto['CONTADOR_PB'] + df_remoto['CONTADOR_COR']
    # print(df_remoto)
    df_local = repo.recuperarDadosLocaisImpressoras()
    df_remoto = df_remoto.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
       
    print("Dados do banco local")
    print(df_local)
    print()
    print("Dados do banco remoto")
    print(df_remoto)

# Dados api
wsdl_url = config.wsdl_url
service_method = config.service_method
output_csv = config.output_csv
payload = config.payload

#insert_printer('output-reference-2023-10-17.csv', 'HP')
#send_soap_request_and_write_to_csv(wsdl_url, service_method, output_csv, payload)
df_remoto = recuperar_dados_webservice(wsdl_url, service_method, payload)

# dfContagem = inserir_contagem_impressoras(dfContagem)
df_local = repo.recuperarDadosLocaisImpressoras()

inserir_contagem_impressoras(df_remoto)