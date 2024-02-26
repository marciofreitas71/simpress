from datetime import datetime
import zeep
import pandas as pd
import repository_gestao_impressoras as repo
import config
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
    # df_remoto = df_remoto[['SERIALNUMBER', 'DATA_LEITURA', 'CONTADOR_PB', 'CONTADOR_COR']]
    # df_remoto = df_remoto.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
    # df_local = repo.recuperarDadosLocaisImpressoras()
       
    # print("Dados do banco local")
    # print(df_local)
    print()
    # print("Dados do banco remoto")
    # print(df_remoto)
    # df_remoto.to_csv("dataframe_remoto.csv", sep=';')
    # df_zeros = df_remoto.loc[df_remoto['CONTADOR_TOTAL'] == 0]
    # print(df_zeros)

  
    # TODO criar iteração no dataframe para fazer a busca por valores iguais a zero.
    # ...


    df_remoto.sort_values(by='DATA_LEITURA', ascending=True, inplace=True)
    for index, row in df_remoto.iterrows():
        if row['CONTADOR_TOTAL'] == 0:
            print(index, row['PRINTERDEVICEID'], row['DATA_LEITURA'], row['CONTADOR_TOTAL'])
            
            # Procura no webservice a impressora com valores não nulos para copiar os valores
            # de contador_cor e contador_pb neste dataframe onde os valores são nulos
            search_payload = {
                'printerDeviceID': row['PRINTERDEVICEID'],
                'startDate': (pd.to_datetime(row['DATA_LEITURA'], format='%Y-%m-%d') - pd.DateOffset(days=1)).strftime('%Y-%m-%d'),
                'endDate': (row['DATA_LEITURA'] - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
            }

            try:
                # Recupera os dados do webservice para a impressora específica e data anterior
                previous_day_data = recuperar_dados_webservice(wsdl_url, service_method, search_payload, timeout=5)

                # Se houver valores, copia para o dataframe original
                if not previous_day_data.empty:
                    df_remoto.at[index, 'CONTADOR_PB'] = previous_day_data.iloc[0]['ReferenceMono']
                    df_remoto.at[index, 'CONTADOR_COR'] = previous_day_data.iloc[0]['ReferenceColor']

            except Exception as e:
                logging.error(f"Erro ao recuperar dados do webservice para a impressora {row['PRINTERDEVICEID']}: {str(e)}")

    
                
    # TODO buscar nos dados do webservice (dia anterior ao da coleta de dados) os valores não nulos para cada impressora encontrada no passo anterior
    # TODO se houver valores no dia anterior, preencher os dados do banco com os valores não nulos recuperados
    # TODO se não houver valor na data anterior, procurar as outras datas até achar uma com valores não nulos
  


# Dados api
wsdl_url = config.wsdl_url
service_method = config.service_method
output_csv = config.output_csv
payload = config.payload

#insert_printer('output-reference-2023-10-17.csv', 'HP')
#send_soap_request_and_write_to_csv(wsdl_url, service_method, output_csv, payload)
df_remoto = recuperar_dados_webservice(wsdl_url, service_method, payload,timeout=5)

# dfContagem = inserir_contagem_impressoras(dfContagem)
df_local = repo.recuperarDadosLocaisImpressoras()

inserir_contagem_impressoras(df_remoto)