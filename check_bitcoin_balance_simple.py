#!/usr/bin/env python3
"""
Script simples para verificar saldo de endereço Bitcoin Testnet
Usa Blockstream API (mais confiável)
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def check_bitcoin_balance(address: str):
    """Verifica saldo Bitcoin usando Blockstream API"""
    try:
        print(f"\n{'='*70}")
        print(f"🔍 Verificando saldo Bitcoin Testnet")
        print(f"{'='*70}")
        print(f"📋 Endereço: {address}")
        
        # Usar Blockstream API (mais confiável para testnet)
        url = f"https://blockstream.info/testnet/api/address/{address}"
        print(f"\n🌐 Consultando: {url}")
        
        response = requests.get(url, timeout=15, headers={'Cache-Control': 'no-cache'})
        
        if response.status_code == 200:
            data = response.json()
            
            # Blockstream retorna chain_stats e mempool_stats
            chain_stats = data.get('chain_stats', {})
            mempool_stats = data.get('mempool_stats', {})
            
            # Saldo confirmado (na blockchain)
            funded = chain_stats.get('funded_txo_sum', 0)
            spent = chain_stats.get('spent_txo_sum', 0)
            balance_satoshis = funded - spent
            balance_btc = balance_satoshis / 100000000
            
            # Saldo não confirmado (na mempool)
            mempool_funded = mempool_stats.get('funded_txo_sum', 0)
            mempool_spent = mempool_stats.get('spent_txo_sum', 0)
            mempool_balance_satoshis = mempool_funded - mempool_spent
            mempool_balance_btc = mempool_balance_satoshis / 100000000
            
            # Saldo total (confirmado + não confirmado)
            total_balance_btc = balance_btc + mempool_balance_btc
            
            print(f"\n{'='*70}")
            print(f"💰 SALDO BITCOIN TESTNET")
            print(f"{'='*70}")
            print(f"✅ Saldo Confirmado: {balance_btc:.8f} BTC ({balance_satoshis:,} satoshis)")
            print(f"⏳ Saldo Não Confirmado: {mempool_balance_btc:.8f} BTC ({mempool_balance_satoshis:,} satoshis)")
            print(f"📊 Saldo Total: {total_balance_btc:.8f} BTC")
            print(f"\n📈 Estatísticas:")
            print(f"   Total Recebido: {chain_stats.get('funded_txo_sum', 0) / 100000000:.8f} BTC")
            print(f"   Total Enviado: {chain_stats.get('spent_txo_sum', 0) / 100000000:.8f} BTC")
            print(f"   Transações: {chain_stats.get('tx_count', 0)}")
            print(f"\n🔗 Explorer: https://blockstream.info/testnet/address/{address}")
            print(f"{'='*70}\n")
            
            # Verificar UTXOs também
            print(f"🔍 Verificando UTXOs...")
            utxo_url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
            utxo_response = requests.get(utxo_url, timeout=15)
            
            if utxo_response.status_code == 200:
                utxos = utxo_response.json()
                print(f"✅ UTXOs encontrados: {len(utxos)}")
                
                if utxos:
                    total_utxo_value = sum(u.get('value', 0) for u in utxos)
                    print(f"💰 Valor total dos UTXOs: {total_utxo_value / 100000000:.8f} BTC ({total_utxo_value:,} satoshis)")
                    print(f"\n📋 Primeiros 5 UTXOs:")
                    for i, utxo in enumerate(utxos[:5]):
                        confirmed = utxo.get('status', {}).get('confirmed', False)
                        status = "✅ Confirmado" if confirmed else "⏳ Pendente"
                        print(f"   {i+1}. {utxo.get('value', 0):,} sats ({utxo.get('value', 0) / 100000000:.8f} BTC) - {status}")
                else:
                    print(f"⚠️  Nenhum UTXO encontrado (endereço sem saldo ou todos gastos)")
            
            return {
                "success": True,
                "address": address,
                "balance_btc": balance_btc,
                "balance_satoshis": balance_satoshis,
                "mempool_balance_btc": mempool_balance_btc,
                "total_balance_btc": total_balance_btc,
                "utxos_count": len(utxos) if utxo_response.status_code == 200 else 0,
                "explorer_url": f"https://blockstream.info/testnet/address/{address}"
            }
        else:
            print(f"❌ Erro ao consultar saldo: Status {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "response": response.text[:200]
            }
            
    except Exception as e:
        print(f"❌ Erro ao verificar saldo: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Endereço do .env ou usar o padrão
    address = (
        os.getenv('BITCOIN_TESTNET_ADDRESS') or 
        os.getenv('BITCOIN_ADDRESS') or 
        os.getenv('BTC_ADDRESS') or
        "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"  # Endereço padrão do sistema
    )
    
    result = check_bitcoin_balance(address)
    
    # Retornar JSON se chamado via API
    if os.getenv('RETURN_JSON'):
        print(json.dumps(result, indent=2))


