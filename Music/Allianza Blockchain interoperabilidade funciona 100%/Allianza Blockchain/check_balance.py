#!/usr/bin/env python3
"""Verifica saldo de um endereço Bitcoin testnet"""
import sys
import requests

if len(sys.argv) < 2:
    print("Uso: python check_balance.py <endereco_bitcoin>")
    print("Exemplo: python check_balance.py mft38vhDpoF4qEAFChbfxZ5UrUemSViHHh")
    sys.exit(1)

address = sys.argv[1]
print(f"🔍 Verificando saldo do endereço: {address}")

try:
    url = f"https://blockstream.info/testnet/api/address/{address}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance_sats = funded - spent
        balance_btc = balance_sats / 100000000
        
        print(f"✅ Saldo: {balance_sats} satoshis ({balance_btc:.8f} BTC)")
        print(f"   Transações recebidas: {data.get('chain_stats', {}).get('tx_count', 0)}")
        
        # Verificar UTXOs
        utxo_url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
        utxo_response = requests.get(utxo_url, timeout=10)
        if utxo_response.status_code == 200:
            utxos = utxo_response.json()
            confirmed_utxos = [u for u in utxos if u.get('status', {}).get('confirmed', False)]
            print(f"   UTXOs confirmados: {len(confirmed_utxos)}")
            
            if confirmed_utxos:
                total_confirmed = sum(u['value'] for u in confirmed_utxos)
                print(f"   ✅ Total confirmado: {total_confirmed} satoshis ({total_confirmed/100000000:.8f} BTC)")
                print(f"   ✅ Pronto para usar!")
            else:
                print(f"   ⚠️  Nenhum UTXO confirmado ainda - aguarde confirmações")
        else:
            print(f"   ⚠️  Erro ao buscar UTXOs: {utxo_response.status_code}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"   {response.text[:200]}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

