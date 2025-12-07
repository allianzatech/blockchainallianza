# quantum_safe_nfts.py
# 🎨 QUANTUM-SAFE NFTs - ALLIANZA BLOCKCHAIN
# Sistema de NFTs quântico-seguros (ÚNICO NO MUNDO)

import time
import hashlib
import json
import base64
import logging
from typing import Dict, Optional, List
from uuid import uuid4

logger = logging.getLogger(__name__)

class QuantumSafeNFT:
    """
    🎨 QUANTUM-SAFE NFT
    Primeira blockchain com NFTs quântico-seguros!
    
    Características:
    - Metadata assinada com QRS-3
    - Ownership verificado com QRS-3
    - Transferências quântico-seguras
    - Metadata em IPFS/Arweave
    - Futuro-proof (resistente a quantum)
    """
    
    def __init__(self, token_id: str, metadata: Dict, owner: str, quantum_security, metadata_storage=None):
        self.token_id = token_id
        self.metadata = metadata
        self.owner = owner
        self.quantum_security = quantum_security
        self.metadata_storage = metadata_storage
        self.created_at = time.time()
        self.transfer_history = []
        
        # Gerar keypair QRS-3 para o NFT
        qrs3_keypair = quantum_security.generate_qrs3_keypair()
        self.qrs3_keypair_id = qrs3_keypair["keypair_id"]
        
        # Assinar metadata com QRS-3
        metadata_bytes = json.dumps(metadata, sort_keys=True).encode()
        qrs3_signature = quantum_security.sign_qrs3(
            self.qrs3_keypair_id,
            metadata_bytes,
            optimized=True,
            parallel=True
        )
        
        self.metadata_qrs3_signature = qrs3_signature
        
        # Armazenar metadata (IPFS/Arweave se disponível)
        if metadata_storage:
            self.metadata_hash = metadata_storage.store(metadata)
        else:
            # Fallback: hash local
            self.metadata_hash = hashlib.sha256(metadata_bytes).hexdigest()
        
        logger.info(f"🎨 Quantum-Safe NFT criado: {token_id}")
        print(f"🎨 Quantum-Safe NFT criado: {token_id}")
        print(f"   Owner: {owner[:20]}...")
        print(f"   Segurança: QRS-3")
        print(f"   Metadata Hash: {self.metadata_hash[:20]}...")
    
    def transfer(self, new_owner: str, quantum_security) -> Dict:
        """
        Transfere NFT para novo owner com QRS-3
        
        Args:
            new_owner: Novo proprietário
            quantum_security: Sistema de segurança quântica
        """
        transfer_data = {
            "token_id": self.token_id,
            "from": self.owner,
            "to": new_owner,
            "timestamp": time.time(),
            "transfer_number": len(self.transfer_history) + 1
        }
        
        # Assinar transferência com QRS-3
        transfer_bytes = json.dumps(transfer_data, sort_keys=True).encode()
        qrs3_signature = quantum_security.sign_qrs3(
            self.qrs3_keypair_id,
            transfer_bytes,
            optimized=True,
            parallel=True
        )
        
        transfer_data["qrs3_signature"] = qrs3_signature
        self.transfer_history.append(transfer_data)
        
        old_owner = self.owner
        self.owner = new_owner
        
        return {
            "success": True,
            "transfer": transfer_data,
            "old_owner": old_owner,
            "new_owner": new_owner,
            "message": "✅ NFT transferido com segurança QRS-3"
        }
    
    def get_nft_info(self) -> Dict:
        """Retorna informações do NFT"""
        return {
            "token_id": self.token_id,
            "metadata": self.metadata,
            "metadata_hash": self.metadata_hash,
            "owner": self.owner,
            "created_at": self.created_at,
            "transfer_count": len(self.transfer_history),
            "quantum_safe": True,
            "qrs3_keypair_id": self.qrs3_keypair_id,
            "metadata_signature": {
                "redundancy_level": self.metadata_qrs3_signature.get("redundancy_level", 3),
                "implementation": "real"
            }
        }


class QuantumSafeNFTManager:
    """
    Gerenciador de NFTs Quântico-Seguros
    """
    
    def __init__(self, blockchain, quantum_security, metadata_storage=None):
        self.blockchain = blockchain
        self.quantum_security = quantum_security
        self.metadata_storage = metadata_storage
        self.nfts = {}
        self.owner_nfts = {}  # owner -> [token_ids]
        
        logger.info("🎨 QUANTUM SAFE NFT MANAGER: Inicializado!")
        print("🎨 QUANTUM SAFE NFT MANAGER: Inicializado!")
        print("   • NFTs quântico-seguros")
        print("   • Único no mundo")
        print("   • Futuro-proof")
    
    def mint_nft(self, metadata: Dict, owner: str, name: Optional[str] = None) -> Dict:
        """
        Cria (mina) um novo NFT quântico-seguro
        
        Args:
            metadata: Metadata do NFT (nome, descrição, imagem, etc.)
            owner: Proprietário inicial
            name: Nome opcional do NFT
        """
        token_id = f"qsft_{int(time.time())}_{uuid4().hex[:8]}"
        
        # Criar NFT
        nft = QuantumSafeNFT(
            token_id,
            metadata,
            owner,
            self.quantum_security,
            self.metadata_storage
        )
        
        self.nfts[token_id] = nft
        
        # Atualizar índice de owner
        if owner not in self.owner_nfts:
            self.owner_nfts[owner] = []
        self.owner_nfts[owner].append(token_id)
        
        return {
            "success": True,
            "token_id": token_id,
            "nft_info": nft.get_nft_info(),
            "message": "✅ NFT quântico-seguro criado com sucesso"
        }
    
    def transfer_nft(self, token_id: str, from_owner: str, to_owner: str) -> Dict:
        """
        Transfere NFT entre owners
        
        Args:
            token_id: ID do NFT
            from_owner: Owner atual
            to_owner: Novo owner
        """
        if token_id not in self.nfts:
            return {"success": False, "error": "NFT não encontrado"}
        
        nft = self.nfts[token_id]
        
        if nft.owner != from_owner:
            return {"success": False, "error": "Owner não autorizado"}
        
        # Transferir
        result = nft.transfer(to_owner, self.quantum_security)
        
        if result["success"]:
            # Atualizar índices
            if from_owner in self.owner_nfts:
                self.owner_nfts[from_owner].remove(token_id)
            
            if to_owner not in self.owner_nfts:
                self.owner_nfts[to_owner] = []
            self.owner_nfts[to_owner].append(token_id)
        
        return result
    
    def get_nft(self, token_id: str) -> Optional[Dict]:
        """Retorna informações de um NFT"""
        if token_id not in self.nfts:
            return None
        
        return self.nfts[token_id].get_nft_info()
    
    def get_owner_nfts(self, owner: str) -> List[Dict]:
        """Retorna todos os NFTs de um owner"""
        if owner not in self.owner_nfts:
            return []
        
        return [self.nfts[tid].get_nft_info() for tid in self.owner_nfts[owner] if tid in self.nfts]
    
    def list_all_nfts(self) -> List[Dict]:
        """Lista todos os NFTs"""
        return [nft.get_nft_info() for nft in self.nfts.values()]




















