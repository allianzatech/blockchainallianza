#!/usr/bin/env python3
"""
📝 Script para atualizar o arquivo .env com as variáveis do bridge Allianza
"""

import os
import re
from pathlib import Path

def update_env_file(bridge_address: str, bridge_balance: str = "1000000.0"):
    """Atualiza o arquivo .env com as variáveis do bridge"""
    
    env_path = Path(".env")
    
    # Ler arquivo .env existente
    env_vars = {}
    comments = []
    sections = {}
    current_section = None
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()
                
                # Capturar comentários e seções
                if line.strip().startswith('#') or not line.strip():
                    if line.strip().startswith('#') and ('=' not in line):
                        # É um comentário de seção
                        if current_section is None:
                            current_section = line.strip()
                            sections[current_section] = []
                        comments.append(line)
                    else:
                        comments.append(line)
                    continue
                
                # Processar variáveis
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remover duplicatas (manter última ocorrência)
                    env_vars[key] = value
                    
                    # Adicionar à seção atual
                    if current_section:
                        sections[current_section].append(f"{key}={value}")
    
    # Adicionar/atualizar variáveis do bridge
    env_vars['ALLIANZA_BRIDGE_ADDRESS'] = bridge_address
    env_vars['ALLIANZA_BRIDGE_INITIAL_BALANCE'] = bridge_balance
    
    # Criar conteúdo organizado
    content = []
    
    # Adicionar cabeçalho
    content.append("# =============================================================================")
    content.append("# ALLIANZA BLOCKCHAIN - VARIÁVEIS DE AMBIENTE")
    content.append("# =============================================================================")
    content.append("# ⚠️  MANTENHA ESTE ARQUIVO SECRETO! NÃO COMMITE NO GIT!")
    content.append("")
    
    # Seção: Flask Configuration
    content.append("# =============================================================================")
    content.append("# FLASK CONFIGURATION")
    content.append("# =============================================================================")
    content.append("FLASK_ENV=development")
    content.append("FLASK_DEBUG=True")
    if 'SECRET_KEY' not in env_vars:
        content.append("# SECRET_KEY será gerado automaticamente se não configurado")
    else:
        content.append(f"SECRET_KEY={env_vars.get('SECRET_KEY', '')}")
    content.append("")
    
    # Seção: Allianza Bridge Configuration
    content.append("# =============================================================================")
    content.append("# ALLIANZA BRIDGE CONFIGURATION")
    content.append("# =============================================================================")
    content.append("# Endereço Allianza usado para transferências cross-chain")
    content.append(f"ALLIANZA_BRIDGE_ADDRESS={bridge_address}")
    content.append(f"ALLIANZA_BRIDGE_INITIAL_BALANCE={bridge_balance}")
    content.append("# Opcional: Chave privada do bridge (formato PEM)")
    content.append("# ALLIANZA_BRIDGE_PRIVATE_KEY=<sua_chave_privada_pem>")
    content.append("")
    
    # Seção: Blockchain APIs (Testnet)
    content.append("# =============================================================================")
    content.append("# BLOCKCHAIN APIs (TESTNET)")
    content.append("# =============================================================================")
    if 'BLOCKCYPHER_API_TOKEN' in env_vars:
        content.append(f"BLOCKCYPHER_API_TOKEN={env_vars['BLOCKCYPHER_API_TOKEN']}")
    if 'BITCOIN_PRIVATE_KEY' in env_vars:
        content.append(f"BITCOIN_PRIVATE_KEY={env_vars['BITCOIN_PRIVATE_KEY']}")
    if 'BITCOIN_TESTNET_ADDRESS' in env_vars:
        content.append(f"BITCOIN_TESTNET_ADDRESS={env_vars['BITCOIN_TESTNET_ADDRESS']}")
    content.append("")
    
    # Seção: EVM Chains (Testnet)
    content.append("# =============================================================================")
    content.append("# EVM CHAINS (TESTNET)")
    content.append("# =============================================================================")
    
    # Ethereum
    if 'ETH_RPC_URL' in env_vars:
        content.append(f"ETH_RPC_URL={env_vars['ETH_RPC_URL']}")
    elif 'REAL_ETH_PRIVATE_KEY' in env_vars:
        content.append(f"ETH_RPC_URL=https://sepolia.infura.io/v3/{env_vars.get('INFURA_PROJECT_ID', 'YOUR_KEY')}")
    if 'REAL_ETH_PRIVATE_KEY' in env_vars:
        content.append(f"ETH_PRIVATE_KEY={env_vars['REAL_ETH_PRIVATE_KEY']}")
    content.append("")
    
    # Polygon
    if 'POLYGON_RPC_URL' in env_vars:
        content.append(f"POLYGON_RPC_URL={env_vars['POLYGON_RPC_URL']}")
    if 'POLYGON_PRIVATE_KEY' in env_vars:
        content.append(f"POLYGON_PRIVATE_KEY={env_vars['POLYGON_PRIVATE_KEY']}")
    if 'POLYGON_MASTER_WALLET' in env_vars:
        content.append(f"POLYGON_MASTER_WALLET={env_vars['POLYGON_MASTER_WALLET']}")
    if 'POLYGON_MASTER_PRIVATE_KEY' in env_vars:
        content.append(f"POLYGON_MASTER_PRIVATE_KEY={env_vars['POLYGON_MASTER_PRIVATE_KEY']}")
    content.append("")
    
    # Base
    if 'BASE_RPC_URL' in env_vars:
        content.append(f"BASE_RPC_URL={env_vars['BASE_RPC_URL']}")
    if 'BASE_ADDRESS' in env_vars:
        content.append(f"BASE_ADDRESS={env_vars['BASE_ADDRESS']}")
    if 'BASE_PRIVATE_KEY' in env_vars:
        content.append(f"BASE_PRIVATE_KEY={env_vars['BASE_PRIVATE_KEY']}")
    content.append("")
    
    # Seção: Solana (Testnet)
    content.append("# =============================================================================")
    content.append("# SOLANA (TESTNET)")
    content.append("# =============================================================================")
    if 'SOLANA_RPC_URL' in env_vars:
        content.append(f"SOLANA_RPC_URL={env_vars['SOLANA_RPC_URL']}")
    if 'SOLANA_ADDRESS' in env_vars:
        content.append(f"SOLANA_ADDRESS={env_vars['SOLANA_ADDRESS']}")
    if 'SOLANA_PRIVATE_KEY' in env_vars:
        content.append(f"SOLANA_PRIVATE_KEY={env_vars['SOLANA_PRIVATE_KEY']}")
    content.append("")
    
    # Seção: Infura/BlockCypher
    content.append("# =============================================================================")
    content.append("# INFURA / BLOCKCYPHER")
    content.append("# =============================================================================")
    if 'INFURA_PROJECT_ID' in env_vars:
        content.append(f"INFURA_PROJECT_ID={env_vars['INFURA_PROJECT_ID']}")
    if 'INFURA_PROJECT_SECRET' in env_vars:
        content.append(f"INFURA_PROJECT_SECRET={env_vars['INFURA_PROJECT_SECRET']}")
    content.append("")
    
    # Seção: Bridge Contracts (se existirem)
    bridge_contracts = []
    for key in ['BRIDGE_CONTRACT_ETH', 'BRIDGE_CONTRACT_POLY', 'ALZ_CONTRACT_POLYGON']:
        if key in env_vars and env_vars[key]:
            bridge_contracts.append(key)
    
    if bridge_contracts:
        content.append("# =============================================================================")
        content.append("# BRIDGE CONTRACTS")
        content.append("# =============================================================================")
        for key in bridge_contracts:
            content.append(f"{key}={env_vars[key]}")
        content.append("")
    
    # Seção: Outras configurações
    other_keys = set(env_vars.keys()) - {
        'FLASK_ENV', 'FLASK_DEBUG', 'SECRET_KEY',
        'ALLIANZA_BRIDGE_ADDRESS', 'ALLIANZA_BRIDGE_INITIAL_BALANCE',
        'BLOCKCYPHER_API_TOKEN', 'BITCOIN_PRIVATE_KEY', 'BITCOIN_TESTNET_ADDRESS',
        'ETH_RPC_URL', 'ETH_PRIVATE_KEY', 'REAL_ETH_PRIVATE_KEY',
        'POLYGON_RPC_URL', 'POLYGON_PRIVATE_KEY', 'POLYGON_MASTER_WALLET', 'POLYGON_MASTER_PRIVATE_KEY',
        'BASE_RPC_URL', 'BASE_ADDRESS', 'BASE_PRIVATE_KEY',
        'SOLANA_RPC_URL', 'SOLANA_ADDRESS', 'SOLANA_PRIVATE_KEY',
        'INFURA_PROJECT_ID', 'INFURA_PROJECT_SECRET',
        'BRIDGE_CONTRACT_ETH', 'BRIDGE_CONTRACT_POLY', 'ALZ_CONTRACT_POLYGON',
        'BLOCKCHAIN_MODE', 'ENCRYPTION_KEY', 'REAL_POLY_PRIVATE_KEY', 'REAL_BRIDGE_OWNER', 'POLY_RPC_URL'
    }
    
    if other_keys:
        content.append("# =============================================================================")
        content.append("# OUTRAS CONFIGURAÇÕES")
        content.append("# =============================================================================")
        for key in sorted(other_keys):
            if env_vars[key]:  # Só adicionar se não estiver vazio
                content.append(f"{key}={env_vars[key]}")
        content.append("")
    
    # Escrever arquivo
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Arquivo .env atualizado com sucesso!")
    print(f"📍 Bridge Address: {bridge_address}")
    print(f"💰 Saldo inicial: {bridge_balance} ALZ")

if __name__ == "__main__":
    import sys
    
    # Obter endereço bridge do argumento ou gerar
    if len(sys.argv) > 1:
        bridge_address = sys.argv[1]
    else:
        # Tentar ler do output do script anterior ou usar padrão
        bridge_address = "1BCLZRNRohVyG4X24WRarBCREYF5iDNKv11ivZZYNLuFKv86iz"
    
    bridge_balance = sys.argv[2] if len(sys.argv) > 2 else "1000000.0"
    
    update_env_file(bridge_address, bridge_balance)


