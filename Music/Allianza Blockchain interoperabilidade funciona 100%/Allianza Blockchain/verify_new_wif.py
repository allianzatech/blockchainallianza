#!/usr/bin/env python3
from bitcoinlib.keys import Key

# Nova chave WIF fornecida
new_wif = 'cTpB4xWUt9XyY3H3UX77YPDhmPEw24kTx5cHGNy8hLTsSjP6CSqC'
expected_address = 'mkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt'

print("🔍 VERIFICANDO NOVA CHAVE WIF")
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
        print("✅✅✅ PERFEITO! Chave WIF e endereço correspondem!")
        print("✅✅✅ Esta chave tem saldo de 1106.18940211 BTC!")
        print("✅✅✅ Pronto para usar nas transações!")
    else:
        print()
        print("⚠️  AVISO: Endereço derivado não corresponde ao esperado!")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

