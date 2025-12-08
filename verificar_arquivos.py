#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script de Verificação de Arquivos - Allianza Blockchain
Verifica se todos os arquivos listados existem e têm conteúdo
"""

import os
import sys
from pathlib import Path

# Lista de arquivos para verificar
ARQUIVOS_VERIFICAR = [
    "tests/quantum_attack_simulations.py",
    "ROADMAP_KPIS.md",
    "docs/RWA_TOKENIZATION_STRATEGY.md",
    "core/interoperability/solana_bridge.py",
    "tests/cross_chain_recovery.py",
    "tests/benchmark_independent.py",
    "RISK_ANALYSIS.md",
    "proofs/HASHES_INDEX.md"
]

def verificar_arquivo(caminho: str) -> dict:
    """Verifica se um arquivo existe e tem conteúdo"""
    resultado = {
        "arquivo": caminho,
        "existe": False,
        "tamanho": 0,
        "linhas": 0,
        "erro": None
    }
    
    try:
        caminho_completo = Path(caminho)
        if caminho_completo.exists():
            resultado["existe"] = True
            resultado["tamanho"] = caminho_completo.stat().st_size
            
            # Contar linhas
            with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                resultado["linhas"] = sum(1 for _ in f)
        else:
            resultado["erro"] = "Arquivo não encontrado"
    except Exception as e:
        resultado["erro"] = str(e)
    
    return resultado

def main():
    """Função principal"""
    print("=" * 70)
    print("🔍 VERIFICAÇÃO DE ARQUIVOS - ALLIANZA BLOCKCHAIN")
    print("=" * 70)
    print()
    
    resultados = []
    total_arquivos = len(ARQUIVOS_VERIFICAR)
    arquivos_encontrados = 0
    
    for arquivo in ARQUIVOS_VERIFICAR:
        resultado = verificar_arquivo(arquivo)
        resultados.append(resultado)
        
        if resultado["existe"]:
            arquivos_encontrados += 1
            status = "✅"
            info = f"{resultado['linhas']} linhas, {resultado['tamanho']} bytes"
        else:
            status = "❌"
            info = resultado.get("erro", "Não encontrado")
        
        print(f"{status} {arquivo}")
        print(f"   {info}")
        print()
    
    # Resumo
    print("=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    print(f"Total de arquivos verificados: {total_arquivos}")
    print(f"Arquivos encontrados: {arquivos_encontrados}")
    print(f"Arquivos não encontrados: {total_arquivos - arquivos_encontrados}")
    print()
    
    if arquivos_encontrados == total_arquivos:
        print("✅ TODOS OS ARQUIVOS FORAM ENCONTRADOS!")
        return 0
    else:
        print("⚠️  ALGUNS ARQUIVOS NÃO FORAM ENCONTRADOS")
        return 1

if __name__ == "__main__":
    sys.exit(main())

