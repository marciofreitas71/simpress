from app import webservice
from utils import utils
import os
import logging
import pandas as pd
import zeep

def main():
    # Chame a função do utils
    # utils.salva_dados_csv('2024-05-16')
    # utils.gera_arquivo_csv_compilado('D:/projetos/simpress/testes/arquivos_final')
    utils.insere_dados_csv_to_bd()

# A seguinte linha é executada somente se o módulo main.py for executado diretamente
if __name__ == "__main__":
    main()