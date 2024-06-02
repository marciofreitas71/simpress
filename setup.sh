#!/bin/bash

# Função para criar diretórios
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
        echo "Diretório '$diretorio' criado ou já existe."
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
    echo "Ambiente virtual criado."

    # Ativar o ambiente virtual
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        echo "Sistema operacional não suportado para ativação automática do ambiente virtual."
        return
    fi
    echo "Ambiente virtual ativado."
}

# Função para instalar dependências
instalar_dependencias() {
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        echo "Dependências instaladas."
    else
        echo "Arquivo requirements.txt não encontrado."
    fi
}

# Execução das funções
criar_diretorios
criar_venv
instalar_dependencias
