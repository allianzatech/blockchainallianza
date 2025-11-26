#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 API PARA TOKENOMICS E GOVERNANÇA
API RESTful para acessar Tokenomics e Governança
"""

from flask import Flask, request, jsonify
from functools import wraps
import json

def create_tokenomics_api(bridge_instance):
    """
    Criar API Flask para Tokenomics e Governança
    
    Args:
        bridge_instance: Instância do RealCrossChainBridge
        
    Returns:
        Flask app
    """
    app = Flask(__name__)
    
    # Verificar se Tokenomics está disponível
    if not hasattr(bridge_instance, 'tokenomics') or bridge_instance.tokenomics is None:
        @app.route('/api/v1/tokenomics/info', methods=['GET'])
        def tokenomics_not_available():
            return jsonify({
                "success": False,
                "error": "Tokenomics não está disponível"
            }), 503
        
        return app
    
    tokenomics = bridge_instance.tokenomics
    governance = bridge_instance.governance if hasattr(bridge_instance, 'governance') else None
    
    # =========================================================================
    # TOKENOMICS ENDPOINTS
    # =========================================================================
    
    @app.route('/api/v1/tokenomics/info', methods=['GET'])
    def get_tokenomics_info():
        """Obter informações completas de tokenomics"""
        try:
            info = tokenomics.get_tokenomics_info()
            return jsonify({
                "success": True,
                "data": info
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/distribution', methods=['GET'])
    def get_distribution():
        """Obter distribuição de tokens"""
        try:
            distribution = tokenomics.calculate_distribution_amounts()
            return jsonify({
                "success": True,
                "data": distribution
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/revenue', methods=['GET'])
    def get_revenue_model():
        """Obter modelo de receita"""
        try:
            revenue = tokenomics.get_revenue_model()
            return jsonify({
                "success": True,
                "data": revenue
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/calculate-fee', methods=['POST'])
    def calculate_fee_with_alz():
        """Calcular taxa com desconto ALZ"""
        try:
            data = request.json
            fee_type = data.get('fee_type')  # 'gas' ou 'bridge'
            base_fee = float(data.get('base_fee', 0))
            alz_balance = float(data.get('alz_balance', 0))
            
            if fee_type == 'gas':
                result = tokenomics.calculate_gas_fee_with_alz(base_fee, alz_balance)
            elif fee_type == 'bridge':
                result = tokenomics.calculate_bridge_fee_with_alz(base_fee, alz_balance)
            else:
                return jsonify({
                    "success": False,
                    "error": "fee_type deve ser 'gas' ou 'bridge'"
                }), 400
            
            return jsonify({
                "success": True,
                "data": result
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/staking/pools', methods=['GET'])
    def get_staking_pools():
        """Obter todos os pools de staking"""
        try:
            pools = list(tokenomics.staking_pools.values())
            return jsonify({
                "success": True,
                "data": pools,
                "count": len(pools)
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/staking/create-pool', methods=['POST'])
    def create_staking_pool():
        """Criar novo pool de staking"""
        try:
            data = request.json
            result = tokenomics.create_staking_pool(
                pool_id=data.get('pool_id'),
                apy=float(data.get('apy', 0.10)),
                min_stake=float(data.get('min_stake', 1000.0)),
                lock_period_days=int(data.get('lock_period_days', 0))
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/staking/stake', methods=['POST'])
    def stake_tokens():
        """Fazer stake de tokens"""
        try:
            data = request.json
            result = tokenomics.stake_tokens(
                pool_id=data.get('pool_id'),
                address=data.get('address'),
                amount=float(data.get('amount', 0))
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/v1/tokenomics/staking/rewards', methods=['POST'])
    def calculate_rewards():
        """Calcular recompensas de staking"""
        try:
            data = request.json
            result = tokenomics.calculate_staking_rewards(
                pool_id=data.get('pool_id'),
                address=data.get('address')
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # =========================================================================
    # GOVERNANCE ENDPOINTS
    # =========================================================================
    
    if governance:
        @app.route('/api/v1/governance/proposals', methods=['GET'])
        def get_proposals():
            """Obter todas as propostas"""
            try:
                status = request.args.get('status')
                proposals = governance.get_all_proposals(status=status)
                return jsonify({
                    "success": True,
                    "data": proposals,
                    "count": len(proposals)
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @app.route('/api/v1/governance/proposals', methods=['POST'])
        def create_proposal():
            """Criar nova proposta"""
            try:
                data = request.json
                result = governance.create_proposal(
                    proposer=data.get('proposer'),
                    title=data.get('title'),
                    description=data.get('description'),
                    action=data.get('action'),
                    deposit=float(data.get('deposit', 100.0)),
                    voting_period=int(data.get('voting_period', 604800)) if data.get('voting_period') else None,
                    quorum=float(data.get('quorum')) if data.get('quorum') else None,
                    threshold=float(data.get('threshold')) if data.get('threshold') else None
                )
                return jsonify(result)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @app.route('/api/v1/governance/proposals/<proposal_id>', methods=['GET'])
        def get_proposal(proposal_id):
            """Obter proposta específica"""
            try:
                status = governance.check_proposal_status(proposal_id)
                return jsonify(status)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @app.route('/api/v1/governance/proposals/<proposal_id>/vote', methods=['POST'])
        def vote_proposal(proposal_id):
            """Votar em proposta"""
            try:
                data = request.json
                result = governance.vote(
                    proposal_id=proposal_id,
                    voter=data.get('voter'),
                    vote_type=data.get('vote_type'),
                    amount=float(data.get('amount', 0))
                )
                return jsonify(result)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @app.route('/api/v1/governance/proposals/<proposal_id>/votes', methods=['GET'])
        def get_proposal_votes(proposal_id):
            """Obter votos de uma proposta"""
            try:
                votes = governance.get_proposal_votes(proposal_id)
                return jsonify({
                    "success": True,
                    "data": votes,
                    "count": len(votes)
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @app.route('/api/v1/governance/proposals/<proposal_id>/execute', methods=['POST'])
        def execute_proposal(proposal_id):
            """Executar proposta aprovada"""
            try:
                result = governance.execute_proposal(proposal_id)
                return jsonify(result)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
    
    return app

if __name__ == '__main__':
    print("="*70)
    print("🌐 API TOKENOMICS E GOVERNANÇA")
    print("="*70)
    print("\n✅ API criada!")
    print("   Use create_tokenomics_api(bridge_instance) para criar a app Flask")



