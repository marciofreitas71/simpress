#!/bin/bash

# Função para criar diretórios necessários
criar_diretorios() {
    # Lista de diretórios a serem criados
    diretorios=(
        "site/assets"
        "site/css"
        "site/img"
        "site/js"
        "temp/dados_compilados"
        "temp/dados_diarios"
    )

    # Cria cada diretório na lista
    for diretorio in "${diretorios[@]}"; do
        mkdir -p "$diretorio"  # Cria o diretório, incluindo pais se necessário
        if [[ -d "$diretorio" ]]; then  # Verifica se o diretório foi criado com sucesso
            echo "Diretório '$diretorio' criado ou já existe."
        else
            echo "Erro ao criar o diretório '$diretorio'."  # Exibe mensagem de erro se a criação falhar
            exit 1  # Sai do script com status de erro
        fi
    done
}

# Função para detectar o comando Python correto
detectar_python() {
    if command -v python3 &>/dev/null; then
        echo "python3"  # Retorna "python3" se estiver disponível
    elif command -v python &>/dev/null; then
        echo "python"  # Retorna "python" se estiver disponível
    else
        echo "Nenhuma instalação do Python encontrada."  # Exibe mensagem de erro se nenhuma instalação do Python for encontrada
        exit 1  # Sai do script com status de erro
    fi
}

# Função para criar e ativar o ambiente virtual
criar_venv() {
    local python_cmd
    python_cmd=$(detectar_python)  # Detecta o comando Python correto

    $python_cmd -m venv venv  # Cria o ambiente virtual
    if [[ -d "venv" ]]; then  # Verifica se o ambiente virtual foi criado com sucesso
        echo "Ambiente virtual criado."
    else
        echo "Erro ao criar o ambiente virtual."  # Exibe mensagem de erro se a criação falhar
        exit 1  # Sai do script com status de erro
    fi

    # Ativa o ambiente virtual com base no sistema operacional
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate  # Ativa no Linux ou macOS
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate  # Ativa no Windows
    else
        echo "Sistema operacional não suportado para ativação automática do ambiente virtual."
        return
    fi

    # Verifica se o ambiente virtual foi ativado com sucesso
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "Ambiente virtual ativado."
    else
        echo "Erro ao ativar o ambiente virtual."  # Exibe mensagem de erro se a ativação falhar
        exit 1  # Sai do script com status de erro
    fi
}

# Função para instalar dependências do projeto
instalar_dependencias() {
    if [[ -f "requirements.txt" ]]; then  # Verifica se o arquivo requirements.txt existe
        pip install -r requirements.txt  # Instala as dependências listadas no requirements.txt
        if [[ $? -eq 0 ]]; then  # Verifica se a instalação foi bem-sucedida
            echo "Dependências instaladas."
        else
            echo "Erro ao instalar as dependências."  # Exibe mensagem de erro se a instalação falhar
            exit 1  # Sai do script com status de erro
        fi
    else
        echo "Arquivo requirements.txt não encontrado."  # Exibe mensagem de erro se o arquivo não for encontrado
    fi
}

# Função para configurar o PYTHONPATH do projeto
configurar_pythonpath() {
    # Obtém o diretório onde o script está localizado
    PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    # Identifica o sistema operacional
    OS="$(uname -s)"

    # Configura o PYTHONPATH com base no sistema operacional
    case "$OS" in
        Linux*|Darwin*)    
            export PYTHONPATH="$PROJECT_PATH:$PYTHONPATH"
            echo "PYTHONPATH configurado para $PYTHONPATH"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            export PYTHONPATH="$PROJECT_PATH;$PYTHONPATH"
            echo "PYTHONPATH configurado para $PYTHONPATH"
            ;;
        *)
            echo "Sistema operacional desconhecido, não foi possível configurar o PYTHONPATH"  # Exibe mensagem de erro se o SO não for suportado
            exit 1  # Sai do script com status de erro
            ;;
    esac

    # Verifica se o PYTHONPATH foi configurado corretamente
    if python -c "import sys; assert '$PROJECT_PATH' in sys.path" &>/dev/null; then
        echo "PYTHONPATH configurado corretamente."
    else
        echo "Erro ao configurar o PYTHONPATH."  # Exibe mensagem de erro se a configuração falhar
        exit 1  # Sai do script com status de erro
    fi
}

# Execução das funções principais do script
criar_diretorios  # Cria os diretórios necessários
criar_venv  # Cria e ativa o ambiente virtual
configurar_pythonpath  # Configura o PYTHONPATH
instalar_dependencias  # Instala as dependências do projeto

echo "Setup concluído com sucesso."  # Exibe mensagem de sucesso ao final do script
