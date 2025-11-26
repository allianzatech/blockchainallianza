# test_bitcoin_fixes.py
# 🧪 TESTE COMPLETO DAS CORREÇÕES IMPLEMENTADAS

import os
import json
from bitcoin_transaction_fixer import bitcoin_transaction_fixer

def test_bitcoin_transaction_fixes():
    """Testa todas as correções implementadas"""
    
    print("🧪 INICIANDO TESTE DAS CORREÇÕES BITCOIN")
    print("=" * 50)
    
    # Configuração de teste
    test_private_key = os.getenv('BITCOIN_PRIVATE_KEY') or "cSamqcRz79F2mQbwJZLaSFkKpVa9T5cQz3R2jZqJ8XK1NvGtYbWw"
    test_to_address = "mzBc4XEFSdzCDcTxAgf6EZXgsZWpztRhef"
    test_amount = 0.00001  # 1000 satoshis
    
    print(f"🔑 Chave privada: {test_private_key[:10]}...")
    print(f"📫 Endereço destino: {test_to_address}")
    print(f"💰 Quantidade: {test_amount} BTC")
    
    # Teste 1: Validação de endereço
    print("\n1. ✅ TESTANDO VALIDAÇÃO DE ENDEREÇO...")
    is_valid, error = bitcoin_transaction_fixer._validate_bitcoin_address(test_to_address)
    if is_valid:
        print("   ✅ Validação de endereço: OK")
    else:
        print(f"   ❌ Validação de endereço falhou: {error}")
        return False
    
    # Teste 2: Obtenção de UTXOs
    print("\n2. ✅ TESTANDO OBTENÇÃO DE UTXOs...")
    from_address = bitcoin_transaction_fixer._get_address_from_private_key(test_private_key)
    if from_address:
        print(f"   ✅ Endereço obtido da chave: {from_address}")
        utxos = bitcoin_transaction_fixer._get_utxos_fixed(from_address)
        if utxos:
            print(f"   ✅ UTXOs encontrados: {len(utxos)}")
            for utxo in utxos[:3]:  # Mostrar apenas os 3 primeiros
                print(f"      📦 {utxo['txid'][:20]}...:{utxo['vout']} = {utxo['value']} sats")
        else:
            print("   ⚠️  Nenhum UTXO encontrado (pode ser normal para novo endereço)")
    else:
        print("   ❌ Não foi possível obter endereço da chave privada")
        return False
    
    # Teste 3: Método Blockstream
    print("\n3. ✅ TESTANDO MÉTODO BLOCKSTREAM...")
    if utxos:
        blockstream_result = bitcoin_transaction_fixer._try_blockstream_method(
            test_private_key, from_address, test_to_address, 1000, utxos
        )
        if blockstream_result.get("success"):
            print("   ✅ Método Blockstream: OK")
            print(f"      TX Hash: {blockstream_result.get('tx_hash')}")
        else:
            print(f"   ⚠️  Método Blockstream falhou: {blockstream_result.get('error')}")
    else:
        print("   ⚠️  Pulando teste Blockstream (sem UTXOs)")
    
    # Teste 4: Método BlockCypher Corrigido
    print("\n4. ✅ TESTANDO MÉTODO BLOCKCYPHER CORRIGIDO...")
    if utxos:
        blockcypher_result = bitcoin_transaction_fixer._try_blockcypher_fixed(
            from_address, test_to_address, 1000, utxos
        )
        if blockcypher_result.get("success"):
            print("   ✅ Método BlockCypher: OK")
            if blockcypher_result.get("needs_signing"):
                print("      ⚠️  Transação precisa de assinatura manual")
            else:
                print(f"      TX Hash: {blockcypher_result.get('tx_hash')}")
        else:
            print(f"   ⚠️  Método BlockCypher falhou: {blockcypher_result.get('error')}")
    else:
        print("   ⚠️  Pulando teste BlockCypher (sem UTXOs)")
    
    # Teste 5: Método Principal Completo
    print("\n5. ✅ TESTANDO MÉTODO PRINCIPAL COMPLETO...")
    main_result = bitcoin_transaction_fixer.fix_and_send_transaction(
        from_private_key=test_private_key,
        to_address=test_to_address,
        amount_btc=test_amount
    )
    
    print(f"   📊 Resultado principal: {main_result.get('success')}")
    if main_result.get("success"):
        print("   ✅ ✅ ✅ TODAS AS CORREÇÕES FUNCIONANDO! ✅ ✅ ✅")
        print(f"      TX Hash: {main_result.get('tx_hash')}")
        print(f"      Método: {main_result.get('method')}")
        print(f"      Explorer: {main_result.get('explorer_url')}")
    else:
        print(f"   ❌ Método principal falhou: {main_result.get('error')}")
        print(f"      Detalhes: {json.dumps(main_result, indent=2)}")
    
    print("\n" + "=" * 50)
    print("🧪 TESTE CONCLUÍDO")
    
    return main_result.get("success", False)

if __name__ == "__main__":
    success = test_bitcoin_transaction_fixes()
    if success:
        print("\n🎉 PARABÉNS! Todas as correções estão funcionando!")
        print("   Os erros 'function object has no attribute hex' e 'tx_data is not defined'")
        print("   foram resolvidos com sucesso! 🚀")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os logs acima.")