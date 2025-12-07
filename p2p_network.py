#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2P Network Layer para Allianza Blockchain
Preparado para integração com Substrate ou implementação custom
"""

import asyncio
import json
import time
import hashlib
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class NodeType(Enum):
    """Tipos de nós na rede"""
    VALIDATOR = "validator"
    FULL_NODE = "full_node"
    LIGHT_NODE = "light_node"
    RPC_NODE = "rpc_node"

@dataclass
class Peer:
    """Representa um peer na rede"""
    node_id: str
    address: str
    port: int
    node_type: NodeType
    last_seen: float
    is_connected: bool = False
    version: str = "1.0.0"

class P2PNetwork:
    """
    Camada P2P para Allianza Blockchain
    Preparada para integração com Substrate ou implementação custom
    """
    
    def __init__(self, node_id: str, node_type: NodeType = NodeType.FULL_NODE):
        self.node_id = node_id
        self.node_type = node_type
        self.peers: Dict[str, Peer] = {}
        self.bootstrap_nodes: List[str] = []
        self.is_running = False
        self.message_queue = asyncio.Queue()
        self.blockchain_state = {}
        
        logger.info(f"🌐 P2P Network inicializado: {node_id} ({node_type.value})")
    
    def add_bootstrap_node(self, address: str, port: int):
        """Adiciona nó bootstrap para conectar na rede"""
        node_id = f"{address}:{port}"
        self.bootstrap_nodes.append(node_id)
        logger.info(f"📡 Bootstrap node adicionado: {node_id}")
    
    def add_peer(self, peer: Peer):
        """Adiciona peer à rede"""
        self.peers[peer.node_id] = peer
        logger.info(f"👥 Peer adicionado: {peer.node_id} ({peer.node_type.value})")
    
    def remove_peer(self, node_id: str):
        """Remove peer da rede"""
        if node_id in self.peers:
            del self.peers[node_id]
            logger.info(f"❌ Peer removido: {node_id}")
    
    def get_connected_peers(self) -> List[Peer]:
        """Retorna lista de peers conectados"""
        return [peer for peer in self.peers.values() if peer.is_connected]
    
    async def broadcast_message(self, message_type: str, data: Dict):
        """Broadcast mensagem para todos os peers"""
        message = {
            "type": message_type,
            "data": data,
            "sender": self.node_id,
            "timestamp": time.time()
        }
        
        # Em produção, isso enviaria via protocolo P2P real
        # Por agora, simula broadcast
        connected_peers = self.get_connected_peers()
        logger.info(f"📢 Broadcast: {message_type} para {len(connected_peers)} peers")
        
        return {
            "success": True,
            "peers_reached": len(connected_peers),
            "message": message
        }
    
    async def receive_message(self, message: Dict):
        """Processa mensagem recebida"""
        message_type = message.get("type")
        data = message.get("data", {})
        sender = message.get("sender")
        
        logger.info(f"📨 Mensagem recebida: {message_type} de {sender}")
        
        # Processar diferentes tipos de mensagem
        if message_type == "block":
            return await self._handle_block(data)
        elif message_type == "transaction":
            return await self._handle_transaction(data)
        elif message_type == "peer_discovery":
            return await self._handle_peer_discovery(data)
        elif message_type == "sync_request":
            return await self._handle_sync_request(data)
        
        return {"success": False, "error": "Tipo de mensagem desconhecido"}
    
    async def _handle_block(self, block_data: Dict):
        """Processa novo bloco recebido"""
        # Em produção, validaria e adicionaria ao blockchain
        logger.info(f"📦 Bloco recebido: {block_data.get('hash', 'unknown')}")
        return {"success": True, "message": "Bloco processado"}
    
    async def _handle_transaction(self, tx_data: Dict):
        """Processa nova transação recebida"""
        # Em produção, validaria e adicionaria ao pool
        logger.info(f"💸 Transação recebida: {tx_data.get('hash', 'unknown')}")
        return {"success": True, "message": "Transação processada"}
    
    async def _handle_peer_discovery(self, peer_data: Dict):
        """Processa descoberta de novo peer"""
        # Em produção, adicionaria peer à rede
        logger.info(f"🔍 Peer descoberto: {peer_data.get('node_id', 'unknown')}")
        return {"success": True, "message": "Peer adicionado"}
    
    async def _handle_sync_request(self, sync_data: Dict):
        """Processa requisição de sincronização"""
        # Em produção, enviaria blocos faltantes
        logger.info(f"🔄 Sync request: {sync_data.get('from_block', 'unknown')}")
        return {"success": True, "message": "Sync iniciado"}
    
    def get_network_info(self) -> Dict:
        """Retorna informações da rede"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "total_peers": len(self.peers),
            "connected_peers": len(self.get_connected_peers()),
            "bootstrap_nodes": len(self.bootstrap_nodes),
            "is_running": self.is_running
        }

# Instância global (será inicializada quando necessário)
global_p2p_network: Optional[P2PNetwork] = None

def initialize_p2p_network(node_id: str, node_type: NodeType = NodeType.FULL_NODE) -> P2PNetwork:
    """Inicializa rede P2P global"""
    global global_p2p_network
    global_p2p_network = P2PNetwork(node_id, node_type)
    return global_p2p_network

def get_p2p_network() -> Optional[P2PNetwork]:
    """Retorna instância global da rede P2P"""
    return global_p2p_network



















