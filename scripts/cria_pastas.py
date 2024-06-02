import os

def criar_pastas_projeto():
    diretorios = [
        'temp/dados_compilados',
        'temp/dados_diarios'
    ]

    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        print(f'Diretório "{diretorio}" criado ou já existe.')

if __name__ == "__main__":
    criar_pastas_projeto()
