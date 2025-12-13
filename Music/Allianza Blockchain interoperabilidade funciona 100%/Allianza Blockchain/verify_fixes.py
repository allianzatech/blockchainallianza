# verify_fixes.py
# 🔍 VERIFICA SE AS CORREÇÕES ESPECÍFICAS ESTÃO IMPLEMENTADAS

import inspect
from bitcoin_transaction_fixer import BitcoinTransactionFixer

def verify_fixes_implemented():
    """Verifica se todas as correções específicas foram implementadas"""
    
    print("🔍 VERIFICANDO IMPLEMENTAÇÃO DAS CORREÇÕES")
    print("=" * 50)
    
    fixer = BitcoinTransactionFixer()
    
    # 1. Verificar correção do erro 'function object has no attribute hex'
    print("\n1. ✅ VERIFICANDO CORREÇÃO: 'function object has no attribute hex'")
    method_source = inspect.getsource(fixer._get_raw_tx_corrected)
    
    checks = [
        "callable" in method_source,  # Verifica se é callable
        "raw_hex()" in method_source,  # Chama como função
        "hasattr" in method_source,    # Verifica atributos
        "multiple methods" in method_source or "métodos" in method_source  # Fallback
    ]
    
    if all(checks):
        print("   ✅ Correção implementada: Verificação de callable + múltiplos métodos")
    else:
        print("   ❌ Correção incompleta")
        print(f"      Checks: {checks}")
    
    # 2. Verificar correção do erro 'tx_data is not defined'
    print("\n2. ✅ VERIFICANDO CORREÇÃO: 'tx_data is not defined'")
    blockcypher_source = inspect.getsource(fixer._try_blockcypher_fixed)
    
    checks = [
        "tx_data_corrected" in blockcypher_source,  # Variável definida corretamente
        "tx_data_corrected =" in blockcypher_source,  # Atribuição correta
        "json=tx_data_corrected" in blockcypher_source  # Uso correto
    ]
    
    if all(checks):
        print("   ✅ Correção implementada: tx_data_corrected definido antes do uso")
    else:
        print("   ❌ Correção incompleta")
        print(f"      Checks: {checks}")
    
    # 3. Verificar métodos disponíveis
    print("\n3. ✅ VERIFICANDO MÉTODOS DISPONÍVEIS")
    methods = [m for m in dir(fixer) if not m.startswith('_')]
    print(f"   Métodos públicos: {methods}")
    
    required_methods = ['fix_and_send_transaction', '_try_blockstream_method', '_try_blockcypher_fixed']
    missing_methods = [m for m in required_methods if m not in methods]
    
    if not missing_methods:
        print("   ✅ Todos os métodos necessários estão disponíveis")
    else:
        print(f"   ❌ Métodos faltando: {missing_methods}")
    
    print("\n" + "=" * 50)
    print("🔍 VERIFICAÇÃO CONCLUÍDA")

if __name__ == "__main__":
    verify_fixes_implemented()