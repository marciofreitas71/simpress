from datetime import datetime
import zeep
import pandas as pd
import repository_gestao_impressoras as repo

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

def inserir_contagem_impressoras(dataframe):
    dataframe = dataframe.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
    dataframe.columns = dataframe.columns.str.upper()
    dataframe = dataframe[['SERIALNUMBER', 'DATA_LEITURA', 'CONTADOR_PB', 'CONTADOR_COR']]
    dataframe['CONTADOR_TOTAL'] = dataframe['CONTADOR_PB'] + dataframe['CONTADOR_COR']
    # print(dataframe)
    dataframe2 = repo.recuperarDadosLocaisImpressoras()
    # dataframe = dataframe.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
    #print('-----------------------------------------------')
    
    
    #-------------inicio do trecho alterado------------------#

    # df3 = pd.merge(dataframe, dataframe2, on='SERIALNUMBER', how='outer')

    # pd.set_option('display.max_rows', None)
    # df3.fillna(0, inplace=True)
    
    # print(dataframe.sort_values(by='SERIALNUMBER'))
    print(dataframe2)
    print()
    print(dataframe)
    # print(dataframe2.shape)

    # print(df3.sort_values(by='SERIALNUMBER'))
    # # print('Impressao de dataframe')
    # print(df3.columns)

    # dataframe = pd.DataFrame(columns=[['IMPRESSORA_ID', 'SERIALNUMBER', 'DATA_LEITURA', 'CONTADOR_PB', 'CONTADOR_COR', 'CONTADOR_TOTAL']])

    # for index, row in df3.iterrows():
    #     if row['CONTADOR_TOTAL_y'] < row['CONTADOR_TOTAL_x'] or row['CONTADOR_TOTAL_y'] == 0:
    #         registro = [row['IMPRESSORA_ID'], row['SERIALNUMBER'], pd.to_datetime(row['DATA_LEITURA_x']), str(row['CONTADOR_PB_x']), str(row['CONTADOR_COR_x']), str(row['CONTADOR_TOTAL_x'])]
    #         dataframe.loc[len(dataframe)] = registro
    #     else:
    #         registro = [row['IMPRESSORA_ID'], row['SERIALNUMBER'], pd.to_datetime(row['DATA_LEITURA_y']), str(row['CONTADOR_PB_y']), str(row['CONTADOR_COR_y']), str(row['CONTADOR_TOTAL_y'])]
    #         dataframe.loc[len(dataframe)] = registro
        

    # # Adiciona a data atual à coluna 'CREATED_AT' para todas as linhas
    # dataframe['CREATED_AT'] = datetime.now()
                
    # # #-------------fim do trecho alterado------------------#
       
    
    # dataframe.drop('SERIALNUMBER', axis=1, inplace=True)
    # df1 = df3[['IMPRESSORA_ID','CONTADOR_PB_x','CONTADOR_COR_x','CONTADOR_TOTAL_x','CONTADOR_PB_y','CONTADOR_COR_y','CONTADOR_TOTAL_y']]
    # # print(df1)
    # # repo.cadastrarContagemImpressoras(dataframe)
    # df2 = dataframe[['IMPRESSORA_ID','CONTADOR_PB','CONTADOR_COR','CONTADOR_TOTAL']]
    # # print(df2)
    # result = (pd.concat([df1, df2], axis=1)).sort_values(by='IMPRESSORA_ID')
    # print(result.drop(columns=['IMPRESSORA_ID']))

# Example usage
wsdl_url = 'https://api-counters.nddprint.com/CountersWS/CountersData.asmx?WSDL'
service_method = 'GetReferenceCountersData' #'GetPlainCountersData'
output_csv = 'output-reference-2023-10-27.csv' #'output-plain-2023-10-15.csv'
payload = {
    'dealerName': 'SIMPRESS',
    'dealerUserEmail': 'ruguedes@tre-ba.jus.br',
    'dealerUserPassword': '8lYKAfLbl2FKqAJgWWRA5Q==',
    #'dateTimeStart': '2023-10-17 00:00:00',
    'dateTimeEnd': '2023-12-01 02:00:00',
    'maxLimitDaysEarlier': 1,
    'enterpriseName': '9853_TRE_BA',
    'serialNumber': '',
    'siteName': '',
    'siteDivisionName': '',
    'engaged': False,
    'fieldsList': 'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #'EnterpriseName;PrinterDeviceID;SerialNumber;AddressName;siteName;EnabledCounters;CounterTypeName;FirstCounterTotal;LatestCounterTotal;FirstCounterMono;LatestCounterMono;FirstCounterColor;LatestCounterColor' #'EnterpriseName;PrinterDeviceID;BrandName;PrinterModelName;SerialNumber;AddressName;DateTimeRead;ReferenceMono;ReferenceColor;Engaged' #
}

#insert_printer('output-reference-2023-10-17.csv', 'HP')
#send_soap_request_and_write_to_csv(wsdl_url, service_method, output_csv, payload)
dfContagem = recuperar_dados_webservice(wsdl_url, service_method, payload)

# dfContagem = inserir_contagem_impressoras(dfContagem)
dfContagemLocal = repo.recuperarDadosLocaisImpressoras()

inserir_contagem_impressoras(dfContagem)