#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to rename Portuguese files to English
"""

import os
from pathlib import Path

# Mapping of Portuguese to English file names
RENAME_MAP = {
    # Main proof/test files
    "PROVA_INTEROPERABILIDADE_REAL.py": "PROOF_INTEROPERABILITY_REAL.py",
    "PROVA_PILAR_1_INTEROPERABILIDADE_REAL.py": "PROOF_PILLAR_1_INTEROPERABILITY_REAL.py",
    "PROVA_PILAR_2_SEGURANCA_QUANTICA.py": "PROOF_PILLAR_2_QUANTUM_SECURITY.py",
    "PROVA_PQC_COMPLETA.py": "PROOF_PQC_COMPLETE.py",
    "PROVA_QRS3_MULTISIG.py": "PROOF_QRS3_MULTISIG.py",
    "PROVA_QUANTUM_SAFE_INTEROPERABILITY.py": "PROOF_QUANTUM_SAFE_INTEROPERABILITY.py",
    "PROVA_QUANTUM_SAFE_ROUTING.py": "PROOF_QUANTUM_SAFE_ROUTING.py",
    "GERAR_PROVAS_INVESTIDORES.py": "GENERATE_INVESTOR_PROOFS.py",
    "EXECUTAR_TODOS_TESTES_INVESTIDORES.py": "RUN_ALL_INVESTOR_TESTS.py",
    "EXECUTAR_TODOS_TESTES.bat": "RUN_ALL_TESTS.bat",
    "executar_todos_testes.py": "run_all_tests.py",
    
    # Test files
    "TESTE_STRESS_QRS3.py": "TEST_STRESS_QRS3.py",
    "TESTE_COM_HASH_REAL.py": "TEST_WITH_REAL_HASH.py",
    "TESTE_REAL_50_MELHORIAS.py": "TEST_REAL_50_IMPROVEMENTS.py",
    "TESTE_TODAS_50_MELHORIAS.py": "TEST_ALL_50_IMPROVEMENTS.py",
    "TESTE_TODAS_MELHORIAS_V2.py": "TEST_ALL_IMPROVEMENTS_V2.py",
    "TESTE_PERFORMANCE_OTIMIZADO.py": "TEST_OPTIMIZED_PERFORMANCE.py",
    "TESTE_COMPRESSAO_ASSINATURAS.py": "TEST_SIGNATURE_COMPRESSION.py",
    "TESTE_FALCON_COMPACTO.py": "TEST_COMPACT_FALCON.py",
    "TESTE_BATCH_VERIFICATION.py": "TEST_BATCH_VERIFICATION.py",
    "TESTE_TODAS_INOVACOES.py": "TEST_ALL_INNOVATIONS.py",
    "TESTE_PERFORMANCE_PQC.py": "TEST_PQC_PERFORMANCE.py",
    "TESTE_TODAS_MELHORIAS.py": "TEST_ALL_IMPROVEMENTS.py",
    "teste_novas_melhorias.py": "test_new_improvements.py",
    "teste_benchmark_real_fase2.py": "test_benchmark_real_phase2.py",
    "teste_fase2_investidor.py": "test_phase2_investor.py",
    "teste_fase2_simples.py": "test_phase2_simple.py",
    "testar_testes_profissionais.py": "run_professional_tests.py",
    "testar_testes_implementados.py": "run_implemented_tests.py",
    
    # Utility files
    "gerar_chave_teste.py": "generate_test_key.py",
    "gerar_chave_wif_bitcoin.py": "generate_bitcoin_wif_key.py",
    "gerar_endereco_bitcoin.py": "generate_bitcoin_address.py",
    "verificar_prova.py": "verify_proof.py",
    "DEMONSTRACAO_VALIDACAO_REAL.py": "DEMONSTRATION_REAL_VALIDATION.py",
    
    # Documentation files (main ones)
    "ESTRUTURA_REPOSITORIO_PUBLICO.md": "PUBLIC_REPOSITORY_STRUCTURE.md",
    "IMPLEMENTACAO_COMPLETA.md": "COMPLETE_IMPLEMENTATION.md",
    "CHECKLIST_3_ITENS.md": "CHECKLIST_3_ITEMS.md",
    "GUIA_DEMO_GIF.md": "DEMO_GIF_GUIDE.md",
    "PROVAS_TECNICAS_COMPLETAS_FINAL.json": "COMPLETE_TECHNICAL_PROOFS_FINAL.json",
    "PROVAS_TECNICAS_COMPLETAS_FINAL_EN.json": "COMPLETE_TECHNICAL_PROOFS_FINAL_EN.json",
}

def rename_files():
    """Rename files according to mapping"""
    root = Path(".")
    renamed = []
    errors = []
    
    for old_name, new_name in RENAME_MAP.items():
        old_path = root / old_name
        new_path = root / new_name
        
        if old_path.exists():
            try:
                old_path.rename(new_path)
                renamed.append((old_name, new_name))
                print(f"✅ Renamed: {old_name} → {new_name}")
            except Exception as e:
                errors.append((old_name, str(e)))
                print(f"❌ Error renaming {old_name}: {e}")
        else:
            print(f"⚠️  File not found: {old_name}")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Renamed: {len(renamed)} files")
    print(f"   ❌ Errors: {len(errors)} files")
    
    if errors:
        print(f"\n❌ Errors:")
        for old_name, error in errors:
            print(f"   {old_name}: {error}")
    
    return renamed, errors

if __name__ == "__main__":
    print("🔄 Renaming Portuguese files to English...\n")
    renamed, errors = rename_files()
    print(f"\n✅ Done! Renamed {len(renamed)} files.")

