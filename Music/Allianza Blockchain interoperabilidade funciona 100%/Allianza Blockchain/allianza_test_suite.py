#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allianza Test Suite - Testes Públicos para Desenvolvedores
Qualquer pessoa pode baixar e executar localmente

Uso:
    python allianza_test_suite.py --test-all
    python allianza_test_suite.py --test qrs3
    python allianza_test_suite.py --test interop
"""

import argparse
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from allianza_blockchain import AllianzaBlockchain
    from quantum_security import QuantumSecuritySystem
    from testnet_public_tests import PublicTestRunner
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("Certifique-se de estar no diretório raiz do projeto")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Allianza Test Suite - Testes Públicos')
    parser.add_argument('--test-all', action='store_true', help='Executar todos os testes')
    parser.add_argument('--test', choices=['qrs3', 'interop', 'perf', 'block', 'security'], help='Executar teste específico')
    parser.add_argument('--output', default='allianza_test_results', help='Nome do arquivo de saída (sem extensão)')
    
    args = parser.parse_args()
    
    if not args.test_all and not args.test:
        parser.print_help()
        sys.exit(1)
    
    print("=" * 70)
    print("ALLIANZA QUANTUM TESTNET - TEST SUITE PÚBLICO")
    print("=" * 70)
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Versão: 1.0.0")
    print("=" * 70)
    print()
    
    # Inicializar sistemas
    print("🔧 Inicializando sistemas...")
    blockchain = AllianzaBlockchain()
    quantum_security = QuantumSecuritySystem()
    
    print("✅ Sistemas inicializados")
    print()
    
    # Criar test runner
    test_runner = PublicTestRunner(blockchain, quantum_security)
    
    if args.test_all:
        # Executar todos os testes
        print("🚀 Executando todos os testes...")
        print()
        result = test_runner.run_all_tests()
    else:
        # Executar teste específico
        test_methods = {
            'qrs3': test_runner.test_qrs3_signature,
            'interop': test_runner.test_interoperability,
            'perf': test_runner.test_performance,
            'block': test_runner.test_block_validation,
            'security': test_runner.test_quantum_security
        }
        
        test_method = test_methods.get(args.test)
        if not test_method:
            print(f"❌ Teste '{args.test}' não encontrado")
            sys.exit(1)
        
        print(f"🚀 Executando teste: {args.test}")
        print()
        result = test_method()
    
    # Salvar resultados
    output_file = Path(f"{args.output}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result if isinstance(result, dict) else {"result": result}, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 70)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 70)
    print(f"📄 Resultados salvos em: {output_file}")
    print()
    
    # Verificar sucesso baseado na estrutura do resultado
    all_passed = False
    if isinstance(result, dict):
        # Para run_all_tests, verificar summary
        if "summary" in result:
            summary = result["summary"]
            all_passed = summary.get("failed", 1) == 0 and summary.get("success_rate", 0) == 100.0
        # Para testes individuais, verificar success direto
        elif result.get("success"):
            all_passed = True
    
    if all_passed:
        print("✅ Todos os testes passaram!")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam")
        if isinstance(result, dict) and "summary" in result:
            summary = result["summary"]
            print(f"   📊 Taxa de sucesso: {summary.get('success_rate', 0):.1f}%")
            print(f"   ✅ Passaram: {summary.get('passed', 0)}/{summary.get('total_tests', 0)}")
            print(f"   ❌ Falharam: {summary.get('failed', 0)}/{summary.get('total_tests', 0)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

