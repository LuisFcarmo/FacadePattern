#!/bin/bash

set -e

VENV_ACTIVATE="venv/bin/activate"
    
if [ -f "$VENV_ACTIVATE" ]; then
    echo "Ativando o ambiente virtual..."
    source "$VENV_ACTIVATE"
else
    echo "Erro: Ambiente virtual 'venv' não encontrado."
    echo "Por favor, crie-o primeiro com o comando: python3 -m venv venv"
    exit 1
fi

echo "Iniciando o servidor FastAPI em http://127.0.0.1:8000"
uvicorn app.api.main:app --reload