import tkinter as tk
from tkinter import messagebox
import os
from sqlalchemy import create_engine

# Função para obter uma conexão com o banco de dados
def getConnection():
    # Conecta ao banco de dados Oracle
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')
    dsn = f"oracle+cx_oracle://{user_name}:{password}@{host}:{port}/{service_name}"
    return create_engine(dsn)

# Função para atualizar o banco de dados com os dados da impressora
def atualizar_banco_de_dados(localizacao, municipio, fila, modelo, serie, unidade):
    try:
        # Estabelecer conexão com o banco de dados
        engine = getConnection()

        # Inserir os dados da impressora no banco de dados
        with engine.connect() as connection:
            connection.execute("INSERT INTO impressoras (Localizacao, Municipio, Fila, Modelo, Serie, Unidade) VALUES (:1, :2, :3, :4, :5, :6)",
                               (localizacao, municipio, fila, modelo, serie, unidade))

        messagebox.showinfo("Sucesso", "Os dados da impressora foram atualizados no banco de dados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar o banco de dados: {str(e)}")

# Função para lidar com o clique do botão "Atualizar"
def atualizar():
    localizacao = entry_localizacao.get()
    municipio = entry_municipio.get()
    fila = entry_fila.get()
    modelo = entry_modelo.get()
    serie = entry_serie.get()
    unidade = entry_unidade.get()

    if localizacao and municipio and fila and modelo and serie and unidade:
        atualizar_banco_de_dados(localizacao, municipio, fila, modelo, serie, unidade)
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

# Criar a janela principal
root = tk.Tk()
root.title("Atualização de Impressoras")

# Criar os rótulos e campos de entrada para cada informação da impressora
tk.Label(root, text="Localização:").grid(row=0, column=0, padx=5, pady=5)
entry_localizacao = tk.Entry(root)
entry_localizacao.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Município:").grid(row=1, column=0, padx=5, pady=5)
entry_municipio = tk.Entry(root)
entry_municipio.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Fila:").grid(row=2, column=0, padx=5, pady=5)
entry_fila = tk.Entry(root)
entry_fila.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Modelo:").grid(row=3, column=0, padx=5, pady=5)
entry_modelo = tk.Entry(root)
entry_modelo.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Série:").grid(row=4, column=0, padx=5, pady=5)
entry_serie = tk.Entry(root)
entry_serie.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Unidade:").grid(row=5, column=0, padx=5, pady=5)
entry_unidade = tk.Entry(root)
entry_unidade.grid(row=5, column=1, padx=5, pady=5)

# Botão para atualizar os dados da impressora
btn_atualizar = tk.Button(root, text="Atualizar", command=atualizar)
btn_atualizar.grid(row=6, column=0, columnspan=2, pady=10)

# Iniciar a aplicação
root.mainloop()
