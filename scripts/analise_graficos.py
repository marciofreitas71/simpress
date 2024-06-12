import pandas as pd
import plotly.graph_objs as go
import dash
from datetime import datetime
from dash import dcc, html
from dash.dependencies import Input, Output

# Carrega os dados do arquivo CSV
file_path = 'testes/data/contagem_impressora_10-06-2024.csv'
df = pd.read_csv(file_path)

# Converte a coluna 'DATA_LEITURA' para datetime
df['DATA_LEITURA'] = pd.to_datetime(df['DATA_LEITURA'], format='%d/%m/%y %H:%M:%S')

# Ordena os dados por 'DATA_LEITURA'
df = df.sort_values(by='DATA_LEITURA')

# Obtém a lista de números de série únicos das impressoras
impressoras_possiveis = sorted(list(df['IMPRESSORA_ID'].unique()))

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Define o layout do aplicativo
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-impressora',
        options=[{'label': impressora, 'value': impressora} for impressora in impressoras_possiveis],
        value=impressoras_possiveis[0] if impressoras_possiveis else None,
        style={'margin-bottom': '20px'}
    ),
    dcc.Graph(id='grafico-impressora')
])

@app.callback(
    Output('grafico-impressora', 'figure'),
    [Input('dropdown-impressora', 'value')]
)
def atualizar_grafico(serial_number_desejado):
    # Filtra os dados com base no número de série selecionado
    df_filtrado = df[df['IMPRESSORA_ID'] == serial_number_desejado]

    if df_filtrado.empty:
        return {}

    # Remove duplicatas
    df_filtrado = df_filtrado.drop_duplicates(subset=['DATA_LEITURA'])

    # Cria um gráfico de linha para as impressões
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['DATA_LEITURA'], 
        y=df_filtrado['CONTADOR_TOTAL'], 
        mode='lines+markers', 
        name='Impressões',
        line=dict(color='royalblue', width=2),
        marker=dict(size=6, color='blue'),
        hovertext=[f'COR: {CONTADOR_COR}, PB: {CONTADOR_PB}, Data: {DATA_LEITURA}' 
                   for CONTADOR_COR, CONTADOR_PB, DATA_LEITURA in zip(df_filtrado['CONTADOR_COR'], df_filtrado['CONTADOR_PB'], df_filtrado['DATA_LEITURA'])]
    ))

    # Atualiza o layout do gráfico
    fig.update_layout(
        title=f'Impressora: {serial_number_desejado}',
        xaxis_title='Data',
        yaxis_title='Quantidade de Impressões',
        template='plotly_white',
        title_font=dict(size=24, family='Arial, bold'),
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=True
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
