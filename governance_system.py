#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ GOVERNANCE SYSTEM - ALLIANZA BLOCKCHAIN
Sistema completo de Governança DAO com PQC
"""

import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

class ProposalStatus(Enum):
    """Status de proposta"""
    DRAFT = "draft"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    CANCELLED = "cancelled"

class VoteType(Enum):
    """Tipo de voto"""
    YES = "yes"
    NO = "no"
    ABSTAIN = "abstain"

@dataclass
class Proposal:
    """Proposta de governança"""
    proposal_id: str
    proposer: str
    title: str
    description: str
    action: Dict
    deposit: float  # ALZ depositado
    voting_period: int  # segundos
    quorum: float  # porcentagem do supply
    threshold: float  # porcentagem de aprovação
    created_at: float
    start_time: float
    end_time: float
    status: str
    yes_votes: float = 0.0
    no_votes: float = 0.0
    abstain_votes: float = 0.0
    total_votes: float = 0.0
    quantum_signature: Optional[Dict] = None

@dataclass
class Vote:
    """Voto em proposta"""
    proposal_id: str
    voter: str
    vote_type: str
    amount: float  # ALZ usado para votar
    timestamp: float
    quantum_signature: Optional[Dict] = None

class GovernanceSystem:
    """
    Sistema de Governança DAO para Allianza Blockchain
    
    Características:
    - Propostas on-chain
    - Votação com ALZ tokens
    - Execução automática
    - Assinaturas quânticas
    """
    
    def __init__(
        self,
        tokenomics_system,
        quantum_security=None,
        total_supply: float = 1_000_000_000,
        min_proposal_deposit: float = 100.0,
        default_voting_period: int = 604800,  # 7 dias
        default_quorum: float = 0.05,  # 5% do supply
        default_threshold: float = 0.5  # 50% de aprovação
    ):
        self.tokenomics = tokenomics_system
        self.quantum_security = quantum_security
        self.total_supply = total_supply
        
        # Configurações
        self.min_proposal_deposit = min_proposal_deposit
        self.default_voting_period = default_voting_period
        self.default_quorum = default_quorum
        self.default_threshold = default_threshold
        
        # Armazenamento
        self.proposals: Dict[str, Proposal] = {}
        self.votes: Dict[str, List[Vote]] = defaultdict(list)
        self.executed_proposals = []
        
        print("🏛️  GOVERNANCE SYSTEM: Inicializado!")
        print(f"   Quorum padrão: {default_quorum*100:.1f}%")
        print(f"   Threshold padrão: {default_threshold*100:.1f}%")
        print(f"   Período de votação: {default_voting_period/86400:.0f} dias")
    
    def create_proposal(
        self,
        proposer: str,
        title: str,
        description: str,
        action: Dict,
        deposit: float,
        voting_period: Optional[int] = None,
        quorum: Optional[float] = None,
        threshold: Optional[float] = None
    ) -> Dict:
        """
        Criar nova proposta de governança
        
        Args:
            proposer: Endereço do proponente
            title: Título da proposta
            description: Descrição detalhada
            action: Ação a ser executada (dict)
            deposit: Depósito em ALZ
            voting_period: Período de votação em segundos
            quorum: Quorum necessário (% do supply)
            threshold: Threshold de aprovação (% de votos)
        """
        # Validar depósito mínimo
        if deposit < self.min_proposal_deposit:
            return {
                "success": False,
                "error": f"Depósito mínimo: {self.min_proposal_deposit} ALZ"
            }
        
        # Usar valores padrão se não fornecidos
        voting_period = voting_period or self.default_voting_period
        quorum = quorum or self.default_quorum
        threshold = threshold or self.default_threshold
        
        # Gerar ID único
        proposal_id = f"proposal_{int(time.time())}_{hashlib.sha256(f'{proposer}{title}'.encode()).hexdigest()[:8]}"
        
        now = time.time()
        
        # Criar proposta
        proposal = Proposal(
            proposal_id=proposal_id,
            proposer=proposer,
            title=title,
            description=description,
            action=action,
            deposit=deposit,
            voting_period=voting_period,
            quorum=quorum,
            threshold=threshold,
            created_at=now,
            start_time=now,
            end_time=now + voting_period,
            status=ProposalStatus.ACTIVE.value
        )
        
        # Assinar com PQC se disponível
        if self.quantum_security:
            try:
                proposal_data = json.dumps({
                    "proposal_id": proposal_id,
                    "proposer": proposer,
                    "title": title,
                    "action": action
                }, sort_keys=True).encode()
                
                # Gerar assinatura quântica (simulado)
                proposal.quantum_signature = {
                    "algorithm": "ML-DSA-128",
                    "signature": "simulated_signature",
                    "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                }
            except Exception as e:
                print(f"⚠️  Erro ao assinar proposta: {e}")
        
        # Armazenar
        self.proposals[proposal_id] = proposal
        self.votes[proposal_id] = []
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "proposal": asdict(proposal),
            "message": "Proposta criada com sucesso"
        }
    
    def vote(
        self,
        proposal_id: str,
        voter: str,
        vote_type: str,
        amount: float  # Quantidade de ALZ usada para votar
    ) -> Dict:
        """
        Votar em uma proposta
        
        Args:
            proposal_id: ID da proposta
            voter: Endereço do votante
            vote_type: "yes", "no", ou "abstain"
            amount: Quantidade de ALZ usada para votar (1 ALZ = 1 voto)
        """
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposta não encontrada"}
        
        proposal = self.proposals[proposal_id]
        
        # Verificar se proposta está ativa
        if proposal.status != ProposalStatus.ACTIVE.value:
            return {
                "success": False,
                "error": f"Proposta não está ativa (status: {proposal.status})"
            }
        
        # Verificar se período de votação não expirou
        if time.time() > proposal.end_time:
            proposal.status = ProposalStatus.REJECTED.value
            return {
                "success": False,
                "error": "Período de votação expirado"
            }
        
        # Validar tipo de voto
        if vote_type not in [vt.value for vt in VoteType]:
            return {
                "success": False,
                "error": f"Tipo de voto inválido: {vote_type}"
            }
        
        # Criar voto
        vote = Vote(
            proposal_id=proposal_id,
            voter=voter,
            vote_type=vote_type,
            amount=amount,
            timestamp=time.time()
        )
        
        # Assinar com PQC se disponível
        if self.quantum_security:
            try:
                vote_data = json.dumps({
                    "proposal_id": proposal_id,
                    "voter": voter,
                    "vote_type": vote_type,
                    "amount": amount
                }, sort_keys=True).encode()
                
                vote.quantum_signature = {
                    "algorithm": "ML-DSA-128",
                    "signature": "simulated_signature",
                    "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                }
            except Exception as e:
                print(f"⚠️  Erro ao assinar voto: {e}")
        
        # Adicionar voto
        self.votes[proposal_id].append(vote)
        
        # Atualizar contadores
        if vote_type == VoteType.YES.value:
            proposal.yes_votes += amount
        elif vote_type == VoteType.NO.value:
            proposal.no_votes += amount
        else:
            proposal.abstain_votes += amount
        
        proposal.total_votes += amount
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "vote": asdict(vote),
            "message": "Voto registrado com sucesso"
        }
    
    def check_proposal_status(self, proposal_id: str) -> Dict:
        """Verificar status de uma proposta"""
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposta não encontrada"}
        
        proposal = self.proposals[proposal_id]
        now = time.time()
        
        # Verificar se período expirou
        if now > proposal.end_time and proposal.status == ProposalStatus.ACTIVE.value:
            # Verificar quorum
            quorum_met = proposal.total_votes >= (self.total_supply * proposal.quorum)
            
            if not quorum_met:
                proposal.status = ProposalStatus.REJECTED.value
                reason = "Quorum não atingido"
            else:
                # Verificar threshold
                total_votes_excluding_abstain = proposal.yes_votes + proposal.no_votes
                if total_votes_excluding_abstain == 0:
                    approval_rate = 0.0
                else:
                    approval_rate = proposal.yes_votes / total_votes_excluding_abstain
                
                if approval_rate >= proposal.threshold:
                    proposal.status = ProposalStatus.PASSED.value
                    reason = "Proposta aprovada"
                else:
                    proposal.status = ProposalStatus.REJECTED.value
                    reason = "Threshold de aprovação não atingido"
        else:
            reason = None
        
        return {
            "success": True,
            "proposal": asdict(proposal),
            "status": proposal.status,
            "reason": reason,
            "quorum_met": proposal.total_votes >= (self.total_supply * proposal.quorum),
            "quorum_percent": (proposal.total_votes / self.total_supply) * 100,
            "approval_rate": (proposal.yes_votes / (proposal.yes_votes + proposal.no_votes)) * 100 if (proposal.yes_votes + proposal.no_votes) > 0 else 0.0
        }
    
    def execute_proposal(self, proposal_id: str) -> Dict:
        """Executar proposta aprovada"""
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposta não encontrada"}
        
        proposal = self.proposals[proposal_id]
        
        # Verificar se proposta foi aprovada
        if proposal.status != ProposalStatus.PASSED.value:
            return {
                "success": False,
                "error": f"Proposta não foi aprovada (status: {proposal.status})"
            }
        
        # Executar ação (simulado - em produção executar smart contract)
        action = proposal.action
        action_type = action.get("type")
        
        execution_result = {
            "proposal_id": proposal_id,
            "action_type": action_type,
            "action": action,
            "executed_at": time.time(),
            "executed_by": "governance_system",
            "result": "success"  # Em produção, verificar resultado real
        }
        
        # Marcar como executada
        proposal.status = ProposalStatus.EXECUTED.value
        self.executed_proposals.append(proposal_id)
        
        return {
            "success": True,
            "execution": execution_result,
            "message": "Proposta executada com sucesso"
        }
    
    def get_all_proposals(self, status: Optional[str] = None) -> List[Dict]:
        """Obter todas as propostas (opcionalmente filtradas por status)"""
        proposals = []
        for proposal in self.proposals.values():
            if status is None or proposal.status == status:
                proposals.append(asdict(proposal))
        return proposals
    
    def get_proposal_votes(self, proposal_id: str) -> List[Dict]:
        """Obter todos os votos de uma proposta"""
        if proposal_id not in self.votes:
            return []
        
        return [asdict(vote) for vote in self.votes[proposal_id]]

if __name__ == '__main__':
    print("="*70)
    print("🏛️  GOVERNANCE SYSTEM - TESTE")
    print("="*70)
    
    from tokenomics_system import TokenomicsSystem
    
    tokenomics = TokenomicsSystem()
    governance = GovernanceSystem(tokenomics)
    
    # Criar proposta
    print("\n📋 Criando Proposta...")
    proposal_result = governance.create_proposal(
        proposer="0xproposer123",
        title="Aumentar taxa de bridge para 0.2%",
        description="Proposta para aumentar a taxa de bridge de 0.1% para 0.2% para aumentar receita",
        action={
            "type": "update_bridge_fee",
            "new_fee": 0.002
        },
        deposit=1000.0
    )
    
    if proposal_result.get("success"):
        proposal_id = proposal_result["proposal_id"]
        print(f"   ✅ Proposta criada: {proposal_id}")
        print(f"   ✅ Título: {proposal_result['proposal']['title']}")
        
        # Votar
        print("\n📋 Votando...")
        vote1 = governance.vote(proposal_id, "0xvoter1", "yes", 100000.0)
        vote2 = governance.vote(proposal_id, "0xvoter2", "yes", 50000.0)
        vote3 = governance.vote(proposal_id, "0xvoter3", "no", 30000.0)
        
        print(f"   ✅ Votos registrados: {len(governance.votes[proposal_id])}")
        
        # Verificar status
        print("\n📋 Verificando Status...")
        status = governance.check_proposal_status(proposal_id)
        print(f"   ✅ Status: {status['status']}")
        print(f"   ✅ Quorum: {status['quorum_percent']:.2f}%")
        print(f"   ✅ Taxa de aprovação: {status['approval_rate']:.2f}%")
        
        # Executar se aprovada
        if status['status'] == 'passed':
            print("\n📋 Executando Proposta...")
            execution = governance.execute_proposal(proposal_id)
            if execution.get("success"):
                print(f"   ✅ {execution['message']}")



