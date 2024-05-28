import pandas as pd
from datetime import datetime
import os

# Carregando os dados e convertendo 'DateTimeRead' para datetime
dados_webservice = pd.read_csv('arquivo_final.csv')
dados_webservice['DateTimeRead'] = pd.to_datetime(dados_webservice['DateTimeRead'])

# Filtrando registros anteriores a 01/01/2024
registros_anteriores = (dados_webservice[dados_webservice['RealDataCapture'] < '2024-01-01']).sort_values(by='DateTimeRead',ascending=False )

# Carregando a lista de impressoras
todas_impressoras = pd.read_csv('data/todas_impressoras.csv')

# Inicializando variáveis
data_limite = pd.to_datetime('2024-01-01')
qtd_impressoras = len(todas_impressoras)
num_impressora = 1
lista_dataframes = []  # Lista para armazenar DataFrames temporários

# Iterando sobre as impressoras
for impressora in todas_impressoras['SerialNumber']:

    # Lista vazia para armazenar registros da impressora atual
    lista_registros = []

    # Iterando sobre os registros
    for indice, registro in dados_webservice.iterrows():

        # Verificando se o registro pertence à impressora e data limite
        if registro['SerialNumber'] == impressora and registro['DateTimeRead'] < data_limite:

            # Encontrando o último registro da impressora antes de 01/01/2024
            ultimo_registro = registro.copy()

            # Atualizando data para 01/01/2024
            ultimo_registro['DateTimeRead'] = '2024-01-01'
            ultimo_registro['RealDataCapture'] = '2024-01-01'

            # Adicionando o registro à lista temporária
            lista_registros.append(ultimo_registro)

    # Se houver registros para a impressora, cria um DataFrame e concatena na lista
    if lista_registros:
        df_impressora = pd.concat(lista_registros)
        lista_dataframes.append(df_impressora)

    # Atualizando contadores
    num_impressora += 1

# Salvando o DataFrame final (concatenação final)
arquivo_final = pd.concat(lista_dataframes)
arquivo_final.to_csv('arquivo_final-15-05-2024.csv')