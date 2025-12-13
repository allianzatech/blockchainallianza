#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VERIFICAÇÃO FINAL DA CONFIGURAÇÃO DO RENDER
Confirma que a chave privada gera o endereço correto
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
if os.path.exists('.env'):
    load_dotenv('.env')

print("=" * 70)
print("✅ VERIFICAÇÃO FINAL DA CONFIGURAÇÃO")
print("=" * 70)

# Valores esperados
CHAVE_CORRETA = "cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ"
ENDERECO_ESPERADO = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"

print(f"\n📋 CONFIGURAÇÃO ESPERADA:")
print(f"   BITCOIN_PRIVATE_KEY: {CHAVE_CORRETA[:30]}...")
print(f"   BITCOIN_TESTNET_ADDRESS: {ENDERECO_ESPERADO}")

# Verificar do ambiente
chave_real = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or os.getenv('BTC_PRIVATE_KEY')
endereco_real = os.getenv('BITCOIN_TESTNET_ADDRESS') or os.getenv('BITCOIN_ADDRESS') or os.getenv('BTC_ADDRESS')

print(f"\n📋 CONFIGURAÇÃO NO AMBIENTE:")
if chave_real:
    print(f"   ✅ BITCOIN_PRIVATE_KEY: {chave_real[:30]}... (tamanho: {len(chave_real)})")
else:
    print(f"   ❌ BITCOIN_PRIVATE_KEY: NÃO DEFINIDA")

if endereco_real:
    print(f"   ✅ BITCOIN_TESTNET_ADDRESS: {endereco_real}")
else:
    print(f"   ❌ BITCOIN_TESTNET_ADDRESS: NÃO DEFINIDA")

# Verificar correspondência
print(f"\n🔍 VERIFICAÇÃO DE CORRESPONDÊNCIA:")

if chave_real:
    try:
        from bitcoinlib.keys import HDKey
        key = HDKey(chave_real.strip(), network='testnet')
        endereco_derivado = key.address()
        
        print(f"   Endereço derivado da chave: {endereco_derivado}")
        print(f"   Endereço esperado: {ENDERECO_ESPERADO}")
        
        if endereco_derivado == ENDERECO_ESPERADO:
            print(f"   ✅✅✅ CORRESPONDÊNCIA PERFEITA!")
        else:
            print(f"   ❌❌❌ NÃO CORRESPONDE!")
            print(f"   ⚠️  A chave gera um endereço diferente!")
        
        # Verificar se corresponde ao endereço do .env
        if endereco_real:
            if endereco_derivado == endereco_real:
                print(f"   ✅ Endereço derivado corresponde ao do .env")
            else:
                print(f"   ❌ Endereço derivado NÃO corresponde ao do .env")
                print(f"      Derivado: {endereco_derivado}")
                print(f"      .env: {endereco_real}")
    except Exception as e:
        print(f"   ❌ Erro ao derivar endereço: {e}")
        import traceback
        traceback.print_exc()

# Verificar saldo
print(f"\n💰 VERIFICAÇÃO DE SALDO:")
if endereco_real:
    try:
        import requests
        url = f"https://blockstream.info/testnet/api/address/{endereco_real}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
            spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
            balance = funded - spent
            print(f"   ✅ Saldo: {balance:,} satoshis ({balance/100000000:.8f} BTC)")
            
            # UTXOs
            utxo_url = f"{url}/utxo"
            utxo_resp = requests.get(utxo_url, timeout=10)
            if utxo_resp.status_code == 200:
                utxos = utxo_resp.json()
                print(f"   ✅ UTXOs: {len(utxos)} encontrados")
        else:
            print(f"   ❌ Erro ao verificar saldo: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

print(f"\n" + "=" * 70)
print(f"🎯 CONCLUSÃO:")
print(f"=" * 70)

if chave_real and chave_real.strip() == CHAVE_CORRETA:
    print(f"✅ Chave privada está CORRETA!")
else:
    print(f"❌ Chave privada está INCORRETA ou não corresponde!")

if endereco_real and endereco_real == ENDERECO_ESPERADO:
    print(f"✅ Endereço está CORRETO!")
else:
    print(f"❌ Endereço está INCORRETO ou não corresponde!")

print(f"\n💡 PRÓXIMOS PASSOS:")
print(f"   1. Se tudo está correto, reinicie o serviço no Render")
print(f"   2. Tente fazer uma transferência novamente")
print(f"   3. Os logs devem mostrar o saldo correto agora")
print(f"=" * 70)

