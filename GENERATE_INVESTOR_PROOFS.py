#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Master: Gera todas as provas para investidores
Executa testes diretamente e gera relatório consolidado
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Criar diretório de resultados
RESULTS_DIR = Path("proofs") / "relatorio_investidores"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

class ProofGenerator:
    """Gera provas consolidadas para investidores"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "proofs": {},
            "summary": {
                "total_proofs": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0.0
            }
        }
        self.start_time = time.time()
        
    def run_proof(self, proof_name: str, script_module: str, description: str) -> Dict:
        """Executar uma prova importando o módulo diretamente"""
        print("=" * 70)
        print(f"📋 PROVA: {proof_name}")
        print("=" * 70)
        print(f"📝 {description}")
        print()
        
        start_time = time.time()
        try:
            # Importar e executar o módulo
            if script_module.endswith('.py'):
                script_module = script_module[:-3]
            
            # Substituir / por . para importação
            module_path = script_module.replace('/', '.').replace('\\', '.')
            
            # Executar o módulo
            import importlib.util
            spec = importlib.util.spec_from_file_location(script_module, script_module + '.py')
            if spec is None:
                raise ImportError(f"Não foi possível carregar {script_module}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[script_module] = module
            spec.loader.exec_module(module)
            
            elapsed_time = time.time() - start_time
            
            # Se chegou aqui sem exceção, consideramos sucesso
            proof_result = {
                "proof_name": proof_name,
                "script": script_module,
                "description": description,
                "status": "SUCESSO",
                "elapsed_time_seconds": elapsed_time,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results["summary"]["successful"] += 1
            print(f"✅ {proof_name}: SUCESSO ({elapsed_time:.2f}s)")
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            proof_result = {
                "proof_name": proof_name,
                "script": script_module,
                "description": description,
                "status": "ERRO",
                "elapsed_time_seconds": elapsed_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            self.results["summary"]["failed"] += 1
            print(f"❌ {proof_name}: ERRO - {str(e)[:100]}")
        
        self.results["summary"]["total_proofs"] += 1
        self.results["proofs"][proof_name] = proof_result
        print()
        return proof_result
    
    def generate_all_proofs(self):
        """Gerar todas as provas"""
        print("=" * 70)
        print("🚀 GERANDO TODAS AS PROVAS PARA INVESTIDORES")
        print("=" * 70)
        print()
        
        # Lista de provas a gerar
        proofs = [
            {
                "name": "PILAR_1_INTEROPERABILIDADE",
                "script": "PROVA_PILAR_1_INTEROPERABILIDADE_REAL",
                "description": "Prova de Interoperabilidade - Validação Universal de Assinaturas e Proof-of-Lock ZK"
            },
            {
                "name": "PILAR_2_SEGURANCA_QUANTICA",
                "script": "PROVA_PILAR_2_SEGURANCA_QUANTICA",
                "description": "Prova de Segurança Quântica - QRS-3, ML-DSA, ML-KEM, SPHINCS+"
            },
            {
                "name": "PERFORMANCE_PQC",
                "script": "TESTE_PERFORMANCE_PQC",
                "description": "Análise de Performance e Escalabilidade PQC"
            },
            {
                "name": "BATCH_VERIFICATION",
                "script": "TESTE_BATCH_VERIFICATION",
                "description": "Otimização de Escalabilidade - Batch Verification QRS-3"
            },
            {
                "name": "FALCON_COMPACTO",
                "script": "TESTE_FALCON_COMPACTO",
                "description": "Alternativa Compacta - FALCON vs ML-DSA"
            },
            {
                "name": "COMPRESSAO_ASSINATURAS",
                "script": "TESTE_COMPRESSAO_ASSINATURAS",
                "description": "Otimização de Escalabilidade - Compressão de Assinaturas"
            },
            {
                "name": "STRESS_QRS3",
                "script": "TESTE_STRESS_QRS3",
                "description": "Teste de Stress - QRS-3 sob Carga Alta"
            },
            {
                "name": "TODAS_INOVACOES",
                "script": "TESTE_TODAS_INOVACOES",
                "description": "Inovações - Quantum-Safe Cross-Chain, QRS-3 Multi-Sig, Quantum-Safe AI Routing"
            },
            {
                "name": "PROVAS_COMPLETAS",
                "script": "generate_complete_proof",
                "description": "Gerador de Provas Completas - Salva em pasta com data/hora (POCs e todas as provas)"
            }
        ]
        
        # Executar cada prova
        for proof in proofs:
            self.run_proof(proof["name"], proof["script"], proof["description"])
            time.sleep(0.5)  # Pequena pausa entre provas
        
        # Calcular taxa de sucesso
        total = self.results["summary"]["total_proofs"]
        successful = self.results["summary"]["successful"]
        self.results["summary"]["success_rate"] = (successful / total * 100) if total > 0 else 0
        
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
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salvar JSON
        json_path = RESULTS_DIR / f"provas_completas_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Gerar relatório em Markdown para investidores
        md_path = RESULTS_DIR / f"RELATORIO_PROVAS_INVESTIDORES_{timestamp}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# 📊 RELATÓRIO DE PROVAS - ALLIANZA BLOCKCHAIN\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Tempo Total:** {self.results['summary']['total_time_seconds']:.2f} segundos\n\n")
            
            f.write("---\n\n")
            f.write("## 📈 RESUMO EXECUTIVO\n\n")
            f.write(f"- **Total de Provas:** {self.results['summary']['total_proofs']}\n")
            f.write(f"- **Provas Bem-Sucedidas:** {self.results['summary']['successful']}\n")
            f.write(f"- **Provas com Erro:** {self.results['summary']['failed']}\n")
            f.write(f"- **Taxa de Sucesso:** {self.results['summary']['success_rate']:.1f}%\n\n")
            
            f.write("---\n\n")
            f.write("## 🧪 DETALHES DAS PROVAS\n\n")
            
            for proof_name, proof_result in self.results["proofs"].items():
                status_icon = "✅" if proof_result["status"] == "SUCESSO" else "❌"
                f.write(f"### {status_icon} {proof_name}\n\n")
                f.write(f"**Descrição:** {proof_result.get('description', 'N/A')}\n\n")
                f.write(f"**Status:** {proof_result['status']}\n\n")
                f.write(f"**Tempo:** {proof_result['elapsed_time_seconds']:.2f}s\n\n")
                if proof_result.get("error"):
                    f.write(f"**Erro:** {proof_result['error']}\n\n")
                f.write("---\n\n")
        
        # Gerar relatório em texto simples
        txt_path = RESULTS_DIR / f"RELATORIO_PROVAS_INVESTIDORES_{timestamp}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("📊 RELATÓRIO DE PROVAS - ALLIANZA BLOCKCHAIN\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Tempo Total: {self.results['summary']['total_time_seconds']:.2f} segundos\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("📈 RESUMO EXECUTIVO\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total de Provas: {self.results['summary']['total_proofs']}\n")
            f.write(f"Provas Bem-Sucedidas: {self.results['summary']['successful']}\n")
            f.write(f"Provas com Erro: {self.results['summary']['failed']}\n")
            f.write(f"Taxa de Sucesso: {self.results['summary']['success_rate']:.1f}%\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("🧪 DETALHES DAS PROVAS\n")
            f.write("=" * 70 + "\n\n")
            
            for proof_name, proof_result in self.results["proofs"].items():
                status_icon = "✅" if proof_result["status"] == "SUCESSO" else "❌"
                f.write(f"{status_icon} {proof_name}\n")
                f.write(f"   Descrição: {proof_result.get('description', 'N/A')}\n")
                f.write(f"   Status: {proof_result['status']}\n")
                f.write(f"   Tempo: {proof_result['elapsed_time_seconds']:.2f}s\n")
                if proof_result.get("error"):
                    f.write(f"   Erro: {proof_result['error']}\n")
                f.write("\n")
        
        print(f"✅ Relatório JSON salvo em: {json_path}")
        print(f"✅ Relatório Markdown salvo em: {md_path}")
        print(f"✅ Relatório TXT salvo em: {txt_path}")
        print()
        
        return json_path, md_path, txt_path
    
    def print_summary(self):
        """Imprimir resumo final"""
        print("=" * 70)
        print("📊 RESUMO FINAL")
        print("=" * 70)
        print()
        print(f"Total de Provas: {self.results['summary']['total_proofs']}")
        print(f"✅ Bem-Sucedidas: {self.results['summary']['successful']}")
        print(f"❌ Com Erro: {self.results['summary']['failed']}")
        print(f"📈 Taxa de Sucesso: {self.results['summary']['success_rate']:.1f}%")
        print(f"⏱️  Tempo Total: {self.results['summary']['total_time_seconds']:.2f}s")
        print()
        
        if self.results['summary']['success_rate'] == 100.0:
            print("✅✅✅ TODAS AS PROVAS FORAM GERADAS COM SUCESSO!")
            print("   O projeto está pronto para apresentação a investidores!")
        elif self.results['summary']['success_rate'] >= 80.0:
            print("✅ Maioria das provas foram geradas com sucesso!")
            print("   Algumas provas podem precisar de revisão.")
        else:
            print("⚠️  Algumas provas falharam.")
            print("   Revise os resultados antes de apresentar.")
        
        print()
        print("=" * 70)

if __name__ == "__main__":
    generator = ProofGenerator()
    generator.generate_all_proofs()
    generator.generate_report()
    generator.print_summary()

