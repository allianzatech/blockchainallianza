#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICAR SALDO BITCOIN TESTNET
Consulta o saldo atual de um endereço Bitcoin testnet
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_bitcoin_balance(address: str = None):
    """Verifica saldo Bitcoin testnet"""
    
    # Se não fornecido, ler do .env
    if not address:
        address = os.getenv('BITCOIN_TESTNET_ADDRESS') or os.getenv('BTC_ADDRESS')
    
    if not address:
        print("❌ ERRO: Endereço não fornecido e não encontrado no .env")
        print("   Configure BITCOIN_TESTNET_ADDRESS ou forneça como argumento")
        return None
    
    print(f"\n{'='*70}")
    print(f"🔍 VERIFICANDO SALDO BITCOIN TESTNET")
    print(f"{'='*70}")
    print(f"📋 Endereço: {address}")
    print()
    
    try:
        # Usar Blockstream API (mais confiável)
        print("1. 📡 Consultando Blockstream API...")
        url = f"https://blockstream.info/testnet/api/address/{address}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Estatísticas da chain
            chain_stats = data.get('chain_stats', {})
            mempool_stats = data.get('mempool_stats', {})
            
            # Calcular saldo
            funded = chain_stats.get('funded_txo_sum', 0)
            spent = chain_stats.get('spent_txo_sum', 0)
            balance_sats = funded - spent
            
            # Mempool (não confirmado)
            mempool_funded = mempool_stats.get('funded_txo_sum', 0)
            mempool_spent = mempool_stats.get('spent_txo_sum', 0)
            mempool_balance_sats = mempool_funded - mempool_spent
            
            balance_btc = balance_sats / 100000000
            mempool_balance_btc = mempool_balance_sats / 100000000
            
            print(f"   ✅ Saldo confirmado: {balance_sats:,} satoshis ({balance_btc:.8f} BTC)")
            if mempool_balance_sats != 0:
                print(f"   ⏳ Saldo não confirmado: {mempool_balance_sats:,} satoshis ({mempool_balance_btc:.8f} BTC)")
            
            # Estatísticas detalhadas
            tx_count = chain_stats.get('tx_count', 0)
            print(f"   📊 Total de transações: {tx_count}")
            
            # Verificar UTXOs
            print(f"\n2. 📦 Consultando UTXOs...")
            utxo_url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
            utxo_response = requests.get(utxo_url, timeout=15)
            
            if utxo_response.status_code == 200:
                utxos = utxo_response.json()
                confirmed_utxos = [u for u in utxos if u.get('status', {}).get('confirmed', False)]
                unconfirmed_utxos = [u for u in utxos if not u.get('status', {}).get('confirmed', False)]
                
                print(f"   ✅ UTXOs confirmados: {len(confirmed_utxos)}")
                if confirmed_utxos:
                    total_confirmed = sum(u['value'] for u in confirmed_utxos)
                    print(f"   💰 Total confirmado: {total_confirmed:,} satoshis ({total_confirmed/100000000:.8f} BTC)")
                
                if unconfirmed_utxos:
                    print(f"   ⏳ UTXOs não confirmados: {len(unconfirmed_utxos)}")
                    total_unconfirmed = sum(u['value'] for u in unconfirmed_utxos)
                    print(f"   💰 Total não confirmado: {total_unconfirmed:,} satoshis ({total_unconfirmed/100000000:.8f} BTC)")
                
                # Mostrar alguns UTXOs maiores
                if confirmed_utxos:
                    print(f"\n3. 📋 Maiores UTXOs confirmados:")
                    sorted_utxos = sorted(confirmed_utxos, key=lambda x: x['value'], reverse=True)[:5]
                    for i, utxo in enumerate(sorted_utxos, 1):
                        txid = utxo.get('txid', 'N/A')
                        vout = utxo.get('vout', 'N/A')
                        value = utxo.get('value', 0)
                        print(f"   {i}. {txid[:16]}...:{vout} = {value:,} satoshis ({value/100000000:.8f} BTC)")
            
            # Verificar se saldo é suficiente para transação
            print(f"\n4. 💸 Verificando se saldo é suficiente para transação...")
            amount_btc = 0.0001  # Valor típico de transferência
            fee_btc = 0.000005  # Taxa estimada (5.000 satoshis)
            required_btc = amount_btc + fee_btc
            
            print(f"   Valor da transferência: {amount_btc:.8f} BTC")
            print(f"   Taxa estimada: {fee_btc:.8f} BTC")
            print(f"   Total necessário: {required_btc:.8f} BTC")
            print(f"   Saldo disponível: {balance_btc:.8f} BTC")
            
            if balance_btc >= required_btc:
                print(f"   ✅✅✅ SALDO SUFICIENTE! Pode fazer a transferência!")
                remaining = balance_btc - required_btc
                print(f"   💰 Saldo restante após transferência: {remaining:.8f} BTC")
            else:
                deficit = required_btc - balance_btc
                print(f"   ❌ SALDO INSUFICIENTE!")
                print(f"   ⚠️  Faltam {deficit:.8f} BTC ({deficit*100000000:.0f} satoshis)")
                print(f"   💡 Use um faucet Bitcoin testnet para adicionar fundos")
            
            # Links úteis
            print(f"\n{'='*70}")
            print(f"🔗 LINKS ÚTEIS:")
            print(f"{'='*70}")
            print(f"   Explorer: https://blockstream.info/testnet/address/{address}")
            print(f"   Faucets:")
            print(f"   - https://bitcoinfaucet.uo1.net/")
            print(f"   - https://testnet-faucet.mempool.co/")
            print(f"   - https://coinfaucet.eu/en/btc-testnet/")
            print(f"{'='*70}\n")
            
            return {
                "address": address,
                "balance_sats": balance_sats,
                "balance_btc": balance_btc,
                "mempool_balance_sats": mempool_balance_sats,
                "mempool_balance_btc": mempool_balance_btc,
                "tx_count": tx_count,
                "utxos_count": len(utxos) if utxo_response.status_code == 200 else 0,
                "confirmed_utxos": len(confirmed_utxos) if utxo_response.status_code == 200 else 0,
                "sufficient_for_transfer": balance_btc >= required_btc
            }
        else:
            print(f"   ❌ Erro ao consultar: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao verificar saldo: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    import sys
    
    # Aceitar endereço como argumento
    address = sys.argv[1] if len(sys.argv) > 1 else None
    
    result = check_bitcoin_balance(address)
    
    if result:
        print(f"\n✅ Verificação concluída!")
        if result['sufficient_for_transfer']:
            print(f"✅ Saldo suficiente para transferência de 0.0001 BTC")
        else:
            print(f"⚠️  Saldo insuficiente. Adicione mais fundos via faucet.")

