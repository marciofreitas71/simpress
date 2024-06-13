import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Carregar o arquivo CSV
file_path = '../testes/data/contagem_impressora_01-01-2024-11-06-2024.csv'
data = pd.read_csv(file_path)

# Converter a coluna de datas para o formato datetime
data['DATA_LEITURA'] = pd.to_datetime(data['DATA_LEITURA'], format='%d/%m/%y %H:%M:%S')

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard de Impressoras"),
    
    dcc.Dropdown(
        id='impressora-dropdown',
        options=[{'label': str(i), 'value': i} for i in data['IMPRESSORA_ID'].unique()],
        multi=True,
        placeholder="Selecione a Impressora"
    ),
    
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=data['DATA_LEITURA'].min(),
        end_date=data['DATA_LEITURA'].max(),
        display_format='DD/MM/YYYY'
    ),
    
    dcc.Graph(id='contador-graph'),
    
    html.Label("Contador:"),
    dcc.RadioItems(
        id='contador-radio',
        options=[
            {'label': 'PB', 'value': 'CONTADOR_PB'},
            {'label': 'Cor', 'value': 'CONTADOR_COR'},
            {'label': 'Total', 'value': 'CONTADOR_TOTAL'}
        ],
        value='CONTADOR_TOTAL'
    )
])

# Callback para atualizar o gráfico com base nas seleções
@app.callback(
    Output('contador-graph', 'figure'),
    [
        Input('impressora-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('contador-radio', 'value')
    ]
)
def update_graph(selected_impressoras, start_date, end_date, selected_contador):
    filtered_data = data[(data['DATA_LEITURA'] >= start_date) & (data['DATA_LEITURA'] <= end_date)]
    
    if selected_impressoras:
        filtered_data = filtered_data[filtered_data['IMPRESSORA_ID'].isin(selected_impressoras)]
    
    fig = px.line(filtered_data, x='DATA_LEITURA', y=selected_contador, color='IMPRESSORA_ID',
                  title=f'Contagem {selected_contador}')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
