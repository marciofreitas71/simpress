# Projeto de Análise de Dados de Impressoras

Este projeto é uma aplicação completa que realiza a manipulação, análise e visualização de dados de impressoras. Ele também integra um serviço da web para recuperar dados, permitindo uma análise abrangente dos dados coletados.

## Estrutura do Projeto

- **app/**: Contém módulos principais para configuração, operações CRUD e integração com o serviço da web.
  - **config.py**: Configuração e conexão com o banco de dados.
  - **crud.py**: Funções CRUD para manipulação de dados no banco de dados.
  - **webservice.py**: Funções para integração com o serviço da web SOAP.

- **credenciais/**: Contém informações de configuração e credenciais.

- **scripts/**: Contém scripts para manipulação e análise de dados.
  - **prepara_dados.py**: Manipulação de dados e geração de arquivos CSV.
  - **analise_graficos.py**: Visualização de dados usando Dash.

- **site/**: Contém arquivos para o site.

- **temp/**: Contém dados temporários gerados pelos scripts.

- **testes/**: Scripts de teste.

- **utils/**: Utilitários auxiliares.

## Configuração

### Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
user_name=<SEU_USUARIO>
password=<SUA_SENHA>
host=<SEU_HOST>
port=<SUA_PORTA>
service_name=<SEU_SERVICE_NAME>
```

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

## Funcionalidade

### Configuração e Conexão

**config.py**

Este módulo configura os caminhos e estabelece a conexão com o banco de dados Oracle. As credenciais e detalhes de conexão são carregados a partir de um arquivo `.env`.

### Operações CRUD

**crud.py**

Este módulo define operações CRUD para manipulação dos dados no banco de dados, como criar, ler, atualizar e excluir registros de impressoras e contagens de impressoras.

- **create_impressora**: Cria uma nova impressora no banco de dados.
- **create_contagem_impressoras**: Registra uma contagem de impressoras no banco de dados.
- **read_contagem_impressoras**: Lê os registros de contagem de impressoras do banco de dados.
- **update_contagem_impressora**: Atualiza os registros de contagem de impressoras no banco de dados.
- **delete_contagem_impressora**: Exclui os registros de contagem de impressoras do banco de dados.
- **delete_all_registros**: Exclui todos os registros de contagem de impressoras do banco de dados.
- **delete_all_impressoras**: Exclui todas as impressoras do banco de dados.
- **read_impressoras_data**: Lê os registros de contagem de impressoras do banco de dados para uma determinada data.

### Consultas SQL

**queries.py**

Este módulo contém consultas SQL utilizadas nas operações CRUD.

### Modelos

**models.py**

Este módulo define classes que representam os modelos de dados do banco de dados.

- **ContagemImpressoras**: Representa uma contagem de impressoras.
- **Impressoras**: Representa uma impressora.

### Serviço Web

**webservice.py**

Este módulo fornece funcionalidades para recuperar dados de um serviço da web SOAP, utilizando bibliotecas como SQLAlchemy, dotenv, pandas e zeep.

- **recuperar_dados**: Recupera dados de um serviço da web SOAP e retorna um DataFrame Pandas com os dados.

### Manipulação e Análise de Dados

**prepara_dados.py**

Este script realiza diversas operações de manipulação de dados, como salvar dados do webservice, gerar arquivos CSV compilados e preencher dados de impressoras.

- **salva_dados_csv**: Salva os dados do webservice em arquivos CSV para um intervalo de datas.
- **gera_arquivo_csv_compilado**: Gera um arquivo CSV compilado a partir de vários arquivos CSV em uma pasta.
- **preenche_dados_csv**: Preenche os dados de um arquivo CSV com informações de impressoras e datas.
- **df_impressoras**: Lê os dados de impressoras de um arquivo CSV específico.

### Visualização de Dados

**analise_graficos.py**

Este script cria um aplicativo Dash para visualizar dados de impressoras, permitindo a seleção interativa de impressoras e a visualização das contagens de impressões ao longo do tempo.

- **atualizar_grafico**: Atualiza o gráfico com base na impressora selecionada.

## Uso
- Scripts de Manipulação de Dados
    - prepara_dados.py: Este script realiza diversas operações de manipulação de dados, como salvar dados do webservice, gerar arquivos CSV compilados e preencher dados de impressoras.

Execute o script:

```
python scripts/prepara_dados.py
```
## Análise e Visualização
- analise_graficos.py: Este script cria um aplicativo Dash para visualizar dados de impressoras.

Execute o script:
```
python scripts/analise_graficos.py
```
## Operações CRUD
- crud.py: Este módulo contém funções para realizar operações CRUD no banco de dados.

## Consultas SQL
- queries.py: Este módulo contém consultas SQL usadas nas operações CRUD.

## Modelos
- models.py: Este módulo define classes que representam os modelos de dados do banco de dados.

## Serviço Web
- webservice.py: Este módulo contém funções para interagir com um serviço da web SOAP para recuperar dados.

## Licença:
Este projeto está licenciado sob a Licença MIT.