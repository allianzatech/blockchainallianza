#!/usr/bin/env python3
from bitcoinlib.keys import Key, HDKey
import base58

# WIF fornecido
provided_wif = 'cTpB4xWUt9XyY3H3UX77YPDhmPEw24kTx5cHGNy8hLTsSjP6CSqC'
expected_address = 'mkHS9ne12qx9pS9VojpwU5xtRd4T7X7ZUt'

print("🔍 TESTANDO WIF FORNECIDO")
print("="*70)
print(f"WIF fornecido: {provided_wif}")
print(f"Endereço esperado: {expected_address}")
print()

# Tentar diferentes métodos
methods = [
    ("Key (testnet)", lambda: Key(provided_wif, network='testnet')),
    ("HDKey (testnet)", lambda: HDKey(provided_wif, network='testnet')),
    ("Key (mainnet)", lambda: Key(provided_wif, network='bitcoin')),
    ("HDKey (mainnet)", lambda: HDKey(provided_wif, network='bitcoin')),
]

for method_name, method_func in methods:
    try:
        print(f"Tentando {method_name}...")
        key = method_func()
        address = key.address()
        print(f"   ✅ Sucesso! Endereço: {address}")
        print(f"   ✅ Coincide: {address == expected_address}")
        if address == expected_address:
            print(f"   ✅✅✅ ENCONTRADO! Use este método: {method_name}")
            print(f"   ✅ WIF válido: {provided_wif}")
            break
    except Exception as e:
        print(f"   ❌ Falhou: {str(e)[:80]}")

print()
print("💡 Se nenhum método funcionou, o WIF pode estar incorreto ou em formato diferente")

