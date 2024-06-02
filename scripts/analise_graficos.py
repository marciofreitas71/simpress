"""
Este módulo cria um aplicativo Dash para visualização de dados de impressoras.

Pacotes importados:
- os: Para interações com o sistema operacional.
- pandas as pd: Para manipulação de dados em estruturas DataFrame.
- plotly.graph_objs as go: Para criação de gráficos interativos.
- dash: Para criação do aplicativo web.
- datetime: Para manipulação de datas e horários.
- dcc, html (dash): Para componentes do layout do aplicativo.
- Input, Output (dash.dependencies): Para interatividade do aplicativo.

Funções:
- atualizar_grafico(serial_number_desejado): Atualiza o gráfico com base na impressora selecionada.
"""

import os
import pandas as pd
import plotly.graph_objs as go
import dash
from datetime import datetime
from dash import dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv('../temp/dados_compilados/df_filled.csv')
df['RealDateCapture'] = pd.to_datetime(df['RealDateCapture'], format='%Y-%m-%d')

impressoras_possiveis = sorted(list(df['SerialNumber'].unique()))

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-impressora',
        options=[{'label': impressora, 'value': impressora} for impressora in impressoras_possiveis],
        value=impressoras_possiveis[0] if impressoras_possiveis else None
    ),
    dcc.Graph(id='grafico-impressora')
])

@app.callback(
    Output('grafico-impressora', 'figure'),
    [Input('dropdown-impressora', 'value')]
)
def atualizar_grafico(serial_number_desejado):
    df_filtrado = df[df['SerialNumber'] == serial_number_desejado]

    if df_filtrado.empty:
        print("Não há registros para o SerialNumber fornecido.")
        return {}
    df_filtrado['total'] = df_filtrado['ReferenceMono'] +  df_filtrado['ReferenceColor'] 

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['RealDateCapture'], 
        y=df_filtrado['ReferenceMono'], 
        mode='lines', 
        name='Impressões',
        hovertext=[f'ReferenceColor: {referencecolor}, ReferenceMono: {referencemono}, Data: {datetimeread}' 
                   for referencecolor, referencemono, datetimeread in zip(df_filtrado['ReferenceColor'], df_filtrado['ReferenceMono'], df_filtrado['RealDateCapture'])]
    ))

    fig.update_layout(
        title=f'Impressora: {serial_number_desejado}: ',
        xaxis_title='Data',
        yaxis_title='Quantidade de Impressões'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
