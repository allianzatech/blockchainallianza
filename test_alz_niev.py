# test_alz_niev.py
# Testes completos para ALZ-NIEV (5 camadas de interoperabilidade)

import time
from alz_niev_interoperability import (
    ALZNIEV,
    ConsensusType,
    ELNI,
    ZKEF,
    UPNMT,
    MCL,
    AES
)

def test_elni():
    """Teste da Camada 1: ELNI"""
    print("\n" + "="*70)
    print("🔵 TESTE 1: ELNI - Execution-Level Native Interop")
    print("="*70)
    
    elni = ELNI()
    
    result = elni.execute_native_function(
        source_chain="allianza",
        target_chain="polygon",
        function_name="getBalance",
        function_params={"address": "0x1234..."}
    )
    
    assert result.success, "ELNI deve executar com sucesso"
    assert result.return_value is not None, "ELNI deve retornar valor"
    
    print(f"✅ ELNI: Teste passou!")
    print(f"   Result: {result.return_value}")
    print(f"   Time: {result.execution_time_ms:.2f}ms")
    
    return True

def test_zkef():
    """Teste da Camada 2: ZKEF"""
    print("\n" + "="*70)
    print("🟣 TESTE 2: ZKEF - Zero-Knowledge External Functions")
    print("="*70)
    
    elni = ELNI()
    zkef = ZKEF()
    
    # Executar função
    result = elni.execute_native_function(
        source_chain="allianza",
        target_chain="ethereum",
        function_name="transfer",
        function_params={"to": "0x5678...", "amount": 100}
    )
    
    # Gerar prova ZK
    zk_proof = zkef.generate_zk_proof(
        result,
        circuit_id="transfer_circuit",
        verifier_id="ethereum_verifier"
    )
    
    assert zk_proof.proof_type == "zk-snark", "Prova deve ser zk-snark"
    assert len(zk_proof.public_inputs) > 0, "Prova deve ter public inputs"
    assert zk_proof.proof_data is not None, "Prova deve ter dados"
    
    # Verificar prova
    verified = zkef.verify_zk_proof(zk_proof)
    assert verified, "Prova ZK deve ser verificada"
    
    print(f"✅ ZKEF: Teste passou!")
    print(f"   Proof hash: {zk_proof.proof_data[:32]}...")
    print(f"   Verified: {verified}")
    
    return True

def test_upnmt():
    """Teste da Camada 3: UP-NMT"""
    print("\n" + "="*70)
    print("🟢 TESTE 3: UP-NMT - Universal Proof Normalized Merkle Tunneling")
    print("="*70)
    
    upnmt = UPNMT()
    
    # Testar com diferentes blockchains
    chains = ["bitcoin", "ethereum", "solana", "cosmos"]
    
    for chain in chains:
        merkle_proof = upnmt.create_universal_merkle_proof(
            chain_id=chain,
            block_hash=f"block_{chain}_{int(time.time())}",
            transaction_hash=f"tx_{chain}_{int(time.time())}",
            block_height=1000
        )
        
        assert merkle_proof.merkle_root is not None, f"Merkle root deve existir para {chain}"
        assert merkle_proof.leaf_hash is not None, f"Leaf hash deve existir para {chain}"
        assert len(merkle_proof.proof_path) > 0, f"Proof path deve existir para {chain}"
        
        # Verificar prova
        verified = upnmt.verify_universal_merkle_proof(merkle_proof)
        assert verified, f"Prova Merkle deve ser verificada para {chain}"
        
        print(f"   ✅ {chain}: Prova criada e verificada")
    
    print(f"✅ UP-NMT: Teste passou para todas as chains!")
    
    return True

def test_mcl():
    """Teste da Camada 4: MCL"""
    print("\n" + "="*70)
    print("🟡 TESTE 4: MCL - Multi-Consensus Layer")
    print("="*70)
    
    mcl = MCL()
    
    # Testar diferentes tipos de consenso
    consensus_types = [
        (ConsensusType.POW, "bitcoin"),
        (ConsensusType.POS, "ethereum"),
        (ConsensusType.PARALLEL, "solana"),
        (ConsensusType.TENDERMINT, "cosmos")
    ]
    
    for consensus_type, chain_id in consensus_types:
        consensus_proof = mcl.generate_consensus_proof(
            chain_id=chain_id,
            consensus_type=consensus_type,
            block_height=1000,
            block_hash=f"block_{chain_id}"
        )
        
        assert consensus_proof.consensus_type == consensus_type, f"Tipo de consenso deve ser {consensus_type}"
        assert consensus_proof.proof_data is not None, f"Proof data deve existir para {chain_id}"
        
        # Verificar prova
        verified = mcl.verify_consensus_proof(consensus_proof)
        assert verified, f"Prova de consenso deve ser verificada para {chain_id}"
        
        print(f"   ✅ {consensus_type.value} ({chain_id}): Prova criada e verificada")
    
    print(f"✅ MCL: Teste passou para todos os tipos de consenso!")
    
    return True

