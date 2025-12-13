#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 VERIFICADOR DE CORRESPONDÊNCIA CHAVE-ENDEREÇO
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
if os.path.exists('.env'):
    load_dotenv('.env')

print("=== VERIFICAÇÃO CRÍTICA ===")

# Sua chave privada do ambiente
CHAVE_PRIVADA = "cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN"
ENDERECO_ESPERADO = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"

print(f"🔑 Chave privada fornecida: {CHAVE_PRIVADA[:30]}...")
print(f"📍 Endereço esperado: {ENDERECO_ESPERADO}")

try:
    # 1. Derivar endereço da chave
    print(f"\n1. 🔄 Derivando endereço da chave...")
    from bitcoinlib.keys import HDKey
    key = HDKey(CHAVE_PRIVADA, network='testnet')
    endereco_derivado = key.address()
    print(f"   ✅ Endereço derivado: {endereco_derivado}")
    print(f"   🔍 Correspondem? {endereco_derivado == ENDERECO_ESPERADO}")
    
    if endereco_derivado != ENDERECO_ESPERADO:
        print(f"   ❌❌❌ PROBLEMA GRAVE: Endereços NÃO correspondem!")
        print(f"      Isso explica saldo zero!")
    
    # 2. Verificar saldo do endereço derivado
    print(f"\n2. 💰 Verificando saldo do endereço derivado...")
    import requests
    url = f"https://blockstream.info/testnet/api/address/{endereco_derivado}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance = funded - spent
        print(f"   📊 Saldo de {endereco_derivado}:")
        print(f"      {balance} satoshis ({balance/100000000:.8f} BTC)")
    else:
        print(f"   ❌ Erro ao verificar saldo: {response.status_code}")
    
    # 3. Verificar saldo do endereço esperado
    print(f"\n3. 💰 Verificando saldo do endereço ESPERADO...")
    url_esperado = f"https://blockstream.info/testnet/api/address/{ENDERECO_ESPERADO}"
    response_esperado = requests.get(url_esperado, timeout=10)
    
    if response_esperado.status_code == 200:
        data_esperado = response_esperado.json()
        funded_esperado = data_esperado.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent_esperado = data_esperado.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance_esperado = funded_esperado - spent_esperado
        print(f"   📊 Saldo de {ENDERECO_ESPERADO}:")
        print(f"      {balance_esperado} satoshis ({balance_esperado/100000000:.8f} BTC)")
    else:
        print(f"   ❌ Erro ao verificar saldo: {response_esperado.status_code}")
        
except Exception as e:
    print(f"❌ Erro ao processar chave: {e}")
    import traceback
    traceback.print_exc()

# 4. Verificar qual chave está no ambiente REAL
print(f"\n4. 🌍 Verificando variáveis de ambiente...")
env_vars = ['BITCOIN_PRIVATE_KEY', 'BITCOIN_TESTNET_PRIVATE_KEY', 'BTC_PRIVATE_KEY', 'BASE_PRIVATE_KEY', 'PRIVATE_KEY']
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"   {var}: {value[:30]}... (tamanho: {len(value)})")
        print(f"      Primeiro char: '{value[0]}'")
        
        # Tentar derivar endereço desta chave
        try:
            from bitcoinlib.keys import HDKey
            if value.startswith(('c', '9', '5', 'L', 'K')):
                test_key = HDKey(value, network='testnet')
                test_addr = test_key.address()
                print(f"      → Endereço derivado: {test_addr}")
                if test_addr == ENDERECO_ESPERADO:
                    print(f"      ✅✅✅ ESTA CHAVE CORRESPONDE AO ENDEREÇO ESPERADO!")
                else:
                    print(f"      ❌ Esta chave NÃO corresponde ao endereço esperado")
        except Exception as e:
            print(f"      ⚠️  Não foi possível derivar endereço: {e}")
    else:
        print(f"   {var}: ❌ NÃO DEFINIDA")

print(f"\n🎯 CONCLUSÃO:")
print(f"   Se os endereços não correspondem, o sistema está usando")
print(f"   uma chave que gera um endereço DIFERENTE do que tem saldo!")

