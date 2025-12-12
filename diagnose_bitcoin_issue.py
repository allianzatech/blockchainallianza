#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO COMPLETO - Problema de Saldo Bitcoin
Verifica todos os aspectos do problema de saldo/UTXOs
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def diagnose_bitcoin_issue():
    """Diagnóstico completo do problema"""
    
    print(f"\n{'='*70}")
    print(f"🔍 DIAGNÓSTICO COMPLETO - PROBLEMA DE SALDO BITCOIN")
    print(f"{'='*70}\n")
    
    # 1. Verificar chave privada
    print("1. 🔑 VERIFICANDO CHAVE PRIVADA:")
    print("-" * 70)
    private_key = (
        os.getenv('BITCOIN_PRIVATE_KEY') or 
        os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or 
        os.getenv('BTC_PRIVATE_KEY')
    )
    
    if not private_key:
        print("   ❌ Nenhuma chave privada encontrada no .env")
        return
    
    print(f"   ✅ Chave encontrada: {private_key[:20]}... (tamanho: {len(private_key)})")
    print(f"   Primeiro char: '{private_key[0]}'")
    
    # 2. Derivar endereço da chave
    print(f"\n2. 📍 DERIVANDO ENDEREÇO DA CHAVE:")
    print("-" * 70)
    derived_address = None
    try:
        from bitcoinlib.keys import HDKey
        key = HDKey(private_key, network='testnet')
        derived_address = key.address()
        print(f"   ✅ Endereço derivado: {derived_address}")
    except Exception as e:
        print(f"   ❌ Erro ao derivar endereço: {e}")
        return
    
    # 3. Verificar endereço do .env
    print(f"\n3. 📋 VERIFICANDO ENDEREÇO DO .ENV:")
    print("-" * 70)
    env_address = (
        os.getenv('BITCOIN_TESTNET_ADDRESS') or 
        os.getenv('BITCOIN_ADDRESS') or 
        os.getenv('BTC_ADDRESS')
    )
    
    if env_address:
        print(f"   ✅ Endereço do .env: {env_address}")
        if env_address != derived_address:
            print(f"   ⚠️  AVISO: Endereço do .env difere do derivado!")
            print(f"      .env: {env_address}")
            print(f"      Derivado: {derived_address}")
    else:
        print(f"   ⚠️  Nenhum endereço no .env")
    
    # Usar endereço derivado ou do .env
    address_to_check = derived_address if derived_address else env_address
    
    if not address_to_check:
        print(f"   ❌ Nenhum endereço disponível para verificar")
        return
    
    print(f"\n   🎯 Usando endereço: {address_to_check}")
    
    # 4. Verificar saldo via Blockstream
    print(f"\n4. 💰 VERIFICANDO SALDO VIA BLOCKSTREAM:")
    print("-" * 70)
    try:
        url = f"https://blockstream.info/testnet/api/address/{address_to_check}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            chain_stats = data.get('chain_stats', {})
            funded = chain_stats.get('funded_txo_sum', 0)
            spent = chain_stats.get('spent_txo_sum', 0)
            balance_sats = funded - spent
            balance_btc = balance_sats / 100000000
            
            print(f"   ✅ Saldo confirmado: {balance_sats:,} satoshis ({balance_btc:.8f} BTC)")
            print(f"   📊 Total de transações: {chain_stats.get('tx_count', 0)}")
        else:
            print(f"   ❌ Erro: status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 5. Verificar UTXOs via Blockstream
    print(f"\n5. 📦 VERIFICANDO UTXOs VIA BLOCKSTREAM:")
    print("-" * 70)
    try:
        utxo_url = f"https://blockstream.info/testnet/api/address/{address_to_check}/utxo"
        utxo_response = requests.get(utxo_url, timeout=15)
        
        if utxo_response.status_code == 200:
            utxos = utxo_response.json()
            confirmed_utxos = [u for u in utxos if u.get('status', {}).get('confirmed', False)]
            
            print(f"   ✅ Total UTXOs: {len(utxos)}")
            print(f"   ✅ UTXOs confirmados: {len(confirmed_utxos)}")
            
            if confirmed_utxos:
                total_value = sum(u['value'] for u in confirmed_utxos)
                print(f"   💰 Valor total confirmado: {total_value:,} satoshis ({total_value/100000000:.8f} BTC)")
                
                print(f"\n   📋 Primeiros 5 UTXOs confirmados:")
                for i, utxo in enumerate(confirmed_utxos[:5], 1):
                    txid = utxo.get('txid', 'N/A')
                    vout = utxo.get('vout', 'N/A')
                    value = utxo.get('value', 0)
                    print(f"      {i}. {txid[:16]}...:{vout} = {value:,} sats ({value/100000000:.8f} BTC)")
            else:
                print(f"   ⚠️  Nenhum UTXO confirmado encontrado")
        else:
            print(f"   ❌ Erro: status {utxo_response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 6. Verificar saldo via BlockCypher
    print(f"\n6. 💰 VERIFICANDO SALDO VIA BLOCKCYPHER:")
    print("-" * 70)
    try:
        api_token = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
        bc_url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{address_to_check}/balance?token={api_token}"
        bc_response = requests.get(bc_url, timeout=15)
        
        if bc_response.status_code == 200:
            bc_data = bc_response.json()
            bc_balance_sats = bc_data.get('balance', 0)
            bc_balance_btc = bc_balance_sats / 100000000
            
            print(f"   ✅ Saldo BlockCypher: {bc_balance_sats:,} satoshis ({bc_balance_btc:.8f} BTC)")
            print(f"   📊 Total de transações: {bc_data.get('n_tx', 0)}")
            
            # Verificar UTXOs BlockCypher
            unspent = bc_data.get('txrefs', [])
            if unspent:
                print(f"   📦 UTXOs BlockCypher: {len(unspent)}")
                total_unspent = sum(tx.get('value', 0) for tx in unspent)
                print(f"   💰 Valor total UTXOs: {total_unspent:,} satoshis ({total_unspent/100000000:.8f} BTC)")
        else:
            print(f"   ❌ Erro: status {bc_response.status_code}")
            print(f"   Resposta: {bc_response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 7. Verificar se endereço está correto
    print(f"\n7. ✅ VERIFICAÇÃO FINAL:")
    print("-" * 70)
    print(f"   Endereço verificado: {address_to_check}")
    print(f"   Endereço esperado: tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q")
    
    if address_to_check == "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q":
        print(f"   ✅✅✅ ENDEREÇO CORRETO!")
    else:
        print(f"   ⚠️  AVISO: Endereço verificado difere do esperado!")
        print(f"   💡 Isso pode explicar por que o saldo não está sendo encontrado")
    
    print(f"\n{'='*70}")
    print(f"📋 CONCLUSÃO:")
    print(f"{'='*70}")
    print(f"Se o saldo aparece aqui mas não no sistema, pode ser:")
    print(f"   1. Cache da API BlockCypher (aguardar alguns minutos)")
    print(f"   2. Endereço derivado diferente do esperado")
    print(f"   3. Problema na busca de UTXOs no código")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    diagnose_bitcoin_issue()

