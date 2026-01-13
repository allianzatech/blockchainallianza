#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script de Verificação de Provas Técnicas - Allianza Blockchain
Verifica todas as provas técnicas documentadas no repositório
"""

import json
import os
import sys
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

def verify_file_exists(file_path, description):
    """Verifica se arquivo existe"""
    path = Path(file_path)
    if path.exists():
        print_success(f"{description}: {file_path}")
        return True
    else:
        print_error(f"{description} não encontrado: {file_path}")
        return False

def verify_json_structure(file_path, required_keys):
    """Verifica estrutura JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        missing_keys = []
        for key in required_keys:
            if key not in data:
                missing_keys.append(key)
        
        if missing_keys:
            print_error(f"Chaves faltando em {file_path}: {', '.join(missing_keys)}")
            return False
        
        print_success(f"Estrutura JSON válida: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print_error(f"JSON inválido em {file_path}: {e}")
        return False
    except Exception as e:
        print_error(f"Erro ao ler {file_path}: {e}")
        return False

def verify_technical_proofs():
    """Verifica arquivo principal de provas técnicas"""
    print_header("VERIFICANDO PROVAS TÉCNICAS PRINCIPAIS")
    
    proof_file = "COMPLETE_TECHNICAL_PROOFS_FINAL.json"
    if not verify_file_exists(proof_file, "Arquivo de provas técnicas"):
        return False
    
    required_keys = [
        "metadata",
        "summary",
        "main_proofs",
        "certification"
    ]
    
    if not verify_json_structure(proof_file, required_keys):
        return False
    
    # Verificar conteúdo
    with open(proof_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    summary = data.get("summary", {})
    total = summary.get("total_validations", 0)
    success_rate = summary.get("overall_statistics", {}).get("overall_success_rate", 0)
    
    print_info(f"Total de validações: {total}")
    print_info(f"Taxa de sucesso: {success_rate}%")
    
    if success_rate >= 100.0:
        print_success("Taxa de sucesso: 100% ✅")
    else:
        print_warning(f"Taxa de sucesso: {success_rate}%")
    
    return True

def verify_proofs_directory():
    """Verifica diretório de provas"""
    print_header("VERIFICANDO DIRETÓRIO DE PROVAS")
    
    proofs_dir = Path("proofs")
    if not proofs_dir.exists():
        print_error("Diretório 'proofs' não encontrado")
        return False
    
    print_success(f"Diretório 'proofs' encontrado")
    
    # Verificar arquivos principais
    main_files = [
        "PROVAS_TECNICAS_COMPLETAS.json",
        "PROVAS_TECNICAS_COMPLETAS_EXPANDIDO.json"
    ]
    
    for file in main_files:
        file_path = proofs_dir / file
        if file_path.exists():
            print_success(f"Arquivo encontrado: {file_path}")
        else:
            print_warning(f"Arquivo não encontrado: {file_path}")
    
    # Verificar subdiretórios importantes
    important_dirs = [
        "pilar_1_interoperabilidade",
        "pilar_2_seguranca_quantica",
        "qrs3",
        "interoperability_real"
    ]
    
    for dir_name in important_dirs:
        dir_path = proofs_dir / dir_name
        if dir_path.exists():
            file_count = len(list(dir_path.glob("*.json")))
            print_success(f"Diretório '{dir_name}' encontrado ({file_count} arquivos JSON)")
        else:
            print_warning(f"Diretório '{dir_name}' não encontrado")
    
    return True

def verify_on_chain_proofs():
    """Verifica documentação de provas on-chain"""
    print_header("VERIFICANDO PROVAS ON-CHAIN")
    
    proof_file = "VERIFIABLE_ON_CHAIN_PROOFS.md"
    if not verify_file_exists(proof_file, "Documentação de provas on-chain"):
        return False
    
    # Verificar se contém hashes de transação
    with open(proof_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar presença de hashes Bitcoin (64 caracteres hex)
    bitcoin_hashes = [line for line in content.split('\n') if len(line.strip()) == 64 and all(c in '0123456789abcdef' for c in line.strip().lower())]
    
    if bitcoin_hashes:
        print_success(f"Encontrados {len(bitcoin_hashes)} hashes Bitcoin")
    else:
        print_warning("Nenhum hash Bitcoin encontrado")
    
    # Verificar presença de hashes Ethereum (0x seguido de 64 caracteres)
    ethereum_hashes = [line for line in content.split('\n') if line.strip().startswith('0x') and len(line.strip()) == 66]
    
    if ethereum_hashes:
        print_success(f"Encontrados {len(ethereum_hashes)} hashes Ethereum")
    else:
        print_warning("Nenhum hash Ethereum encontrado")
    
    return True

def verify_documentation():
    """Verifica documentação técnica"""
    print_header("VERIFICANDO DOCUMENTAÇÃO TÉCNICA")
    
    docs = [
        ("VERIFICATION.md", "Guia de verificação"),
        ("TECHNICAL_VALIDATION_REPORT.md", "Relatório de validação técnica"),
        ("AUDIT_GUIDE.md", "Guia de auditoria"),
        ("VERIFIABLE_ON_CHAIN_PROOFS.md", "Provas on-chain verificáveis")
    ]
    
    all_exist = True
    for doc_file, description in docs:
        if verify_file_exists(doc_file, description):
            # Verificar se arquivo não está vazio
            file_path = Path(doc_file)
            if file_path.stat().st_size > 0:
                print_success(f"{description} não está vazio")
            else:
                print_warning(f"{description} está vazio")
        else:
            all_exist = False
    
    return all_exist

def verify_code_structure():
    """Verifica estrutura de código público"""
    print_header("VERIFICANDO ESTRUTURA DE CÓDIGO")
    
    important_dirs = [
        "core/crypto",
        "core/consensus",
        "core/interoperability"
    ]
    
    all_exist = True
    for dir_path in important_dirs:
        path = Path(dir_path)
        if path.exists():
            files = list(path.glob("*.py"))
            print_success(f"Diretório '{dir_path}' encontrado ({len(files)} arquivos Python)")
        else:
            print_warning(f"Diretório '{dir_path}' não encontrado")
            all_exist = False
    
    return all_exist

def generate_report(results):
    """Gera relatório de verificação"""
    print_header("RELATÓRIO DE VERIFICAÇÃO")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    print_info(f"Total de verificações: {total}")
    print_success(f"Passou: {passed}")
    if failed > 0:
        print_error(f"Falhou: {failed}")
    
    print("\n" + "="*70)
    print("DETALHES:")
    print("="*70)
    
    for check, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {check}")
    
    print("\n" + "="*70)
    
    # Generate log file
    log_file = Path("verification_reports") / f"verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_file.parent.mkdir(exist_ok=True)
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ALLIANZA BLOCKCHAIN - VERIFICATION REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Verifications: {total}\n")
            f.write(f"Passed: {passed}\n")
            f.write(f"Failed: {failed}\n")
            f.write(f"Success Rate: {(passed/total*100):.1f}%\n")
            f.write("\n" + "="*70 + "\n")
            f.write("DETAILS:\n")
            f.write("="*70 + "\n")
            
            for check, result in results.items():
                status = "PASSED" if result else "FAILED"
                f.write(f"{status}: {check}\n")
            
            f.write("\n" + "="*70 + "\n")
            if failed == 0:
                f.write("ALL VERIFICATIONS PASSED!\n")
            else:
                f.write(f"{failed} VERIFICATION(S) FAILED\n")
        
        print_success(f"Log file saved: {log_file}")
    except Exception as e:
        print_warning(f"Could not save log file: {e}")
    
    if failed == 0:
        print_success("TODAS AS VERIFICAÇÕES PASSARAM!")
        return True
    else:
        print_error(f"{failed} VERIFICAÇÃO(ÕES) FALHARAM")
        return False

def main():
    """Função principal"""
    print_header("VERIFICAÇÃO DE PROVAS TÉCNICAS - ALLIANZA BLOCKCHAIN")
    
    print_info(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Diretório: {os.getcwd()}\n")
    
    results = {}
    
    # Executar verificações
    results["Provas Técnicas Principais"] = verify_technical_proofs()
    results["Diretório de Provas"] = verify_proofs_directory()
    results["Provas On-Chain"] = verify_on_chain_proofs()
    results["Documentação Técnica"] = verify_documentation()
    results["Estrutura de Código"] = verify_code_structure()
    
    # Gerar relatório
    success = generate_report(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
