#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICAR TODAS AS VARIÁVEIS DE AMBIENTE BITCOIN
Verifica todas as variáveis relacionadas a Bitcoin no sistema
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_all_bitcoin_env():
    """Verifica todas as variáveis de ambiente Bitcoin"""
    print(f"\n{'='*70}")
    print(f"🔍 VERIFICANDO TODAS AS VARIÁVEIS DE AMBIENTE BITCOIN")
    print(f"{'='*70}")
    
    # Lista de todas as variáveis Bitcoin possíveis
    bitcoin_vars = [
        'BITCOIN_PRIVATE_KEY',
        'BITCOIN_TESTNET_PRIVATE_KEY',
        'BTC_PRIVATE_KEY',
        'BITCOIN_ADDRESS',
        'BITCOIN_TESTNET_ADDRESS',
        'BTC_ADDRESS',
        'BITCOIN_BRIDGE_ADDRESS',
        'BLOCKCYPHER_API_TOKEN'
    ]
    
    print(f"\n📋 VARIÁVEIS DE AMBIENTE:")
    found_vars = {}
    
    for var in bitcoin_vars:
        value = os.getenv(var)
        if value:
            # Mascarar chaves privadas
            if 'PRIVATE_KEY' in var:
                display_value = f"{value[:10]}...{value[-5:]}" if len(value) > 15 else "***"
            else:
                display_value = value
            
            found_vars[var] = value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ⚠️  {var}: NÃO CONFIGURADA")
    
    print(f"\n{'='*70}")
    print(f"📊 ANÁLISE")
    print(f"{'='*70}")
    
    # Verificar qual chave privada será usada (ordem de prioridade)
    private_key = (
        os.getenv('BITCOIN_PRIVATE_KEY') or 
        os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or 
        os.getenv('BTC_PRIVATE_KEY')
    )
    
    if private_key:
        print(f"\n✅ Chave privada que será usada:")
        print(f"   Variável: {'BITCOIN_PRIVATE_KEY' if os.getenv('BITCOIN_PRIVATE_KEY') else 'BITCOIN_TESTNET_PRIVATE_KEY' if os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') else 'BTC_PRIVATE_KEY'}")
        print(f"   Chave: {private_key[:20]}... (tamanho: {len(private_key)})")
        
        # Verificar formato
        if private_key.startswith(('c', '9', '5', 'K', 'L')):
            print(f"   Formato: WIF ✅")
        elif len(private_key) == 64 or (private_key.startswith('0x') and len(private_key) == 66):
            print(f"   Formato: HEX ⚠️  (será convertido para WIF)")
        else:
            print(f"   Formato: DESCONHECIDO ❌")
        
        # Derivar endereço
        try:
            from bitcoinlib.keys import HDKey
            key = HDKey(private_key, network='testnet')
            derived_address = key.address()
            print(f"   Endereço derivado: {derived_address}")
            
            # Verificar saldo
            import requests
            balance_url = f"https://blockstream.info/testnet/api/address/{derived_address}"
            balance_resp = requests.get(balance_url, timeout=10)
            if balance_resp.status_code == 200:
                balance_data = balance_resp.json()
                funded = balance_data.get('chain_stats', {}).get('funded_txo_sum', 0)
                spent = balance_data.get('chain_stats', {}).get('spent_txo_sum', 0)
                balance = funded - spent
                print(f"   Saldo: {balance} satoshis ({balance/100000000:.8f} BTC)")
                
                if balance > 0:
                    print(f"   ✅ Endereço tem saldo!")
                else:
                    print(f"   ⚠️  Endereço não tem saldo")
        except Exception as e:
            print(f"   ❌ Erro ao derivar endereço: {e}")
    else:
        print(f"\n❌ NENHUMA CHAVE PRIVADA CONFIGURADA!")
        print(f"   Configure uma das seguintes variáveis:")
        print(f"   - BITCOIN_PRIVATE_KEY")
        print(f"   - BITCOIN_TESTNET_PRIVATE_KEY")
        print(f"   - BTC_PRIVATE_KEY")
    
    # Verificar endereço configurado
    address = (
        os.getenv('BITCOIN_TESTNET_ADDRESS') or 
        os.getenv('BITCOIN_ADDRESS') or 
        os.getenv('BTC_ADDRESS')
    )
    
    if address:
        print(f"\n✅ Endereço configurado:")
        print(f"   {address}")
        
        if private_key:
            try:
                from bitcoinlib.keys import HDKey
                key = HDKey(private_key, network='testnet')
                derived_address = key.address()
                
                if address == derived_address:
                    print(f"   ✅✅✅ Endereço corresponde à chave privada!")
                else:
                    print(f"   ⚠️  Endereço NÃO corresponde à chave privada!")
                    print(f"   Endereço configurado: {address}")
                    print(f"   Endereço derivado:    {derived_address}")
            except:
                pass
    
    print(f"\n{'='*70}")
    print(f"💡 RECOMENDAÇÕES")
    print(f"{'='*70}")
    
    if not private_key:
        print(f"1. Configure BITCOIN_PRIVATE_KEY no .env")
        print(f"   Exemplo: BITCOIN_PRIVATE_KEY=cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ")
    
    if private_key and address:
        try:
            from bitcoinlib.keys import HDKey
            key = HDKey(private_key, network='testnet')
            derived_address = key.address()
            if address != derived_address:
                print(f"2. Atualize BITCOIN_TESTNET_ADDRESS para corresponder à chave:")
                print(f"   BITCOIN_TESTNET_ADDRESS={derived_address}")
        except:
            pass
    
    print(f"{'='*70}")

if __name__ == "__main__":
    check_all_bitcoin_env()

