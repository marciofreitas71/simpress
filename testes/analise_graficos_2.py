import os
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime


# Carregar os arquivos CSV para os DataFrames do pandas
df1 = pd.read_csv('arquivo_final.csv')  # Substitua pelo nome do primeiro arquivo CSV
df2 = pd.read_csv('banco_oracle.csv')  # Substitua pelo nome do segundo arquivo CSV



# Supondo que 'DateTimeRead' seja o nome da sua coluna que você quer converter
df2['DateTimeRead'] = pd.to_datetime(df2['DateTimeRead'], format='%d/%m/%y %H:%M:%S')


# Criar listas de todas as impressoras possíveis em cada conjunto de dados
impressoras_possiveis_df1 = list(df1['SerialNumber'].unique())
impressoras_possiveis_df2 = list(df2['SerialNumber'].unique())

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    # Dropdown para seleção da impressora para o primeiro DataFrame
    html.Div([
        html.H3("Arquivo excel"),
        dcc.Dropdown(
            id='dropdown-impressora-df1',
            options=[{'label': impressora, 'value': impressora} for impressora in impressoras_possiveis_df1],
            value=impressoras_possiveis_df1[0] if impressoras_possiveis_df1 else None
        ),
        dcc.Graph(id='grafico-impressora-df1')
        
    ]),
    # Dropdown para seleção da impressora para o segundo DataFrame
    html.Div([
        html.H3("Banco Oracle"),
        dcc.Dropdown(
            id='dropdown-impressora-df2',
            options=[{'label': impressora, 'value': impressora} for impressora in impressoras_possiveis_df2],
            value=impressoras_possiveis_df2[0] if impressoras_possiveis_df2 else None
        ),
        dcc.Graph(id='grafico-impressora-df2')
    ])
])

# Função para criar um gráfico com base nos dados e nos valores selecionados
def criar_grafico(df, serial_number_desejado):
    # Filtrar o DataFrame para incluir apenas registros com o SerialNumber desejado
    df_filtrado = df[df['SerialNumber'] == serial_number_desejado]

    # Verificar se existem registros para o SerialNumber fornecido
    if df_filtrado.empty:
        print(f"Não há registros para o SerialNumber {serial_number_desejado}.")
        return {}

    # Criar um gráfico de linha para os valores de ReferenceMono e ReferenceColor
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['DateTimeRead'],
        y=df_filtrado['ReferenceMono'],
        mode='lines',
        name='ReferenceMono',
        hovertext=[f'ReferenceMono: {referencemono}, ReferenceColor: {referencecolor}, Data: {datetimeread}'
                   for referencemono, referencecolor, datetimeread in
                   zip(df_filtrado['ReferenceMono'], df_filtrado['ReferenceColor'], df_filtrado['DateTimeRead'])]
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado['DateTimeRead'],
        y=df_filtrado['ReferenceColor'],
        mode='lines',
        name='ReferenceColor',
        hovertext=[f'ReferenceMono: {referencemono}, ReferenceColor: {referencecolor}, Data: {datetimeread}'
                   for referencemono, referencecolor, datetimeread in
                   zip(df_filtrado['ReferenceMono'], df_filtrado['ReferenceColor'], df_filtrado['DateTimeRead'])]
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title=f'Impressora: {serial_number_desejado}',
        xaxis_title='Data',
        yaxis_title='Quantidade de Impressões'
    )

    return fig

# Callback para atualizar o gráfico do primeiro DataFrame com base na impressora selecionada
@app.callback(
    Output('grafico-impressora-df1', 'figure'),
    [Input('dropdown-impressora-df1', 'value')]
)
def atualizar_grafico_df1(serial_number_desejado):
    return criar_grafico(df1, serial_number_desejado)

# Callback para atualizar o gráfico do segundo DataFrame com base na impressora selecionada
@app.callback(
    Output('grafico-impressora-df2', 'figure'),
    [Input('dropdown-impressora-df2', 'value')]
)
def atualizar_grafico_df2(serial_number_desejado):
    return criar_grafico(df2, serial_number_desejado)

# Executar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)



    # Verificando o tipo de dado após a conversão
    print(df2.dtypes)