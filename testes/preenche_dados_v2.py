import pandas as pd
from tqdm import tqdm
import numpy as np

# Carregar o conjunto de dados
print("Carregando o conjunto de dados...")
df = pd.read_csv('D:/projetos/simpress/testes/arquivo_final-16-05-2024.csv')
df = df[df['BrandName'] == 'HP']

print(f"Conjunto de dados carregado com {len(df)} registros.")

# Criando uma lista de impressoras
imp = df['SerialNumber'].unique()

# Generate a DataFrame of dates
date_range = pd.date_range(start='2022-03-10', end='2024-05-16', freq='D')
df_dates = pd.DataFrame({'RealDateCapture': date_range})

# Create a DataFrame for the final result
df_result = pd.DataFrame(columns=['SerialNumber', 'DateTimeRead', 'EnterpriseName', 'PrinterDeviceID', 'BrandName', 'PrinterModelName', 'AddressName', 'ReferenceMono', 'ReferenceColor', 'Engaged', 'RealDateCapture'])

lista_dataframes = []

# Populate the result DataFrame
for serial_number in tqdm(imp):
    # Filter data for the current printer
    printer_data = df[df['SerialNumber'] == serial_number].copy()

    # Convert DateTimeRead to datetime format (assuming it's a string)
    printer_data['RealDateCapture'] = pd.to_datetime(printer_data['RealDateCapture'])

    # Merge date range with printer data
    merged_df = df_dates.merge(printer_data, how='left', on='RealDateCapture')

    # Fill in missing values with NaN
    merged_df.fillna(value=np.nan, inplace=True)

    # Append merged data to list lista_dataframe
    lista_dataframes.append(merged_df)

df_result = pd.concat(lista_dataframes)

df_result.to_csv('D:/projetos/simpress/testes/df_merged.csv')

print("DataFrame preenchido com registros para todas as datas e impressoras.")
