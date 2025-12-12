#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICADOR DE CHAVE PRIVADA E ENDEREÇO BITCOIN
Verifica se a chave privada do .env corresponde ao endereço usado
"""

import os
from dotenv import load_dotenv

load_dotenv()

def verify_bitcoin_key_address():
    """Verifica se a chave privada corresponde ao endereço"""
    print(f"\n{'='*70}")
    print(f"🔍 VERIFICANDO CHAVE PRIVADA E ENDEREÇO BITCOIN")
    print(f"{'='*70}")
    
    # 1. Obter chave privada do .env
    private_key = (
        os.getenv('BITCOIN_PRIVATE_KEY') or 
        os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or 
        os.getenv('BTC_PRIVATE_KEY')
    )
    
    if not private_key:
        print(f"❌ NENHUMA CHAVE PRIVADA ENCONTRADA NO .env")
        print(f"\n💡 Configure uma das seguintes variáveis:")
        print(f"   - BITCOIN_PRIVATE_KEY")
        print(f"   - BITCOIN_TESTNET_PRIVATE_KEY")
        print(f"   - BTC_PRIVATE_KEY")
        return
    
    print(f"\n1. 📋 Chave privada do .env:")
    print(f"   Variável: {'BITCOIN_PRIVATE_KEY' if os.getenv('BITCOIN_PRIVATE_KEY') else 'BITCOIN_TESTNET_PRIVATE_KEY' if os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') else 'BTC_PRIVATE_KEY'}")
    print(f"   Chave: {private_key[:20]}... (tamanho: {len(private_key)})")
    
    # 2. Verificar formato
    formato = "WIF" if private_key.startswith(('c', '9', '5', 'K', 'L')) else "HEX" if len(private_key) == 64 or (private_key.startswith('0x') and len(private_key) == 66) else "INVALID"
    print(f"   Formato: {formato}")
    
    # 3. Derivar endereço da chave
    print(f"\n2. 🔑 Derivando endereço da chave privada...")
    try:
        from bitcoinlib.keys import HDKey
        
        # Se for HEX, converter para WIF primeiro
        if formato == "HEX":
            print(f"   🔄 Convertendo HEX para WIF...")
            hex_key = private_key[2:] if private_key.startswith('0x') else private_key
            key_bytes = bytes.fromhex(hex_key)
            key = HDKey(key_bytes, network='testnet')
            wif = key.wif()
            print(f"   ✅ WIF: {wif[:20]}...")
        else:
            # Já é WIF
            key = HDKey(private_key, network='testnet')
            wif = private_key
        
        # Obter endereço
        derived_address = key.address()
        print(f"   ✅ Endereço derivado: {derived_address}")
        
    except Exception as e:
        print(f"   ❌ Erro ao derivar endereço: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Obter endereço do .env (se configurado)
    env_address = (
        os.getenv('BITCOIN_TESTNET_ADDRESS') or 
        os.getenv('BITCOIN_ADDRESS') or 
        os.getenv('BTC_ADDRESS')
    )
    
    print(f"\n3. 📍 Endereço do .env:")
    if env_address:
        print(f"   Endereço: {env_address}")
        
        # Comparar
        if derived_address == env_address:
            print(f"   ✅✅✅ ENDEREÇOS COINCIDEM! Chave privada corresponde ao endereço!")
        else:
            print(f"   ⚠️  ENDEREÇOS NÃO COINCIDEM!")
            print(f"   Endereço derivado da chave: {derived_address}")
            print(f"   Endereço no .env:           {env_address}")
            print(f"\n💡 SOLUÇÃO:")
            print(f"   Atualize o .env com o endereço correto:")
            print(f"   BITCOIN_TESTNET_ADDRESS={derived_address}")
    else:
        print(f"   ⚠️  Nenhum endereço configurado no .env")
        print(f"\n💡 RECOMENDAÇÃO:")
        print(f"   Adicione ao .env:")
        print(f"   BITCOIN_TESTNET_ADDRESS={derived_address}")
    
    # 5. Verificar saldo do endereço derivado
    print(f"\n4. 💰 Verificando saldo do endereço derivado...")
    try:
        import requests
        balance_url = f"https://blockstream.info/testnet/api/address/{derived_address}"
        balance_resp = requests.get(balance_url, timeout=10)
        
        if balance_resp.status_code == 200:
            balance_data = balance_resp.json()
            funded = balance_data.get('chain_stats', {}).get('funded_txo_sum', 0)
            spent = balance_data.get('chain_stats', {}).get('spent_txo_sum', 0)
            balance = funded - spent
            print(f"   💰 Saldo: {balance} satoshis ({balance/100000000:.8f} BTC)")
            
            if balance > 0:
                print(f"   ✅ Endereço tem saldo disponível!")
            else:
                print(f"   ⚠️  Endereço não tem saldo. Use um faucet para obter fundos.")
        else:
            print(f"   ⚠️  Erro ao verificar saldo: {balance_resp.status_code}")
    except Exception as e:
        print(f"   ⚠️  Erro ao verificar saldo: {e}")
    
    print(f"\n{'='*70}")
    print(f"📋 RESUMO")
    print(f"{'='*70}")
    print(f"   Chave privada: {private_key[:20]}... ({formato})")
    print(f"   Endereço derivado: {derived_address}")
    if env_address:
        print(f"   Endereço no .env: {env_address}")
        print(f"   Coincidem: {'✅ SIM' if derived_address == env_address else '❌ NÃO'}")
    print(f"{'='*70}")

if __name__ == "__main__":
    verify_bitcoin_key_address()

