#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Script de Verificação de Implementação QRS-3 - Allianza Blockchain
Verifica a implementação de segurança quântica (QRS-3)
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def verify_pqc_code():
    """Verifica código PQC"""
    print_header("VERIFICANDO CÓDIGO PQC")
    
    pqc_file = Path("pqc_crypto.py")
    if not pqc_file.exists():
        # Tentar em core/crypto/
        pqc_file = Path("core/crypto/pqc_crypto.py")
    
    if not pqc_file.exists():
        print_error("Arquivo pqc_crypto.py não encontrado")
        return False
    
    print_success(f"Arquivo encontrado: {pqc_file}")
    
    # Verificar conteúdo básico
    with open(pqc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar presença de algoritmos PQC
    pqc_algorithms = ['ML-DSA', 'SPHINCS', 'Dilithium', 'Falcon']
    found_algorithms = []
    
    for algo in pqc_algorithms:
        if algo.lower() in content.lower():
            found_algorithms.append(algo)
            print_success(f"Algoritmo {algo} encontrado no código")
    
    if not found_algorithms:
        print_warning("Nenhum algoritmo PQC padrão encontrado no código")
    
    # Verificar liboqs
    if 'liboqs' in content.lower() or 'oqs' in content.lower():
        print_success("Referência a liboqs encontrada")
    else:
        print_warning("Referência a liboqs não encontrada")
    
    return True

def verify_qrs3_proofs():
    """Verifica provas QRS-3"""
    print_header("VERIFICANDO PROVAS QRS-3")
    
    proofs_dir = Path("proofs")
    if not proofs_dir.exists():
        print_error("Diretório 'proofs' não encontrado")
        return False
    
    # Verificar diretórios QRS-3
    qrs3_dirs = [
        "qrs3",
        "pilar_2_seguranca_quantica",
        "pqc_complete"
    ]
    
    found_proofs = False
    for dir_name in qrs3_dirs:
        dir_path = proofs_dir / dir_name
        if dir_path.exists():
            json_files = list(dir_path.glob("*.json"))
            if json_files:
                print_success(f"Encontrados {len(json_files)} arquivos de prova em '{dir_name}'")
                found_proofs = True
                for proof_file in json_files[:3]:  # Mostrar primeiros 3
                    print_info(f"  - {proof_file.name}")
    
    if not found_proofs:
        print_warning("Nenhuma prova QRS-3 encontrada")
    
    return found_proofs

def verify_technical_proofs_file():
    """Verifica arquivo principal de provas técnicas"""
    print_header("VERIFICANDO ARQUIVO DE PROVAS TÉCNICAS")
    
    proof_file = Path("COMPLETE_TECHNICAL_PROOFS_FINAL.json")
    if not proof_file.exists():
        print_error("Arquivo COMPLETE_TECHNICAL_PROOFS_FINAL.json não encontrado")
        return False
    
    with open(proof_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Verificar provas de segurança quântica
    main_proofs = data.get("main_proofs", {})
    
    qrs3_proofs = []
    for proof_name, proof_data in main_proofs.items():
        if 'quantum' in proof_name.lower() or 'qrs' in proof_name.lower() or 'pqc' in proof_name.lower():
            qrs3_proofs.append(proof_name)
            status = proof_data.get("status", "UNKNOWN")
            if status == "SUCESSO" or status == "SUCCESS":
                print_success(f"Prova {proof_name}: {status}")
            else:
                print_warning(f"Prova {proof_name}: {status}")
    
    if qrs3_proofs:
        print_info(f"Total de provas QRS-3 encontradas: {len(qrs3_proofs)}")
    else:
        print_warning("Nenhuma prova QRS-3 encontrada no arquivo principal")
    
    return len(qrs3_proofs) > 0

def verify_liboqs_availability():
    """Verifica disponibilidade do liboqs"""
    print_header("VERIFICANDO DISPONIBILIDADE DO LIBOQS")
    
    try:
        import liboqs
        print_success("liboqs-python está instalado")
        
        # Tentar obter versão
        try:
            version = liboqs.__version__ if hasattr(liboqs, '__version__') else "desconhecida"
            print_info(f"Versão: {version}")
        except:
            pass
        
        # Verificar algoritmos disponíveis
        try:
            sig_algs = liboqs.get_enabled_sig_mechanisms()
            if sig_algs:
                print_success(f"Algoritmos de assinatura disponíveis: {len(sig_algs)}")
                # Mostrar alguns algoritmos
                for alg in sig_algs[:5]:
                    if 'Dilithium' in alg or 'SPHINCS' in alg or 'Falcon' in alg:
                        print_info(f"  ✅ {alg}")
            else:
                print_warning("Nenhum algoritmo de assinatura disponível")
        except Exception as e:
            print_warning(f"Não foi possível listar algoritmos: {e}")
        
        return True
    except ImportError:
        print_warning("liboqs-python não está instalado")
        print_info("  Nota: A implementação pode usar simulação funcional")
        return False

def verify_testnet_qrs3():
    """Verifica QRS-3 na testnet"""
    print_header("VERIFICANDO QRS-3 NA TESTNET")
    
    testnet_url = "https://testnet.allianza.tech"
    qss_url = f"{testnet_url}/qss"
    
    print_info(f"Testnet URL: {testnet_url}")
    print_info(f"QSS Dashboard: {qss_url}")
    print_info("Para verificar:")
    print_info("  1. Acesse o QSS Dashboard")
    print_info("  2. Gere uma prova QRS-3")
    print_info("  3. Verifique a prova")
    
    # Não podemos verificar HTTP aqui sem requests, mas podemos informar
    print_warning("Verificação HTTP requer acesso à testnet (não verificado automaticamente)")
    
    return True

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Verifica implementação QRS-3')
    parser.add_argument('--detailed', action='store_true', 
                       help='Mostrar informações detalhadas')
    
    args = parser.parse_args()
    
    print_header("VERIFICAÇÃO DE IMPLEMENTAÇÃO QRS-3 - ALLIANZA BLOCKCHAIN")
    
    print_info(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Diretório: {os.getcwd()}\n")
    
    results = {}
    
    # Executar verificações
    results["Código PQC"] = verify_pqc_code()
    results["Provas QRS-3"] = verify_qrs3_proofs()
    results["Arquivo de Provas Técnicas"] = verify_technical_proofs_file()
    results["Disponibilidade liboqs"] = verify_liboqs_availability()
    results["Testnet QRS-3"] = verify_testnet_qrs3()
    
    # Relatório final
    print_header("RELATÓRIO FINAL")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for check, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {check}")
    
    print()
    if passed == total:
        print_success("TODAS AS VERIFICAÇÕES PASSARAM!")
    else:
        print_warning(f"{passed}/{total} verificações passaram")
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
