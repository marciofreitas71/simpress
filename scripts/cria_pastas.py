import os

def criar_pastas_projeto():
    """
    Cria os diretórios necessários para o projeto, se eles não existirem.

    Os diretórios a serem criados são:
    - 'temp/dados_compilados'
    - 'temp/dados_diarios'
    """
    diretorios = [
        'temp/dados_compilados',
        'temp/dados_diarios'
    ]

    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        print(f'Diretório "{diretorio}" criado ou já existe.')

if __name__ == "__main__":
    # Executa a função para criar os diretórios do projeto
    criar_pastas_projeto()
