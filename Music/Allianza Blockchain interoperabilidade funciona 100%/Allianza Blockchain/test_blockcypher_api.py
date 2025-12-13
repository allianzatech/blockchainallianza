#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste direto da API BlockCypher para verificar formato correto
"""

import requests
import json
import os

def test_blockcypher_transaction():
    """Testa criação de transação Bitcoin via BlockCypher API"""
    print(f"\n{'='*70}")
    print(f"🧪 TESTE DIRETO - API BLOCKCYPHER")
    print(f"{'='*70}")
    
    # Dados do UTXO válido (confirmado pelo check_bitcoin_address.py)
    txid = "7bb559f92c6d3862dbaaf483667798a3c757dcf0a53071326bd9803129dde108"
    vout = 1
    value = 136960  # satoshis
    
    from_address = "mft38vhDpoF4qEAFChbfxZ5UrUemSViHHh"
    to_address = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"
    amount_sats = 10000  # 0.0001 BTC
    fee_sats = 500
    
    print(f"\n📋 Dados da transação:")
    print(f"   De: {from_address}")
    print(f"   Para: {to_address}")
    print(f"   Valor: {amount_sats} satoshis")
    print(f"   Fee: {fee_sats} satoshis")
    print(f"\n📦 UTXO:")
    print(f"   TXID: {txid}")
    print(f"   VOUT: {vout}")
    print(f"   Valor: {value} satoshis")
    
    # Normalizar txid para lowercase
    txid_normalized = txid.lower().strip()
    print(f"   TXID normalizado: {txid_normalized}")
    
    # Preparar payload
    token = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
    
    # Teste 1: Formato com 'value'
    print(f"\n{'='*70}")
    print(f"🧪 TESTE 1: Formato com campo 'value'")
    print(f"{'='*70}")
    
    tx_data_1 = {
        "inputs": [{
            "prev_hash": txid_normalized,
            "output_index": int(vout),
            "value": int(value)
        }],
        "outputs": [{
            "addresses": [to_address],
            "value": amount_sats
        }],
        "fees": fee_sats
    }
    
    # Adicionar change se necessário
    change_sats = value - amount_sats - fee_sats
    if change_sats > 546:
        tx_data_1["outputs"].append({
            "addresses": [from_address],
            "value": change_sats
        })
        print(f"   Change: {change_sats} satoshis")
    
    print(f"\n📦 Payload:")
    print(json.dumps(tx_data_1, indent=2))
    
    create_url = f"https://api.blockcypher.com/v1/btc/test3/txs/new?token={token}"
    print(f"\n📡 Enviando para: {create_url}")
    
    try:
        response = requests.post(create_url, json=tx_data_1, timeout=30)
        print(f"\n📊 Status: {response.status_code}")
        print(f"📋 Response:")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(json.dumps(result, indent=2))
            print(f"\n✅✅✅ SUCESSO! Transação criada!")
            if 'tosign' in result:
                print(f"   Hash(es) para assinar: {len(result['tosign'])}")
        else:
            print(response.text)
            print(f"\n❌ ERRO: {response.status_code}")
            
            # Tentar parsear erro
            try:
                error_data = response.json()
                if 'errors' in error_data:
                    print(f"\n🔍 Erros detalhados:")
                    for error in error_data['errors']:
                        print(f"   - {error}")
            except:
                pass
    except Exception as e:
        print(f"\n❌ Exceção: {e}")
        import traceback
        traceback.print_exc()
    
    # Teste 2: Formato SEM 'value' (para comparação)
    print(f"\n{'='*70}")
    print(f"🧪 TESTE 2: Formato SEM campo 'value' (para comparação)")
    print(f"{'='*70}")
    
    tx_data_2 = {
        "inputs": [{
            "prev_hash": txid_normalized,
            "output_index": int(vout)
        }],
        "outputs": [{
            "addresses": [to_address],
            "value": amount_sats
        }],
        "fees": fee_sats
    }
    
    if change_sats > 546:
        tx_data_2["outputs"].append({
            "addresses": [from_address],
            "value": change_sats
        })
    
    print(f"\n📦 Payload:")
    print(json.dumps(tx_data_2, indent=2))
    
    try:
        response2 = requests.post(create_url, json=tx_data_2, timeout=30)
        print(f"\n📊 Status: {response2.status_code}")
        if response2.status_code not in [200, 201]:
            print(f"📋 Response:")
            print(response2.text[:500])
    except Exception as e:
        print(f"\n❌ Exceção: {e}")

if __name__ == "__main__":
    test_blockcypher_transaction()

