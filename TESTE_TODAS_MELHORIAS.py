#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Completo de Todas as Melhorias Implementadas
"""

import time
import sys
from datetime import datetime

print("=" * 70)
print("🧪 TESTE COMPLETO DE TODAS AS MELHORIAS")
print("=" * 70)
print()

# Contador de sucessos
success_count = 0
total_tests = 0

def test_result(test_name, success, details=""):
    global success_count, total_tests
    total_tests += 1
    if success:
        success_count += 1
        print(f"✅ {test_name}: PASSOU")
    else:
        print(f"❌ {test_name}: FALHOU")
    if details:
        print(f"   {details}")
    print()

# ============================================================================
# TESTE 1: CONSENSO ADAPTATIVO AVANÇADO
# ============================================================================

print("=" * 70)
print("🌟 TESTE 1: CONSENSO ADAPTATIVO AVANÇADO")
print("=" * 70)
print()

try:
    from advanced_adaptive_consensus import AdvancedAdaptiveConsensus, ConsensusType
    
    # Criar blockchain mock
    class MockBlockchain:
        def __init__(self):
            self.wallets = {
                "addr1": {"staked": 5000},
                "addr2": {"staked": 3000},
                "addr3": {"staked": 2000}
            }
    
    blockchain = MockBlockchain()
    consensus = AdvancedAdaptiveConsensus(blockchain)
    
    # Testar adaptação
    consensus.update_network_state({
        "load": 0.9,  # Alta carga
        "validators": 5,
        "pending_txs": 100,
        "urgent_txs": 0,
        "qrs3_txs": 0
    })
    
    info = consensus.get_consensus_info()
    test_result("Consenso Adaptativo", info["current_consensus"] in ["PoA", "PoH"], 
                f"Consenso atual: {info['current_consensus']}")
    
except Exception as e:
    test_result("Consenso Adaptativo", False, f"Erro: {e}")

# ============================================================================
# TESTE 2: SHARDING DINÂMICO
# ============================================================================

print("=" * 70)
print("🔀 TESTE 2: SHARDING DINÂMICO")
print("=" * 70)
print()

try:
    from dynamic_sharding import DynamicSharding
    
    blockchain = MockBlockchain()
    blockchain.shards = {i: [] for i in range(8)}
    blockchain.pending_transactions = {i: [] for i in range(8)}
    blockchain.create_genesis_block = lambda x: {"shard_id": x, "index": 0}
    
    sharding = DynamicSharding(blockchain, min_shards=4, max_shards=1000)
    
    # Testar criação de shard
    loads = sharding.get_all_shard_loads()
    stats = sharding.get_sharding_stats()
    
    test_result("Sharding Dinâmico", stats["total_shards"] == 8,
                f"Shards: {stats['total_shards']}, Carga média: {stats['average_load']:.2%}")
    
except Exception as e:
    test_result("Sharding Dinâmico", False, f"Erro: {e}")

# ============================================================================
# TESTE 3: STATE CHANNELS
# ============================================================================

print("=" * 70)
print("⚡ TESTE 3: STATE CHANNELS QUÂNTICO-SEGUROS")
print("=" * 70)
print()

try:
    from quantum_security import QuantumSecuritySystem
    from quantum_safe_state_channels import QuantumSafeStateChannelManager
    
    blockchain = MockBlockchain()
    blockchain.get_balance = lambda x: 10000
    
    qs = QuantumSecuritySystem()
    manager = QuantumSafeStateChannelManager(blockchain, qs)
    
    # Abrir canal
    result = manager.open_channel(
        "party1",
        "party2",
        {"party1": {"ALZ": 1000}, "party2": {"ALZ": 500}}
    )
    
    if result.get("success"):
        channel_id = result["channel_id"]
        
        # Atualizar estado
        update_result = manager.update_channel(channel_id, "party1", "party2", 100, "ALZ")
        
        test_result("State Channels", update_result.get("success"),
                   f"Canal: {channel_id}, Latência: {update_result.get('latency_ms', 0)} ms")
    else:
        test_result("State Channels", False, result.get("error", "Erro desconhecido"))
    
except Exception as e:
    test_result("State Channels", False, f"Erro: {e}")

# ============================================================================
# TESTE 4: AGREGAÇÃO DE ASSINATURAS
# ============================================================================

print("=" * 70)
print("📦 TESTE 4: AGREGAÇÃO DE ASSINATURAS")
print("=" * 70)
print()

try:
    from signature_aggregation import SignatureAggregation
    from quantum_security import QuantumSecuritySystem
    
    qs = QuantumSecuritySystem()
    aggregator = SignatureAggregation()
    
    # Gerar múltiplas assinaturas
    signatures = []
    for i in range(5):
        keypair = qs.generate_qrs3_keypair()
        if keypair.get("success"):
            sig = qs.sign_qrs3(keypair["keypair_id"], f"message_{i}".encode())
            if sig.get("success"):
                signatures.append(sig)
    
    if len(signatures) >= 2:
        # Agregar
        aggregated = aggregator.aggregate_qrs3_signatures(signatures)
        
        if aggregated.get("success"):
            reduction = aggregated.get("size_reduction", 0)
            test_result("Agregação de Assinaturas", True,
                       f"Redução: {reduction:.1%}, {aggregated['count']} assinaturas")
        else:
            test_result("Agregação de Assinaturas", False, aggregated.get("error"))
    else:
        test_result("Agregação de Assinaturas", False, "Não foi possível gerar assinaturas")
    
except Exception as e:
    test_result("Agregação de Assinaturas", False, f"Erro: {e}")

# ============================================================================
# TESTE 5: NFTs QUÂNTICO-SEGUROS
# ============================================================================

print("=" * 70)
print("🎨 TESTE 5: NFTs QUÂNTICO-SEGUROS")
print("=" * 70)
print()

try:
    from quantum_safe_nfts import QuantumSafeNFTManager
    from quantum_security import QuantumSecuritySystem
    
    blockchain = MockBlockchain()
    qs = QuantumSecuritySystem()
    nft_manager = QuantumSafeNFTManager(blockchain, qs)
    
    # Mint NFT
    result = nft_manager.mint_nft(
        {
            "name": "Quantum Art #1",
            "description": "Primeira arte quântico-segura",
            "image": "ipfs://QmHash..."
        },
        "owner1"
    )
    
    if result.get("success"):
        token_id = result["token_id"]
        nft_info = nft_manager.get_nft(token_id)
        
        test_result("NFTs Quântico-Seguros", nft_info is not None,
                   f"Token ID: {token_id}, Quantum Safe: {nft_info.get('quantum_safe', False)}")
    else:
        test_result("NFTs Quântico-Seguros", False, result.get("error"))
    
except Exception as e:
    test_result("NFTs Quântico-Seguros", False, f"Erro: {e}")

# ============================================================================
# TESTE 6: MULTI-LAYER SECURITY
# ============================================================================

print("=" * 70)
print("🛡️ TESTE 6: MULTI-LAYER SECURITY")
print("=" * 70)
print()

try:
    from multi_layer_security import MultiLayerSecurity
    from quantum_security import QuantumSecuritySystem
    
    qs = QuantumSecuritySystem()
    security = MultiLayerSecurity(qs)
    
    # Validar transação
    tx = {
        "id": "tx1",
        "sender": "addr1",
        "receiver": "addr2",
        "amount": 100,
        "qrs3_signature": {"redundancy_level": 3}
    }
    
    result = security.validate_transaction(tx)
    
    test_result("Multi-Layer Security", result.get("success"),
               f"Camadas passadas: {result.get('layers_passed', 0)}/{result.get('total_layers', 0)}")
    
except Exception as e:
    test_result("Multi-Layer Security", False, f"Erro: {e}")

# ============================================================================
# TESTE 7: DeFi QUÂNTICO-SEGURO
# ============================================================================

print("=" * 70)
print("💰 TESTE 7: DeFi QUÂNTICO-SEGURO")
print("=" * 70)
print()

try:
    from quantum_safe_defi import QuantumSafeDeFi
    from quantum_security import QuantumSecuritySystem
    
    qs = QuantumSecuritySystem()
    defi = QuantumSafeDeFi(qs)
    
    # Criar pool DEX
    pool_result = defi.dex.create_pool("ALZ", "BTC", {"ALZ": 10000, "BTC": 1})
    
    if pool_result.get("success"):
        pool_id = pool_result["pool_id"]
        
        # Realizar swap
        swap_result = defi.dex.swap(pool_id, "ALZ", "BTC", 100)
        
        test_result("DeFi Quântico-Seguro", swap_result.get("success"),
                   f"Pool: {pool_id}, Quantum Safe: {swap_result.get('swap', {}).get('quantum_safe', False)}")
    else:
        test_result("DeFi Quântico-Seguro", False, pool_result.get("error"))
    
except Exception as e:
    test_result("DeFi Quântico-Seguro", False, f"Erro: {e}")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("=" * 70)
print("📊 RESUMO FINAL")
print("=" * 70)
print()

print(f"✅ Testes Passados: {success_count}/{total_tests}")
print(f"📈 Taxa de Sucesso: {(success_count/total_tests*100):.1f}%")
print()

if success_count == total_tests:
    print("🎉 TODAS AS MELHORIAS FUNCIONANDO!")
    print("   • Consenso Adaptativo Avançado")
    print("   • Sharding Dinâmico")
    print("   • State Channels")
    print("   • Agregação de Assinaturas")
    print("   • NFTs Quântico-Seguros")
    print("   • Multi-Layer Security")
    print("   • DeFi Quântico-Seguro")
else:
    print(f"⚠️  {total_tests - success_count} teste(s) falharam")
    print("   Verifique os erros acima")

print()
print("=" * 70)



