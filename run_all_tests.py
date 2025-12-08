#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar TODOS os testes da blockchain Allianza
Gera relatório completo com resultados
"""

import sys
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def run_test(test_file, category=""):
    """Executa um teste e retorna o resultado"""
    try:
        print_info(f"Executando: {test_file}")
        start_time = time.time()
        
        # Definir variável de ambiente para modo automatizado
        env = os.environ.copy()
        env['AUTOMATED_TEST'] = 'true'
        
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos máximo por teste
            env=env
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print_success(f"{test_file} - PASSOU ({elapsed:.2f}s)")
            return {
                "file": test_file,
                "category": category,
                "status": "PASSOU",
                "elapsed": elapsed,
                "output": result.stdout,
                "error": result.stderr
            }
        else:
            print_error(f"{test_file} - FALHOU ({elapsed:.2f}s)")
            return {
                "file": test_file,
                "category": category,
                "status": "FALHOU",
                "elapsed": elapsed,
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
    except subprocess.TimeoutExpired:
        print_error(f"{test_file} - TIMEOUT (>5min)")
        return {
            "file": test_file,
            "category": category,
            "status": "TIMEOUT",
            "elapsed": 300,
            "error": "Teste excedeu 5 minutos"
        }
    except Exception as e:
        print_error(f"{test_file} - ERRO: {str(e)}")
        return {
            "file": test_file,
            "category": category,
            "status": "ERRO",
            "elapsed": 0,
            "error": str(e)
        }

def main():
    print_header("🧪 EXECUTANDO TODOS OS TESTES DA BLOCKCHAIN ALLIANZA")
    
    # Lista de todos os testes organizados por categoria
    tests = {
        "Testes Principais": [
            "testar_toda_blockchain.py",
            "testar_integracao_melhorias.py",
            "test_allianza_blockchain.py",
        ],
        "Testes de Interoperabilidade": [
            "test_all_chains.py",
            "test_real_interoperability.py",
            "test_transferencia_real_cross_chain.py",
            "test_uec_complete.py",
            "test_uec_interoperability.py",
            "test_universal_blockchain.py",
            "teste_interoperabilidade_real_mainnet.py",
            "PROVA_INTEROPERABILIDADE_REAL.py",
            "PROVA_PILAR_1_INTEROPERABILIDADE_REAL.py",
        ],
        "Testes de Segurança Quântica": [
            "teste_prova_seguranca_quantica.py",
            "PROVA_PILAR_2_SEGURANCA_QUANTICA.py",
            "PROVA_PQC_COMPLETA.py",
            "PROVA_QRS3_MULTISIG.py",
            "PROVA_QUANTUM_SAFE_INTEROPERABILITY.py",
            "PROVA_QUANTUM_SAFE_ROUTING.py",
            "TESTE_STRESS_QRS3.py",
            "TESTE_PERFORMANCE_PQC.py",
            "TESTE_COMPRESSAO_ASSINATURAS.py",
            "TESTE_BATCH_VERIFICATION.py",
        ],
        "Testes de Melhorias": [
            "test_all_improvements.py",
            "TESTE_REAL_50_MELHORIAS.py",
            "TESTE_TODAS_50_MELHORIAS.py",
            "TESTE_TODAS_MELHORIAS.py",
            "TESTE_TODAS_MELHORIAS_V2.py",
            "TESTE_TODAS_INOVACOES.py",
            "testar_todas_melhorias.py",
            "testar_melhorias_avancadas.py",
            "testar_melhorias_infraestrutura.py",
            "testar_otimizacoes_avancadas.py",
        ],
        "Testes de Performance": [
            "test_performance.py",
            "TESTE_PERFORMANCE_OTIMIZADO.py",
            "test_stress_uec.py",
        ],
        "Testes de POCs": [
            "test_all_pocs.py",
            "POC_INTEROPERABILIDADE_UNIVERSAL.py",
            "POC_PREDICAO_GAS_80_PRECISAO.py",
            "POC_PROOF_OF_LOCK_ZK.py",
            "POC_VALIDACAO_UNIVERSAL_FINAL.py",
        ],
        "Testes de Rotas/API": [
            "test_routes.py",
            "test_rotas_teste.py",
        ],
        "Testes Específicos": [
            "test_bitcoin_bridge.py",
            "test_bridge_fixed.py",
            "test_config.py",
            "test_token_validation.py",
            "test_web3.py",
            "test_liboqs.py",
            "testar_liboqs_instalacao.py",
            "testar_sphincs_integracao.py",
            "testar_sphincs_real.py",
            "teste_polygon_bitcoin_testnet.py",
            "teste_com_faucet.py",
            "TESTE_COM_HASH_REAL.py",
            "TESTE_FALCON_COMPACTO.py",
        ],
        "Testes de Correções": [
            "teste_correcoes_criticas.py",
            "testar_implementacao_completa.py",
        ],
    }
    
    results = []
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # Executar todos os testes
    for category, test_files in tests.items():
        print_header(f"📁 {category}")
        
        for test_file in test_files:
            # Verificar se o arquivo existe
            if not Path(test_file).exists():
                print_error(f"{test_file} - ARQUIVO NÃO ENCONTRADO")
                results.append({
                    "file": test_file,
                    "category": category,
                    "status": "NÃO ENCONTRADO",
                    "elapsed": 0
                })
                failed_tests += 1
                continue
            
            result = run_test(test_file, category)
            results.append(result)
            total_tests += 1
            
            if result["status"] == "PASSOU":
                passed_tests += 1
            else:
                failed_tests += 1
            
            time.sleep(0.5)  # Pequena pausa entre testes
    
    # Resumo final
    print_header("📊 RESUMO FINAL DOS TESTES")
    
    print(f"\n{Colors.BOLD}Total de Testes: {total_tests}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Passaram: {passed_tests}{Colors.RESET}")
    print(f"{Colors.RED}❌ Falharam: {failed_tests}{Colors.RESET}")
    
    if total_tests > 0:
        success_rate = (passed_tests / total_tests) * 100
        print(f"{Colors.BOLD}📈 Taxa de Sucesso: {success_rate:.1f}%{Colors.RESET}\n")
    
    # Detalhes por categoria
    print(f"\n{Colors.BOLD}📋 Detalhes por Categoria:{Colors.RESET}\n")
    for category in tests.keys():
        category_results = [r for r in results if r.get("category") == category]
        category_passed = sum(1 for r in category_results if r.get("status") == "PASSOU")
        category_total = len(category_results)
        
        if category_total > 0:
            category_rate = (category_passed / category_total) * 100
            status_color = Colors.GREEN if category_rate >= 80 else Colors.YELLOW if category_rate >= 50 else Colors.RED
            print(f"{status_color}{category}: {category_passed}/{category_total} ({category_rate:.1f}%){Colors.RESET}")
    
    # Listar testes que falharam
    failed = [r for r in results if r.get("status") != "PASSOU" and r.get("status") != "NÃO ENCONTRADO"]
    if failed:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Testes que Falharam:{Colors.RESET}\n")
        for result in failed:
            print(f"{Colors.RED}  • {result['file']} - {result['status']}{Colors.RESET}")
            if result.get("error"):
                error_preview = result["error"][:100] if len(result["error"]) > 100 else result["error"]
                print(f"    {Colors.YELLOW}Erro: {error_preview}...{Colors.RESET}")
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"relatorio_testes_{timestamp}.txt"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO DE TESTES - ALLIANZA BLOCKCHAIN\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total de Testes: {total_tests}\n")
        f.write(f"Passaram: {passed_tests}\n")
        f.write(f"Falharam: {failed_tests}\n")
        if total_tests > 0:
            f.write(f"Taxa de Sucesso: {(passed_tests/total_tests)*100:.1f}%\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("DETALHES DOS TESTES\n")
        f.write("="*80 + "\n\n")
        
        for result in results:
            f.write(f"Arquivo: {result['file']}\n")
            f.write(f"Categoria: {result.get('category', 'N/A')}\n")
            f.write(f"Status: {result['status']}\n")
            f.write(f"Tempo: {result.get('elapsed', 0):.2f}s\n")
            if result.get("error"):
                f.write(f"Erro: {result['error']}\n")
            f.write("-"*80 + "\n")
    
    print(f"\n{Colors.CYAN}📄 Relatório salvo em: {report_file}{Colors.RESET}\n")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

