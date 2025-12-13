#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Master: Executa todos os testes e gera relatório consolidado para investidores
"""

import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Criar diretório de resultados
RESULTS_DIR = Path("proofs") / "relatorio_investidores"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

class TestRunner:
    """Executa todos os testes e gera relatório consolidado"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "success_rate": 0.0
            }
        }
        self.start_time = time.time()
        
    def run_test(self, test_name: str, script_path: str, description: str) -> Dict:
        """Executar um teste e capturar resultados"""
        print("=" * 70)
        print(f"🧪 TESTE: {test_name}")
        print("=" * 70)
        print(f"📝 Descrição: {description}")
        print(f"📄 Script: {script_path}")
        print()
        
        start_time = time.time()
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos máximo
            )
            
            elapsed_time = time.time() - start_time
            success = result.returncode == 0
            
            # Analisar saída para determinar sucesso
            output = result.stdout + result.stderr
            success_keywords = ["✅", "PASSOU", "100%", "SUCESSO", "SUCCESS", "100.0%", "Taxa de sucesso: 4/4", "Taxa de sucesso: 100"]
            failure_keywords = ["❌", "ERRO", "ERROR", "FALHOU", "FAILED", "Traceback", "Exception"]
            
            has_success = any(kw in output for kw in success_keywords)
            has_failure = any(kw in output for kw in failure_keywords)
            
            # Determinar status final
            # Se o script retornou 0 (sucesso) e não há erros explícitos, considerar passou
            if result.returncode == 0:
                if has_failure and not has_success:
                    status = "FALHOU"
                else:
                    status = "PASSOU"  # Assumir sucesso se returncode é 0
            else:
                status = "FALHOU"
            
            test_result = {
                "test_name": test_name,
                "script": script_path,
                "description": description,
                "status": status,
                "elapsed_time_seconds": elapsed_time,
                "return_code": result.returncode,
                "has_output": len(output) > 0,
                "output_preview": output[:500] if output else "",
                "timestamp": datetime.now().isoformat()
            }
            
            if status == "PASSOU":
                self.results["summary"]["passed"] += 1
                print(f"✅ {test_name}: PASSOU ({elapsed_time:.2f}s)")
            else:
                self.results["summary"]["failed"] += 1
                print(f"❌ {test_name}: FALHOU ({elapsed_time:.2f}s)")
            
            self.results["summary"]["total_tests"] += 1
            return test_result
            
        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            print(f"⏱️  {test_name}: TIMEOUT ({elapsed_time:.2f}s)")
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total_tests"] += 1
            return {
                "test_name": test_name,
                "script": script_path,
                "description": description,
                "status": "TIMEOUT",
                "elapsed_time_seconds": elapsed_time,
                "error": "Teste excedeu tempo limite de 10 minutos"
            }
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"❌ {test_name}: ERRO - {str(e)}")
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total_tests"] += 1
            return {
                "test_name": test_name,
                "script": script_path,
                "description": description,
                "status": "ERRO",
                "elapsed_time_seconds": elapsed_time,
                "error": str(e)
            }
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("=" * 70)
        print("🚀 EXECUTANDO TODOS OS TESTES PARA INVESTIDORES")
        print("=" * 70)
        print()
        
        # Lista de testes a executar
        tests = [
            {
                "name": "PILAR_1_INTEROPERABILIDADE",
                "script": "PROVA_PILAR_1_INTEROPERABILIDADE_REAL.py",
                "description": "Prova de Interoperabilidade - Validação Universal de Assinaturas e Proof-of-Lock ZK"
            },
            {
                "name": "PILAR_2_SEGURANCA_QUANTICA",
                "script": "PROVA_PILAR_2_SEGURANCA_QUANTICA.py",
                "description": "Prova de Segurança Quântica - QRS-3, ML-DSA, ML-KEM, SPHINCS+"
            },
            {
                "name": "PERFORMANCE_PQC",
                "script": "TESTE_PERFORMANCE_PQC.py",
                "description": "Análise de Performance e Escalabilidade PQC"
            },
            {
                "name": "BATCH_VERIFICATION",
                "script": "TESTE_BATCH_VERIFICATION.py",
                "description": "Otimização de Escalabilidade - Batch Verification QRS-3"
            },
            {
                "name": "FALCON_COMPACTO",
                "script": "TESTE_FALCON_COMPACTO.py",
                "description": "Alternativa Compacta - FALCON vs ML-DSA"
            },
            {
                "name": "COMPRESSAO_ASSINATURAS",
                "script": "TESTE_COMPRESSAO_ASSINATURAS.py",
                "description": "Otimização de Escalabilidade - Compressão de Assinaturas"
            },
            {
                "name": "STRESS_QRS3",
                "script": "TESTE_STRESS_QRS3.py",
                "description": "Teste de Stress - QRS-3 sob Carga Alta"
            },
            {
                "name": "TODAS_INOVACOES",
                "script": "TESTE_TODAS_INOVACOES.py",
                "description": "Inovações - Quantum-Safe Cross-Chain, QRS-3 Multi-Sig, Quantum-Safe AI Routing"
            }
        ]
        
        # Executar cada teste
        for test in tests:
            result = self.run_test(test["name"], test["script"], test["description"])
            self.results["tests"][test["name"]] = result
            print()
            time.sleep(1)  # Pequena pausa entre testes
        
        # Calcular taxa de sucesso
        total = self.results["summary"]["total_tests"]
        passed = self.results["summary"]["passed"]
        self.results["summary"]["success_rate"] = (passed / total * 100) if total > 0 else 0
        
        # Tempo total
        total_time = time.time() - self.start_time
        self.results["summary"]["total_time_seconds"] = total_time
        
    def generate_report(self):
        """Gerar relatório consolidado"""
        print()
        print("=" * 70)
        print("📊 GERANDO RELATÓRIO CONSOLIDADO")
        print("=" * 70)
        print()
        
        # Salvar JSON
        json_path = RESULTS_DIR / f"relatorio_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Gerar relatório em texto
        report_path = RESULTS_DIR / f"RELATORIO_INVESTIDORES_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("📊 RELATÓRIO CONSOLIDADO - ALLIANZA BLOCKCHAIN\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Tempo Total: {self.results['summary']['total_time_seconds']:.2f} segundos\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("📈 RESUMO EXECUTIVO\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total de Testes: {self.results['summary']['total_tests']}\n")
            f.write(f"Testes Passando: {self.results['summary']['passed']}\n")
            f.write(f"Testes Falhando: {self.results['summary']['failed']}\n")
            f.write(f"Taxa de Sucesso: {self.results['summary']['success_rate']:.1f}%\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("🧪 DETALHES DOS TESTES\n")
            f.write("=" * 70 + "\n\n")
            
            for test_name, test_result in self.results["tests"].items():
                status_icon = "✅" if test_result["status"] == "PASSOU" else "❌"
                f.write(f"{status_icon} {test_name}\n")
                f.write(f"   Descrição: {test_result.get('description', 'N/A')}\n")
                f.write(f"   Status: {test_result['status']}\n")
                f.write(f"   Tempo: {test_result['elapsed_time_seconds']:.2f}s\n")
                if test_result.get("error"):
                    f.write(f"   Erro: {test_result['error']}\n")
                f.write("\n")
        
        print(f"✅ Relatório JSON salvo em: {json_path}")
        print(f"✅ Relatório TXT salvo em: {report_path}")
        print()
        
        return json_path, report_path
    
    def print_summary(self):
        """Imprimir resumo final"""
        print("=" * 70)
        print("📊 RESUMO FINAL")
        print("=" * 70)
        print()
        print(f"Total de Testes: {self.results['summary']['total_tests']}")
        print(f"✅ Passando: {self.results['summary']['passed']}")
        print(f"❌ Falhando: {self.results['summary']['failed']}")
        print(f"📈 Taxa de Sucesso: {self.results['summary']['success_rate']:.1f}%")
        print(f"⏱️  Tempo Total: {self.results['summary']['total_time_seconds']:.2f}s")
        print()
        
        if self.results['summary']['success_rate'] == 100.0:
            print("✅✅✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
            print("   O projeto está pronto para apresentação a investidores!")
        elif self.results['summary']['success_rate'] >= 80.0:
            print("✅ Maioria dos testes passou!")
            print("   Alguns testes podem precisar de ajustes.")
        else:
            print("⚠️  Alguns testes falharam.")
            print("   Revise os resultados antes de apresentar.")
        
        print()
        print("=" * 70)

if __name__ == "__main__":
    runner = TestRunner()
    runner.run_all_tests()
    runner.generate_report()
    runner.print_summary()
