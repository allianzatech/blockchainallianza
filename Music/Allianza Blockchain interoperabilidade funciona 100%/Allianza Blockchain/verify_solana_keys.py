#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar chave privada e endereço Solana
"""

import os
import base58
from dotenv import load_dotenv

load_dotenv()

# Chaves do .env
private_key = os.getenv('SOLANA_PRIVATE_KEY', '').strip()
address = os.getenv('SOLANA_ADDRESS', '').strip()

print("=" * 70)
print("🔍 VERIFICAÇÃO DE CHAVES SOLANA")
print("=" * 70)

print(f"\n📋 Chave Privada (primeiros 20 chars): {private_key[:20]}...")
print(f"📋 Chave Privada (últimos 20 chars): ...{private_key[-20:]}")
print(f"📋 Comprimento: {len(private_key)} caracteres")

print(f"\n📍 Endereço: {address}")
print(f"📍 Comprimento: {len(address)} caracteres")

# Tentar decodificar chave privada
print(f"\n🔐 Decodificando chave privada Base58...")
try:
    keypair_bytes = base58.b58decode(private_key)
    print(f"   ✅ Decodificação Base58 bem-sucedida!")
    print(f"   📏 Tamanho decodificado: {len(keypair_bytes)} bytes")
    
    if len(keypair_bytes) == 64:
        print(f"   ✅ Tamanho correto! (64 bytes)")
    else:
        print(f"   ❌ Tamanho incorreto! Esperado: 64 bytes, Obtido: {len(keypair_bytes)} bytes")
        
    # Mostrar primeiros e últimos bytes
    print(f"   🔑 Primeiros 8 bytes: {keypair_bytes[:8].hex()}")
    print(f"   🔑 Últimos 8 bytes: {keypair_bytes[-8:].hex()}")
    
except Exception as e:
    print(f"   ❌ Erro ao decodificar Base58: {e}")
    import traceback
    traceback.print_exc()

# Tentar validar endereço
print(f"\n📍 Validando endereço Base58...")
try:
    address_bytes = base58.b58decode(address)
    print(f"   ✅ Decodificação Base58 bem-sucedida!")
    print(f"   📏 Tamanho decodificado: {len(address_bytes)} bytes")
    
    if len(address_bytes) == 32:
        print(f"   ✅ Tamanho correto! (32 bytes)")
    else:
        print(f"   ⚠️  Tamanho: {len(address_bytes)} bytes (esperado 32 para endereço Solana)")
        
except Exception as e:
    print(f"   ❌ Erro ao decodificar endereço: {e}")

# Tentar usar bibliotecas Solana se disponíveis
print(f"\n📚 Verificando bibliotecas Solana...")
try:
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    
    print(f"   ✅ Bibliotecas Solana disponíveis!")
    
    # Tentar criar keypair
    print(f"\n🔑 Criando Keypair...")
    try:
        keypair = Keypair.from_bytes(keypair_bytes)
        print(f"   ✅ Keypair criado com sucesso!")
        
        # Obter endereço público do keypair
        pubkey = keypair.pubkey()
        derived_address = str(pubkey)
        
        print(f"\n📍 Endereço derivado do Keypair: {derived_address}")
        print(f"📍 Endereço do .env:            {address}")
        
        if derived_address == address:
            print(f"   ✅✅✅ ENDEREÇOS COINCIDEM! Chave privada corresponde ao endereço!")
        else:
            print(f"   ❌❌❌ ENDEREÇOS NÃO COINCIDEM!")
            print(f"   ⚠️  A chave privada não corresponde ao endereço configurado")
            print(f"   💡 Use o endereço derivado ou gere uma nova chave privada")
            
    except Exception as e:
        print(f"   ❌ Erro ao criar Keypair: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError:
    print(f"   ⚠️  Bibliotecas Solana não disponíveis")
    print(f"   💡 Instale: pip install solana solders")
    print(f"   ⚠️  Não é possível verificar se a chave corresponde ao endereço")

print(f"\n" + "=" * 70)
print("✅ Verificação concluída!")
print("=" * 70)

