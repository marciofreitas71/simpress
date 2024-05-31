# Simpress

## Automação para registrar contagem diária de impressões.

Este projeto tem como objetivo disponibilizar no BI as informações sobre as impressões na Simpress. 

### Credenciais
Para evitar a exposição das credenciais foram criados os arquivos .env e config.py. 
- **arquivo .env**: O arquivo .env é utilizado para armazenar de forma segura as credenciais do banco de dados, protegendo informações sensíveis fora do código-fonte. A biblioteca dotenv carrega essas variáveis durante a execução do aplicativo, garantindo acesso seguro. Para manter o .env fora do controle de versão, foi compartilhado no repositório apenas um modelo (.env.exemplo) para indicar variáveis sem expor valores reais.
- **arquivo config.py**:
O arquivo config.py armazena as credenciais do webservice, como chaves de API, protegendo informações sensíveis fora do código-fonte. Ao acessar essas credenciais no código por meio da importação do arquivo, recomenda-se não rastreá-lo no controle de versão. Para orientação, crie um modelo, por exemplo, config_exemplo.py, indicando variáveis essenciais sem expor valores reais.

### Dependências

Para instalar as dependências necessárias, utilize o arquivo requirements.txt. Execute o seguinte comando em seu ambiente virtual para garantir a correta instalação:  
```
pip install -r requirements.txt
```
Certifique-se de que seu ambiente virtual esteja ativado antes de executar este comando. Isso garantirá que as versões corretas das dependências sejam instaladas, facilitando a gestão de pacotes e evitando conflitos.