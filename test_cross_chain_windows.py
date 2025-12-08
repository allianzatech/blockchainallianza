#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar Cross-Chain Transfers no Windows
Uso: python test_cross_chain_windows.py
"""

import requests
import json

BASE_URL = "https://testnet.allianza.tech"

def test_create_transfer():
    """Testa criação de transferência cross-chain"""
    print("\n" + "="*60)
    print("🧪 TESTE 1: Criar Transferência Cross-Chain")
    print("="*60)
    
    data = {
        "source_chain": "polygon",
        "target_chain": "ethereum",
        "amount": 0.1,
        "recipient": "0x86AE40869EB6ACb9477b42BfC9150c0A2Cc21f5E",
        "token_symbol": "ETH",
        "send_real": False  # Simulação (não requer private key)
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/cross-chain/transfer",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        result = response.json()
        
        if result.get("success"):
            print("✅ Transferência criada com sucesso!")
            print(f"   UChainID: {result.get('uchain_id', 'N/A')}")
            print(f"   Transfer ID: {result.get('transfer_id', 'N/A')}")
            print(f"   Has ZK Proof: {result.get('has_zk_proof', False)}")
            if result.get('tx_hash'):
                print(f"   TX Hash: {result.get('tx_hash')}")
            if result.get('explorer_url'):
                print(f"   Explorer: {result.get('explorer_url')}")
            return result.get('uchain_id')
        else:
            print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_search_proof(uchain_id):
    """Testa busca de prova por UChainID"""
    if not uchain_id:
        print("\n⚠️  Pulando busca de prova (UChainID não disponível)")
        return
    
    print("\n" + "="*60)
    print("🧪 TESTE 2: Buscar Prova por UChainID")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/cross-chain/proof/{uchain_id}"
        )
        
        result = response.json()
        
        if result.get("success"):
            print("✅ Prova encontrada!")
            print(f"   UChainID: {result.get('uchain_id')}")
            print(f"   Source Chain: {result.get('source_chain')}")
            print(f"   Target Chain: {result.get('target_chain')}")
            print(f"   Amount: {result.get('amount')}")
        else:
            print(f"❌ Erro: {result.get('error', 'Prova não encontrada')}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_list_proofs():
    """Testa listagem de todas as provas"""
    print("\n" + "="*60)
    print("🧪 TESTE 3: Listar Todas as Provas")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/cross-chain/proofs?limit=50"
        )
        
        result = response.json()
        
        if result.get("success"):
            print(f"✅ {result.get('total', 0)} provas encontradas")
            print(f"   Mostrando: {result.get('returned', 0)} provas")
            
            proofs = result.get('proofs', [])
            if proofs:
                print("\n   Primeiras 5 provas:")
                for i, proof in enumerate(proofs[:5], 1):
                    print(f"   {i}. UChainID: {proof.get('uchain_id')}")
                    print(f"      Source: {proof.get('source_chain')} → Target: {proof.get('target_chain')}")
                    print(f"      Amount: {proof.get('amount')}")
                    print(f"      Has ZK Proof: {proof.get('has_zk_proof', False)}")
        else:
            print(f"❌ Erro: {result.get('error', 'Erro ao listar provas')}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_status():
    """Testa status do sistema"""
    print("\n" + "="*60)
    print("🧪 TESTE 4: Status do Sistema")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/cross-chain/status")
        result = response.json()
        
        if result.get("success"):
            print("✅ Status do Sistema:")
            print(f"   State Commitments: {result.get('state_commitments', 0)}")
            print(f"   ZK Proofs: {result.get('zk_proofs', 0)}")
            print(f"   Applied States: {result.get('applied_states', 0)}")
            print(f"   UChainIDs: {result.get('uchain_ids', 0)}")
        else:
            print(f"❌ Erro: {result.get('error', 'Erro ao obter status')}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌉 TESTE DE CROSS-CHAIN TRANSFERS - ALLIANZA TESTNET")
    print("="*60)
    print(f"\n📡 Conectando a: {BASE_URL}")
    
    # Teste 1: Criar transferência
    uchain_id = test_create_transfer()
    
    # Teste 2: Buscar prova
    test_search_proof(uchain_id)
    
    # Teste 3: Listar provas
    test_list_proofs()
    
    # Teste 4: Status
    test_status()
    
    print("\n" + "="*60)
    print("✅ Testes concluídos!")
    print("="*60)
    print("\n💡 Dica: Acesse https://testnet.allianza.tech/cross-chain-test")
    print("   para testar via interface web!")

