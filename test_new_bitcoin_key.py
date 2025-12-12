#!/usr/bin/env python3
# Teste da nova chave Bitcoin

from bitcoinlib.keys import HDKey

# ⚠️ SEGURANÇA: Ler de variáveis de ambiente, não hardcoded
import os
from dotenv import load_dotenv
load_dotenv()

# Dados fornecidos - ler de env ou usar None
private_key_hex = os.getenv('BITCOIN_PRIVATE_KEY_HEX') or None
expected_address = os.getenv('BITCOIN_TESTNET_ADDRESS') or None
provided_wif = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or None

if not private_key_hex or not expected_address or not provided_wif:
    print("❌ ERRO: Configure as seguintes variáveis de ambiente:")
    print("   BITCOIN_PRIVATE_KEY_HEX - chave privada em formato hex")
    print("   BITCOIN_TESTNET_ADDRESS - endereço Bitcoin testnet esperado")
    print("   BITCOIN_PRIVATE_KEY - chave privada em formato WIF")
    exit(1)

print("🔍 TESTANDO NOVA CHAVE BITCOIN")
print("="*70)
print(f"Private Key HEX: {private_key_hex}")
print(f"WIF fornecido: {provided_wif}")
print(f"Endereço esperado: {expected_address}")
print()

# Tentar converter HEX para WIF
try:
    print("1. 🔄 Convertendo HEX para WIF (Legacy P2PKH)...")
    key_bytes = bytes.fromhex(private_key_hex)
    
    # Tentar gerar endereço Legacy (P2PKH) - começa com 'm' ou 'n' em testnet
    # IMPORTANTE: HDKey com bytes cria uma chave privada, então wif() retorna o WIF correto
    key_legacy = HDKey(key_bytes, network='testnet', witness_type='legacy')
    # Para obter WIF de chave privada, usar wif() diretamente
    correct_wif_legacy = key_legacy.wif()
    derived_address_legacy = key_legacy.address()
    
    # Verificar se é WIF de chave privada (começa com 'c' ou '9' em testnet)
    if not correct_wif_legacy.startswith(('c', '9')):
        # Se não começar com 'c' ou '9', tentar obter WIF da chave privada diretamente
        from bitcoinlib.keys import Key
        key_priv = Key(key_bytes, network='testnet')
        correct_wif_legacy = key_priv.wif()
        print(f"   🔄 WIF corrigido (usando Key): {correct_wif_legacy[:20]}...")
    
    print(f"   ✅ WIF Legacy gerado: {correct_wif_legacy}")
    print(f"   ✅ Endereço Legacy derivado: {derived_address_legacy}")
    print(f"   ✅ Endereço esperado: {expected_address}")
    print(f"   ✅ Coincide: {derived_address_legacy == expected_address}")
    
    # Também tentar SegWit
    key_segwit = HDKey(key_bytes, network='testnet', witness_type='segwit')
    derived_address_segwit = key_segwit.address()
    print(f"   📋 Endereço SegWit (para referência): {derived_address_segwit}")
    
    if derived_address_legacy == expected_address:
        print()
        print("✅✅✅ CHAVE E ENDEREÇO CORRETOS!")
        print(f"✅✅✅ USE ESTE WIF: {correct_wif_legacy}")
        final_wif = correct_wif_legacy
    else:
        print()
        print("⚠️  AVISO: Endereço Legacy derivado não corresponde ao esperado!")
        print(f"   Endereço Legacy derivado: {derived_address_legacy}")
        print(f"   Endereço esperado: {expected_address}")
        print()
        print("💡 Tentando verificar se o endereço esperado é válido...")
        
        # Verificar se o endereço esperado é válido
        try:
            from bitcoinlib.keys import Address
            addr_obj = Address.import_address(expected_address, network='testnet')
            print(f"   ✅ Endereço esperado é válido!")
            print(f"   💡 Pode ser que a chave HEX não corresponda a este endereço")
        except:
            print(f"   ⚠️  Endereço esperado pode ser inválido")
        
        final_wif = correct_wif_legacy
        
    # Testar o WIF fornecido
    print()
    print("2. 🔄 Testando WIF fornecido...")
    try:
        test_key = HDKey(provided_wif, network='testnet')
        print(f"   ✅ WIF fornecido é válido!")
        test_address = test_key.address()
        print(f"   Endereço do WIF fornecido: {test_address}")
        print(f"   Coincide com esperado: {test_address == expected_address}")
    except Exception as wif_err:
        print(f"   ❌ WIF fornecido é inválido: {wif_err}")
        print(f"   💡 Use o WIF correto gerado acima")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

