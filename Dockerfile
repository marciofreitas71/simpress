# Use a imagem base do Python
FROM python:3.10.10

# Crie o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie os scripts Python para o diretório de trabalho
COPY simpress_print.py repository_gestao_impressoras.py config.py README.md /app/

# Comando para executar o script
CMD ["python", "simpress_print.py"]