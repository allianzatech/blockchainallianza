#!/usr/bin/env python3
"""
Script para testar validação de endereço Bitcoin
"""
import sys

def test_address(address):
    print(f"🔍 Testando endereço: {address}")
    print(f"   Comprimento: {len(address)} caracteres")
    print(f"   Formato: {'Bech32 Testnet' if address.startswith('tb1') else 'Desconhecido'}")
    
    # Teste 1: bech32
    print("\n📋 Teste 1: Biblioteca bech32")
    try:
        import bech32
        hrp = "tb"
        decoded = bech32.decode(hrp, address)
        if decoded:
            print(f"   ✅ bech32.decode OK")
            print(f"   HRP: {decoded[0]}")
            print(f"   Data length: {len(decoded[1])} bytes")
            if len(decoded[1]) in [20, 32]:
                print(f"   ✅ Comprimento válido")
            else:
                print(f"   ❌ Comprimento inválido (esperado 20 ou 32)")
        else:
            print(f"   ❌ bech32.decode retornou None")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: bitcoinlib
    print("\n📋 Teste 2: Biblioteca bitcoinlib")
    try:
        from bitcoinlib.keys import Address
        addr_obj = Address.import_address(address, network='testnet')
        if addr_obj:
            print(f"   ✅ bitcoinlib validou")
            print(f"   Address: {addr_obj.address}")
        else:
            print(f"   ❌ bitcoinlib retornou None")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Validação básica
    print("\n📋 Teste 3: Validação básica de formato")
    if len(address) >= 14 and len(address) <= 90:
        print(f"   ✅ Comprimento OK")
        bech32_chars = set('qpzry9x8gf2tvdw0s3jn54khce6mua7l')
        address_lower = address.lower()
        if all(c in bech32_chars or c.isdigit() for c in address_lower[3:]):
            print(f"   ✅ Caracteres válidos")
        else:
            print(f"   ❌ Caracteres inválidos")
    else:
        print(f"   ❌ Comprimento inválido")

if __name__ == "__main__":
    address = "tb1qxy2kgdygjrsqtzq2n0yrf2493p83kkfhrcndzj"
    if len(sys.argv) > 1:
        address = sys.argv[1]
    
    test_address(address)

