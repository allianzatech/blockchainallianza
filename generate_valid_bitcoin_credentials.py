#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerar credenciais Bitcoin válidas para testnet
"""

from bitcoinlib.keys import Key
import secrets

print("="*70)
print("🔑 GERANDO NOVAS CREDENCIAIS BITCOIN TESTNET VÁLIDAS")
print("="*70)

# Gerar chave privada aleatória
print("\n1. 🔑 Gerando chave privada aleatória...")
private_key_bytes = secrets.token_bytes(32)
print(f"   ✅ Chave privada gerada: {len(private_key_bytes)} bytes")
print(f"   HEX: {private_key_bytes.hex()}")

# Criar Key a partir dos bytes (chave privada)
print("\n2. 🔑 Criando Key (chave privada)...")
key = Key(private_key_bytes, network='testnet')
print(f"   ✅ Key criada")
print(f"   É privada: {key.is_private}")

# Obter WIF (chave privada)
print("\n3. 🟦 WIF Testnet (compressado - chave privada):")
wif = key.wif()
print(f"   {wif}")

# Verificar se é WIF válido
if wif.startswith(('c', '9', 'L', 'K')):
    print(f"   ✅ WIF válido (formato correto)")
else:
    print(f"   ❌ WIF inválido (deve começar com c, 9, L ou K)")

# Obter endereço
address = key.address()
print(f"\n4. ✅ Endereço Bitcoin Testnet3:")
print(f"   {address}")

# Obter HEX
private_hex = key.private_hex
print(f"\n5. 🔑 Private Key (HEX):")
print(f"   {private_hex}")

# Verificar se endereço é válido
print(f"\n6. 🔍 Validando endereço...")
try:
    import requests
    url = f"https://blockstream.info/testnet/api/address/{address}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        funded_txo_sum = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        spent_txo_sum = data.get('chain_stats', {}).get('spent_txo_sum', 0)
        balance = (funded_txo_sum - spent_txo_sum) / 100000000
        
        print(f"   ✅ Endereço válido e existe na rede")
        print(f"   Saldo: {balance:.8f} BTC")
        
        if balance < 0.0001:
            print(f"   ⚠️  Saldo insuficiente para testar (mínimo: 0.0001 BTC)")
            print(f"   💡 Use um faucet para adicionar fundos")
    elif response.status_code == 400:
        print(f"   ⚠️  Endereço pode não existir ainda (normal para novo endereço)")
    else:
        print(f"   ⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Erro ao verificar: {e}")

# Verificar se WIF deriva o endereço correto
print(f"\n7. 🔍 Verificando se WIF deriva o endereço correto...")
try:
    from bitcoinlib.keys import Key as KeyCheck
    key_check = KeyCheck(wif, network='testnet')
    derived_address = key_check.address()
    print(f"   WIF: {wif[:20]}...")
    print(f"   Endereço derivado: {derived_address}")
    print(f"   Endereço esperado: {address}")
    print(f"   ✅ Coincide: {derived_address == address}")
    
    if derived_address != address:
        print(f"   ❌ ERRO: Endereço derivado não corresponde!")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print(f"\n" + "="*70)
print("✅ CREDENCIAIS GERADAS COM SUCESSO!")
print("="*70)
print(f"\n📝 Adicione ao seu arquivo .env:")
print(f"BITCOIN_TESTNET_ADDRESS={address}")
print(f"BITCOIN_PRIVATE_KEY={wif}")
print(f"BTC_PRIVATE_KEY={wif}")
print(f"\n" + "="*70)
