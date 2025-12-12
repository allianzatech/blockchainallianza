#!/usr/bin/env python3
from bitcoinlib.keys import Key

# ⚠️ SEGURANÇA: Ler de variáveis de ambiente, não hardcoded
import os
from dotenv import load_dotenv
load_dotenv()

# Novo endereço gerado - ler de env
new_wif = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or None
expected_address = os.getenv('BITCOIN_TESTNET_ADDRESS') or None

if not new_wif or not expected_address:
    print("❌ ERRO: Configure BITCOIN_PRIVATE_KEY e BITCOIN_TESTNET_ADDRESS no .env")
    exit(1)

print("🔍 VERIFICANDO NOVO ENDEREÇO GERADO")
print("="*70)

try:
    key = Key(new_wif, network='testnet')
    derived_address = key.address()
    private_hex = key.private_hex
    
    print(f"✅ WIF válido!")
    print(f"   WIF: {new_wif}")
    print(f"   Endereço derivado: {derived_address}")
    print(f"   Endereço esperado: {expected_address}")
    print(f"   ✅ Coincide: {derived_address == expected_address}")
    print(f"   Private key hex: {private_hex}")
    
    if derived_address == expected_address:
        print()
        print("✅✅✅ PERFEITO! WIF e endereço correspondem!")
        print("✅✅✅ Pronto para usar após pegar fundos do faucet!")
    else:
        print()
        print("⚠️  AVISO: Endereço derivado não corresponde ao esperado!")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

