#!/usr/bin/env python3
"""
Gera novo endereço Bitcoin Testnet3 com chave privada WIF
"""

from bitcoinlib.keys import Key
import secrets

print("🔐 GERANDO NOVO ENDEREÇO BITCOIN TESTNET")
print("="*70)

# Gerar chave privada aleatória (32 bytes)
private_key_bytes = secrets.token_bytes(32)

# Criar chave Bitcoin testnet (compressed)
key = Key(private_key_bytes, network='testnet', compressed=True)

# Obter WIF e endereço
wif = key.wif()
address = key.address()
private_hex = key.private_hex

print()
print("✅ NOVO ENDEREÇO GERADO!")
print("="*70)
print()
print("🏦 Endereço Bitcoin Testnet3:")
print(f"   {address}")
print()
print("🔑 Chave Privada (WIF - Testnet, compressed):")
print(f"   {wif}")
print()
print("🔑 Chave Privada (HEX):")
print(f"   {private_hex}")
print()
print("="*70)
print()
print("📋 INSTRUÇÕES:")
print("   1. Copie o endereço acima")
print("   2. Acesse um faucet Bitcoin testnet:")
print("      - https://bitcoinfaucet.uo1.net/")
print("      - https://testnet-faucet.mempool.co/")
print("      - https://coinfaucet.eu/en/btc-testnet/")
print("   3. Cole o endereço e solicite fundos")
print("   4. Aguarde algumas confirmações")
print("   5. Use este WIF no código:")
print(f"      BITCOIN_PRIVATE_KEY={wif}")
print()
print("⚠️  IMPORTANTE: Guarde este WIF em local seguro!")
print("   Este é um endereço de TESTE, mas ainda assim mantenha privado.")
print()

