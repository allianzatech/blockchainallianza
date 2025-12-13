# advanced_routes.py
# 🌟 ROTAS PARA SISTEMAS AVANÇADOS - ALLIANZA BLOCKCHAIN

from flask import jsonify, request
import logging

logger = logging.getLogger(__name__)

def init_advanced_routes(app, blockchain):
    """
    Inicializa rotas para sistemas avançados
    """
    
    # ============================================================================
    # ROTAS: CONSENSO ADAPTATIVO AVANÇADO
    # ============================================================================
    
    @app.route('/advanced/consensus/info', methods=['GET'])
    def get_consensus_info():
        """Retorna informações do consenso adaptativo"""
        try:
            if not hasattr(blockchain, 'advanced_consensus') or blockchain.advanced_consensus is None:
                return jsonify({"success": False, "error": "Consenso adaptativo não disponível"})
            
            info = blockchain.advanced_consensus.get_consensus_info()
            return jsonify({"success": True, "consensus_info": info})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/consensus/update-state', methods=['POST'])
    def update_consensus_state():
        """Atualiza estado da rede para adaptação do consenso"""
        try:
            if not hasattr(blockchain, 'advanced_consensus') or blockchain.advanced_consensus is None:
                return jsonify({"success": False, "error": "Consenso adaptativo não disponível"})
            
            data = request.get_json() or {}
            blockchain.advanced_consensus.update_network_state(data)
            
            info = blockchain.advanced_consensus.get_consensus_info()
            return jsonify({"success": True, "consensus_info": info})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    # ============================================================================
    # ROTAS: SHARDING DINÂMICO
    # ============================================================================
    
    @app.route('/advanced/sharding/stats', methods=['GET'])
    def get_sharding_stats():
        """Retorna estatísticas de sharding"""
        try:
            if not hasattr(blockchain, 'dynamic_sharding') or blockchain.dynamic_sharding is None:
                return jsonify({"success": False, "error": "Sharding dinâmico não disponível"})
            
            stats = blockchain.dynamic_sharding.get_sharding_stats()
            return jsonify({"success": True, "sharding_stats": stats})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/sharding/adapt', methods=['POST'])
    def adapt_sharding():
        """Adapta sharding baseado na carga"""
        try:
            if not hasattr(blockchain, 'dynamic_sharding') or blockchain.dynamic_sharding is None:
                return jsonify({"success": False, "error": "Sharding dinâmico não disponível"})
            
            blockchain.dynamic_sharding.adapt_shards()
            stats = blockchain.dynamic_sharding.get_sharding_stats()
            return jsonify({"success": True, "sharding_stats": stats})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    # ============================================================================
    # ROTAS: STATE CHANNELS
    # ============================================================================
    
    @app.route('/advanced/channels/open', methods=['POST'])
    def open_state_channel():
        """Abre um state channel quântico-seguro"""
        try:
            if not hasattr(blockchain, 'state_channels') or blockchain.state_channels is None:
                return jsonify({"success": False, "error": "State channels não disponíveis"})
            
            data = request.get_json() or {}
            party1 = data.get("party1")
            party2 = data.get("party2")
            initial_balance = data.get("initial_balance", {})
            
            result = blockchain.state_channels.open_channel(party1, party2, initial_balance)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/channels/<channel_id>/update', methods=['POST'])
    def update_state_channel(channel_id):
        """Atualiza estado de um channel"""
        try:
            if not hasattr(blockchain, 'state_channels') or blockchain.state_channels is None:
                return jsonify({"success": False, "error": "State channels não disponíveis"})
            
            data = request.get_json() or {}
            from_party = data.get("from")
            to_party = data.get("to")
            amount = data.get("amount")
            asset = data.get("asset", "ALZ")
            
            result = blockchain.state_channels.update_channel(channel_id, from_party, to_party, amount, asset)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/channels/<channel_id>/close', methods=['POST'])
    def close_state_channel(channel_id):
        """Fecha um state channel"""
        try:
            if not hasattr(blockchain, 'state_channels') or blockchain.state_channels is None:
                return jsonify({"success": False, "error": "State channels não disponíveis"})
            
            data = request.get_json() or {}
            final_state_number = data.get("final_state_number")
            
            result = blockchain.state_channels.close_channel(channel_id, final_state_number)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    # ============================================================================
    # ROTAS: NFTs QUÂNTICO-SEGUROS
    # ============================================================================
    
    @app.route('/advanced/nfts/mint', methods=['POST'])
    def mint_quantum_nft():
        """Cria um NFT quântico-seguro"""
        try:
            if not hasattr(blockchain, 'nft_manager') or blockchain.nft_manager is None:
                return jsonify({"success": False, "error": "NFT manager não disponível"})
            
            data = request.get_json() or {}
            metadata = data.get("metadata", {})
            owner = data.get("owner")
            name = data.get("name")
            
            result = blockchain.nft_manager.mint_nft(metadata, owner, name)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/nfts/<token_id>', methods=['GET'])
    def get_quantum_nft(token_id):
        """Retorna informações de um NFT"""
        try:
            if not hasattr(blockchain, 'nft_manager') or blockchain.nft_manager is None:
                return jsonify({"success": False, "error": "NFT manager não disponível"})
            
            nft = blockchain.nft_manager.get_nft(token_id)
            if nft:
                return jsonify({"success": True, "nft": nft})
            else:
                return jsonify({"success": False, "error": "NFT não encontrado"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/nfts/owner/<owner>', methods=['GET'])
    def get_owner_nfts(owner):
        """Retorna NFTs de um owner"""
        try:
            if not hasattr(blockchain, 'nft_manager') or blockchain.nft_manager is None:
                return jsonify({"success": False, "error": "NFT manager não disponível"})
            
            nfts = blockchain.nft_manager.get_owner_nfts(owner)
            return jsonify({"success": True, "nfts": nfts, "count": len(nfts)})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    # ============================================================================
    # ROTAS: AGREGAÇÃO DE ASSINATURAS
    # ============================================================================
    
    @app.route('/advanced/signatures/aggregate', methods=['POST'])
    def aggregate_signatures():
        """Agrega múltiplas assinaturas QRS-3"""
        try:
            if not hasattr(blockchain, 'signature_aggregation') or blockchain.signature_aggregation is None:
                return jsonify({"success": False, "error": "Agregação não disponível"})
            
            data = request.get_json() or {}
            signatures = data.get("signatures", [])
            
            if len(signatures) < 2:
                return jsonify({"success": False, "error": "Pelo menos 2 assinaturas necessárias"})
            
            result = blockchain.signature_aggregation.aggregate_qrs3_signatures(signatures)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    # ============================================================================
    # ROTAS: MULTI-LAYER SECURITY
    # ============================================================================
    
    @app.route('/advanced/security/validate', methods=['POST'])
    def validate_transaction_multi_layer():
        """Valida transação através de múltiplas camadas"""
        try:
            if not hasattr(blockchain, 'multi_security') or blockchain.multi_security is None:
                return jsonify({"success": False, "error": "Multi-layer security não disponível"})
            
            data = request.get_json() or {}
            transaction = data.get("transaction", {})
            
            result = blockchain.multi_security.validate_transaction(transaction)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/security/stats', methods=['GET'])
    def get_security_stats():
        """Retorna estatísticas de segurança"""
        try:
            if not hasattr(blockchain, 'multi_security') or blockchain.multi_security is None:
                return jsonify({"success": False, "error": "Multi-layer security não disponível"})
            
            stats = blockchain.multi_security.get_security_stats()
            return jsonify({"success": True, "security_stats": stats})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    # ============================================================================
    # ROTAS: DeFi QUÂNTICO-SEGURO
    # ============================================================================
    
    @app.route('/advanced/defi/dex/pool', methods=['POST'])
    def create_dex_pool():
        """Cria pool de liquidez DEX"""
        try:
            from quantum_safe_defi import QuantumSafeDeFi
            from quantum_security import QuantumSecuritySystem
            
            qs = QuantumSecuritySystem()
            defi = QuantumSafeDeFi(qs)
            
            data = request.get_json() or {}
            token1 = data.get("token1")
            token2 = data.get("token2")
            initial_liquidity = data.get("initial_liquidity", {})
            
            result = defi.dex.create_pool(token1, token2, initial_liquidity)
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/advanced/defi/stats', methods=['GET'])
    def get_defi_stats():
        """Retorna estatísticas do DeFi"""
        try:
            from quantum_safe_defi import QuantumSafeDeFi
            from quantum_security import QuantumSecuritySystem
            
            qs = QuantumSecuritySystem()
            defi = QuantumSafeDeFi(qs)
            
            stats = defi.get_defi_stats()
            return jsonify({"success": True, "defi_stats": stats})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    logger.info("🌟 ROTAS AVANÇADAS: Inicializadas!")
    print("🌟 ROTAS AVANÇADAS: Inicializadas!")
    print("   • /advanced/consensus/* - Consenso Adaptativo")
    print("   • /advanced/sharding/* - Sharding Dinâmico")
    print("   • /advanced/channels/* - State Channels")
    print("   • /advanced/nfts/* - NFTs Quântico-Seguros")
    print("   • /advanced/signatures/* - Agregação")
    print("   • /advanced/security/* - Multi-Layer Security")
    print("   • /advanced/defi/* - DeFi Quântico-Seguro")




















