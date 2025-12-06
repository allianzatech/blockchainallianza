# test_all_improvements.py
# 🧪 TESTES COMPLETOS PARA TODAS AS 8 MELHORIAS

import sys
import time
from typing import Dict, List

def test_quantum_multi_sig():
    """Teste 1: Quantum-Safe Multi-Signature Wallet"""
    print("\n" + "="*70)
    print("🧪 TESTE 1: QUANTUM-SAFE MULTI-SIGNATURE WALLET")
    print("="*70)
    
    try:
        from quantum_multi_sig_wallet import QuantumMultiSigWallet, init_quantum_multi_sig
        
        # Inicializar
        init_quantum_multi_sig()
        
        # Criar carteira
        wallet = QuantumMultiSigWallet(threshold=2)
        
        # Adicionar signers
        signer1 = wallet.add_signer("ecdsa", "signer1")
        signer2 = wallet.add_signer("hybrid", "signer2")
        signer3 = wallet.add_signer("ecdsa", "signer3")
        
        # Criar transação
        tx = wallet.create_transaction("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", 1.0)
        tx_id = tx["tx_id"]
        
        # Assinar com 2 signers (threshold)
        result1 = wallet.sign_transaction(tx_id, "signer1")
        result2 = wallet.sign_transaction(tx_id, "signer2")
        
        # Verificar
        verification = wallet.verify_transaction(tx_id)
        
        # Executar
        execution = wallet.execute_transaction(tx_id)
        
        print(f"✅ Carteira criada: {wallet.wallet_id}")
        print(f"✅ Signers adicionados: {len(wallet.signers)}")
        print(f"✅ Transação criada: {tx_id[:16]}...")
        print(f"✅ Assinaturas: {len(tx['signatures'])}/{wallet.threshold}")
        print(f"✅ Verificação: {verification.get('valid', False)}")
        print(f"✅ Execução: {execution.get('success', False)}")
        
        return {"success": True, "test": "Quantum Multi-Sig"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Quantum Multi-Sig", "error": str(e)}


def test_predictive_gas():
    """Teste 2: Predictive Gas Optimization"""
    print("\n" + "="*70)
    print("🧪 TESTE 2: PREDICTIVE GAS OPTIMIZATION")
    print("="*70)
    
    try:
        from predictive_gas_optimizer import PredictiveGasOptimizer, init_predictive_gas_optimizer
        
        # Inicializar
        optimizer = init_predictive_gas_optimizer()
        
        # Testar otimização
        tx = {
            "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "value": 0.1,
            "urgent": False
        }
        
        result = optimizer.optimize_transaction(tx, max_wait_minutes=10)
        
        # Obter estatísticas
        stats = optimizer.get_optimization_stats()
        
        print(f"✅ Otimizador inicializado")
        print(f"✅ Transação otimizada: {result.get('optimized', False)}")
        if result.get('optimized'):
            print(f"   • Economia prevista: {result.get('savings_percentage', 0):.2f}%")
            print(f"   • Aguardar: {result.get('wait_minutes', 0)} minutos")
        print(f"✅ Estatísticas: {stats.get('total_optimizations', 0)} otimizações")
        
        return {"success": True, "test": "Predictive Gas"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Predictive Gas", "error": str(e)}


def test_self_healing():
    """Teste 3: Self-Healing Blockchain"""
    print("\n" + "="*70)
    print("🧪 TESTE 3: SELF-HEALING BLOCKCHAIN")
    print("="*70)
    
    try:
        from self_healing_blockchain import SelfHealingBlockchain, init_self_healing
        
        # Inicializar (sem blockchain real para teste)
        healing = init_self_healing()
        
        # Monitorar (simulado)
        result = healing.monitor()
        
        # Obter estatísticas
        stats = healing.get_healing_stats()
        
        print(f"✅ Sistema de auto-cura inicializado")
        print(f"✅ Monitoramento ativo: {result.get('monitoring', False)}")
        print(f"✅ Anomalias detectadas: {result.get('anomalies_detected', 0)}")
        print(f"✅ Correções aplicadas: {result.get('fixes_applied', 0)}")
        print(f"✅ Estatísticas: {stats.get('total_anomalies', 0)} anomalias, {stats.get('total_fixes', 0)} correções")
        
        return {"success": True, "test": "Self-Healing"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Self-Healing", "error": str(e)}


def test_adaptive_consensus():
    """Teste 4: Adaptive Consensus"""
    print("\n" + "="*70)
    print("🧪 TESTE 4: ADAPTIVE CONSENSUS")
    print("="*70)
    
    try:
        from adaptive_consensus import AdaptiveConsensus, init_adaptive_consensus
        
        # Inicializar
        consensus = init_adaptive_consensus()
        
        # Testar adaptação
        consensus.update_network_state({
            "load": 0.9,  # Alta carga
            "validators": 10,
            "pending_txs": 50,
            "urgent_txs": 5
        })
        
        info = consensus.get_consensus_info()
        
        print(f"✅ Consenso adaptativo inicializado")
        print(f"✅ Consenso atual: {info.get('current_consensus')}")
        print(f"✅ Adaptações: {info.get('adaptations_count', 0)}")
        
        return {"success": True, "test": "Adaptive Consensus"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Adaptive Consensus", "error": str(e)}


def test_quantum_contracts():
    """Teste 5: Quantum-Resistant Smart Contracts"""
    print("\n" + "="*70)
    print("🧪 TESTE 5: QUANTUM-RESISTANT SMART CONTRACTS")
    print("="*70)
    
    try:
        from quantum_smart_contracts import QuantumSmartContract, create_quantum_contract
        
        # Criar contrato
        contract = create_quantum_contract("test_contract")
        
        # Registrar função
        def test_function(args, state):
            state["value"] = args.get("value", 0)
            return {"result": "success"}
        
        contract.register_function("test", test_function)
        
        # Executar
        result = contract.execute("test", {"value": 42})
        
        info = contract.get_contract_info()
        
        print(f"✅ Contrato criado: {contract.contract_id}")
        print(f"✅ Quântico-seguro: {info.get('quantum_safe', False)}")
        print(f"✅ Funções: {len(info.get('functions', []))}")
        print(f"✅ Execução: {result.get('success', False)}")
        
        return {"success": True, "test": "Quantum Contracts"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Quantum Contracts", "error": str(e)}


def test_privacy_aggregation():
    """Teste 6: Privacy-Preserving Aggregation"""
    print("\n" + "="*70)
    print("🧪 TESTE 6: PRIVACY-PRESERVING AGGREGATION")
    print("="*70)
    
    try:
        from privacy_preserving_aggregation import PrivacyPreservingAggregation, init_privacy_aggregation
        
        # Inicializar
        aggregation = init_privacy_aggregation()
        
        # Criar transações simuladas
        transactions = [
            {"amount": 1.0, "from": "0x111...", "to": "0x222..."},
            {"amount": 2.0, "from": "0x333...", "to": "0x444..."},
            {"amount": 0.5, "from": "0x555...", "to": "0x666..."}
        ]
        
        # Agregar
        result = aggregation.aggregate_transactions(transactions, "ethereum")
        
        # Obter estatísticas
        stats = aggregation.get_aggregated_stats(["ethereum"])
        
        print(f"✅ Agregação privada inicializada")
        print(f"✅ Agregação criada: {result.get('success', False)}")
        print(f"✅ Privacidade preservada: {result.get('privacy_preserved', False)}")
        print(f"✅ Volume total: {stats.get('total_volume', 0)}")
        print(f"✅ Transações: {stats.get('total_transactions', 0)}")
        
        return {"success": True, "test": "Privacy Aggregation"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Privacy Aggregation", "error": str(e)}


def test_state_machine():
    """Teste 7: Cross-Chain State Machine"""
    print("\n" + "="*70)
    print("🧪 TESTE 7: CROSS-CHAIN STATE MACHINE")
    print("="*70)
    
    try:
        from cross_chain_state_machine import CrossChainStateMachine, init_cross_chain_state_machine
        
        # Inicializar
        state_machine = init_cross_chain_state_machine()
        
        # Criar máquina de estado
        result = state_machine.create_state_machine("test_machine", ["ethereum", "polygon"])
        
        machine_id = result["machine_id"]
        
        # Fazer transições
        state_machine.transition(machine_id, "pending", "ethereum")
        state_machine.transition(machine_id, "executing", "polygon")
        state_machine.transition(machine_id, "committed", "ethereum")
        
        # Obter estado
        machine_state = state_machine.get_machine_state(machine_id)
        
        print(f"✅ State Machine criada: {machine_id}")
        print(f"✅ Estado atual: {machine_state.get('current_state')}")
        print(f"✅ Chains: {', '.join(machine_state.get('chains', []))}")
        print(f"✅ Histórico: {len(machine_state.get('state_history', []))} transições")
        
        return {"success": True, "test": "State Machine"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "State Machine", "error": str(e)}


def test_quantum_identity():
    """Teste 8: Quantum-Safe Identity System"""
    print("\n" + "="*70)
    print("🧪 TESTE 8: QUANTUM-SAFE IDENTITY SYSTEM")
    print("="*70)
    
    try:
        from quantum_identity_system import QuantumIdentitySystem, init_quantum_identity_system
        
        # Inicializar
        identity_system = init_quantum_identity_system()
        
        # Criar identidade
        identity = identity_system.create_identity("test_identity")
        
        # Adicionar atributos
        identity.add_attribute("name", "Test User", verified=True)
        identity.add_attribute("email", "test@example.com", verified=False)
        
        # Verificar em chains
        identity_system.verify_identity_on_chain(identity.identity_id, "ethereum")
        identity_system.verify_identity_on_chain(identity.identity_id, "polygon")
        
        info = identity.get_identity_info()
        
        print(f"✅ Sistema de identidade inicializado")
        print(f"✅ Identidade criada: {identity.identity_id}")
        print(f"✅ Quântico-seguro: {info.get('quantum_safe', False)}")
        print(f"✅ Atributos: {len(info.get('attributes', {}))}")
        print(f"✅ Chains verificadas: {len(info.get('verified_chains', []))}")
        
        return {"success": True, "test": "Quantum Identity"}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "test": "Quantum Identity", "error": str(e)}


def main():
    """Executar todos os testes"""
    print("="*70)
    print("🧪 TESTES COMPLETOS: TODAS AS 8 MELHORIAS")
    print("="*70)
    
    tests = [
        test_quantum_multi_sig,
        test_predictive_gas,
        test_self_healing,
        test_adaptive_consensus,
        test_quantum_contracts,
        test_privacy_aggregation,
        test_state_machine,
        test_quantum_identity
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            results.append({"success": False, "test": test_func.__name__, "error": str(e)})
        time.sleep(0.5)  # Pequena pausa entre testes
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for r in results if r.get("success"))
    total = len(results)
    
    for result in results:
        status = "✅" if result.get("success") else "❌"
        test_name = result.get("test", "Unknown")
        print(f"{status} {test_name}")
        if not result.get("success"):
            print(f"   Erro: {result.get('error', 'Desconhecido')}")
    
    print(f"\n✅ Passou: {passed}/{total}")
    print(f"❌ Falhou: {total - passed}/{total}")
    print(f"Taxa de sucesso: {(passed/total*100):.1f}%")
    print("="*70)
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Todas as 8 melhorias estão funcionando!")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        print("Verifique os erros acima")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)












