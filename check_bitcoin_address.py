#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar endereço Bitcoin e seus UTXOs
"""

import requests
import json

def check_bitcoin_address(address: str):
    """Verifica endereço Bitcoin e seus UTXOs"""
    print(f"\n{'='*70}")
    print(f"🔍 VERIFICANDO ENDEREÇO BITCOIN")
    print(f"{'='*70}")
    print(f"📍 Endereço: {address}")
    
    # 1. Verificar informações do endereço
    print(f"\n1. 📊 Informações do endereço...")
    addr_url = f"https://blockstream.info/testnet/api/address/{address}"
    addr_resp = requests.get(addr_url, timeout=15)
    
    if addr_resp.status_code == 200:
        addr_data = addr_resp.json()
        funded = addr_data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent = addr_data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance = funded - spent
        print(f"   💰 Saldo: {balance} satoshis ({balance/100000000:.8f} BTC)")
        print(f"   📥 Total recebido: {funded} satoshis")
        print(f"   📤 Total gasto: {spent} satoshis")
    else:
        print(f"   ❌ Erro ao buscar informações: {addr_resp.status_code}")
    
    # 2. Buscar UTXOs
    print(f"\n2. 🔍 Buscando UTXOs...")
    utxo_url = f"https://blockstream.info/testnet/api/address/{address}/utxo"
    utxo_resp = requests.get(utxo_url, timeout=15)
    
    if utxo_resp.status_code == 200:
        utxos = utxo_resp.json()
        print(f"   📦 Total UTXOs encontrados: {len(utxos)}")
        
        if not utxos:
            print(f"   ⚠️  NENHUM UTXO ENCONTRADO! O endereço não tem fundos disponíveis.")
            return
        
        # 3. Validar cada UTXO
        print(f"\n3. ✅ Validando UTXOs...")
        valid_utxos = []
        
        for i, utxo in enumerate(utxos):
            txid = utxo.get('txid')
            vout = utxo.get('vout')
            value = utxo.get('value', 0)
            status = utxo.get('status', {})
            
            print(f"\n   UTXO {i+1}:")
            print(f"      TXID: {txid}")
            print(f"      VOUT: {vout}")
            print(f"      Valor: {value} satoshis ({value/100000000:.8f} BTC)")
            print(f"      Status: {status}")
            
            # Verificar se está confirmado
            if not status.get('confirmed', False):
                print(f"      ⚠️  NÃO CONFIRMADO - pulando...")
                continue
            
            # Verificar se existe na rede e não foi gasto
            try:
                tx_url = f"https://blockstream.info/testnet/api/tx/{txid}"
                tx_resp = requests.get(tx_url, timeout=10)
                
                if tx_resp.status_code != 200:
                    print(f"      ❌ Transação não encontrada (status {tx_resp.status_code})")
                    continue
                
                tx_data = tx_resp.json()
                
                # Verificar se o vout existe
                if vout >= len(tx_data.get('vout', [])):
                    print(f"      ❌ VOUT {vout} não existe na transação (total vouts: {len(tx_data.get('vout', []))})")
                    continue
                
                vout_data = tx_data['vout'][vout]
                
                # Verificar se foi gasto
                if vout_data.get('spent', False):
                    print(f"      ❌ JÁ FOI GASTO!")
                    continue
                
                # Verificar valor
                vout_value = vout_data.get('value', 0)
                if vout_value != value:
                    print(f"      ⚠️  Valor não corresponde (esperado {value}, encontrado {vout_value})")
                
                # UTXO VÁLIDO!
                valid_utxos.append(utxo)
                print(f"      ✅ UTXO VÁLIDO!")
                
            except Exception as val_err:
                print(f"      ❌ Erro na validação: {val_err}")
                continue
        
        print(f"\n{'='*70}")
        print(f"📊 RESUMO")
        print(f"{'='*70}")
        print(f"   Total UTXOs encontrados: {len(utxos)}")
        print(f"   UTXOs válidos: {len(valid_utxos)}")
        
        if valid_utxos:
            total_value = sum(u['value'] for u in valid_utxos)
            print(f"   💰 Valor total disponível: {total_value} satoshis ({total_value/100000000:.8f} BTC)")
            print(f"\n   ✅ UTXOs válidos:")
            for i, utxo in enumerate(valid_utxos):
                print(f"      {i+1}. {utxo['txid'][:16]}...:{utxo['vout']} = {utxo['value']} sats")
        else:
            print(f"   ⚠️  NENHUM UTXO VÁLIDO! O endereço não tem fundos disponíveis para transações.")
    else:
        print(f"   ❌ Erro ao buscar UTXOs: {utxo_resp.status_code}")

if __name__ == "__main__":
    # Endereço do erro
    address = "mft38vhDpoF4qEAFChbfxZ5UrUemSViHHh"
    check_bitcoin_address(address)
    
    print(f"\n{'='*70}")
    print(f"💡 PRÓXIMOS PASSOS")
    print(f"{'='*70}")
    print(f"   1. Se não houver UTXOs válidos, envie fundos para o endereço")
    print(f"   2. Se houver UTXOs válidos, verifique se a chave privada corresponde ao endereço")
    print(f"   3. Use um faucet Bitcoin testnet para obter fundos:")
    print(f"      - https://bitcoinfaucet.uo1.net/")
    print(f"      - https://testnet-faucet.mempool.co/")

