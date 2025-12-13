#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICADOR DE CHAVE BITCOIN NO RENDER
Verifica se a chave configurada gera o endereço correto
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
if os.path.exists('.env'):
    load_dotenv('.env')

print("="*70)
print("🔍 VERIFICAÇÃO DE CHAVE BITCOIN")
print("="*70)

# Chave correta que gera o endereço com saldo
CHAVE_CORRETA = "cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ"
ENDERECO_ESPERADO = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"

# Chave errada (exemplo)
CHAVE_ERRADA = "cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN"

print(f"\n📍 Endereço esperado (com saldo): {ENDERECO_ESPERADO}")
print(f"🔑 Chave CORRETA: {CHAVE_CORRETA[:30]}...")
print(f"❌ Chave ERRADA (exemplo): {CHAVE_ERRADA[:30]}...")

try:
    from bitcoinlib.keys import HDKey
    
    # Verificar chave correta
    print(f"\n1. ✅ Verificando chave CORRETA...")
    key_correta = HDKey(CHAVE_CORRETA, network='testnet')
    addr_correta = key_correta.address()
    print(f"   Endereço gerado: {addr_correta}")
    print(f"   ✅ Correspondem? {addr_correta == ENDERECO_ESPERADO}")
    
    # Verificar chave errada
    print(f"\n2. ❌ Verificando chave ERRADA...")
    key_errada = HDKey(CHAVE_ERRADA, network='testnet')
    addr_errada = key_errada.address()
    print(f"   Endereço gerado: {addr_errada}")
    print(f"   ❌ Correspondem? {addr_errada == ENDERECO_ESPERADO}")
    
    # Verificar chave do ambiente
    print(f"\n3. 🌍 Verificando chave do AMBIENTE...")
    env_key = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or os.getenv('BTC_PRIVATE_KEY')
    
    if env_key:
        print(f"   Chave encontrada: {env_key[:30]}... (tamanho: {len(env_key)})")
        
        # Verificar se é a chave correta
        if env_key.strip() == CHAVE_CORRETA:
            print(f"   ✅✅✅ CHAVE CORRETA CONFIGURADA!")
        elif env_key.strip() == CHAVE_ERRADA:
            print(f"   ❌❌❌ CHAVE ERRADA CONFIGURADA!")
            print(f"   ⚠️  Esta chave gera um endereço diferente e sem saldo!")
        else:
            print(f"   ⚠️  Chave diferente das conhecidas, verificando...")
            try:
                key_env = HDKey(env_key.strip(), network='testnet')
                addr_env = key_env.address()
                print(f"   Endereço gerado: {addr_env}")
                if addr_env == ENDERECO_ESPERADO:
                    print(f"   ✅✅✅ Esta chave gera o endereço correto!")
                else:
                    print(f"   ❌ Esta chave NÃO gera o endereço esperado!")
                    print(f"   ⚠️  Endereço esperado: {ENDERECO_ESPERADO}")
                    print(f"   ⚠️  Endereço gerado: {addr_env}")
            except Exception as e:
                print(f"   ❌ Erro ao processar chave: {e}")
    else:
        print(f"   ❌ Nenhuma chave Bitcoin encontrada no ambiente!")
        print(f"   Configure BITCOIN_PRIVATE_KEY, BITCOIN_TESTNET_PRIVATE_KEY ou BTC_PRIVATE_KEY")
    
    print(f"\n" + "="*70)
    print(f"🎯 INSTRUÇÕES PARA CORRIGIR NO RENDER:")
    print(f"="*70)
    print(f"\n1. Acesse o Render Dashboard")
    print(f"2. Vá em Environment Variables")
    print(f"3. Configure BITCOIN_PRIVATE_KEY com:")
    print(f"   {CHAVE_CORRETA}")
    print(f"\n4. OU configure BITCOIN_TESTNET_PRIVATE_KEY com:")
    print(f"   {CHAVE_CORRETA}")
    print(f"\n5. Reinicie o serviço após alterar")
    print(f"\n⚠️  IMPORTANTE: A chave deve gerar o endereço:")
    print(f"   {ENDERECO_ESPERADO}")
    print(f"\n" + "="*70)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

