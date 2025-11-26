#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 API ENDPOINTS PARA TRANSACTION TRACKING
Endpoints RESTful para rastreamento de transações
"""

from flask import Blueprint, request, jsonify
from typing import Optional

def create_transaction_tracking_api(transaction_tracker, circuit_breaker_manager, gas_optimizer) -> Blueprint:
    """Criar blueprint Flask para transaction tracking"""
    api_bp = Blueprint('transaction_tracking', __name__, url_prefix='/api/v1/transactions')
    
    @api_bp.route('/<tx_id>/status')
    def get_transaction_status(tx_id: str):
        """Obter status detalhado de uma transação"""
        if not transaction_tracker:
            return jsonify({"error": "Transaction tracker não disponível"}), 503
        
        state = transaction_tracker.get_transaction(tx_id)
        if not state:
            return jsonify({"error": "Transação não encontrada"}), 404
        
        return jsonify({
            "tx_id": state.tx_id,
            "source_chain": state.source_chain,
            "target_chain": state.target_chain,
            "status": state.status.value,
            "source_tx_hash": state.source_tx_hash,
            "target_tx_hash": state.target_tx_hash,
            "amount": state.amount,
            "token_symbol": state.token_symbol,
            "confirmations": state.confirmations,
            "required_confirmations": state.required_confirmations,
            "created_at": state.created_at,
            "updated_at": state.updated_at,
            "estimated_completion": state.estimated_completion,
            "error": state.error,
            "metadata": state.metadata
        })
    
    @api_bp.route('/<tx_id>/summary')
    def get_transaction_summary(tx_id: str):
        """Obter resumo de status de uma transação"""
        if not transaction_tracker:
            return jsonify({"error": "Transaction tracker não disponível"}), 503
        
        summary = transaction_tracker.get_status_summary(tx_id)
        if "error" in summary:
            return jsonify(summary), 404
        
        return jsonify(summary)
    
    @api_bp.route('/statistics')
    def get_statistics():
        """Obter estatísticas de transações"""
        if not transaction_tracker:
            return jsonify({"error": "Transaction tracker não disponível"}), 503
        
        stats = transaction_tracker.get_all_statistics()
        return jsonify(stats)
    
    @api_bp.route('/statistics/<chain>')
    def get_chain_statistics(chain: str):
        """Obter estatísticas de uma chain específica"""
        if not transaction_tracker:
            return jsonify({"error": "Transaction tracker não disponível"}), 503
        
        stats = transaction_tracker.get_chain_statistics(chain)
        return jsonify(stats)
    
    @api_bp.route('/circuit-breakers')
    def get_circuit_breakers():
        """Obter status de todos os circuit breakers"""
        if not circuit_breaker_manager:
            return jsonify({"error": "Circuit breaker manager não disponível"}), 503
        
        status = circuit_breaker_manager.get_all_status()
        return jsonify(status)
    
    @api_bp.route('/gas-optimizer/statistics')
    def get_gas_optimizer_stats():
        """Obter estatísticas do gas optimizer"""
        if not gas_optimizer:
            return jsonify({"error": "Gas optimizer não disponível"}), 503
        
        chain = request.args.get('chain')
        stats = gas_optimizer.get_statistics(chain)
        return jsonify(stats)
    
    return api_bp



