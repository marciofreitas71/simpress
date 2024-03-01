# Use a imagem base do Python
FROM python:3.12

RUN mkdir app

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os scripts Python para o diretório de trabalho
COPY . /app/


# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Comando para executar o script
CMD ["python", "simpress_print.py"]