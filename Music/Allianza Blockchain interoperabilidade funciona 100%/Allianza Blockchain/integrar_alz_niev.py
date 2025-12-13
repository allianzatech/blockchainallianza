# integrar_alz_niev.py
# Script para integrar ALZ-NIEV ao sistema de testnet existente

import time
from typing import Dict, List, Tuple, Any
from alz_niev_interoperability import alz_niev, ALZNIEV
from testnet_interoperability import TestnetInteroperability

class TestnetInteroperabilityALZNIEV(TestnetInteroperability):
    """
    Extensão do TestnetInteroperability com ALZ-NIEV
    """
    
    def __init__(self, blockchain_instance):
        super().__init__(blockchain_instance)
        self.alz_niev = ALZNIEV()
        print("🌐 ALZ-NIEV integrado ao Testnet Interoperability!")
    
    def test_alz_niev_execution(
        self,
        source_chain: str,
        target_chain: str,
        function_name: str,
        function_params: Dict[str, Any]
    ) -> Dict:
        """
        Teste de execução ALZ-NIEV com todas as 5 camadas
        """
        test_id = f"alz_niev_{int(time.time())}"
        
        try:
            print(f"\n{'='*70}")
            print(f"🌐 TESTE ALZ-NIEV: {source_chain} → {target_chain}")
            print(f"{'='*70}")
            
            # Executar com todas as provas
            result = self.alz_niev.execute_cross_chain_with_proofs(
                source_chain=source_chain,
                target_chain=target_chain,
                function_name=function_name,
                function_params=function_params
            )
            
            # Preparar resultado para o testnet
            return {
                "success": result.success,
                "test_id": test_id,
                "test_name": "ALZ-NIEV Execution",
                "results": {
                    "source_chain": source_chain,
                    "target_chain": target_chain,
                    "function_name": function_name,
                    "function_params": function_params,
                    "return_value": result.return_value,
                    "execution_time_ms": result.execution_time_ms,
                    "has_zk_proof": result.zk_proof is not None,
                    "has_merkle_proof": result.merkle_proof is not None,
                    "has_consensus_proof": result.consensus_proof is not None
                },
                "proofs": {
                    "zk_proof": {
                        "proof_type": result.zk_proof.proof_type if result.zk_proof else None,
                        "verifier_id": result.zk_proof.verifier_id if result.zk_proof else None,
                        "circuit_id": result.zk_proof.circuit_id if result.zk_proof else None,
                        "proof_hash": result.zk_proof.proof_data[:32] + "..." if result.zk_proof else None
                    },
                    "merkle_proof": {
                        "merkle_root": result.merkle_proof.merkle_root[:32] + "..." if result.merkle_proof else None,
                        "chain_id": result.merkle_proof.chain_id if result.merkle_proof else None,
                        "tree_depth": result.merkle_proof.tree_depth if result.merkle_proof else None
                    },
                    "consensus_proof": {
                        "consensus_type": result.consensus_proof.consensus_type.value if result.consensus_proof else None,
                        "block_height": result.consensus_proof.block_height if result.consensus_proof else None
                    }
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_id": test_id,
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
            }
    
    def test_alz_niev_atomic(
        self,
        chains: List[Tuple[str, str, Dict[str, Any]]]
    ) -> Dict:
        """
        Teste de execução atômica multi-chain ALZ-NIEV
        """
        test_id = f"alz_niev_atomic_{int(time.time())}"
        
        try:
            print(f"\n{'='*70}")
            print(f"🔴 TESTE ALZ-NIEV ATOMIC: {len(chains)} chains")
            print(f"{'='*70}")
            
            # Executar atomicamente
            results = self.alz_niev.execute_atomic_multi_chain(chains)
            
            # Preparar resultado
            all_success = all(r.success for r in results.values())
            
            return {
                "success": all_success,
                "test_id": test_id,
                "test_name": "ALZ-NIEV Atomic Execution",
                "results": {
                    "chains": [chain for chain, _, _ in chains],
                    "all_success": all_success,
                    "execution_count": len(results),
                    "success_count": sum(1 for r in results.values() if r.success)
                },
                "chain_results": {
                    chain: {
                        "success": result.success,
                        "has_zk_proof": result.zk_proof is not None,
                        "has_merkle_proof": result.merkle_proof is not None,
                        "has_consensus_proof": result.consensus_proof is not None,
                        "execution_time_ms": result.execution_time_ms
                    }
                    for chain, result in results.items()
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_id": test_id,
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
            }

