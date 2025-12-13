#!/usr/bin/env python3
from bitcoinlib.keys import Key

# Chave WIF atual
current_wif = 'cRgLZfL8aoee5RYRqqKvqeZJTscb9rq6MTN1kNrcCQWqEAihLz21'
target_address = 'mkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt'

print("🔍 Verificando se a chave WIF corresponde ao endereço com saldo")
print("="*70)

try:
    key = Key(current_wif, network='testnet')
    derived_address = key.address()
    
    print(f"WIF atual: {current_wif}")
    print(f"Endereço derivado: {derived_address}")
    print(f"Endereço esperado: {target_address}")
    print(f"✅ Coincide: {derived_address == target_address}")
    
    if derived_address == target_address:
        print()
        print("✅✅✅ PERFEITO! A chave WIF atual corresponde ao endereço com saldo!")
        print("✅✅✅ O código já deve funcionar!")
    else:
        print()
        print("⚠️  A chave WIF atual NÃO corresponde ao endereço com saldo")
        print("💡 É necessário fornecer a chave WIF correspondente a:")
        print(f"   Endereço: {target_address}")
        print()
        print("💡 Para obter a chave WIF, você pode:")
        print("   1. Exportar da sua wallet Bitcoin testnet")
        print("   2. Ou usar o comando: bitcoin-cli dumpprivkey mkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

