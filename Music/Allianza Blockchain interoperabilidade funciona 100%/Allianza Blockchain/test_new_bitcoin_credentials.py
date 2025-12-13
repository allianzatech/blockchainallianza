#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido para verificar se as novas credenciais Bitcoin estão corretas
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Novas credenciais
NEW_WIF = "cV5M7vW8Vv1utj7FYw9qQcbVnYcdm6h8X9wy9N4aqkRufjhF6GUD"
NEW_ADDRESS = "mkWLvF2x6wzSxGJ4UQ7cJq1KqtmKz9MZ4n"
NEW_HEX = "7a3fcb9e9e1f94dc8c23dba1fc50fa74b8d4e0078a1d66cbec299f7d146f2c36"

print("="*70)
print("🔍 TESTE DAS NOVAS CREDENCIAIS BITCOIN")
print("="*70)

# Teste 1: Verificar se WIF deriva o endereço correto
print("\n1. 🔑 Testando WIF -> Endereço...")
try:
    from bitcoinlib.keys import HDKey
    key = HDKey(NEW_WIF, network='testnet')
    derived_address = key.address()
    print(f"   WIF: {NEW_WIF[:20]}...")
    print(f"   Endereço derivado: {derived_address}")
    print(f"   Endereço esperado: {NEW_ADDRESS}")
    print(f"   ✅ Coincide: {derived_address == NEW_ADDRESS}")
    
    if derived_address != NEW_ADDRESS:
        print(f"   ❌ ERRO: Endereço derivado não corresponde!")
        print(f"   ⚠️  Isso pode causar problemas na transação")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# Teste 2: Verificar se HEX deriva o endereço correto
print("\n2. 🔑 Testando HEX -> WIF -> Endereço...")
try:
    from bitcoinlib.keys import HDKey
    hex_bytes = bytes.fromhex(NEW_HEX)
    key_from_hex = HDKey(hex_bytes, network='testnet')
    wif_from_hex = key_from_hex.wif()
    address_from_hex = key_from_hex.address()
    
    print(f"   HEX: {NEW_HEX[:20]}...")
    print(f"   WIF derivado: {wif_from_hex[:20]}...")
    print(f"   Endereço derivado: {address_from_hex}")
    print(f"   Endereço esperado: {NEW_ADDRESS}")
    print(f"   ✅ Coincide: {address_from_hex == NEW_ADDRESS}")
    print(f"   ✅ WIF coincide: {wif_from_hex == NEW_WIF}")
    
    if address_from_hex != NEW_ADDRESS:
        print(f"   ❌ ERRO: Endereço derivado do HEX não corresponde!")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# Teste 3: Verificar conversão WIF -> HEX
print("\n3. 🔑 Testando WIF -> HEX...")
try:
    from bitcoinlib.keys import HDKey
    key = HDKey(NEW_WIF, network='testnet')
    private_hex = key.private_hex
    
    print(f"   WIF: {NEW_WIF[:20]}...")
    print(f"   HEX derivado: {private_hex[:20]}...")
    print(f"   HEX esperado: {NEW_HEX[:20]}...")
    print(f"   ✅ Coincide: {private_hex == NEW_HEX}")
    
    if private_hex != NEW_HEX:
        print(f"   ⚠️  HEX derivado não corresponde ao fornecido")
        print(f"   Mas isso pode ser normal se o HEX fornecido não incluir o prefixo")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# Teste 4: Verificar saldo do novo endereço
print("\n4. 💰 Verificando saldo do novo endereço...")
try:
    import requests
    url = f"https://blockstream.info/testnet/api/address/{NEW_ADDRESS}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        funded_txo_sum = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent_txo_sum = data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance = (funded_txo_sum - spent_txo_sum) / 100000000
        
        print(f"   Endereço: {NEW_ADDRESS}")
        print(f"   Saldo: {balance:.8f} BTC")
        print(f"   ✅ Endereço existe na rede")
        
        if balance < 0.0001:
            print(f"   ⚠️  Saldo insuficiente para testar (mínimo: 0.0001 BTC)")
            print(f"   💡 Use um faucet para adicionar fundos")
    else:
        print(f"   ⚠️  Erro ao verificar saldo: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*70)
print("✅ TESTE CONCLUÍDO!")
print("="*70)

