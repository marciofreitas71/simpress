import pandas as pd
from datetime import datetime, timedelta
import os

def gera_dados_completos(data_final, df, imp):
    df = df.loc[df['BrandName'] == 'HP']

    df['DateTimeRead'] = pd.to_datetime(df['DateTimeRead'])
    df['RealDateCapture'] = pd.to_datetime(data_final)

    # Classifica o DataFrame pelos valores da coluna 'DateTimeRead' em ordem decrescente
    df = df.sort_values(by='DateTimeRead', ascending=False)

    # Dataframe para contar as impressoras
    imp = df.drop_duplicates(subset=['SerialNumber'])

    # Filtra o DataFrame para manter apenas as entradas antes da data final
    data_final_str = data_final.strftime('%Y-%m-%d') + ' 00:00:00'
    data_final_dt = datetime.strptime(data_final_str, '%Y-%m-%d %H:%M:%S')
    df = df[df['DateTimeRead'] < data_final_dt]

    # Inicializa a lista e o DataFrame final
    registros_final = pd.DataFrame(columns=df.columns)
    lista_registros = []

    # Contador para controlar quantas impressoras foram adicionadas
    qtd_impressoras = 0

    # Enquanto o número de impressoras adicionadas for menor que o número total de impressoras em 'imp'
    while qtd_impressoras < len(imp):
        # Itera sobre as impressoras em 'imp'
        for index, row1 in imp.iterrows():
            print(f'Pesquisando as impressoras do dia {data_final}')
            print(f'{qtd_impressoras} impressoras adicionadas')
            print(f'{len(imp) - qtd_impressoras} impressoras restantes')
            print(f'Procurando impressora {row1["SerialNumber"]}...')
            # Verifica se a impressora já foi adicionada à lista
            if row1["SerialNumber"] not in lista_registros:
                # Flag para verificar se a impressora foi encontrada nos registros
                encontrada = False
                # Itera sobre as linhas do DataFrame
                for index, row2 in df.iterrows():
                    # Verifica se a impressora atual corresponde à impressora na linha
                    if row2["SerialNumber"] == row1["SerialNumber"]:
                        # Adiciona informações da impressora à lista
                        lista_registros.append([
                            row2["EnterpriseName"],
                            row2["PrinterDeviceID"],
                            row2["BrandName"],
                            row2["PrinterModelName"],
                            row2["SerialNumber"],
                            row2["AddressName"],
                            row2["DateTimeRead"],
                            row2["ReferenceMono"],
                            row2["ReferenceColor"],
                            row2["Engaged"],
                            '2024-01-01'
                        ])
                        print(f'{row1["SerialNumber"]} adicionada!')
                        # Define a flag como True pois a impressora foi encontrada
                        encontrada = True
                        # Limpa a saída do terminal após cada iteração completa
                        os.system('cls' if os.name == 'nt' else 'clear')
                        # Sai do loop de linhas e passa para a próxima impressora
                        break
                # Se a impressora não foi encontrada nos registros, adiciona com valores padrão
                if not encontrada:
                    print(f'Procurando impressoras não encontradas...')
                    lista_registros.append([
                        row1["EnterpriseName"],
                        row1["PrinterDeviceID"],
                        row1["BrandName"],
                        row1["PrinterModelName"],
                        row1["SerialNumber"],
                        'Não alocada',
                        data_final_dt,
                        0,
                        0,
                        False,
                        data_final
                    ])
                    print(f'{row1["SerialNumber"]} não encontrada. Adicionada com valores padrão.')
                    # Limpa a saída do terminal após cada iteração completa
                    os.system('cls' if os.name == 'nt' else 'clear')
            # Incrementa o contador de impressoras adicionadas
            qtd_impressoras += 1
            
        # Se o número de impressoras adicionadas for igual ao número total de impressoras, saia do loop
        if qtd_impressoras == len(df):
            break
    return lista_registros

if __name__ == "__main__":    
    data_inicial = '2024-05-01'
    data_final = '2024-05-03'
    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
    data_final = datetime.strptime(data_final, '%Y-%m-%d')
    caminho_arquivo = 'D:/projetos/simpress/testes/arquivo_final-16-05-2024.csv'

    df = pd.read_csv(caminho_arquivo)

    # Dataframe para contar as impressoras
    imp = df.drop_duplicates(subset=['SerialNumber'])

    lista_registros = []

    while data_final >= data_inicial:
        registros = gera_dados_completos(data_final, df, imp)
        lista_registros.extend(registros)
        data_final -= timedelta(days=1)  # Retrocede um dia

    # Converte a lista de listas em um DataFrame
    registros_final = pd.DataFrame(lista_registros, columns=[
        "EnterpriseName", "PrinterDeviceID", "BrandName", "PrinterModelName",
        "SerialNumber", "AddressName", "DateTimeRead", "ReferenceMono",
        "ReferenceColor", "Engaged", "RealDateCapture"
    ])

    # Converte a data para uma string
    data_final_str = data_final.strftime("%d-%m-%Y")

    print(f'Foram adicionadas ao arquivo {len(registros_final)} impressoras de um total de {len(imp)}')
    registros_final.to_csv(f'data_final-{data_final_str}.csv', index=False)