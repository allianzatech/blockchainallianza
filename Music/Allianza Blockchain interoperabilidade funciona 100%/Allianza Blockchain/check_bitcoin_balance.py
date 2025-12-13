#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 CONSULTAR SALDO BITCOIN TESTNET
Consulta o saldo de um endereço Bitcoin testnet via Blockstream API
"""

import requests
import sys

def check_balance(address):
    """Consulta saldo e UTXOs de um endereço Bitcoin testnet"""
    print(f"\n{'='*70}")
    print(f"🔍 CONSULTA DE SALDO BITCOIN TESTNET")
    print(f"{'='*70}")
    print(f"\n📋 Endereço: {address}")
    
    # 1. Consultar saldo via Blockstream
    print(f"\n1. 💰 Consultando saldo via Blockstream API...")
    try:
        balance_url = f"https://blockstream.info/testnet/api/address/{address}"
        response = requests.get(balance_url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
            spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
            balance_sats = funded - spent
            balance_btc = balance_sats / 100000000
            
            print(f"   ✅ Saldo encontrado!")
            print(f"   💰 Fundos recebidos: {funded:,} satoshis ({funded/100000000:.8f} BTC)")
            print(f"   💸 Fundos gastos: {spent:,} satoshis ({spent/100000000:.8f} BTC)")
            print(f"   💵 Saldo disponível: {balance_sats:,} satoshis ({balance_btc:.8f} BTC)")
            
            # Verificar se é suficiente para uma transação
            min_needed = 0.000105  # 0.0001 BTC + fee
            if balance_btc >= min_needed:
                print(f"   ✅✅✅ Saldo suficiente para transação! (precisa {min_needed} BTC)")
            else:
                print(f"   ⚠️  Saldo insuficiente para transação (precisa {min_needed} BTC)")
        else:
            print(f"   ❌ Erro HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Erro ao consultar saldo: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. Consultar UTXOs
    print(f"\n2. 📦 Consultando UTXOs (Unspent Transaction Outputs)...")
    try:
        utxo_url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
        utxo_response = requests.get(utxo_url, timeout=15)
        
        if utxo_response.status_code == 200:
            utxos = utxo_response.json()
            print(f"   ✅ {len(utxos)} UTXOs encontrados")
            
            if utxos:
                total_value = sum(u.get('value', 0) for u in utxos)
                total_btc = total_value / 100000000
                print(f"   💰 Valor total dos UTXOs: {total_value:,} satoshis ({total_btc:.8f} BTC)")
                
                # Mostrar primeiros 5 UTXOs
                print(f"\n   📋 Primeiros 5 UTXOs:")
                for i, utxo in enumerate(utxos[:5], 1):
                    txid = utxo.get('txid', 'N/A')
                    vout = utxo.get('vout', 'N/A')
                    value = utxo.get('value', 0)
                    status = utxo.get('status', {})
                    confirmed = status.get('confirmed', False)
                    
                    print(f"      {i}. TXID: {txid[:20]}...:{vout}")
                    print(f"         Valor: {value:,} satoshis ({value/100000000:.8f} BTC)")
                    print(f"         Status: {'✅ Confirmado' if confirmed else '⏳ Pendente'}")
                
                if len(utxos) > 5:
                    print(f"      ... e mais {len(utxos) - 5} UTXOs")
            else:
                print(f"   ⚠️  Nenhum UTXO encontrado (endereço sem fundos não gastos)")
        else:
            print(f"   ❌ Erro HTTP {utxo_response.status_code}: {utxo_response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Erro ao consultar UTXOs: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Link para explorer
    print(f"\n3. 🔗 Links úteis:")
    print(f"   Blockstream Explorer: https://blockstream.info/testnet/address/{address}")
    print(f"   BlockCypher Explorer: https://live.blockcypher.com/btc-testnet/address/{address}/")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    # Endereço do erro ou argumento da linha de comando
    if len(sys.argv) > 1:
        address = sys.argv[1]
    else:
        # Endereço do erro reportado
        address = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"
    
    check_balance(address)

