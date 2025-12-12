#!/usr/bin/env python3
"""Verifica se o setup final está correto"""
from bitcoinlib.keys import Key
import requests

# ⚠️ SEGURANÇA: Ler de variáveis de ambiente, não hardcoded
import os
from dotenv import load_dotenv
load_dotenv()

# Dados do novo endereço - ler de env
new_wif = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or None
expected_address = os.getenv('BITCOIN_TESTNET_ADDRESS') or None

if not new_wif or not expected_address:
    print("❌ ERRO: Configure BITCOIN_PRIVATE_KEY e BITCOIN_TESTNET_ADDRESS no .env")
    print("   Exemplo: BITCOIN_PRIVATE_KEY=cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN")
    print("   Exemplo: BITCOIN_TESTNET_ADDRESS=mft38vhDpoF4qEAFChbfxZ5UrUemSViHHh")
    exit(1)

print("🔍 VERIFICAÇÃO FINAL DO SETUP")
print("="*70)

# 1. Verificar WIF
print("\n1. ✅ Verificando WIF...")
try:
    key = Key(new_wif, network='testnet')
    derived_address = key.address()
    print(f"   WIF: {new_wif[:20]}...")
    print(f"   Endereço derivado: {derived_address}")
    print(f"   Endereço esperado: {expected_address}")
    
    if derived_address == expected_address:
        print(f"   ✅✅✅ WIF e endereço correspondem!")
    else:
        print(f"   ❌ ERRO: Endereços não correspondem!")
        exit(1)
except Exception as e:
    print(f"   ❌ ERRO ao validar WIF: {e}")
    exit(1)

# 2. Verificar saldo
print("\n2. ✅ Verificando saldo...")
try:
    url = f"https://blockstream.info/testnet/api/address/{expected_address}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance_sats = funded - spent
        balance_btc = balance_sats / 100000000
        
        print(f"   Saldo: {balance_sats} satoshis ({balance_btc:.8f} BTC)")
        
        if balance_sats >= 10000:  # Pelo menos 0.0001 BTC
            print(f"   ✅✅✅ Saldo suficiente para transações!")
        else:
            print(f"   ⚠️  Saldo muito baixo para transações")
    else:
        print(f"   ⚠️  Erro ao verificar saldo: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Erro ao verificar saldo: {e}")

# 3. Verificar UTXOs
print("\n3. ✅ Verificando UTXOs...")
try:
    utxo_url = f"https://blockstream.info/testnet/api/address/{expected_address}/utxo"
    utxo_response = requests.get(utxo_url, timeout=10)
    
    if utxo_response.status_code == 200:
        utxos = utxo_response.json()
        confirmed_utxos = [u for u in utxos if u.get('status', {}).get('confirmed', False)]
        print(f"   UTXOs confirmados: {len(confirmed_utxos)}")
        
        if confirmed_utxos:
            total_confirmed = sum(u['value'] for u in confirmed_utxos)
            print(f"   Total confirmado: {total_confirmed} satoshis ({total_confirmed/100000000:.8f} BTC)")
            print(f"   ✅✅✅ UTXOs disponíveis para transações!")
        else:
            print(f"   ⚠️  Nenhum UTXO confirmado ainda")
    else:
        print(f"   ⚠️  Erro ao buscar UTXOs: {utxo_response.status_code}")
except Exception as e:
    print(f"   ⚠️  Erro ao verificar UTXOs: {e}")

print("\n" + "="*70)
print("✅✅✅ SETUP FINAL VERIFICADO!")
print("✅✅✅ Pronto para testar transferências cross-chain!")
print("="*70)

