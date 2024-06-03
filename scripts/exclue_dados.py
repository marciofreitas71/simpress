import os
import shutil

def excluir_arquivos_recursivamente(pasta):
    """
    Exclui todos os arquivos dentro de uma pasta de forma recursiva.

    Args:
        pasta (str): O caminho da pasta onde os arquivos serão excluídos.
    """
    for root, dirs, files in os.walk(pasta):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f'{file_path} excluído com sucesso.')
            except Exception as e:
                print(f'Erro ao excluir {file_path}: {e}')
            

if __name__ == "__main__":
    # Executa a função para excluir arquivos na pasta 'temp' recursivamente
    excluir_arquivos_recursivamente('temp')
