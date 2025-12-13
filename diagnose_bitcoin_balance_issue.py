#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 DIAGNÓSTICO COMPLETO DO SISTEMA
"""

import os
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
if os.path.exists('.env'):
    load_dotenv('.env')

print("=" * 70)
print("🚨 DIAGNÓSTICO DE EMERGÊNCIA")
print("=" * 70)

# 1. VERIFICAR CHAVE PRIVADA
print("\n1. 🔑 VERIFICAÇÃO DA CHAVE PRIVADA")

CHAVE_ESPERADA = "cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN"
CHAVE_CORRETA = "cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ"

print(f"   Chave esperada (ERRADA): {CHAVE_ESPERADA[:30]}...")
print(f"   Chave correta: {CHAVE_CORRETA[:30]}...")

# Verificar do ambiente
chave_real = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or os.getenv('BTC_PRIVATE_KEY')

if chave_real:
    print(f"   Chave no ambiente: {chave_real[:30]}...")
    print(f"   Tamanho: {len(chave_real)}")
    print(f"   Começa com: '{chave_real[0]}'")
    
    # Tentar derivar endereço
    try:
        from bitcoinlib.keys import HDKey
        key = HDKey(chave_real.strip(), network='testnet')
        endereco_derivado = key.address()
        print(f"   ✅ Endereço derivado: {endereco_derivado}")
        
        # Verificar qual chave corresponde
        if chave_real.strip() == CHAVE_CORRETA:
            print(f"   ✅✅✅ CHAVE CORRETA!")
        elif chave_real.strip() == CHAVE_ESPERADA:
            print(f"   ❌ CHAVE ERRADA (gera endereço diferente)")
        else:
            print(f"   ⚠️  Chave diferente das conhecidas")
    except Exception as e:
        print(f"   ❌ ERRO ao derivar endereço: {e}")
        import traceback
        traceback.print_exc()
else:
    print("   ❌ NENHUMA CHAVE ENCONTRADA NO AMBIENTE!")

# 2. VERIFICAR SALDO REAL NA REDE
print("\n2. 💰 VERIFICAÇÃO DE SALDO NA REDE")

ENDERECO = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"
print(f"   Endereço: {ENDERECO}")

# Blockstream API
print(f"\n   📡 Blockstream API:")
url = f"https://blockstream.info/testnet/api/address/{ENDERECO}"
try:
    resp = requests.get(url, timeout=15)
    print(f"      Status HTTP: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"      Dados completos: {json.dumps(data, indent=2)[:1000]}...")
        
        funded = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent = data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance = funded - spent
        print(f"\n      ✅ Saldo: {balance:,} satoshis ({balance/100000000:.8f} BTC)")
        print(f"      Funded: {funded:,} satoshis")
        print(f"      Spent: {spent:,} satoshis")
        
        # UTXOs
        print(f"\n      📦 Buscando UTXOs...")
        utxo_url = f"{url}/utxo"
        utxo_resp = requests.get(utxo_url, timeout=15)
        print(f"      Status UTXO: {utxo_resp.status_code}")
        if utxo_resp.status_code == 200:
            utxos = utxo_resp.json()
            print(f"      ✅ UTXOs encontrados: {len(utxos)}")
            if utxos:
                total_utxos = sum(u.get('value', 0) for u in utxos)
                print(f"      Total UTXOs: {total_utxos:,} satoshis ({total_utxos/100000000:.8f} BTC)")
                print(f"      Primeiro UTXO: {utxos[0]['txid'][:16]}...:{utxos[0].get('vout', 'N/A')} = {utxos[0].get('value', 0):,} sats")
                print(f"      Último UTXO: {utxos[-1]['txid'][:16]}...:{utxos[-1].get('vout', 'N/A')} = {utxos[-1].get('value', 0):,} sats")
                
                # Verificar status dos UTXOs
                confirmed = [u for u in utxos if u.get('status', {}).get('confirmed', False)]
                print(f"      UTXOs confirmados: {len(confirmed)}")
            else:
                print(f"      ⚠️  Nenhum UTXO encontrado!")
        else:
            print(f"      ❌ Erro ao buscar UTXOs: {utxo_resp.status_code}")
            print(f"      Resposta: {utxo_resp.text[:200]}")
    else:
        print(f"      ❌ Erro HTTP: {resp.status_code}")
        print(f"      Resposta: {resp.text[:200]}")
except Exception as e:
    print(f"      ❌ Exceção: {e}")
    import traceback
    traceback.print_exc()

# BlockCypher API
print(f"\n   📡 BlockCypher API:")
url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{ENDERECO}/balance"
try:
    resp = requests.get(url, timeout=15)
    print(f"      Status HTTP: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        balance = data.get('final_balance', 0)
        print(f"      ✅ Saldo final: {balance:,} satoshis ({balance/100000000:.8f} BTC)")
        print(f"      Total recebido: {data.get('total_received', 0):,} sats")
        print(f"      Total enviado: {data.get('total_sent', 0):,} sats")
        print(f"      Número de transações: {data.get('n_tx', 0)}")
    else:
        print(f"      ❌ Erro HTTP: {resp.status_code}")
        print(f"      Resposta: {resp.text[:200]}")
except Exception as e:
    print(f"      ❌ Exceção: {e}")
    import traceback
    traceback.print_exc()

# 3. VERIFICAR O QUE O SISTEMA ESTÁ FAZENDO
print("\n3. 🐛 LOGS DO SISTEMA")

# Procurar arquivo de erro mais recente
import glob
from pathlib import Path

proof_dir = Path("transaction_proofs")
if proof_dir.exists():
    error_files = list(proof_dir.glob("btc_transaction_*.json"))
    if error_files:
        error_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        latest_error = error_files[0]
        print(f"   Último arquivo de erro: {latest_error}")
        
        try:
            with open(latest_error, 'r', encoding='utf-8') as f:
                error_data = json.load(f)
                print(f"   Conteúdo relevante:")
                if 'real_transaction' in error_data:
                    rt = error_data['real_transaction']
                    print(f"      from_address: {rt.get('from_address', 'N/A')}")
                    print(f"      balance: {rt.get('balance', 'N/A')}")
                    print(f"      utxos_count: {rt.get('utxos_count', 'N/A')}")
                    print(f"      error: {rt.get('error', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Não pude ler o arquivo: {e}")
    else:
        print("   ❌ Nenhum arquivo de erro encontrado")
else:
    print("   ❌ Diretório transaction_proofs não existe")

print("\n" + "=" * 70)
print("🎯 RESUMO DO DIAGNÓSTICO")
print("=" * 70)

print("""
PROBLEMAS POSSÍVEIS:
1. Sistema derivando endereço ERRADO da chave
2. API de blockchain retornando dados incorretos  
3. Cache persistente no sistema
4. Erro na busca de UTXOs
5. Endereço sendo modificado em runtime

SOLUÇÕES:
1. Logar EXATAMENTE qual endereço está sendo usado para buscar saldo
2. Forçar fresh fetch (sem cache) das APIs
3. Verificar se há múltiplos endereços sendo gerados
""")

