from utils import utils
import os
import logging
import pandas as pd
import zeep

def main():
    # Chame a função do utils
#    utisalva_dados_csv('2024-05-14')
    utils.salva_dados_csv('01-01-2022','06-01-2024')

# A seguinte linha é executada somente se o módulo main.py for executado diretamente
if __name__ == "__main__":
    main()