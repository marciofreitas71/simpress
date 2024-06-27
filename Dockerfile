# Usar uma imagem base oficial do Python
FROM python:3.12

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências primeiro, para aproveitar o cache de camadas
COPY requirements.txt ./

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código fonte do projeto para o diretório de trabalho
COPY . .

# Comando para rodar a aplicação
CMD ["python", "main.py"]d