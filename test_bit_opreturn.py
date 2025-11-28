#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar criação de transação Bitcoin com OP_RETURN usando biblioteca 'bit'
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Obter chave privada do .env
private_key_wif = os.getenv('BITCOIN_TESTNET_PRIVATE_KEY') or os.getenv('BITCOIN_PRIVATE_KEY')

if not private_key_wif:
    print("❌ Chave privada não encontrada no .env")
    exit(1)

print(f"🔑 Chave privada: {private_key_wif[:15]}...")

# Testar importação da biblioteca 'bit'
try:
    from bit import PrivateKey
    from bit.network import NetworkAPI
    print("✅ Biblioteca 'bit' importada com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar biblioteca 'bit': {e}")
    exit(1)

# Criar PrivateKey
try:
    key = PrivateKey(private_key_wif)
    print(f"✅ PrivateKey criada! Endereço: {key.address}")
    
    # Buscar UTXOs
    print(f"\n🔍 Buscando UTXOs para {key.address}...")
    unspents = key.get_unspents()
    print(f"✅ {len(unspents)} UTXOs encontrados")
    if unspents:
        total_value = sum(u.amount for u in unspents)
        print(f"   Valor total: {total_value} satoshis ({total_value / 100000000} BTC)")
        for i, u in enumerate(unspents[:3]):  # Mostrar apenas os 3 primeiros
            print(f"   UTXO {i+1}: {u.txid}:{u.txindex} = {u.amount} satoshis")
except Exception as e:
    print(f"❌ Erro ao criar PrivateKey ou buscar UTXOs: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Dados de teste
to_address = "tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q"
amount_satoshis = 1000
op_return_data = "ALZ:188a4e2a8850ecea3a47b1bd85f55496cfd73415ef825bf5249d3f7e364b3427"

print(f"\n📝 Testando criação de transação com OP_RETURN...")
print(f"   Para: {to_address}")
print(f"   Valor: {amount_satoshis} satoshis")
print(f"   OP_RETURN: {op_return_data}")

# Testar diferentes formatos
formats_to_test = [
    ("Formato 1: OP_RETURN como string no output", [
        (to_address, amount_satoshis, 'satoshi'),
        (f"OP_RETURN {op_return_data}", 0, 'satoshi')
    ]),
    ("Formato 2: Dados diretos no output", [
        (to_address, amount_satoshis, 'satoshi'),
        (op_return_data, 0, 'satoshi')
    ]),
    ("Formato 3: Hex dos dados", [
        (to_address, amount_satoshis, 'satoshi'),
        (op_return_data.encode('utf-8').hex(), 0, 'satoshi')
    ]),
    ("Formato 4: Parâmetro op_return", None),  # Será testado separadamente
]

for format_name, outputs in formats_to_test:
    if outputs is None:
        # Testar parâmetro op_return
        print(f"\n🧪 {format_name}...")
        try:
            test_outputs = [(to_address, amount_satoshis, 'satoshi')]
            # Verificar se create_transaction aceita parâmetro op_return
            import inspect
            sig = inspect.signature(key.create_transaction)
            if 'op_return' in sig.parameters:
                print(f"   ✅ create_transaction aceita parâmetro op_return")
                try:
                    tx_hex = key.create_transaction(outputs=test_outputs, op_return=op_return_data)
                    print(f"   ✅✅✅ SUCESSO! Transação criada com parâmetro op_return")
                    print(f"      Tamanho: {len(tx_hex)} bytes")
                    # Verificar se OP_RETURN está na transação
                    if op_return_data.encode('utf-8').hex() in tx_hex or op_return_data in tx_hex:
                        print(f"   ✅ OP_RETURN confirmado na transação!")
                    break
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    print(f"      Tipo: {type(e).__name__}")
            else:
                print(f"   ⚠️  create_transaction NÃO aceita parâmetro op_return")
        except Exception as e:
            print(f"   ❌ Erro ao verificar assinatura: {e}")
    else:
        print(f"\n🧪 {format_name}...")
        try:
            # A biblioteca 'bit' precisa de UTXOs, vamos passar explicitamente
            if unspents:
                tx_hex = key.create_transaction(outputs=outputs, unspents=unspents)
            else:
                # Se não tiver UTXOs, deixar a biblioteca buscar automaticamente
                tx_hex = key.create_transaction(outputs=outputs)
            print(f"   ✅✅✅ SUCESSO! Transação criada")
            print(f"      Tamanho: {len(tx_hex)} bytes")
            # Verificar se OP_RETURN está na transação
            if op_return_data.encode('utf-8').hex() in tx_hex or op_return_data in tx_hex:
                print(f"   ✅ OP_RETURN confirmado na transação!")
            break
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            print(f"      Tipo: {type(e).__name__}")
            import traceback
            traceback.print_exc()

print("\n✅ Teste concluído!")

