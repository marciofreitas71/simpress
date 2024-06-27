# Projeto de Análise de Dados de Impressoras

Este projeto é uma aplicação completa que realiza a manipulação, análise e visualização de dados de impressoras. Ele também integra um serviço da web para recuperar dados, permitindo uma análise abrangente dos dados coletados.

## Estrutura do Projeto
- app/: Contém módulos principais para configuração, operações CRUD e integração com o serviço da web.
- config.py: Configuração e conexão com o banco de dados.
- crud.py: Funções CRUD para manipulação de dados no banco de dados.
- webservice.py: Funções para integração com o serviço da web SOAP.
- credenciais/: Contém informações de configuração e credenciais.
- scripts/: Contém scripts para manipulação e análise de dados.
- prepara_dados.py: Manipulação de dados e geração de arquivos CSV.
- analise_graficos.py: Visualização de dados usando Dash.
- temp/: Contém dados temporários gerados pelos scripts.
- testes/: Scripts de teste.
- utils/: Utilitários auxiliares.

## Configuração

### Arquivo config.py
Define variáveis e configurações necessárias para acessar um serviço web SOAP e fazer uma chamada a este serviço. O serviço web em questão é o "CountersWS" fornecido pela URL especificada no formato WSDL.

Estabelece uma conexão com o banco de dados Oracle.
Retorna uma conexão ativa com o banco de dados Oracle, utilizando as credenciais e informações de conexão fornecidas no arquivo de ambiente (.env) através das variáveis de ambiente user_name, password, host, port e service_name.

'''
connection = get_connection()

## Instalação
Clone o repositório na pasta 'simpress':

```
git clone gitlab.tre-ba.jus.br/assec-ia/simpress.git simpress
```

Torne o script de setup executável:

```
chmod +x setup_project.sh
```

Execute o script de setup:

```
./setup_project.sh
```

Este script irá:

- Criar os diretórios necessários.
- Criar e ativar o ambiente virtual venv.
- Instalar as dependências listadas no requirements.txt.
- Funcionalidade
- Configuração e Conexão



## Operações CRUD (crud.py)

Este módulo define operações CRUD (Create, Read, Update, Delete) para manipulação dos dados no banco de dados.

Funções:
- create_impressora(): Cria uma nova impressora no banco de dados.
- create_contagem_impressoras(): Registra uma contagem de impressoras no banco de dados.
- read_contagem_impressoras(): Lê os registros de contagem de impressoras do banco de dados.
- update_contagem_impressora(): Atualiza os registros de contagem de impressoras no banco de dados.
- delete_contagem_impressora(): Exclui os registros de contagem de impressoras do banco de dados.
- delete_all_registros(): Exclui todos os registros de contagem de impressoras do banco de dados.
- delete_all_impressoras(): Exclui todas as impressoras do banco de dados.
- read_impressoras_data(): Lê os registros de contagem de impressoras do banco de dados para uma determinada data.
- read_all_record_data(): Lê todos os registros da tabela contagem_impressora do banco de dados.
- obter_registros_ultima_data(): Obtém registros da última data de leitura no banco de dados.
- obter_ultima_data_bd(): Obtém a última data de leitura no banco de dados.

## Consultas SQL (queries.py)

Este módulo contém consultas SQL para operações CRUD no banco de dados.

Consultas:
- SELECT_CONTAGEM_IMPRESSORAS: Consulta para selecionar todas as contagens de impressoras associadas a uma impressora específica.
- INSERT_IMPRESSORA: Consulta para inserir uma nova impressora no banco de dados.
- SELECT_IMPRESSORA: Consulta para selecionar uma impressora com base no ID do dispositivo da impressora.
- UPDATE_IMPRESSORA: Consulta para atualizar os detalhes de uma impressora no banco de dados.
- DELETE_IMPRESSORA: Consulta para excluir uma impressora do banco de dados com base no ID do dispositivo da impressora.
- SELECT_LAST_READING_DATE: Consulta para recuperar a última data de leitura no banco de dados.

## Modelos (models.py)

Este módulo define classes que representam os modelos de dados do banco de dados.

Classes:
- ContagemImpressoras: Representa uma contagem de impressoras.
- Impressoras: Representa uma impressora.

## Webservice (webservice.py)

Este módulo fornece funcionalidades para recuperar dados de um serviço da web SOAP, utilizando as bibliotecas SQLAlchemy, dotenv, pandas e zeep. Ele inclui a configuração do cliente SOAP e o processamento de dados recebidos do serviço.

Funções:
- recuperar_dados(data): Recupera dados de um serviço da web SOAP.

Manipulação e Análise de Dados (prepara_dados.py)

Este módulo contém funções para manipulação e inserção de dados de impressoras em um banco de dados a partir de arquivos CSV.

Funções:
- salva_dados_csv(DateTimeStart, DateTimeEnd): Salva os dados do webservice em arquivos CSV para um intervalo de datas.
- gera_arquivo_csv_compilado(pasta): Gera um arquivo CSV compilado a partir de vários arquivos CSV em uma pasta.
- preenche_dados_csv(caminho_csv, data_inicial, data_final, data_inicial_bi): Preenche os dados de um arquivo CSV com informações de impressoras e datas.
- df_impressoras(): Lê os dados de impressoras de um arquivo CSV específico.

## Exclusão de Dados Temporários (exclue_dados.py)

Este script exclui todos os arquivos temporários da pasta temp.

Funções:
- excluir_arquivos_recursivamente(pasta): Exclui todos os arquivos dentro de uma pasta de forma recursiva.

## Visualização de Dados (analise_graficos.py)

Este módulo cria um aplicativo Dash para visualização de dados de impressoras.

Funções:
- update_graph(start_date, end_date, selected_printers, selected_serials): Atualiza o gráfico com base nos filtros selecionados.

Como Utilizar:
Scripts de Manipulação de Dados
prepara_dados.py

Este script realiza diversas operações de manipulação de dados, como salvar dados do webservice, gerar arquivos CSV compilados e preencher dados de impressoras.

Execute o script:

'''
python scripts/prepara_dados.py
'''

Análise e Visualização
analise_graficos.py

Este script cria um aplicativo Dash para visualizar dados de impressoras.

Execute o script:

'''
python scripts/analise_graficos.py
'''

Operações CRUD
crud.py


Este módulo contém funções para realizar operações CRUD no banco de dados.

Consultas SQL
queries.py

Este módulo contém consultas SQL usadas nas operações CRUD.

Modelos
models.py

Este módulo define classes que representam os modelos de dados do banco de dados.

Serviço Web
webservice.py

Este módulo contém funções para interagir com um serviço da web SOAP para recuperar dados.

Licença
Este projeto está licenciado sob a Licença MIT.
