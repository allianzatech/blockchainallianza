#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 Script para Organizar Provas e Hashes de Forma Profissional
Organiza todas as provas em estrutura clara e acessível
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# Estrutura profissional para provas
ESTRUTURA_PROVAS = {
    "proofs/": {
        "on_chain/": "Hashes de transações on-chain verificáveis",
        "qrs3/": "Provas de segurança quântica (QRS-3)",
        "interoperability/": "Provas de interoperabilidade (ALZ-NIEV)",
        "performance/": "Provas de performance",
        "testnet/": "Provas da testnet pública",
    }
}

def criar_estrutura():
    """Cria estrutura de diretórios para provas"""
    for base_dir, subdirs in ESTRUTURA_PROVAS.items():
        Path(base_dir).mkdir(parents=True, exist_ok=True)
        for subdir, desc in subdirs.items():
            full_path = Path(base_dir) / subdir
            full_path.mkdir(parents=True, exist_ok=True)
            # Criar README em cada diretório
            readme_path = full_path / "README.md"
            if not readme_path.exists():
                readme_content = f"# {subdir.replace('_', ' ').title()}\n\n{desc}\n"
                readme_path.write_text(readme_content, encoding='utf-8')
            print(f"✅ Criado: {full_path}")

def organizar_provas():
    """Organiza provas existentes na nova estrutura"""
    movidos = 0
    
    # Mover provas de QRS-3
    qrs3_sources = [
        "proofs/pilar_2_seguranca_quantica/",
        "proofs/pqc_complete/",
        "proofs/qrs3_verification_proof.json",
        "proofs/qss_quantum_proof.json",
    ]
    
    for source in qrs3_sources:
        source_path = Path(source)
        if source_path.exists():
            if source_path.is_file():
                dest = Path("proofs/qrs3") / source_path.name
                if not dest.exists():
                    shutil.copy2(source_path, dest)
                    print(f"✅ Copiado: {source} → {dest}")
                    movidos += 1
            elif source_path.is_dir():
                for file in source_path.glob("*.json"):
                    dest = Path("proofs/qrs3") / file.name
                    if not dest.exists():
                        shutil.copy2(file, dest)
                        print(f"✅ Copiado: {file} → {dest}")
                        movidos += 1
    
    # Mover provas de interoperabilidade
    interop_sources = [
        "proofs/pilar_1_interoperabilidade/",
        "proofs/interoperability_real/",
        "proofs/alz_niev_*.json",
        "proofs/real_transfer_*.json",
    ]
    
    for source in interop_sources:
        if "*" in source:
            # Pattern matching
            import glob
            for file_path in glob.glob(source):
                file = Path(file_path)
                dest = Path("proofs/interoperability") / file.name
                if not dest.exists():
                    shutil.copy2(file, dest)
                    print(f"✅ Copiado: {file} → {dest}")
                    movidos += 1
        else:
            source_path = Path(source)
            if source_path.exists():
                if source_path.is_dir():
                    for file in source_path.glob("*.json"):
                        dest = Path("proofs/interoperability") / file.name
                        if not dest.exists():
                            shutil.copy2(file, dest)
                            print(f"✅ Copiado: {file} → {dest}")
                            movidos += 1
    
    # Mover provas de performance
    perf_sources = [
        "proofs/performance_pqc/",
        "proofs/teste_real_50_melhorias_*.json",
    ]
    
    for source in perf_sources:
        if "*" in source:
            import glob
            for file_path in glob.glob(source):
                file = Path(file_path)
                dest = Path("proofs/performance") / file.name
                if not dest.exists():
                    shutil.copy2(file, dest)
                    print(f"✅ Copiado: {file} → {dest}")
                    movidos += 1
        else:
            source_path = Path(source)
            if source_path.exists():
                if source_path.is_dir():
                    for file in source_path.glob("*.json"):
                        dest = Path("proofs/performance") / file.name
                        if not dest.exists():
                            shutil.copy2(file, dest)
                            print(f"✅ Copiado: {file} → {dest}")
                            movidos += 1
    
    return movidos

def criar_indice_hashes():
    """Cria índice centralizado de hashes"""
    hashes_file = Path("VERIFIABLE_ON_CHAIN_PROOFS.md")
    if hashes_file.exists():
        # Copiar para proofs/on_chain/
        dest = Path("proofs/on_chain") / "VERIFIABLE_HASHES.md"
        shutil.copy2(hashes_file, dest)
        print(f"✅ Índice de hashes copiado: {dest}")
        return True
    return False

def main():
    print("📁 Organizando provas e hashes de forma profissional...\n")
    criar_estrutura()
    print("\n📦 Organizando provas existentes...\n")
    movidos = organizar_provas()
    print("\n🔗 Criando índice de hashes...\n")
    criar_indice_hashes()
    print(f"\n✅ Organização concluída! {movidos} arquivos organizados.")

if __name__ == "__main__":
    main()

