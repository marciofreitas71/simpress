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

    
    
                
    # # Inserir as impressoras que faltam no banco de dados
    # # print(df.columns)
    
    # delete_all_registros()
        
    # create_impressora(PRINTERDEVICEID, PRINTERBRANDNAME, PRINTERMODELNAME, SERIALNUMBER)


    # df = pd.read_csv('data/todas_impressoras.csv')
    # for index, row in df.iterrows():
    #     create_impressora(row['PrinterDeviceID'], row['BrandName'], row['PrinterModelName'], row['SerialNumber'])