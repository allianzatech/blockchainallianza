#!/usr/bin/env python3
from bitcoinlib.keys import Key

# Novo endereço gerado
new_wif = 'cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN'
expected_address = 'mft38vhDpoF4qEAFChbfxZ5UrUemSViHHh'

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

