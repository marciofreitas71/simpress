#!/bin/bash

# Função para criar diretórios necessários
criar_diretorios() {
    diretorios=(
        "site/assets"
        "site/css"
        "site/img"
        "site/js"
        "temp/dados_compilados"
        "temp/dados_diarios"
    )

    for diretorio in "${diretorios[@]}"; do
        mkdir -p "$diretorio"
        if [[ -d "$diretorio" ]]; then
            echo "Diretório '$diretorio' criado ou já existe."
        else
            echo "Erro ao criar o diretório '$diretorio'."
            exit 1
        fi
    done
}

# Função para detectar o comando Python correto
detectar_python() {
    if command -v python3 &>/dev/null; then
        echo "python3"
    elif command -v python &>/dev/null; then
        echo "python"
    else
        echo "Nenhuma instalação do Python encontrada."
        exit 1
    fi
}

# Função para criar e ativar o ambiente virtual
criar_venv() {
    local python_cmd
    python_cmd=$(detectar_python)

    $python_cmd -m venv venv
    if [[ -d "venv" ]]; then
        echo "Ambiente virtual criado."
    else
        echo "Erro ao criar o ambiente virtual."
        exit 1
    fi

    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        echo "Sistema operacional não suportado para ativação automática do ambiente virtual."
        return
    fi

    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "Ambiente virtual ativado."
    else
        echo "Erro ao ativar o ambiente virtual."
        exit 1
    fi
}

# Função para instalar dependências do projeto
instalar_dependencias() {
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        if [[ $? -eq 0 ]]; then
            echo "Dependências instaladas."
        else
            echo "Erro ao instalar as dependências."
            exit 1
        fi
    else
        echo "Arquivo requirements.txt não encontrado."
    fi
}

# Função para configurar o PYTHONPATH do projeto
configurar_pythonpath() {
    PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    OS="$(uname -s)"

    case "$OS" in
        Linux*|Darwin*)    
            export PYTHONPATH="$PROJECT_PATH:$PYTHONPATH"
            echo "PYTHONPATH configurado para $PYTHONPATH"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            PROJECT_PATH_WIN=$(cygpath -w "$PROJECT_PATH")
            export PYTHONPATH="$PROJECT_PATH_WIN;$PYTHONPATH"
            echo "PYTHONPATH configurado para $PYTHONPATH"
            ;;
        *)
            echo "Sistema operacional desconhecido, não foi possível configurar o PYTHONPATH"
            exit 1
            ;;
    esac

    if python -c "import sys; assert '$PROJECT_PATH' in sys.path" &>/dev/null; then
        echo "PYTHONPATH configurado corretamente."
    else
        echo "Erro ao configurar o PYTHONPATH."
        exit 1
    fi
}

criar_diretorios
criar_venv
instalar_dependencias
configurar_pythonpath

echo "Setup concluído com sucesso."