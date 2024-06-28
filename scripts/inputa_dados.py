import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
import pandas as pd
import logging
import csv
import re
from app import crud
from utils import utils


def insere_dados_csv_to_bd():
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    contagem = 0

    with open('../temp/dados_compilados/df_filled_final.csv', mode='r', encoding='utf-8') as csvfile, \
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
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        PRINTERDEVICEID = row['PrinterDeviceID']
        PRINTERBRANDNAME = row['BrandName']
        PRINTERMODELNAME = row['PrinterModelName']
        SERIALNUMBER = row['SerialNumber']
        crud.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # atualiza_lista_impressoras('../temp/dados_compilados/df_impressoras.csv')
    insere_dados_csv_to_bd()