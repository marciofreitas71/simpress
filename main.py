from app import webservice, crud
from utils import utils
import os
import logging
import itertools
import pandas as pd
import numpy as np
import zeep

def main():

          
    # utils.salva_dados_csv('01-01-2022', '28-05-2024')
    # utils.gera_arquivo_csv_compilado('D:/projetos/simpress/testes/arquivos_final')
    
    # utils.preenche_dados_csv('D:/projetos/simpress/testes/arquivo_final-29-05-2024.csv')

    # Insere os dados no dataframe
    # utils.insere_dados_csv_to_bd()

    # # Atualização da lista de impressoras
    # df = pd.read_csv('testes/data/df_impressoras.csv')
    # for index, row in df.iterrows():
    #     PRINTERDEVICEID = row['PrinterDeviceID']
    #     PRINTERBRANDNAME = row['BrandName']
    #     PRINTERMODELNAME = row['PrinterModelName']
    #     SERIALNUMBER = row['SerialNumber']
    #     crud.create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)
    utils.insere_websersvice_banco('29-05-24')

# A seguinte linha é executada somente se o módulo main.py for executado diretamente
if __name__ == "__main__":
    main()