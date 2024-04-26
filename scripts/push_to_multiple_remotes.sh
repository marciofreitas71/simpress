#!/bin/bash

# Verifica se o argumento para a branch foi fornecido
if [ -z "$1" ]; then
    echo "Por favor, forneça o nome da branch."
    exit 1
fi

# Nome da branch
branch="$1"

# Push para o primeiro repositório remoto (GitHub)
echo "Enviando para o repositório GitHub..."
git push github "$branch"

# Push para o segundo repositório remoto (GitLab)
echo "Enviando para o repositório GitLab..."
git push gitlab "$branch"

echo "Envio concluído para ambos os repositórios remotos."
