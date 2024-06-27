import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Carregar os dados
file_path = '../temp/dados_compilados/df_filled_final.csv'
df = pd.read_csv(file_path)

# Criar a coluna Total
df['Total'] = df['ReferenceMono'] + df['ReferenceColor']

# Obter opções únicas para filtros
printer_options = [{'label': str(printer), 'value': printer} for printer in df['PrinterDeviceID'].unique()]
serial_options = [{'label': str(serial), 'value': serial} for serial in df['SerialNumber'].unique()]

# Inicializar o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

# Adicionar estilos personalizados
custom_css = """
    <style>
        .dash-dropdown-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 20px;
        }
        .dash-dropdown {
            margin-right: 10px;
            min-width: 200px;
        }
        .dash-dropdown div div {
            max-height: 150px !important;
            overflow-y: auto !important;
        }
    </style>
"""

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard de Impressoras", className='text-center my-4'),
    html.Div([
        dcc.DatePickerRange(
            id='date-picker',
            start_date=df['RealDateCapture'].min(),
            end_date=df['RealDateCapture'].max(),
            display_format='YYYY-MM-DD',
            className='mr-2 dash-dropdown'
        ),
        dcc.Dropdown(
            id='printer-filter',
            options=printer_options,
            value=[],
            multi=True,
            placeholder='Select printers',
            className='mr-2 dash-dropdown'
        ),
        dcc.Dropdown(
            id='serial-filter',
            options=serial_options,
            value=[],
            multi=True,
            placeholder='Select serial numbers',
            className='mr-2 dash-dropdown'
        ),
    ], className='dash-dropdown-container'),
    dcc.Graph(id='graph'),
    html.Div(id='custom-css', style={'display': 'none'}, children=custom_css)
], className='container')

# Callback para atualizar o gráfico com base nos filtros
@app.callback(
    Output('graph', 'figure'),
    [
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('printer-filter', 'value'),
        Input('serial-filter', 'value')
    ]
)
def update_graph(start_date, end_date, selected_printers, selected_serials):
    """
    Atualiza o gráfico com base nos filtros selecionados.

    Args:
        start_date (str): Data inicial do intervalo selecionado.
        end_date (str): Data final do intervalo selecionado.
        selected_printers (list): Lista de IDs das impressoras selecionadas.
        selected_serials (list): Lista de números de série selecionados.

    Returns:
        plotly.graph_objs._figure.Figure: Figura atualizada com os dados filtrados.
    """
    # Filtrar os dados
    filtered_df = df[(df['RealDateCapture'] >= start_date) & (df['RealDateCapture'] <= end_date)]
    if selected_printers:
        filtered_df = filtered_df[filtered_df['PrinterDeviceID'].isin(selected_printers)]
    if selected_serials:
        filtered_df = filtered_df[filtered_df['SerialNumber'].isin(selected_serials)]

    # Criar a figura do gráfico de linha contínua
    fig = px.line(
        filtered_df,
        x='RealDateCapture',
        y='Total',
        color='PrinterDeviceID',
        labels={'Total': 'Total References', 'RealDateCapture': 'Capture Date'},
        title='Total References by Date'
    )

    fig.update_layout(
        template='plotly_white',
        xaxis_title='Capture Date',
        yaxis_title='Total References',
        title_x=0.5,
        legend_title_text='Printer Device ID'
    )

    return fig

# Executar o aplicativo
if __name__ == '__main__':
    # Executa o servidor do aplicativo Dash
    app.run_server(debug=True)
