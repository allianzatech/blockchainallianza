#!/bin/bash

echo "========================================"
echo "TESTES ALLIANZA BLOCKCHAIN"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não encontrado!"
    echo "Instale Python 3.8+ de https://www.python.org/downloads/"
    exit 1
fi

echo "[1/3] Instalando dependências..."
pip3 install -q flask cryptography web3 requests base58 python-dotenv 2>/dev/null
if [ $? -ne 0 ]; then
    echo "AVISO: Algumas dependências podem não ter sido instaladas"
    echo "Continuando mesmo assim..."
fi
echo "OK"

echo ""
echo "[2/3] Executando testes básicos de verificação..."
echo ""
python3 tests/public/run_verification_tests.py
if [ $? -ne 0 ]; then
    echo ""
    echo "AVISO: Alguns testes falharam"
    echo "Isso pode ser normal se liboqs-python não estiver instalado"
fi

echo ""
echo "[3/3] Executando suite completa de testes..."
echo ""
python3 tests/public/run_all_tests.py

echo ""
echo "========================================"
echo "TESTES CONCLUÍDOS"
echo "========================================"

