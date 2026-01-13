#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 QSS (Quantum Security Service) - Exemplo de Uso
Demonstra como usar o QSS para adicionar segurança quântica a qualquer blockchain
"""

import requests
import json
import hashlib
from typing import Dict, Optional

# URL da API QSS
QSS_API_URL = "https://testnet.allianza.tech/api/qss"

class QSSDemo:
    """
    Demonstração do Quantum Security Service (QSS)
    
    O QSS permite que qualquer blockchain use segurança quântica da Allianza
    sem precisar implementar algoritmos PQC próprios.
    """
    
    def __init__(self, api_url: str = QSS_API_URL):
        self.api_url = api_url
    
    def generate_proof(self, chain: str, tx_hash: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Gera uma prova quântica para uma transação de qualquer blockchain
        
        Args:
            chain: Nome da blockchain (bitcoin, ethereum, polygon, etc.)
            tx_hash: Hash da transação na blockchain original
            metadata: Metadados opcionais (block_height, amount, etc.)
        
        Returns:
            Dict com a prova quântica gerada
        """
        print(f"\n🔐 Gerando prova quântica para {chain.upper()}...")
        print(f"   TX Hash: {tx_hash}")
        
        payload = {
            "chain": chain,
            "tx_hash": tx_hash,
            "metadata": metadata or {}
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/generate-proof",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                proof = result['quantum_proof']
                print(f"✅ Prova gerada com sucesso!")
                print(f"   Proof ID: {proof.get('proof_id')}")
                print(f"   Proof Hash: {proof.get('proof_hash')}")
                print(f"   Algoritmo: {proof.get('algorithm', 'ML-DSA')}")
                return proof
            else:
                print(f"❌ Erro: {result.get('error')}")
                return {}
        except Exception as e:
            print(f"❌ Erro ao gerar prova: {e}")
            return {}
    
    def verify_proof(self, quantum_proof: Dict) -> bool:
        """
        Verifica uma prova quântica
        
        Args:
            quantum_proof: Prova quântica gerada anteriormente
        
        Returns:
            True se a prova for válida
        """
        print(f"\n🔍 Verificando prova quântica...")
        print(f"   Proof ID: {quantum_proof.get('proof_id')}")
        
        payload = {
            "quantum_proof": quantum_proof
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/verify-proof",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success') and result.get('valid'):
                print(f"✅ Prova válida!")
                print(f"   Assinatura ML-DSA: {'✅ Válida' if result.get('verification_details', {}).get('signature_valid') else '❌ Inválida'}")
                print(f"   Merkle Proof: {'✅ Válida' if result.get('verification_details', {}).get('merkle_proof_valid') else '❌ Inválida'}")
                return True
            else:
                print(f"❌ Prova inválida: {result.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Erro ao verificar prova: {e}")
            return False
    
    def anchor_proof(self, quantum_proof: Dict, target_chain: str, target_address: Optional[str] = None) -> Dict:
        """
        Obtém instruções para ancorar uma prova quântica em uma blockchain
        
        Args:
            quantum_proof: Prova quântica a ser ancorada
            target_chain: Blockchain onde ancorar (bitcoin, ethereum, etc.)
            target_address: Endereço opcional na blockchain destino
        
        Returns:
            Dict com instruções de ancoragem
        """
        print(f"\n⚓ Obtendo instruções para ancorar prova em {target_chain.upper()}...")
        
        payload = {
            "quantum_proof": quantum_proof,
            "target_chain": target_chain,
            "target_address": target_address
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/anchor-proof",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                instructions = result.get('anchor_instructions', {})
                print(f"✅ Instruções geradas!")
                print(f"   Método: {instructions.get('method')}")
                print(f"   Dados para ancorar: {instructions.get('data', '')[:50]}...")
                return instructions
            else:
                print(f"❌ Erro: {result.get('error')}")
                return {}
        except Exception as e:
            print(f"❌ Erro ao obter instruções: {e}")
            return {}
    
    def get_status(self) -> Dict:
        """Obtém status do serviço QSS"""
        try:
            response = requests.get(f"{self.api_url}/status", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao obter status: {e}")
            return {}


def demo_completo():
    """Demonstração completa do QSS"""
    print("=" * 70)
    print("🔐 DEMONSTRAÇÃO: Quantum Security Service (QSS)")
    print("=" * 70)
    print("\nO QSS permite que qualquer blockchain use segurança quântica")
    print("sem precisar implementar algoritmos PQC próprios.\n")
    
    qss = QSSDemo()
    
    # 1. Verificar status
    print("\n1️⃣ Verificando status do serviço...")
    status = qss.get_status()
    if status.get('success'):
        print(f"✅ QSS está operacional")
        print(f"   Blockchains suportadas: {', '.join(status.get('supported_chains', []))}")
        print(f"   Algoritmos: {', '.join(status.get('signature_schemes', []))}")
    
    # 2. Gerar prova para uma transação Bitcoin
    print("\n" + "=" * 70)
    print("2️⃣ EXEMPLO: Gerar prova para transação Bitcoin")
    print("=" * 70)
    
    bitcoin_tx = "89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb"
    proof = qss.generate_proof(
        chain="bitcoin",
        tx_hash=bitcoin_tx,
        metadata={"block_height": 0, "amount": "0.01"}
    )
    
    if not proof:
        print("❌ Não foi possível gerar a prova. Continuando com exemplo...")
        return
    
    # 3. Verificar a prova
    print("\n" + "=" * 70)
    print("3️⃣ EXEMPLO: Verificar prova quântica")
    print("=" * 70)
    
    is_valid = qss.verify_proof(proof)
    
    # 4. Ancorar no Ethereum
    if is_valid:
        print("\n" + "=" * 70)
        print("4️⃣ EXEMPLO: Ancorar prova no Ethereum")
        print("=" * 70)
        
        instructions = qss.anchor_proof(
            quantum_proof=proof,
            target_chain="ethereum",
            target_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        )
        
        if instructions:
            print("\n📋 Próximos passos:")
            print("   1. Use os dados fornecidos para criar uma transação")
            print("   2. Envie a transação para a blockchain Ethereum")
            print("   3. A prova quântica estará ancorada permanentemente")
    
    print("\n" + "=" * 70)
    print("✅ DEMONSTRAÇÃO COMPLETA!")
    print("=" * 70)
    print("\n💡 Casos de uso:")
    print("   • Exchanges: Verificar saques com segurança quântica")
    print("   • Bridges: Proteger transferências cross-chain")
    print("   • DeFi: Adicionar segurança quântica a smart contracts")
    print("   • Auditoria: Certificar transações importantes")


if __name__ == "__main__":
    demo_completo()

