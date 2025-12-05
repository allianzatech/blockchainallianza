#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar hashes SHA256 de todos os arquivos para registro no INPI
"""

import hashlib
import os
import json
from datetime import datetime
from pathlib import Path

def calcular_hash_arquivo(caminho_arquivo):
    """Calcula SHA256 de um arquivo"""
    sha256_hash = hashlib.sha256()
    try:
        with open(caminho_arquivo, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"ERRO: {str(e)}"

def gerar_hashes_patentes():
    """Gera hashes dos documentos de patentes"""
    patentes = [
        "INPI_PI_01_ALZ_NIEV_DESCRICAO_COMPLETA.md",
        "INPI_PI_02_QRS3_DESCRICAO_COMPLETA.md",
        "INPI_PI_03_QSS_DESCRICAO_COMPLETA.md",
        "TEMPLATES_DESCRICAO_TECNICA_PATENTES.md",
        "DOCUMENTACAO_INPI_COMPLETA.md"
    ]
    
    hashes = {}
    for patente in patentes:
        if os.path.exists(patente):
            hash_val = calcular_hash_arquivo(patente)
            tamanho = os.path.getsize(patente)
            hashes[patente] = {
                "hash_sha256": hash_val,
                "tamanho_bytes": tamanho,
                "data_geracao": datetime.now().isoformat()
            }
    
    return hashes

def gerar_hash_consolidado(hashes_arquivos):
    """Gera um hash SHA256 consolidado a partir de uma lista de hashes"""
    # Concatena todos os hashes em ordem alfabética (para garantir consistência)
    hashes_ordenados = sorted(hashes_arquivos)
    string_consolidada = "".join(hashes_ordenados)
    # Gera SHA256 da string consolidada
    hash_consolidado = hashlib.sha256(string_consolidada.encode('utf-8')).hexdigest()
    return hash_consolidado

def gerar_hashes_rpc():
    """Gera hashes dos arquivos dos programas de computador"""
    rpc_arquivos = {
        "RPC-1_ALZ_NIEV": [
            "alz_niev_interoperability.py",
            "real_cross_chain_bridge.py",
            "quantum_safe_interoperability.py",
            "test_atomicity_failure.py",
            "test_write_cross_chain.py"
        ],
        "RPC-2_QUANTUM_SECURITY": [
            "quantum_security.py",
            "quantum_security_REAL.py",
            "quantum_multi_sig_wallet.py",
            "qrs3_complete_verification.py",
            "qrs3_optimized_sharding.py"
        ],
        "RPC-3_QSS": [
            "qss_api_service.py",
            "qss-verifier/verify.js"
        ],
        "RPC-4_BRIDGE": [
            "real_cross_chain_bridge.py"
        ]
    }
    
    hashes = {}
    hashes_consolidados = {}
    
    for rpc_nome, arquivos in rpc_arquivos.items():
        hashes[rpc_nome] = {}
        hashes_lista = []
        
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                hash_val = calcular_hash_arquivo(arquivo)
                tamanho = os.path.getsize(arquivo)
                hashes[rpc_nome][arquivo] = {
                    "hash_sha256": hash_val,
                    "tamanho_bytes": tamanho,
                    "data_geracao": datetime.now().isoformat()
                }
                hashes_lista.append(hash_val)
        
        # Gerar hash consolidado para este RPC
        if hashes_lista:
            hash_consolidado = gerar_hash_consolidado(hashes_lista)
            hashes_consolidados[rpc_nome] = {
                "hash_sha256_consolidado": hash_consolidado,
                "arquivos_incluidos": len(hashes_lista),
                "data_geracao": datetime.now().isoformat()
            }
    
    return hashes, hashes_consolidados

def gerar_hashes_documentacao():
    """Gera hashes da documentação"""
    docs = [
        "GUIA_PASSO_A_PASSO_DEPOSITO_INPI.md",
        "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md",
        "WHITEPAPER_ALLIANZA_BLOCKCHAIN.md"
    ]
    
    hashes = {}
    for doc in docs:
        if os.path.exists(doc):
            hash_val = calcular_hash_arquivo(doc)
            tamanho = os.path.getsize(doc)
            hashes[doc] = {
                "hash_sha256": hash_val,
                "tamanho_bytes": tamanho,
                "data_geracao": datetime.now().isoformat()
            }
    
    return hashes

def main():
    """Função principal"""
    print("🔐 Gerando hashes SHA256 para registro no INPI...")
    print("=" * 60)
    
    rpc_hashes, rpc_consolidados = gerar_hashes_rpc()
    
    # Gerar hash consolidado FINAL (todos os programas juntos)
    todos_hashes_rpc = []
    for rpc_nome, dados in rpc_consolidados.items():
        todos_hashes_rpc.append(dados['hash_sha256_consolidado'])
    
    hash_final_todos_programas = gerar_hash_consolidado(todos_hashes_rpc) if todos_hashes_rpc else None
    
    resultado = {
        "data_geracao": datetime.now().isoformat(),
        "patentes": gerar_hashes_patentes(),
        "rpc": rpc_hashes,
        "rpc_consolidados": rpc_consolidados,
        "hash_final_todos_programas": {
            "hash_sha256": hash_final_todos_programas,
            "programas_incluidos": list(rpc_consolidados.keys()),
            "total_programas": len(rpc_consolidados),
            "data_geracao": datetime.now().isoformat()
        } if hash_final_todos_programas else None,
        "documentacao": gerar_hashes_documentacao()
    }
    
    # Salvar em JSON
    arquivo_json = "HASHES_INPI_COMPLETO.json"
    with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Hashes gerados e salvos em: {arquivo_json}")
    print("\n📊 Resumo:")
    print(f"   - Patentes: {len(resultado['patentes'])} arquivos")
    print(f"   - RPCs: {len(resultado['rpc'])} programas")
    print(f"   - Documentação: {len(resultado['documentacao'])} arquivos")
    print(f"\n🔐 Hashes Consolidados por Programa:")
    for rpc_nome, dados in resultado['rpc_consolidados'].items():
        print(f"   - {rpc_nome}: {dados['hash_sha256_consolidado']}")
    
    if resultado['hash_final_todos_programas']:
        print(f"\n🎯 HASH FINAL (TODOS OS PROGRAMAS JUNTOS):")
        print(f"   {resultado['hash_final_todos_programas']['hash_sha256']}")
        print(f"   Programas incluídos: {resultado['hash_final_todos_programas']['total_programas']}")
    
    # Gerar também um resumo em texto
    arquivo_txt = "HASHES_INPI_RESUMO.txt"
    with open(arquivo_txt, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("HASHES SHA256 PARA REGISTRO NO INPI\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Data de Geração: {resultado['data_geracao']}\n\n")
        
        f.write("PATENTES DE INVENÇÃO (PI)\n")
        f.write("-" * 60 + "\n")
        for arquivo, dados in resultado['patentes'].items():
            f.write(f"\n{arquivo}\n")
            f.write(f"  Hash SHA256: {dados['hash_sha256']}\n")
            f.write(f"  Tamanho: {dados['tamanho_bytes']} bytes\n")
        
        f.write("\n\nREGISTROS DE PROGRAMA DE COMPUTADOR (RPC)\n")
        f.write("-" * 60 + "\n")
        for rpc_nome, arquivos in resultado['rpc'].items():
            f.write(f"\n{rpc_nome}:\n")
            for arquivo, dados in arquivos.items():
                f.write(f"  {arquivo}\n")
                f.write(f"    Hash SHA256: {dados['hash_sha256']}\n")
                f.write(f"    Tamanho: {dados['tamanho_bytes']} bytes\n")
        
        f.write("\n\n⚠️ HASHES CONSOLIDADOS (UM HASH POR PROGRAMA) ⚠️\n")
        f.write("=" * 60 + "\n")
        f.write("Use estes hashes se o formulário aceitar apenas UM hash por programa:\n\n")
        for rpc_nome, dados in resultado['rpc_consolidados'].items():
            f.write(f"{rpc_nome}:\n")
            f.write(f"  🔐 HASH CONSOLIDADO SHA256: {dados['hash_sha256_consolidado']}\n")
            f.write(f"  📁 Arquivos incluídos: {dados['arquivos_incluidos']}\n")
            f.write(f"  📅 Data: {dados['data_geracao']}\n\n")
        
        if resultado['hash_final_todos_programas']:
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("🎯 HASH FINAL CONSOLIDADO (TODOS OS PROGRAMAS JUNTOS) 🎯\n")
            f.write("=" * 60 + "\n")
            f.write("⚠️ USE ESTE HASH PARA REGISTRAR TODOS OS PROGRAMAS DE UMA VEZ ⚠️\n\n")
            f.write(f"Hash SHA256 Final:\n")
            f.write(f"{resultado['hash_final_todos_programas']['hash_sha256']}\n\n")
            f.write(f"Programas incluídos ({resultado['hash_final_todos_programas']['total_programas']}):\n")
            for programa in resultado['hash_final_todos_programas']['programas_incluidos']:
                f.write(f"  - {programa}\n")
            f.write(f"\nData de Geração: {resultado['hash_final_todos_programas']['data_geracao']}\n")
            f.write("\n" + "=" * 60 + "\n")
        
        f.write("\n\nDOCUMENTAÇÃO\n")
        f.write("-" * 60 + "\n")
        for arquivo, dados in resultado['documentacao'].items():
            f.write(f"\n{arquivo}\n")
            f.write(f"  Hash SHA256: {dados['hash_sha256']}\n")
            f.write(f"  Tamanho: {dados['tamanho_bytes']} bytes\n")
    
    print(f"✅ Resumo em texto salvo em: {arquivo_txt}")
    print("\n" + "=" * 60)
    print("✅ Processo concluído!")

if __name__ == "__main__":
    main()



