import pandas as pd


data1 = {'IMP': [1, 2, 3, 4, 5, 28,40,110, 120,140,225],
         'CONTADOR_COR': [0, 0, 0, 50, 100,50,150,850,1000,78,130],
         'CONTADOR_PB': [0, 0, 0, 50, 450, 50,280,310,10,150,130]}

data1['CONTADOR_TOTAL'] = [cor + pb for cor, pb in zip(data1['CONTADOR_COR'], data1['CONTADOR_PB'])]

data2 = {'IMP': [1, 2, 4, 5, 7, 40, 120, 160,225],
         'CONTADOR_COR': [0, 200, 10, 0, 0, 0, 280, 840,0],
         'CONTADOR_PB': [100, 300, 10, 0, 0, 0, 700, 500,0]}
data2['CONTADOR_TOTAL'] = [cor + pb for cor, pb in zip(data2['CONTADOR_COR'], data2['CONTADOR_PB'])]

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

df3 = pd.merge(df1, df2, on="IMP", how='outer')

df3.fillna(0, inplace=True)
print(df3)

df4 = pd.DataFrame(columns=['IMP','CONTADOR_COR','CONTADOR_PB','CONTADOR_TOTAL'])

for index, row in df3.iterrows():
    if row['CONTADOR_TOTAL_y'] < row['CONTADOR_TOTAL_x'] or row['CONTADOR_TOTAL_y'] == 0:
        registro = [row['IMP'], str(row['CONTADOR_COR_x']), str(row['CONTADOR_PB_x']), str(row['CONTADOR_TOTAL_x'])]
        df4.loc[len(df4)] = registro
    else:
        registro = [row['IMP'], str(row['CONTADOR_COR_y']), str(row['CONTADOR_PB_y']), str(row['CONTADOR_TOTAL_y'])]
        df4.loc[len(df4)] = registro
        
print(df4)
