#!/usr/bin/env python3
import requests

address = 'mkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt'
print(f"🔍 Verificando saldo do endereço: {address}")

try:
    url = f"https://blockstream.info/testnet/api/address/{address}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        balance = data.get('chain_stats', {}).get('funded_txo_sum', 0) - data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance_btc = balance / 100000000
        
        print(f"✅ Saldo confirmado: {balance} satoshis ({balance_btc:.8f} BTC)")
        print(f"   Transações recebidas: {data.get('chain_stats', {}).get('tx_count', 0)}")
        print(f"   UTXOs confirmados: {data.get('chain_stats', {}).get('funded_txo_count', 0)}")
        print(f"   Total unspent: {data.get('chain_stats', {}).get('funded_txo_count', 0) - data.get('chain_stats', {}).get('spent_txo_count', 0)} UTXOs")
        
        # Verificar UTXOs
        utxo_url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
        utxo_response = requests.get(utxo_url, timeout=10)
        if utxo_response.status_code == 200:
            utxos = utxo_response.json()
            confirmed_utxos = [u for u in utxos if u.get('status', {}).get('confirmed', False)]
            print(f"   UTXOs confirmados disponíveis: {len(confirmed_utxos)}")
            
            if confirmed_utxos:
                total_confirmed = sum(u['value'] for u in confirmed_utxos)
                print(f"   ✅ Total confirmado: {total_confirmed} satoshis ({total_confirmed/100000000:.8f} BTC)")
                print(f"   ✅ Saldo suficiente para transações!")
            else:
                print(f"   ⚠️  Nenhum UTXO confirmado")
        else:
            print(f"   ⚠️  Erro ao buscar UTXOs: {utxo_response.status_code}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"   {response.text[:200]}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

