from app import webservice
from app import crud
from utils import utils
import os
import logging
import pandas as pd
import zeep

def main():
    # Chame a função do utils
    
    utils.salva_dados_csv('01-01-2022', '26-05-2024')
    utils.gera_arquivo_csv_compilado('D:/projetos/simpress/testes/arquivos_final')
    utils.insere_dados_csv_to_bd()

    # df = pd.read_csv('testes/data/df_impressoras.csv')
    # for index, row in df.iterrows():
    #     PRINTERDEVICEID = row['PrinterDeviceID']
    #     PRINTERBRANDNAME = row['BrandName']
    #     PRINTERMODELNAME = row['PrinterModelName']
    #     SERIALNUMBER = row['SerialNumber']
    #     # crud.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)
    #     crud.create_contagem_impressoras()

# A seguinte linha é executada somente se o módulo main.py for executado diretamente
if __name__ == "__main__":
    main()