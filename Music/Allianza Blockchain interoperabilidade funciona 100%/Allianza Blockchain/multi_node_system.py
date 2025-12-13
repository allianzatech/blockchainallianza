#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 MULTI-NODE SYSTEM - ALLIANZA BLOCKCHAIN
Sistema completo de múltiplos nós com sincronização e consenso
"""

import time
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading


class Node:
    """Representa um nó da rede"""
    
    def __init__(self, node_id: str, address: str = None):
        self.node_id = node_id
        self.address = address or f"node_{node_id}"
        self.status = "online"
        self.block_height = 0
        self.peers = []
        self.synced = False
        self.last_sync_time = time.time()
        self.validator = False
        self.stake = 0.0
        
        print(f"🌐 Nó {node_id} inicializado")
    
    def update_block_height(self, height: int):
        """Atualizar altura do bloco"""
        self.block_height = height
        self.last_sync_time = time.time()
    
    def add_peer(self, peer_id: str):
        """Adicionar peer"""
        if peer_id not in self.peers:
            self.peers.append(peer_id)
    
    def sync_with_peers(self, peers: List['Node']) -> Dict:
        """Sincronizar com peers"""
        try:
            if not peers:
                return {
                    "success": False,
                    "error": "Nenhum peer disponível"
                }
            
            # Encontrar maior altura entre peers
            max_height = max(peer.block_height for peer in peers)
            
            # Sincronizar se necessário
            if self.block_height < max_height:
                self.block_height = max_height
                self.synced = True
                self.last_sync_time = time.time()
                return {
                    "success": True,
                    "synced": True,
                    "old_height": self.block_height,
                    "new_height": max_height,
                    "peers_synced": len(peers)
                }
            else:
                return {
                    "success": True,
                    "synced": True,
                    "height": self.block_height,
                    "already_synced": True
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_status(self) -> Dict:
        """Obter status do nó"""
        return {
            "node_id": self.node_id,
            "address": self.address,
            "status": self.status,
            "block_height": self.block_height,
            "peers_count": len(self.peers),
            "synced": self.synced,
            "last_sync_time": self.last_sync_time,
            "validator": self.validator,
            "stake": self.stake
        }


class MultiNodeSystem:
    """
    Sistema de Múltiplos Nós
    
    Funcionalidades:
    - Gerenciamento de múltiplos nós
    - Sincronização entre nós
    - Consenso entre nós
    - Validação de blocos
    """
    
    def __init__(self, num_nodes: int = 3):
        """
        Inicializar sistema de múltiplos nós
        
        Args:
            num_nodes: Número de nós a criar
        """
        self.nodes = {}
        self.consensus_rounds = {}
        self.blockchain_state = {
            "latest_block_height": 0,
            "latest_block_hash": None,
            "consensus_reached": False
        }
        
        # Criar nós
        for i in range(num_nodes):
            node_id = f"node_{i}"
            node = Node(node_id)
            self.nodes[node_id] = node
        
        # Conectar nós como peers
        for node_id, node in self.nodes.items():
            for peer_id, peer in self.nodes.items():
                if node_id != peer_id:
                    node.add_peer(peer_id)
        
        print(f"🌐 MULTI-NODE SYSTEM: Inicializado com {num_nodes} nós!")
        print(f"   • Sincronização automática")
        print(f"   • Consenso entre nós")
        print(f"   • Validação de blocos")
    
    def sync_all_nodes(self) -> Dict:
        """
        Sincronizar todos os nós
        
        Returns:
            Dict com resultado da sincronização
        """
        try:
            nodes_list = list(self.nodes.values())
            sync_results = []
            
            for node in nodes_list:
                # Sincronizar com todos os outros nós
                peers = [n for n in nodes_list if n.node_id != node.node_id]
                result = node.sync_with_peers(peers)
                sync_results.append({
                    "node_id": node.node_id,
                    "result": result
                })
            
            # Verificar se todos estão sincronizados
            all_synced = all(
                r["result"].get("synced", False) for r in sync_results
            )
            
            # Atualizar altura do bloco
            if all_synced:
                max_height = max(node.block_height for node in nodes_list)
                self.blockchain_state["latest_block_height"] = max_height
            
            return {
                "success": all_synced,
                "all_synced": all_synced,
                "sync_results": sync_results,
                "latest_block_height": self.blockchain_state["latest_block_height"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def reach_consensus(self, block_data: Dict) -> Dict:
        """
        Alcançar consenso sobre um bloco
        
        Args:
            block_data: Dados do bloco
        
        Returns:
            Dict com resultado do consenso
        """
        try:
            round_id = f"consensus_{int(time.time())}"
            
            # Cada nó vota no bloco
            votes = {}
            for node_id, node in self.nodes.items():
                # Simular voto (em produção seria assinado com QRS-3)
                vote = {
                    "node_id": node_id,
                    "vote": "approve",
                    "block_hash": hashlib.sha256(
                        json.dumps(block_data, sort_keys=True).encode()
                    ).hexdigest(),
                    "timestamp": time.time()
                }
                votes[node_id] = vote
            
            # Verificar se maioria aprova (2/3)
            approve_count = sum(1 for v in votes.values() if v["vote"] == "approve")
            total_nodes = len(self.nodes)
            threshold = (total_nodes * 2) // 3 + 1
            
            consensus_reached = approve_count >= threshold
            
            consensus_data = {
                "round_id": round_id,
                "block_data": block_data,
                "votes": votes,
                "approve_count": approve_count,
                "total_nodes": total_nodes,
                "threshold": threshold,
                "consensus_reached": consensus_reached,
                "timestamp": datetime.now().isoformat()
            }
            
            self.consensus_rounds[round_id] = consensus_data
            
            if consensus_reached:
                # Atualizar estado da blockchain
                self.blockchain_state["latest_block_height"] += 1
                self.blockchain_state["latest_block_hash"] = votes[list(votes.keys())[0]]["block_hash"]
                self.blockchain_state["consensus_reached"] = True
                
                # Atualizar altura de todos os nós
                for node in self.nodes.values():
                    node.update_block_height(self.blockchain_state["latest_block_height"])
            
            return {
                "success": consensus_reached,
                "consensus_data": consensus_data,
                "blockchain_state": self.blockchain_state.copy()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_nodes_status(self) -> Dict:
        """Obter status de todos os nós"""
        nodes_status = {}
        for node_id, node in self.nodes.items():
            nodes_status[node_id] = node.get_status()
        
        return {
            "nodes": nodes_status,
            "total_nodes": len(self.nodes),
            "blockchain_state": self.blockchain_state.copy(),
            "timestamp": datetime.now().isoformat()
        }
    
    def test_sync_and_consensus(self) -> Dict:
        """Testar sincronização e consenso"""
        results = {
            "test_id": "multi_node_sync_consensus",
            "start_time": datetime.now().isoformat(),
            "tests": {}
        }
        
        # Teste 1: Sincronização
        print("📌 Testando sincronização...")
        sync_result = self.sync_all_nodes()
        results["tests"]["sync"] = sync_result
        
        # Teste 2: Consenso
        print("📌 Testando consenso...")
        block_data = {
            "block_number": 1,
            "transactions": ["tx1", "tx2"],
            "timestamp": time.time()
        }
        consensus_result = self.reach_consensus(block_data)
        results["tests"]["consensus"] = consensus_result
        
        # Teste 3: Status de todos os nós
        print("📌 Obtendo status de todos os nós...")
        status_result = self.get_all_nodes_status()
        results["tests"]["status"] = status_result
        
        results["end_time"] = datetime.now().isoformat()
        results["success"] = (
            sync_result.get("success", False) and
            consensus_result.get("success", False)
        )
        
        return results


# =============================================================================
# EXECUÇÃO DIRETA
# =============================================================================

if __name__ == "__main__":
    # Teste básico
    print("🌐 Testando Multi-Node System...")
    
    system = MultiNodeSystem(num_nodes=5)
    
    # Testar sincronização e consenso
    results = system.test_sync_and_consensus()
    
    print(f"\n✅ Teste concluído: {'SUCESSO' if results['success'] else 'FALHOU'}")
    print(f"   Sincronização: {results['tests']['sync'].get('success', False)}")
    print(f"   Consenso: {results['tests']['consensus'].get('success', False)}")
    
    # Salvar resultados
    with open("multi_node_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Resultados salvos em: multi_node_test_results.json")

