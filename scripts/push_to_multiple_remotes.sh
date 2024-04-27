#!/bin/bash

# Captura os nomes das branches remotas
branches=$(git branch -r | awk -F'/' '{print $NF}')

# Verifica se existem branches remotas
if [ -z "$branches" ]; then
    echo "Nenhuma branch remota encontrada. Saindo do script."
    exit 1
fi

# Itera sobre os nomes das branches e envia para todos os repositórios
for branch in $branches; do
    # Remove espaços em branco adicionais, se houver
    branch=$(echo $branch | tr -d '[:space:]')
    
    echo "Enviando para a branch remota: $branch"

    # Verifica se a branch remota existe
    if git ls-remote --heads github | grep -q "refs/heads/$branch"; then
        echo "Enviando para o repositório GitHub..."
        git push github "$branch"
    else
        echo "A branch remota $branch não existe no repositório GitHub."
    fi

    if git ls-remote --heads gitlab | grep -q "refs/heads/$branch"; then
        echo "Enviando para o repositório GitLab..."
        git push gitlab "$branch"
    else
        echo "A branch remota $branch não existe no repositório GitLab."
    fi

    echo "Envio concluído para a branch remota: $branch"
done

echo "Envio concluído para todas as branches remotas."
