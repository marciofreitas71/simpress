# Use a imagem oficial do Python como base
FROM python:3.10.10

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação estará ouvindo (se necessário)
EXPOSE 5000

# Comando para executar a aplicação quando o contêiner for iniciado
CMD ["python", "simpress_print.py"]
