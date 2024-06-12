#!/bin/bash

: <<'END_DOC'
Este script configura o ambiente de desenvolvimento para o projeto, executando as seguintes etapas:

1. Criação de diretórios necessários para a estrutura do projeto.
2. Detecção do comando Python correto (python3 ou python).
3. Criação e ativação de um ambiente virtual Python.
4. Instalação das dependências listadas no arquivo requirements.txt.
5. Configuração da variável de ambiente PYTHONPATH para incluir o caminho do projeto, garantindo que os módulos possam ser importados corretamente.

Cada função é cuidadosamente projetada para garantir que o ambiente esteja configurado corretamente e pronto para o desenvolvimento.
END_DOC

# Função para criar diretórios necessários
criar_diretorios() {
    # Lista dos diretórios a serem criados
    diretorios=(
        "site/assets"
        "site/css"
        "site/img"
        "site/js"
        "temp/dados_compilados"
        "temp/dados_diarios"
    )

    # Criação de cada diretório e verificação de sucesso
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
    # Verifica se python3 está instalado
    if command -v python3 &>/dev/null; then
        echo "python3"
    # Verifica se python está instalado
    elif command -v python &>/dev/null; then
        echo "python"
    else
        echo "Nenhuma instalação do Python encontrada."
        exit 1
    fi
}

# Função para criar e ativar o ambiente virtual
criar_venv() {
    # Detecta o comando Python correto
    local python_cmd
    python_cmd=$(detectar_python)

    # Cria o ambiente virtual
    $python_cmd -m venv venv
    if [[ -d "venv" ]]; then
        echo "Ambiente virtual criado."
    else
        echo "Erro ao criar o ambiente virtual."
        exit 1
    fi

    # Ativa o ambiente virtual dependendo do sistema operacional
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        echo "Sistema operacional não suportado para ativação automática do ambiente virtual."
        return
    fi

    # Verifica se o ambiente virtual foi ativado com sucesso
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "Ambiente virtual ativado."
    else
        echo "Erro ao ativar o ambiente virtual."
        exit 1
    fi
}

# Função para instalar dependências do projeto
instalar_dependencias() {
    # Verifica se o arquivo requirements.txt existe
    if [[ -f "requirements.txt" ]]; then
        # Instala as dependências listadas no arquivo requirements.txt
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
    # Obtém o caminho absoluto do diretório do projeto
    PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    # Detecta o sistema operacional
    OS="$(uname -s)"

    case "$OS" in
        Linux*|Darwin*)    
            # Configura o PYTHONPATH para sistemas Linux ou MacOS
            export PYTHONPATH="$PROJECT_PATH:$PYTHONPATH"
            echo "PYTHONPATH configurado para $PYTHONPATH"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            # Configura o PYTHONPATH para sistemas Windows
            PROJECT_PATH_WIN=$(cygpath -w "$PROJECT_PATH")
            export PYTHONPATH="$PROJECT_PATH_WIN;$PYTHONPATH"
            echo "PYTHONPATH configurado para $PYTHONPATH"
            ;;
        *)
            # Caso o sistema operacional não seja reconhecido
            echo "Sistema operacional desconhecido, não foi possível configurar o PYTHONPATH"
            exit 1
            ;;
    esac

    # Verifica se o PYTHONPATH foi configurado corretamente
    if python -c "import sys; assert '$PROJECT_PATH' in sys.path" &>/dev/null; then
        echo "PYTHONPATH configurado corretamente."
    else
        echo "Erro ao configurar o PYTHONPATH."
        exit 1
    fi
}

# Chama as funções definidas
criar_diretorios
criar_venv
instalar_dependencias
configurar_pythonpath

echo "Setup concluído com sucesso."
