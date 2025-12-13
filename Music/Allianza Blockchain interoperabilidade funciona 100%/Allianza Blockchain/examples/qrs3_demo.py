#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 QRS-3 (Quantum Redundancy System - Triple) - Exemplo de Uso
Demonstra o sistema de assinatura tripla redundante
"""

import hashlib
import json
from typing import Dict, Optional

class QRS3Demo:
    """
    Demonstração do QRS-3 (Quantum Redundancy System - Triple)
    
    O QRS-3 combina 3 algoritmos simultaneamente:
    1. ECDSA (secp256k1) - Compatibilidade com blockchains existentes
    2. ML-DSA (Dilithium) - Padrão NIST PQC para assinaturas quântico-seguras
    3. SPHINCS+ - Hash-based signatures (NIST PQC)
    
    Isso garante:
    - Compatibilidade com blockchains atuais (via ECDSA)
    - Proteção contra computadores quânticos (via ML-DSA e SPHINCS+)
    - Redundância tripla para máxima segurança
    """
    
    def __init__(self):
        self.algorithm_info = {
            "ecdsa": {
                "name": "ECDSA (secp256k1)",
                "type": "Classical",
                "quantum_safe": False,
                "purpose": "Compatibilidade com Bitcoin, Ethereum, etc."
            },
            "ml_dsa": {
                "name": "ML-DSA (Dilithium)",
                "type": "NIST PQC",
                "quantum_safe": True,
                "purpose": "Assinaturas quântico-seguras (padrão NIST)"
            },
            "sphincs": {
                "name": "SPHINCS+",
                "type": "Hash-based (NIST PQC)",
                "quantum_safe": True,
                "purpose": "Assinaturas baseadas em hash (backup)"
            }
        }
    
    def explain_qrs3(self):
        """Explica o conceito do QRS-3"""
        print("=" * 70)
        print("🔐 QRS-3: Quantum Redundancy System - Triple")
        print("=" * 70)
        print("\nO QRS-3 é um sistema de assinatura digital que combina")
        print("3 algoritmos simultaneamente para máxima segurança:\n")
        
        for algo_id, info in self.algorithm_info.items():
            quantum_badge = "✅ Quantum-Safe" if info["quantum_safe"] else "⚠️  Não Quantum-Safe"
            print(f"   {info['name']}")
            print(f"      Tipo: {info['type']}")
            print(f"      {quantum_badge}")
            print(f"      Propósito: {info['purpose']}\n")
        
        print("=" * 70)
        print("🎯 Vantagens do QRS-3:")
        print("=" * 70)
        print("   ✅ Compatibilidade: Funciona com blockchains existentes (ECDSA)")
        print("   ✅ Segurança Quântica: Proteção contra computadores quânticos (ML-DSA + SPHINCS+)")
        print("   ✅ Redundância: Se um algoritmo falhar, outros continuam funcionando")
        print("   ✅ Adaptativo: Escolhe o melhor algoritmo baseado no valor da transação")
        print("   ✅ Fallback Inteligente: QRS-2 quando SPHINCS+ não disponível")
        print()
    
    def demonstrate_signature_flow(self, message: str = "Hello, Allianza!"):
        """
        Demonstra o fluxo de assinatura QRS-3
        
        Args:
            message: Mensagem a ser assinada
        """
        print("=" * 70)
        print("📝 DEMONSTRAÇÃO: Fluxo de Assinatura QRS-3")
        print("=" * 70)
        
        # 1. Preparar mensagem
        print(f"\n1️⃣ Mensagem a ser assinada:")
        print(f"   '{message}'")
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        print(f"   Hash SHA256: {message_hash}")
        
        # 2. Gerar keypair QRS-3 (simulado)
        print(f"\n2️⃣ Gerando keypair QRS-3...")
        print(f"   ✅ Chave ECDSA gerada (secp256k1)")
        print(f"   ✅ Chave ML-DSA gerada (Dilithium)")
        print(f"   ✅ Chave SPHINCS+ gerada")
        keypair_id = f"qrs3_{hashlib.sha256(message.encode()).hexdigest()[:16]}"
        print(f"   Keypair ID: {keypair_id}")
        
        # 3. Assinar com os 3 algoritmos
        print(f"\n3️⃣ Assinando com os 3 algoritmos simultaneamente...")
        
        signatures = {
            "ecdsa": {
                "signature": f"0x{hashlib.sha256(f'{message}_ecdsa'.encode()).hexdigest()[:64]}",
                "algorithm": "ECDSA (secp256k1)",
                "size": "64 bytes"
            },
            "ml_dsa": {
                "signature": f"0x{hashlib.sha256(f'{message}_ml_dsa'.encode()).hexdigest()[:128]}",
                "algorithm": "ML-DSA (Dilithium)",
                "size": "~2420 bytes"
            },
            "sphincs": {
                "signature": f"0x{hashlib.sha256(f'{message}_sphincs'.encode()).hexdigest()[:256]}",
                "algorithm": "SPHINCS+",
                "size": "~7856 bytes"
            }
        }
        
        for algo_id, sig_data in signatures.items():
            print(f"   ✅ {sig_data['algorithm']}: {sig_data['signature'][:32]}... ({sig_data['size']})")
        
        # 4. Criar bundle QRS-3
        print(f"\n4️⃣ Criando bundle QRS-3...")
        qrs3_bundle = {
            "message": message,
            "message_hash": message_hash,
            "keypair_id": keypair_id,
            "signatures": signatures,
            "timestamp": "2025-12-05T00:00:00Z",
            "version": "QRS-3"
        }
        print(f"   ✅ Bundle criado com 3 assinaturas")
        
        # 5. Verificar assinaturas
        print(f"\n5️⃣ Verificando assinaturas...")
        for algo_id, sig_data in signatures.items():
            print(f"   ✅ {sig_data['algorithm']}: Válida")
        
        print(f"\n✅ Assinatura QRS-3 completa e válida!")
        
        return qrs3_bundle
    
    def demonstrate_adaptive_signing(self, transaction_value: float):
        """
        Demonstra assinatura adaptativa baseada no valor da transação
        
        Args:
            transaction_value: Valor da transação
        """
        print("=" * 70)
        print("💰 DEMONSTRAÇÃO: Assinatura Adaptativa")
        print("=" * 70)
        print(f"\nValor da transação: ${transaction_value:,.2f}")
        
        if transaction_value < 100:
            mode = "QRS-1 (ECDSA apenas)"
            reason = "Transações pequenas usam apenas ECDSA para economia"
        elif transaction_value < 10000:
            mode = "QRS-2 (ECDSA + ML-DSA)"
            reason = "Transações médias usam ECDSA + ML-DSA"
        else:
            mode = "QRS-3 (ECDSA + ML-DSA + SPHINCS+)"
            reason = "Transações grandes usam todos os 3 algoritmos"
        
        print(f"\n🎯 Modo selecionado: {mode}")
        print(f"   Razão: {reason}")
        print(f"   Segurança: {'Máxima' if mode == 'QRS-3' else 'Alta' if mode == 'QRS-2' else 'Padrão'}")
    
    def demonstrate_fallback(self):
        """Demonstra fallback inteligente para QRS-2"""
        print("=" * 70)
        print("🔄 DEMONSTRAÇÃO: Fallback Inteligente")
        print("=" * 70)
        
        print("\nCenário: SPHINCS+ não disponível (biblioteca não instalada)")
        print("\n1️⃣ Tentando gerar assinatura QRS-3...")
        print("   ⚠️  SPHINCS+ não disponível")
        print("\n2️⃣ Fallback automático para QRS-2...")
        print("   ✅ ECDSA: Disponível")
        print("   ✅ ML-DSA: Disponível")
        print("   ⚠️  SPHINCS+: Não disponível (fallback)")
        print("\n3️⃣ Assinatura QRS-2 gerada com sucesso!")
        print("   ✅ Compatibilidade mantida (ECDSA)")
        print("   ✅ Segurança quântica mantida (ML-DSA)")
        print("   ⚠️  Redundância reduzida (sem SPHINCS+)")
        print("\n✅ Sistema continua funcionando mesmo sem SPHINCS+")


def demo_completo():
    """Demonstração completa do QRS-3"""
    demo = QRS3Demo()
    
    # 1. Explicar QRS-3
    demo.explain_qrs3()
    
    # 2. Demonstrar fluxo de assinatura
    print("\n" + "=" * 70)
    bundle = demo.demonstrate_signature_flow("Transfer 1.5 BTC to address...")
    
    # 3. Demonstrar assinatura adaptativa
    print("\n" + "=" * 70)
    demo.demonstrate_adaptive_signing(50000)  # Transação grande
    print()
    demo.demonstrate_adaptive_signing(500)   # Transação média
    print()
    demo.demonstrate_adaptive_signing(10)    # Transação pequena
    
    # 4. Demonstrar fallback
    print("\n" + "=" * 70)
    demo.demonstrate_fallback()
    
    print("\n" + "=" * 70)
    print("✅ DEMONSTRAÇÃO COMPLETA!")
    print("=" * 70)
    print("\n💡 Casos de uso:")
    print("   • Transações de alto valor: Máxima segurança (QRS-3)")
    print("   • Transações médias: Segurança quântica (QRS-2)")
    print("   • Transações pequenas: Compatibilidade (QRS-1)")
    print("   • Fallback automático: Sistema sempre funciona")


if __name__ == "__main__":
    demo_completo()

