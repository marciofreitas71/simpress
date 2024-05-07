from datetime import datetime, timedelta
import repository_gestao_impressoras as repo
import pandas as pd
import csv

def obter_hostname_por_ip(ip):
    try:
        hostname = socket.gethostbyaddr(ip[:-10])
        return hostname[0]  # O nome do host está na primeira posição da tupla retornada
    except socket.herror:
        return "Hostname não encontrado"
    except socket.gaierror:
        return "Endereço IP inválido"


def salva_dados_csv():
    DateTimeEnd = datetime.strptime('2024-04-25', '%Y-%m-%d')

    # Quantidade de dias anteriores à data final
    dias = 1

    while dias < 800:
        # Recupera dados do webservice
        dados_webservice = repo.recuperar_dados_webservice(DateTimeEnd.strftime('%Y-%m-%d'))
        
        # Adiciona a nova coluna com a DateTimeEnd
        dados_webservice['RealDataCapture'] = DateTimeEnd.strftime('%Y-%m-%d')

        # 
        
        # Salva os dados em um arquivo CSV
        dados_webservice.to_csv(f'arquivos/dados-{DateTimeEnd.strftime("%Y-%m-%d")}.csv', index=False)
        
        print(f'Dados do dia {DateTimeEnd.strftime("%Y-%m-%d")} processados e salvos')
        
        dias += 1       
        # Atualiza a data para o dia anterior
        DateTimeEnd -= timedelta(days=1)

# Função para inserir os dados das impressoras do arquivo CSV no banco de dados
def inserir_impressoras_from_csv(nome_arquivo):
    # Ler o arquivo CSV para um DataFrame do Pandas
    df = pd.read_csv(nome_arquivo)

    # Iterar sobre as linhas do DataFrame
    for index, linha in df.iterrows():
        # Extrair os valores dos campos do DataFrame
        PRINTERDEVICEID = linha['PrinterDeviceID']
        PRINTERBRANDNAME = linha['BrandName']
        PRINTERMODELNAME = linha['PrinterModelName']
        SERIALNUMBER = linha['SerialNumber']
        CREATED_AT = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S.%f')  # Converter para objeto datetime
        STATUS = 1  # Definir o status como 1
        
        # Chamar a função create_impressora para inserir os dados no banco de dados
        repo.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER, CREATED_AT, STATUS)

# Chamada da função para inserir os dados do arquivo CSV no banco de dados
inserir_impressoras_from_csv('testes/arquivos_final/arquivo_final-06-04-2024.csv')