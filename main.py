from app import crud, database, models, queries
from app.crud import *
import pandas as pd
from datetime import datetime
import os

if __name__ == "__main__":
    
    pass
           
    # for i in range(50):
    #     print(crud.read_contagem_impressoras(i))
    #     if crud.read_contagem_impressoras(i):
    #         print("a impressora não existe!")

    df = pd.read_csv('testes/arquivos_final/arquivo_final-06-04-2024.csv')
    total = len(df)
    contagem = 10024


    # # # print(df.columns)
    for index, row in df.iterrows():
    
        # String com a data
        data_string = row['RealDateCapture']

        # Converter a string em um objeto datetime
        data_datetime = datetime.strptime(data_string, '%Y-%m-%d')


        try:
            # Tentar inserir os dados
            crud.create_contagem_impressoras(row['PrinterDeviceID'], row['ReferenceMono'], row['ReferenceColor'], data_datetime)
            print(f"Registro  ({row['PrinterDeviceID']}) inserido com sucesso.")
        except Exception as e:
            # Capturar qualquer exceção e imprimir uma mensagem de erro
            print(f"Erro ao inserir registro de contagem - impressora {row['PrinterDeviceID']}: {str(e)}")
            print(f'{row['SerialNumber']} - {row['DateTimeRead']}')
        contagem += 1
        print(f'Inseridos {contagem} de {total}')
        os.system('cls')
            
    # # Inserir as impressoras que faltam no banco de dados
    # # print(df.columns)
    
    # delete_all_registros()
        
    # create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)


    # df = pd.read_csv('data/todas_impressoras.csv')
    # for index, row in df.iterrows():
    #     create_impressora(row['PrinterDeviceID'], row['BrandName'], row['PrinterModelName'], row['SerialNumber'])