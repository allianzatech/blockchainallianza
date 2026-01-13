#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 Script de Verificação de Transações On-Chain - Allianza Blockchain
Verifica transações reais em blockchains públicas
"""

import json
import sys
import argparse
import requests
from pathlib import Path
from datetime import datetime

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def verify_bitcoin_transaction(tx_hash):
    """Verifica transação Bitcoin no Blockstream"""
    print_info(f"Verificando transação Bitcoin: {tx_hash}")
    
    url = f"https://blockstream.info/testnet/api/tx/{tx_hash}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Transação encontrada no Blockstream")
            print_info(f"  Block: {data.get('status', {}).get('block_height', 'N/A')}")
            print_info(f"  Confirmations: {data.get('status', {}).get('block_height', 'N/A')}")
            print_info(f"  Explorer: https://blockstream.info/testnet/tx/{tx_hash}")
            return True
        else:
            print_error(f"Transação não encontrada (status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Erro ao verificar transação: {e}")
        return False

def verify_ethereum_transaction(tx_hash):
    """Verifica transação Ethereum no Etherscan"""
    print_info(f"Verificando transação Ethereum: {tx_hash}")
    
    # Remover 0x se presente
    tx_hash_clean = tx_hash.replace('0x', '')
    
    url = f"https://api-sepolia.etherscan.io/api"
    params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": tx_hash,
        "apikey": "YourApiKeyToken"  # Etherscan permite algumas requisições sem API key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('result') and data['result'] != None:
                print_success(f"Transação encontrada no Etherscan")
                print_info(f"  Explorer: https://sepolia.etherscan.io/tx/{tx_hash}")
                return True
            else:
                print_warning(f"Transação não encontrada ou ainda não confirmada")
                print_info(f"  Explorer: https://sepolia.etherscan.io/tx/{tx_hash}")
                return False
        else:
            print_error(f"Erro ao verificar transação (status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Erro ao verificar transação: {e}")
        return False

def verify_polygon_transaction(tx_hash):
    """Verifica transação Polygon no Polygonscan"""
    print_info(f"Verificando transação Polygon: {tx_hash}")
    
    url = f"https://api-amoy.polygonscan.com/api"
    params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": tx_hash,
        "apikey": "YourApiKeyToken"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('result') and data['result'] != None:
                print_success(f"Transação encontrada no Polygonscan")
                print_info(f"  Explorer: https://amoy.polygonscan.com/tx/{tx_hash}")
                return True
            else:
                print_warning(f"Transação não encontrada ou ainda não confirmada")
                print_info(f"  Explorer: https://amoy.polygonscan.com/tx/{tx_hash}")
                return False
        else:
            print_error(f"Erro ao verificar transação (status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Erro ao verificar transação: {e}")
        return False

def load_proofs_file():
    """Carrega arquivo de provas on-chain"""
    proof_file = Path("VERIFIABLE_ON_CHAIN_PROOFS.md")
    
    if not proof_file.exists():
        print_error("Arquivo VERIFIABLE_ON_CHAIN_PROOFS.md não encontrado")
        return None
    
    with open(proof_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair hashes Bitcoin (64 caracteres hex)
    bitcoin_hashes = []
    for line in content.split('\n'):
        line = line.strip()
        if len(line) == 64 and all(c in '0123456789abcdef' for c in line.lower()):
            bitcoin_hashes.append(line)
    
    # Extrair hashes Ethereum (0x seguido de 64 caracteres)
    ethereum_hashes = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('0x') and len(line) == 66:
            ethereum_hashes.append(line)
    
    # Extrair hashes Polygon (mesmo formato que Ethereum)
    polygon_hashes = []
    # Podemos usar a mesma lógica, mas vamos procurar especificamente por Polygon
    in_polygon_section = False
    for line in content.split('\n'):
        if 'Polygon' in line or 'polygon' in line:
            in_polygon_section = True
        if in_polygon_section and line.strip().startswith('0x') and len(line.strip()) == 66:
            polygon_hashes.append(line.strip())
    
    return {
        'bitcoin': bitcoin_hashes,
        'ethereum': ethereum_hashes,
        'polygon': polygon_hashes
    }

def verify_all_transactions(chain=None):
    """Verifica todas as transações"""
    print_header("VERIFICAÇÃO DE TRANSAÇÕES ON-CHAIN")
    
    proofs = load_proofs_file()
    if not proofs:
        return False
    
    results = {}
    
    # Verificar Bitcoin
    if not chain or chain == 'bitcoin':
        print_header("VERIFICANDO TRANSAÇÕES BITCOIN")
        bitcoin_results = []
        for tx_hash in proofs['bitcoin']:
            result = verify_bitcoin_transaction(tx_hash)
            bitcoin_results.append(result)
        results['bitcoin'] = all(bitcoin_results)
        print()
    
    # Verificar Ethereum
    if not chain or chain == 'ethereum':
        print_header("VERIFICANDO TRANSAÇÕES ETHEREUM")
        ethereum_results = []
        for tx_hash in proofs['ethereum']:
            result = verify_ethereum_transaction(tx_hash)
            ethereum_results.append(result)
        results['ethereum'] = all(ethereum_results)
        print()
    
    # Verificar Polygon
    if not chain or chain == 'polygon':
        print_header("VERIFICANDO TRANSAÇÕES POLYGON")
        polygon_results = []
        for tx_hash in proofs['polygon']:
            result = verify_polygon_transaction(tx_hash)
            polygon_results.append(result)
        results['polygon'] = all(polygon_results)
        print()
    
    # Relatório final
    print_header("RELATÓRIO FINAL")
    
    all_passed = True
    for chain_name, result in results.items():
        if result:
            print_success(f"{chain_name.upper()}: Todas as transações verificadas")
        else:
            print_warning(f"{chain_name.upper()}: Algumas transações não puderam ser verificadas")
            all_passed = False
    
    return all_passed

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Verifica transações on-chain')
    parser.add_argument('--chain', choices=['bitcoin', 'ethereum', 'polygon'], 
                       help='Verificar apenas uma blockchain específica')
    parser.add_argument('--tx', type=str, help='Verificar uma transação específica')
    
    args = parser.parse_args()
    
    if args.tx:
        # Verificar transação específica
        tx_hash = args.tx
        if len(tx_hash) == 64:
            # Bitcoin
            verify_bitcoin_transaction(tx_hash)
        elif tx_hash.startswith('0x') and len(tx_hash) == 66:
            # Ethereum ou Polygon
            if args.chain == 'polygon':
                verify_polygon_transaction(tx_hash)
            else:
                verify_ethereum_transaction(tx_hash)
        else:
            print_error("Formato de hash inválido")
            sys.exit(1)
    else:
        # Verificar todas as transações
        success = verify_all_transactions(args.chain)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
