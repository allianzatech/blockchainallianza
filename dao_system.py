#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de DAO (Decentralized Autonomous Organization) Funcional
Implementação completa de governança on-chain
"""

import time
import json
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ProposalStatus(Enum):
    """Status da proposta"""
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    CANCELLED = "cancelled"

class VoteOption(Enum):
    """Opções de voto"""
    YES = "yes"
    NO = "no"
    ABSTAIN = "abstain"

@dataclass
class Proposal:
    """Representa uma proposta de governança"""
    proposal_id: str
    proposer: str
    title: str
    description: str
    action: Dict  # Ação a ser executada se aprovada
    voting_period: int  # Período de votação em segundos
    quorum: float  # Quorum mínimo (0-1)
    threshold: float  # Threshold de aprovação (0-1)
    created_at: float
    status: ProposalStatus = ProposalStatus.PENDING
    votes: Dict[str, VoteOption] = None  # address -> vote
    vote_weights: Dict[str, float] = None  # address -> weight (stake)
    total_votes: float = 0.0
    yes_votes: float = 0.0
    no_votes: float = 0.0
    abstain_votes: float = 0.0

class DAOSystem:
    """
    Sistema de DAO completo
    Gerencia propostas, votações e execução
    """
    
    def __init__(
        self,
        min_proposal_deposit: float = 100.0,
        default_voting_period: int = 604800,  # 7 dias
        default_quorum: float = 0.05,  # 5% do supply
        default_threshold: float = 0.5  # 50% de aprovação
    ):
        self.proposals: Dict[str, Proposal] = {}
        self.min_proposal_deposit = min_proposal_deposit
        self.default_voting_period = default_voting_period
        self.default_quorum = default_quorum
        self.default_threshold = default_threshold
        self.total_supply = 0.0  # Será atualizado externamente
        self.executed_proposals = []
        
        logger.info("🏛️  DAO System inicializado")
    
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
        Cria nova proposta
        
        Args:
            proposer: Endereço do proponente
            title: Título da proposta
            description: Descrição detalhada
            action: Ação a ser executada se aprovada
            deposit: Depósito mínimo (será retornado se aprovada)
            voting_period: Período de votação (opcional)
            quorum: Quorum mínimo (opcional)
            threshold: Threshold de aprovação (opcional)
        
        Returns:
            Resultado da criação
        """
        if deposit < self.min_proposal_deposit:
            return {
                "success": False,
                "error": f"Depósito mínimo: {self.min_proposal_deposit}"
            }
        
        proposal_id = hashlib.sha256(
            f"{proposer}{title}{time.time()}".encode()
        ).hexdigest()[:16]
        
        proposal = Proposal(
            proposal_id=proposal_id,
            proposer=proposer,
            title=title,
            description=description,
            action=action,
            voting_period=voting_period or self.default_voting_period,
            quorum=quorum or self.default_quorum,
            threshold=threshold or self.default_threshold,
            created_at=time.time(),
            votes={},
            vote_weights={}
        )
        
        self.proposals[proposal_id] = proposal
        
        logger.info(f"📝 Proposta criada: {proposal_id} por {proposer}")
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "proposal": {
                "id": proposal_id,
                "title": title,
                "status": proposal.status.value,
                "voting_ends_at": proposal.created_at + proposal.voting_period
            }
        }
    
    def activate_proposal(self, proposal_id: str) -> Dict:
        """Ativa proposta para votação"""
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposta não encontrada"}
        
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ProposalStatus.PENDING:
            return {"success": False, "error": "Proposta já foi ativada ou cancelada"}
        
        proposal.status = ProposalStatus.ACTIVE
        
        logger.info(f"✅ Proposta ativada: {proposal_id}")
        
        return {
            "success": True,
            "voting_ends_at": proposal.created_at + proposal.voting_period
        }
    
    def vote(
        self,
        proposal_id: str,
        voter: str,
        vote_option: VoteOption,
        vote_weight: float
    ) -> Dict:
        """
        Vota em uma proposta
        
        Args:
            proposal_id: ID da proposta
            voter: Endereço do votante
            vote_option: Opção de voto (YES, NO, ABSTAIN)
            vote_weight: Peso do voto (baseado em stake)
        
        Returns:
            Resultado do voto
        """
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposta não encontrada"}
        
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ProposalStatus.ACTIVE:
            return {"success": False, "error": "Proposta não está ativa"}
        
        # Verificar se ainda está no período de votação
        if time.time() > proposal.created_at + proposal.voting_period:
            return {"success": False, "error": "Período de votação encerrado"}
        
        # Verificar se já votou
        if voter in proposal.votes:
            return {"success": False, "error": "Você já votou nesta proposta"}
        
        # Registrar voto
        proposal.votes[voter] = vote_option
        proposal.vote_weights[voter] = vote_weight
        proposal.total_votes += vote_weight
        
        if vote_option == VoteOption.YES:
            proposal.yes_votes += vote_weight
        elif vote_option == VoteOption.NO:
            proposal.no_votes += vote_weight
        else:
            proposal.abstain_votes += vote_weight
        
        logger.info(f"🗳️  Voto registrado: {voter} -> {vote_option.value} (peso: {vote_weight})")
        
        # Verificar se pode finalizar
        self._check_proposal_status(proposal)
        
        return {
            "success": True,
            "vote": vote_option.value,
            "weight": vote_weight,
            "total_votes": proposal.total_votes
        }
    
    def _check_proposal_status(self, proposal: Proposal):
        """Verifica e atualiza status da proposta"""
        if proposal.status != ProposalStatus.ACTIVE:
            return
        
        # Verificar se período de votação encerrou
        if time.time() > proposal.created_at + proposal.voting_period:
            # Verificar quorum
            quorum_met = proposal.total_votes >= (self.total_supply * proposal.quorum)
            
            if not quorum_met:
                proposal.status = ProposalStatus.REJECTED
                logger.info(f"❌ Proposta rejeitada (quorum não atingido): {proposal.proposal_id}")
                return
            
            # Verificar threshold
            if proposal.total_votes > 0:
                approval_ratio = proposal.yes_votes / proposal.total_votes
                
                if approval_ratio >= proposal.threshold:
                    proposal.status = ProposalStatus.PASSED
                    logger.info(f"✅ Proposta aprovada: {proposal.proposal_id}")
                else:
                    proposal.status = ProposalStatus.REJECTED
                    logger.info(f"❌ Proposta rejeitada (threshold não atingido): {proposal.proposal_id}")
    
    def execute_proposal(self, proposal_id: str) -> Dict:
        """
        Executa proposta aprovada
        
        Args:
            proposal_id: ID da proposta
        
        Returns:
            Resultado da execução
        """
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposta não encontrada"}
        
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ProposalStatus.PASSED:
            return {
                "success": False,
                "error": f"Proposta não está aprovada (status: {proposal.status.value})"
            }
        
        if proposal.status == ProposalStatus.EXECUTED:
            return {"success": False, "error": "Proposta já foi executada"}
        
        # Executar ação
        try:
            # Em produção, isso executaria a ação on-chain
            # Por agora, apenas marca como executada
            proposal.status = ProposalStatus.EXECUTED
            self.executed_proposals.append(proposal_id)
            
            logger.info(f"🚀 Proposta executada: {proposal_id}")
            
            return {
                "success": True,
                "proposal_id": proposal_id,
                "action": proposal.action,
                "message": "Ação executada com sucesso"
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar proposta: {e}")
            return {
                "success": False,
                "error": f"Erro ao executar: {str(e)}"
            }
    
    def get_proposal(self, proposal_id: str) -> Optional[Dict]:
        """Retorna informações da proposta"""
        if proposal_id not in self.proposals:
            return None
        
        proposal = self.proposals[proposal_id]
        
        return {
            "id": proposal.proposal_id,
            "proposer": proposal.proposer,
            "title": proposal.title,
            "description": proposal.description,
            "status": proposal.status.value,
            "created_at": proposal.created_at,
            "voting_ends_at": proposal.created_at + proposal.voting_period,
            "quorum": proposal.quorum,
            "threshold": proposal.threshold,
            "total_votes": proposal.total_votes,
            "yes_votes": proposal.yes_votes,
            "no_votes": proposal.no_votes,
            "abstain_votes": proposal.abstain_votes,
            "votes_count": len(proposal.votes),
            "action": proposal.action
        }
    
    def get_all_proposals(self, status: Optional[ProposalStatus] = None) -> List[Dict]:
        """Retorna lista de propostas"""
        proposals = self.proposals.values()
        
        if status:
            proposals = [p for p in proposals if p.status == status]
        
        return [self.get_proposal(p.proposal_id) for p in proposals]
    
    def get_dao_stats(self) -> Dict:
        """Retorna estatísticas do DAO"""
        total = len(self.proposals)
        active = sum(1 for p in self.proposals.values() if p.status == ProposalStatus.ACTIVE)
        passed = sum(1 for p in self.proposals.values() if p.status == ProposalStatus.PASSED)
        executed = len(self.executed_proposals)
        
        return {
            "total_proposals": total,
            "active_proposals": active,
            "passed_proposals": passed,
            "executed_proposals": executed,
            "min_proposal_deposit": self.min_proposal_deposit,
            "default_voting_period": self.default_voting_period,
            "default_quorum": self.default_quorum,
            "default_threshold": self.default_threshold
        }

# Instância global
global_dao_system: Optional[DAOSystem] = None

def initialize_dao_system(
    min_proposal_deposit: float = 100.0,
    default_voting_period: int = 604800,
    default_quorum: float = 0.05,
    default_threshold: float = 0.5
) -> DAOSystem:
    """Inicializa sistema DAO global"""
    global global_dao_system
    global_dao_system = DAOSystem(
        min_proposal_deposit,
        default_voting_period,
        default_quorum,
        default_threshold
    )
    return global_dao_system

def get_dao_system() -> Optional[DAOSystem]:
    """Retorna instância global do sistema DAO"""
    return global_dao_system










