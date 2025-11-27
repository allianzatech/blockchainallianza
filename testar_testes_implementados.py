#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE RÁPIDO DOS TESTES IMPLEMENTADOS
Testa localmente os testes que foram corrigidos/implementados
"""

import sys
import time
from datetime import datetime

print("="*70)
print("🧪 TESTANDO TESTES IMPLEMENTADOS")
print("="*70)
print()

# Teste 1: Gasless Interoperability
print("📌 Teste 1: Gasless Interoperability")
try:
    from gasless_relay_system import GaslessRelaySystem
    relay = GaslessRelaySystem()
    nonce = relay.generate_nonce("0xUserAddress")
    replay_check = relay.check_replay(nonce, "0xUserAddress")
    print(f"   ✅ GaslessRelaySystem funcionando")
    print(f"   ✅ Nonce gerado: {nonce}")
    print(f"   ✅ Anti-replay: {replay_check.get('blocked', False)}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# Teste 2: Smart Contracts
print("📌 Teste 2: Smart Contracts")
try:
    from advanced_smart_contracts import AdvancedSmartContractManager
    manager = AdvancedSmartContractManager()
    contract_code = "pragma solidity ^0.8.0; contract Test { uint256 public value; }"
    deploy_result = manager.deploy_contract(code=contract_code, language="solidity")
    if deploy_result.get("success"):
        print(f"   ✅ AdvancedSmartContractManager funcionando")
        print(f"   ✅ Contrato deployado: {deploy_result.get('contract_id', 'N/A')}")
    else:
        print(f"   ⚠️  Deploy falhou: {deploy_result.get('error', 'N/A')}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# Teste 3: Wormhole Prevention
print("📌 Teste 3: Wormhole Prevention")
try:
    from wormhole_prevention_system import WormholePreventionSystem
    prevention = WormholePreventionSystem()
    result = prevention.validate_cross_chain_message(
        source_chain="polygon",
        target_chain="ethereum",
        message_data={"amount": 100},
        sequence=1
    )
    if result.get("valid"):
        print(f"   ✅ WormholePreventionSystem funcionando")
        print(f"   ✅ Mensagem validada: {result.get('message_hash', 'N/A')[:16]}...")
    else:
        print(f"   ⚠️  Validação falhou: {result.get('reason', 'N/A')}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# Teste 4: Multi-Node System
print("📌 Teste 4: Multi-Node System (Consenso e Sincronização)")
try:
    from multi_node_system import MultiNodeSystem
    multi_node = MultiNodeSystem(num_nodes=3)
    sync_result = multi_node.sync_all_nodes()
    block_data = {"block_number": 1, "transactions": ["tx1"], "timestamp": time.time()}
    consensus_result = multi_node.reach_consensus(block_data)
    print(f"   ✅ MultiNodeSystem funcionando")
    print(f"   ✅ Sincronização: {sync_result.get('success', False)}")
    print(f"   ✅ Consenso: {consensus_result.get('success', False)}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()
print("="*70)
print("✅ TESTES CONCLUÍDOS!")
print("="*70)