def test_aes():
    """Teste da Camada 5: AES"""
    print("\n" + "="*70)
    print("🔴 TESTE 5: AES - Atomic Execution Sync")
    print("="*70)
    
    alz_niev = ALZNIEV()
    
    # Executar transação atômica em múltiplas chains
    chains = [
        ("polygon", "transfer", {"to": "0x1234...", "amount": 100}),
        ("ethereum", "mint", {"to": "0x5678...", "amount": 50}),
        ("bsc", "swap", {"token_in": "BNB", "token_out": "USDT", "amount": 10})
    ]
    
    results = alz_niev.execute_atomic_multi_chain(chains)
    
    assert len(results) == len(chains), "Deve ter resultado para cada chain"
    
    all_success = all(r.success for r in results.values())
    assert all_success, "Todas as execuções devem ser bem-sucedidas"
    
    # Verificar que todas têm provas
    for chain, result in results.items():
        assert result.zk_proof is not None, f"{chain} deve ter ZK proof"
        assert result.merkle_proof is not None, f"{chain} deve ter Merkle proof"
        assert result.consensus_proof is not None, f"{chain} deve ter Consensus proof"
        print(f"   ✅ {chain}: Todas as provas presentes")
    
    print(f"✅ AES: Teste passou! Transação atômica executada em {len(chains)} chains")
    
    return True

def test_complete_alz_niev():
    """Teste completo do ALZ-NIEV"""
    print("\n" + "="*70)
    print("🌐 TESTE COMPLETO: ALZ-NIEV (Todas as 5 Camadas)")
    print("="*70)
    
    alz_niev = ALZNIEV()
    
    result = alz_niev.execute_cross_chain_with_proofs(
        source_chain="allianza",
        target_chain="polygon",
        function_name="executeContract",
        function_params={
            "contract": "0xABC123...",
            "function": "transfer",
            "params": {"to": "0xDEF456...", "amount": 1000}
        }
    )
    
    assert result.success, "Execução deve ser bem-sucedida"
    assert result.zk_proof is not None, "Deve ter ZK proof"
    assert result.merkle_proof is not None, "Deve ter Merkle proof"
    assert result.consensus_proof is not None, "Deve ter Consensus proof"
    
    print(f"\n✅ ALZ-NIEV Completo: Teste passou!")
    print(f"   ZK Proof: {result.zk_proof.proof_data[:32]}...")
    print(f"   Merkle Root: {result.merkle_proof.merkle_root[:32]}...")
    print(f"   Consensus: {result.consensus_proof.consensus_type.value}")
    print(f"   Execution Time: {result.execution_time_ms:.2f}ms")
    
    return True

def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("🧪 EXECUTANDO TODOS OS TESTES ALZ-NIEV")
    print("="*70)
    
    tests = [
        ("ELNI", test_elni),
        ("ZKEF", test_zkef),
        ("UP-NMT", test_upnmt),
        ("MCL", test_mcl),
        ("AES", test_aes),
        ("ALZ-NIEV Completo", test_complete_alz_niev)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            start_time = time.time()
            success = test_func()
            elapsed = (time.time() - start_time) * 1000
            results[test_name] = {"success": success, "time_ms": elapsed}
        except Exception as e:
            results[test_name] = {"success": False, "error": str(e)}
            print(f"❌ {test_name}: Falhou - {e}")
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for r in results.values() if r.get("success"))
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result.get("success") else "❌ FALHOU"
        time_str = f"({result.get('time_ms', 0):.2f}ms)" if result.get("success") else ""
        error_str = f" - {result.get('error')}" if not result.get("success") else ""
        print(f"{status} {test_name} {time_str}{error_str}")
    
    print(f"\n📈 Taxa de Sucesso: {passed}/{total} ({passed*100/total:.1f}%)")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)








