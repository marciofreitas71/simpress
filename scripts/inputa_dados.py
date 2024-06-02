"""
Este módulo contém funções para manipulação e inserção de dados de impressoras em um banco de dados a partir de arquivos CSV.

Pacotes importados:
- datetime: Para manipulação de datas e horas.
- utils: Módulo utilitário contendo funções auxiliares.
- crud: Módulo para operações CRUD (Create, Read, Update, Delete) no banco de dados.
- pandas (pd): Para manipulação de dados em estruturas DataFrame.
- logging: Para registro de eventos e mensagens.
- csv: Para leitura e escrita de arquivos CSV.
- os: Para interações com o sistema operacional, como manipulação de arquivos e diretórios.
- re: Para operações com expressões regulares.

Funções:
- insere_dados_csv_to_bd(): Insere registros do webservice a partir de um arquivo CSV no banco de dados.
- atualiza_lista_impressoras(csv_path): Atualiza a lista de impressoras no banco de dados a partir de um arquivo CSV.
"""

from datetime import datetime
from utils import utils
from app import crud
import pandas as pd
import logging
import csv
import os
import re

def insere_dados_csv_to_bd():
    """
    Insere registros do webservice a partir de um arquivo CSV no banco de dados.

    Lê um arquivo CSV contendo dados do webservice e insere esses registros em um banco de dados.
    
    O arquivo CSV esperado deve conter as colunas:
    - 'RealDateCapture': Data de captura no formato 'YYYY-MM-DD'
    - 'PrinterDeviceID': ID da impressora
    - 'ReferenceMono': Referência de impressões monocromáticas
    - 'ReferenceColor': Referência de impressões coloridas
    
    Cada registro é inserido no banco de dados utilizando a função 'create_contagem_impressoras' do módulo 'crud'.
    """
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    contagem = 0

    with open('temp/dados_compilados/df_filled_final.csv', mode='r', encoding='utf-8') as csvfile, \
         open('erros_log.csv', mode='w', newline='', encoding='utf-8') as errorfile:
        
        reader = pd.read_csv(csvfile, iterator=True, chunksize=1)
        error_writer = csv.writer(errorfile)
        error_writer.writerow(['PrinterDeviceID', 'SerialNumber', 'ErrorType', 'ErrorMessage'])
        
        for chunk in reader:
            for index, row in chunk.iterrows():
                try:
                    data_string = row['RealDateCapture']
                    data_datetime = datetime.strptime(data_string, '%Y-%m-%d')
                    
                    print(f'{row["SerialNumber"]}')
                    crud.create_contagem_impressoras(row['PrinterDeviceID'], row['ReferenceMono'], row['ReferenceColor'], data_datetime)
                    print(f"Registro ({row['PrinterDeviceID']}) inserido com sucesso.")
                
                except ValueError as ve:
                    logging.error(f"Erro ao converter data para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {ve}")
                    error_writer.writerow([row['PrinterDeviceID'], row['SerialNumber'], 'ValueError', str(ve)])
                
                except KeyError as ke:
                    logging.error(f"Erro ao acessar uma chave inexistente no DataFrame para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {ke}")
                    error_writer.writerow([row['PrinterDeviceID'], row['SerialNumber'], 'KeyError', str(ke)])
                
                except Exception as e:
                    logging.error(f"Erro ao inserir registro de contagem para o registro com PrinterDeviceID {row['PrinterDeviceID']} e SerialNumber {row['SerialNumber']}: {e}")
                    error_writer.writerow([row['PrinterDeviceID'], row['SerialNumber'], 'Exception', str(e)])
                
                contagem += 1
                print(f'Inserido o registro {contagem}')
                os.system('cls')


def atualiza_lista_impressoras(csv_path):
    df = pd.read_csv('temp/dados_compilados/df_impressoras.csv')
    for index, row in df.iterrows():
        PRINTERDEVICEID = row['PrinterDeviceID']
        PRINTERBRANDNAME = row['BrandName']
        PRINTERMODELNAME = row['PrinterModelName']
        SERIALNUMBER = row['SerialNumber']
        crud.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    insere_dados_csv_to_bd()
    atualiza_lista_impressoras('temp/dados_compilados/df_impressoras.csv')