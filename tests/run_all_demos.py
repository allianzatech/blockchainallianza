#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Runner Unificado - Todos os Demos
Roda todos os exemplos e gera relatório completo
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
sys.path.insert(0, str(ROOT_DIR))

class DemoTestRunner:
    """Runner para executar todos os demos e gerar relatório"""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.examples_dir = EXAMPLES_DIR
        
    def find_demo_files(self) -> List[Path]:
        """Encontra todos os arquivos de demo"""
        demos = []
        if self.examples_dir.exists():
            for file in self.examples_dir.glob("*_demo.py"):
                demos.append(file)
        return sorted(demos)
    
    def run_demo(self, demo_path: Path) -> Dict:
        """
        Executa um demo e retorna resultado
        
        Args:
            demo_path: Caminho para o arquivo de demo
        
        Returns:
            Dict com resultado da execução
        """
        demo_name = demo_path.stem
        print(f"\n{'='*70}")
        print(f"🧪 Executando: {demo_name}")
        print(f"{'='*70}")
        
        start_time = time.time()
        result = {
            "demo": demo_name,
            "file": str(demo_path.relative_to(ROOT_DIR)),
            "status": "unknown",
            "execution_time_ms": 0,
            "output": "",
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Executar demo
            process = subprocess.run(
                [sys.executable, str(demo_path)],
                capture_output=True,
                text=True,
                timeout=60,  # 60 segundos timeout
                cwd=str(ROOT_DIR)
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            result["execution_time_ms"] = round(execution_time, 2)
            result["output"] = process.stdout
            result["return_code"] = process.returncode
            
            if process.returncode == 0:
                result["status"] = "success"
                print(f"✅ {demo_name}: Sucesso ({execution_time:.2f}ms)")
            else:
                result["status"] = "error"
                result["error"] = process.stderr
                print(f"❌ {demo_name}: Erro (código {process.returncode})")
                if process.stderr:
                    print(f"   Erro: {process.stderr[:200]}")
            
        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["error"] = "Timeout após 60 segundos"
            print(f"⏱️  {demo_name}: Timeout")
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            print(f"❌ {demo_name}: Exceção - {e}")
        
        return result
    
    def run_all_demos(self) -> List[Dict]:
        """Executa todos os demos"""
        demos = self.find_demo_files()
        
        if not demos:
            print("⚠️  Nenhum demo encontrado em examples/")
            return []
        
        print(f"\n📋 Encontrados {len(demos)} demos para executar:")
        for demo in demos:
            print(f"   • {demo.name}")
        
        print(f"\n🚀 Iniciando execução...")
        
        for demo_path in demos:
            result = self.run_demo(demo_path)
            self.results.append(result)
        
        return self.results
    
    def generate_report(self) -> Dict:
        """Gera relatório completo"""
        total_time = (time.time() - self.start_time) * 1000
        
        successful = [r for r in self.results if r["status"] == "success"]
        failed = [r for r in self.results if r["status"] != "success"]
        
        report = {
            "test_suite": "Allianza Blockchain - Demo Tests",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_demos": len(self.results),
                "successful": len(successful),
                "failed": len(failed),
                "success_rate": round((len(successful) / len(self.results) * 100) if self.results else 0, 2),
                "total_execution_time_ms": round(total_time, 2)
            },
            "results": self.results,
            "environment": {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": str(ROOT_DIR)
            }
        }
        
        return report
    
    def save_report(self, report: Dict, format: str = "json"):
        """Salva relatório em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            report_path = ROOT_DIR / "tests" / f"demo_test_report_{timestamp}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Relatório JSON salvo: {report_path}")
        
        # Também salvar resumo em texto
        summary_path = ROOT_DIR / "tests" / f"demo_test_summary_{timestamp}.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("🧪 RELATÓRIO DE TESTES - DEMOS ALLIANZA BLOCKCHAIN\n")
            f.write("="*70 + "\n\n")
            f.write(f"Data: {report['timestamp']}\n")
            f.write(f"Total de Demos: {report['summary']['total_demos']}\n")
            f.write(f"Sucesso: {report['summary']['successful']}\n")
            f.write(f"Falhas: {report['summary']['failed']}\n")
            f.write(f"Taxa de Sucesso: {report['summary']['success_rate']}%\n")
            f.write(f"Tempo Total: {report['summary']['total_execution_time_ms']:.2f}ms\n\n")
            
            f.write("="*70 + "\n")
            f.write("RESULTADOS DETALHADOS\n")
            f.write("="*70 + "\n\n")
            
            for result in report['results']:
                status_icon = "✅" if result['status'] == 'success' else "❌"
                f.write(f"{status_icon} {result['demo']}\n")
                f.write(f"   Status: {result['status']}\n")
                f.write(f"   Tempo: {result['execution_time_ms']:.2f}ms\n")
                if result.get('error'):
                    f.write(f"   Erro: {result['error']}\n")
                f.write("\n")
        
        print(f"📄 Resumo em texto salvo: {summary_path}")
    
    def print_summary(self, report: Dict):
        """Imprime resumo no console"""
        summary = report['summary']
        
        print("\n" + "="*70)
        print("📊 RESUMO DOS TESTES")
        print("="*70)
        print(f"\n✅ Sucesso: {summary['successful']}/{summary['total_demos']}")
        print(f"❌ Falhas: {summary['failed']}/{summary['total_demos']}")
        print(f"📈 Taxa de Sucesso: {summary['success_rate']}%")
        print(f"⏱️  Tempo Total: {summary['total_execution_time_ms']:.2f}ms")
        
        if summary['successful'] == summary['total_demos']:
            print("\n🎉 TODOS OS DEMOS EXECUTARAM COM SUCESSO!")
        else:
            print(f"\n⚠️  {summary['failed']} demo(s) falharam")
        
        print("\n" + "="*70)


def main():
    """Função principal"""
    print("="*70)
    print("🧪 TEST RUNNER UNIFICADO - ALLIANZA BLOCKCHAIN")
    print("="*70)
    print("\nEste script executa todos os demos e gera um relatório completo.")
    print("Útil para validação end-to-end e preparação para audits.\n")
    
    runner = DemoTestRunner()
    
    # Executar todos os demos
    results = runner.run_all_demos()
    
    if not results:
        print("\n⚠️  Nenhum demo foi executado. Verifique se os arquivos existem em examples/")
        return 1
    
    # Gerar relatório
    report = runner.generate_report()
    
    # Salvar relatório
    runner.save_report(report)
    
    # Imprimir resumo
    runner.print_summary(report)
    
    # Retornar código de saída apropriado
    if report['summary']['failed'] > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

