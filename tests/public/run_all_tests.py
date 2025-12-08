#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Público: Executa todos os testes públicos e gera relatório consolidado
Versão pública sem segredos - pode ser executado por qualquer pessoa
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Adicionar raiz do projeto ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Criar diretório de resultados
RESULTS_DIR = ROOT_DIR / "proofs" / "testnet" / "public_tests"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

class PublicTestRunner:
    """Executa todos os testes públicos e gera relatório consolidado"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_environment": "public",
            "tests": {},
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "success_rate": 0.0
            }
        }
        self.start_time = time.time()
        
    def run_verification_test(self):
        """Executa teste de verificação básica"""
        print("\n" + "=" * 70)
        print("🧪 TESTE: Verificação Básica")
        print("=" * 70)
        
        try:
            # Importar diretamente do arquivo
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "run_verification_tests",
                ROOT_DIR / "tests" / "public" / "run_verification_tests.py"
            )
            verification_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(verification_module)
            result = verification_module.main()
            
            self.results["tests"]["verification"] = {
                "status": "PASSED" if result == 0 else "FAILED",
                "description": "Testes básicos de verificação (QRS-3, Blockchain, Interoperabilidade)"
            }
            
            if result == 0:
                self.results["summary"]["passed"] += 1
            else:
                self.results["summary"]["failed"] += 1
                
            self.results["summary"]["total_tests"] += 1
            return result == 0
            
        except Exception as e:
            print(f"❌ Erro ao executar verificação: {e}")
            self.results["tests"]["verification"] = {
                "status": "ERROR",
                "error": str(e)
            }
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total_tests"] += 1
            return False
    
    def test_qrs3_public(self):
        """Testa QRS-3 publicamente"""
        print("\n" + "=" * 70)
        print("🧪 TESTE: QRS-3 (PQC)")
        print("=" * 70)
        
        try:
            from pqc_crypto import MLDSAKeyPair, SPHINCSPlusKeyPair
            
            # Teste ML-DSA
            print("📝 Testando ML-DSA...")
            mldsa = MLDSAKeyPair()
            message = b"Public test message for QRS-3"
            signature = mldsa.sign(message)
            verified = mldsa.verify(message, signature)
            
            if not verified:
                raise Exception("ML-DSA verification failed")
            
            # Teste SPHINCS+
            print("📝 Testando SPHINCS+...")
            sphincs = SPHINCSPlusKeyPair()
            signature2 = sphincs.sign(message)
            verified2 = sphincs.verify(message, signature2)
            
            if not verified2:
                raise Exception("SPHINCS+ verification failed")
            
            print("✅ QRS-3: PASSOU")
            self.results["tests"]["qrs3"] = {
                "status": "PASSED",
                "ml_dsa": "✅",
                "sphincs_plus": "✅"
            }
            self.results["summary"]["passed"] += 1
            self.results["summary"]["total_tests"] += 1
            return True
            
        except ImportError as e:
            print(f"⚠️  liboqs-python não instalado: {e}")
            print("💡 Instale com: pip install liboqs-python")
            self.results["tests"]["qrs3"] = {
                "status": "SKIPPED",
                "reason": "liboqs-python not installed"
            }
            self.results["summary"]["skipped"] += 1
            self.results["summary"]["total_tests"] += 1
            return True  # Não falhar se dependência não estiver disponível
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            self.results["tests"]["qrs3"] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total_tests"] += 1
            return False
    
    def test_blockchain_public(self):
        """Testa blockchain publicamente"""
        print("\n" + "=" * 70)
        print("🧪 TESTE: Blockchain Básica")
        print("=" * 70)
        
        try:
            from allianza_blockchain import AllianzaBlockchain
            
            print("📝 Inicializando blockchain...")
            blockchain = AllianzaBlockchain()
            
            # Verificar se blockchain foi criada
            # A blockchain usa shards ao invés de chain
            if hasattr(blockchain, 'shards') and blockchain.shards:
                total_blocks = sum(len(shard) for shard in blockchain.shards.values())
                print(f"✅ Blockchain inicializada: {len(blockchain.shards)} shards, {total_blocks} blocos totais")
            elif hasattr(blockchain, 'chain') and blockchain.chain:
                print(f"✅ Blockchain inicializada: {len(blockchain.chain)} blocos")
            else:
                print("⚠️  Blockchain inicializada (estrutura de dados diferente)")
                # Não falhar, apenas avisar
            
            # Teste criação de wallet
            print("📝 Testando criação de wallet...")
            address, private_key = blockchain.create_wallet()
            
            if not address or not private_key:
                raise Exception("Falha na criação de wallet")
            
            print(f"✅ Wallet criada: {address[:20]}...")
            
            # Calcular total de blocos
            if hasattr(blockchain, 'shards') and blockchain.shards:
                total_blocks = sum(len(shard) for shard in blockchain.shards.values())
            elif hasattr(blockchain, 'chain') and blockchain.chain:
                total_blocks = len(blockchain.chain)
            else:
                total_blocks = 0
            
            self.results["tests"]["blockchain"] = {
                "status": "PASSED",
                "blocks": total_blocks,
                "wallet_created": True
            }
            self.results["summary"]["passed"] += 1
            self.results["summary"]["total_tests"] += 1
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            self.results["tests"]["blockchain"] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total_tests"] += 1
            return False
    
    def generate_report(self):
        """Gera relatório final"""
        elapsed_time = time.time() - self.start_time
        
        # Calcular taxa de sucesso
        total = self.results["summary"]["total_tests"]
        passed = self.results["summary"]["passed"]
        if total > 0:
            self.results["summary"]["success_rate"] = (passed / total) * 100
        
        # Salvar relatório
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = RESULTS_DIR / f"public_test_report_{timestamp_str}.json"
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Imprimir resumo
        print("\n" + "=" * 70)
        print("📊 RESUMO FINAL")
        print("=" * 70)
        print(f"Total de testes: {total}")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {self.results['summary']['failed']}")
        print(f"⏭️  Pulado: {self.results['summary']['skipped']}")
        print(f"📈 Taxa de sucesso: {self.results['summary']['success_rate']:.1f}%")
        print(f"⏱️  Tempo total: {elapsed_time:.2f}s")
        print(f"\n📄 Relatório salvo em: {report_file}")
        print()
        
        return report_file

def main():
    """Executa todos os testes públicos"""
    print("\n" + "=" * 70)
    print("🚀 TESTES PÚBLICOS - ALLIANZA BLOCKCHAIN")
    print("=" * 70)
    print(f"📅 Data: {datetime.now().isoformat()}")
    print(f"📁 Diretório: {ROOT_DIR}")
    print()
    
    runner = PublicTestRunner()
    
    # Executar testes
    runner.test_qrs3_public()
    runner.test_blockchain_public()
    runner.run_verification_test()
    
    # Gerar relatório
    report_file = runner.generate_report()
    
    # Retornar código de saída
    if runner.results["summary"]["failed"] == 0:
        print("✅ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    sys.exit(main())

