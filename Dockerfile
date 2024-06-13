# Use uma imagem base oficial do Python
FROM python:3.12

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do projeto para o diretório de trabalho
COPY . .

# Comando para rodar a aplicação
CMD ["python", "main.py"]
