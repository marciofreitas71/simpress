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

# Carrega os dados do arquivo CSV df_filled_final.csv
df = pd.read_csv('temp/dados_compilados/df_filled_final.csv')

df['RealDateCapture'] = pd.to_datetime(df['RealDateCapture'], format='%Y-%m-%d')

# Obtém a lista de números de série únicos das impressoras
impressoras_possiveis = sorted(list(df['SerialNumber'].unique()))

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Define o layout do aplicativo
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
    """
    Atualiza o gráfico com base na impressora selecionada.

    Args:
        serial_number_desejado (str): O número de série da impressora selecionada.

    Returns:
        go.Figure: Um objeto Figure do Plotly contendo o gráfico atualizado.
    """
    # Filtra os dados com base no número de série selecionado
    df_filtrado = df[df['SerialNumber'] == serial_number_desejado]

    if df_filtrado.empty:
        print("Não há registros para o SerialNumber fornecido.")
        return {}
    
    # Calcula o total de impressões (preto e branco + coloridas)
    df_filtrado['total'] = df_filtrado['ReferenceMono'] + df_filtrado['ReferenceColor']

    # Cria um gráfico de linha para as impressões
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['RealDateCapture'], 
        y=df_filtrado['ReferenceMono'], 
        mode='lines', 
        name='Impressões',
        hovertext=[f'ReferenceColor: {referencecolor}, ReferenceMono: {referencemono}, Data: {datetimeread}' 
                   for referencecolor, referencemono, datetimeread in zip(df_filtrado['ReferenceColor'], df_filtrado['ReferenceMono'], df_filtrado['RealDateCapture'])]
    ))

    # Atualiza o layout do gráfico
    fig.update_layout(
        title=f'Impressora: {serial_number_desejado}: ',
        xaxis_title='Data',
        yaxis_title='Quantidade de Impressões'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)