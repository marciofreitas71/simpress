import os
import pandas as pd
import plotly.graph_objs as go
import dash
from datetime import datetime
from dash import dcc, html
from dash.dependencies import Input, Output

# Carregar o arquivo CSV para um DataFrame do pandas

# Função para obter o local onde a impressora está alocada
def processar_ip(ip):
    def obter_hostname_por_ip(ip):
        try:
            hostname = socket.gethostbyaddr(ip)
            return hostname[0]  # O nome do host está na primeira posição da tupla retornada
        except socket.herror:
            return "Hostname não encontrado"
        except socket.gaierror:
            return "Endereço IP inválido"

    def extrair_id_zona(ip):
        padrao = r'10\.171\.(\d+)\.60'
        correspondencia = re.match(padrao, ip)
        if correspondencia:
            return correspondencia.group(1)
        else:
            return "Padrão de IP não corresponde"

    hostname = obter_hostname_por_ip(ip)
    id_zona = extrair_id_zona(ip)
    return hostname, id_zona

df = pd.read_csv('D:/projetos/simpress/testes/df_filled.csv')

df['RealDateCapture'] = pd.to_datetime(df['RealDateCapture'], format='%Y-%m-%d')

# df.sort_values(by='RealDateCapture', ascending=True)

# Criar uma lista de todas as impressoras possíveis no conjunto de dados
impressoras_possiveis = sorted(list(df['SerialNumber'].unique()))

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    # Dropdown para seleção da impressora
    dcc.Dropdown(
        id='dropdown-impressora',
        options=[{'label': impressora, 'value': impressora} for impressora in impressoras_possiveis],
        value=impressoras_possiveis[0] if impressoras_possiveis else None  # Valor padrão é a primeira impressora, se houver
    ),
    # Gráfico de linha para exibir os dados da impressora selecionada
    dcc.Graph(id='grafico-impressora')
])

# Callback para atualizar o gráfico com base na impressora selecionada
@app.callback(
    Output('grafico-impressora', 'figure'),
    [Input('dropdown-impressora', 'value')]
)
def atualizar_grafico(serial_number_desejado):
    # Filtrar o DataFrame para incluir apenas registros com o SerialNumber desejado
    df_filtrado = df[df['SerialNumber'] == serial_number_desejado]

    # Verificar se existem registros para o SerialNumber fornecido
    if df_filtrado.empty:
        print("Não há registros para o SerialNumber fornecido.")
        return {}
    df_filtrado['total'] = df_filtrado['ReferenceMono'] +  df_filtrado['ReferenceColor'] 

    # Criar um gráfico de linha usando plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['RealDateCapture'], 
        y=df_filtrado['ReferenceMono'], 
        mode='lines', 
        name='Impressões',
        hovertext=[f'ReferenceColor: {referencecolor}, ReferenceMono: {referencemono}, Data: {datetimeread}' 
                   for referencecolor, referencemono, datetimeread in zip(df_filtrado['ReferenceColor'], df_filtrado['ReferenceMono'], df_filtrado['RealDateCapture'])]
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title=f'Impressora: {serial_number_desejado}: ',
        xaxis_title='Data',
        yaxis_title='Quantidade de Impressões'
    )

    return fig

# Executar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)
