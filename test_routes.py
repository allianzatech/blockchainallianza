# test_routes.py
# 🧪 ROTAS PARA TESTES INTERATIVOS NO SITE
# Integra as PoCs com interface web

from flask import jsonify, request, render_template
import logging
import time

logger = logging.getLogger(__name__)

# Variáveis globais (serão inicializadas)
poc_validacao = None
poc_gas = None
poc_lock = None

def init_test_routes(app, limiter=None):
    """Inicializar rotas de teste com rate limiting"""
    global poc_validacao, poc_gas, poc_lock
    
    # Decorator helper para rate limiting
    def limit_if_available(limit_str):
        """Aplicar rate limiting se disponível"""
        if limiter:
            return limiter.limit(limit_str)
        return lambda f: f
    
    try:
        from POC_VALIDACAO_UNIVERSAL_FINAL import UniversalSignatureValidationPOC
        poc_validacao = UniversalSignatureValidationPOC()
        logger.info("✅ PoC Validação Universal carregada")
    except Exception as e:
        logger.error(f"⚠️  Erro ao carregar PoC Validação: {e}")
        poc_validacao = None
    
    try:
        from POC_PREDICAO_GAS_80_PRECISAO import GasPricePredictionPOC
        poc_gas = GasPricePredictionPOC()
        logger.info("✅ PoC Predição de Gas carregada")
    except Exception as e:
        logger.error(f"⚠️  Erro ao carregar PoC Gas: {e}")
        poc_gas = None
    
    try:
        from POC_PROOF_OF_LOCK_ZK import ProofOfLockZKPOC
        poc_lock = ProofOfLockZKPOC()
        logger.info("✅ PoC Proof-of-Lock carregada")
    except Exception as e:
        logger.error(f"⚠️  Erro ao carregar PoC Lock: {e}")
        poc_lock = None
    
    # =============================================================================
    # ROTA: PÁGINA DE TESTES
    # =============================================================================
    
    @app.route('/test')
    def test_page():
        """Redirecionar para testnet - página de testes públicos"""
        from flask import redirect, url_for
        # Redirecionar para testnet (mais claro e profissional)
        return redirect('/testnet/public-tests', code=302)
    
    # =============================================================================
    # ROTAS: TESTE 1 - VALIDAÇÃO UNIVERSAL
    # =============================================================================
    
    @app.route('/test/validation/bitcoin', methods=['POST'])
    @limit_if_available("20 per hour")
    def test_validation_bitcoin():
        """Teste de validação Bitcoin (UTXO)"""
        try:
            if not poc_validacao:
                return jsonify({"valid": False, "error": "Sistema não disponível"}), 503
            
            data = request.get_json()
            if not data:
                return jsonify({"valid": False, "error": "Dados JSON obrigatórios"}), 400
            
            tx_hash = data.get('tx_hash', '').strip()
            
            if not tx_hash:
                return jsonify({"valid": False, "error": "Hash de transação obrigatório"}), 400
            
            # Validar formato (Bitcoin hash é hex, mínimo 32 caracteres)
            if len(tx_hash) < 32:
                return jsonify({"valid": False, "error": "Hash de transação inválido (mínimo 32 caracteres)"}), 400
            
            try:
                # Tentar validar como hex
                int(tx_hash, 16)
            except ValueError:
                return jsonify({"valid": False, "error": "Hash de transação deve ser hexadecimal"}), 400
            
            result = poc_validacao.validate_bitcoin_utxo_signature(tx_hash)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Erro no teste Bitcoin: {e}")
            error_msg = str(e)
            # Mensagens de erro mais amigáveis
            if "timeout" in error_msg.lower():
                error_msg = "Timeout ao consultar blockchain Bitcoin. Tente novamente."
            elif "not found" in error_msg.lower():
                error_msg = "Transação não encontrada. Verifique se o hash está correto e é de uma transação confirmada."
            return jsonify({"valid": False, "error": error_msg}), 500
    
    @app.route('/test/validation/solana', methods=['POST'])
    @limit_if_available("20 per hour")
    def test_validation_solana():
        """Teste de validação Solana (Ed25519)"""
        try:
            if not poc_validacao:
                return jsonify({"valid": False, "error": "Sistema não disponível"}), 503
            
            data = request.get_json()
            if not data:
                return jsonify({"valid": False, "error": "Dados JSON obrigatórios"}), 400
            
            signature = data.get('signature', '').strip()
            
            if not signature:
                return jsonify({"valid": False, "error": "Assinatura obrigatória"}), 400
            
            # Validar formato básico (Solana usa base58, mínimo 32 caracteres)
            if len(signature) < 32:
                return jsonify({"valid": False, "error": "Assinatura inválida (mínimo 32 caracteres)"}), 400
            
            result = poc_validacao.validate_solana_transaction(signature)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Erro no teste Solana: {e}")
            error_msg = str(e)
            # Mensagens de erro mais amigáveis
            if "timeout" in error_msg.lower():
                error_msg = "Timeout ao consultar blockchain Solana. Tente novamente."
            elif "not found" in error_msg.lower():
                error_msg = "Transação não encontrada. Verifique se a assinatura está correta e é de uma transação confirmada."
            return jsonify({"valid": False, "error": error_msg}), 500
    
    # =============================================================================
    # ROTAS: TESTE 2 - PREDIÇÃO DE GAS
    # =============================================================================
    
    @app.route('/test/gas/current', methods=['GET'])
    @limit_if_available("60 per hour")
    def test_gas_current():
        """Obter gas price atual"""
        try:
            if not poc_gas:
                return jsonify({"success": False, "error": "Sistema não disponível"}), 503
            
            gas_data = poc_gas.get_current_gas_price()
            
            if not gas_data:
                return jsonify({"success": False, "error": "Não foi possível obter gas price"}), 500
            
            return jsonify({
                "success": True,
                "gas_price_gwei": gas_data.get('gas_price_gwei', 0),
                "block_number": gas_data.get('block_number'),
                "timestamp": gas_data.get('timestamp')
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter gas: {e}")
            error_msg = str(e)
            if "not connected" in error_msg.lower() or "connection" in error_msg.lower():
                error_msg = "Não foi possível conectar à Ethereum. Verifique sua conexão."
            return jsonify({"success": False, "error": error_msg}), 500
    
    @app.route('/test/gas/predict', methods=['POST'])
    @limit_if_available("10 per hour")
    def test_gas_predict():
        """Prever spike de gas"""
        try:
            if not poc_gas:
                return jsonify({"success": False, "error": "Sistema não disponível"}), 503
            
            data = request.get_json() or {}
            minutes_ahead = int(data.get('minutes_ahead', 5))
            confidence_threshold = float(data.get('confidence_threshold', 0.8))
            
            # Validar parâmetros
            if minutes_ahead < 1 or minutes_ahead > 60:
                return jsonify({"success": False, "error": "minutes_ahead deve estar entre 1 e 60"}), 400
            
            if confidence_threshold < 0 or confidence_threshold > 1:
                return jsonify({"success": False, "error": "confidence_threshold deve estar entre 0 e 1"}), 400
            
            # Se histórico muito pequeno, coletar alguns dados primeiro
            if len(poc_gas.gas_history) < 10:
                # Coletar alguns dados rapidamente (não bloqueia)
                import threading
                def collect_quick():
                    for _ in range(5):
                        gas_data = poc_gas.get_current_gas_price()
                        if gas_data:
                            poc_gas.gas_history.append(gas_data)
                        time.sleep(2)
                
                thread = threading.Thread(target=collect_quick, daemon=True)
                thread.start()
            
            result = poc_gas.predict_gas_spike(
                minutes_ahead=minutes_ahead,
                confidence_threshold=confidence_threshold
            )
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Erro na predição de gas: {e}")
            error_msg = str(e)
            if "histórico insuficiente" in error_msg.lower():
                error_msg = "Histórico insuficiente para predição. Aguarde alguns minutos e tente novamente."
            elif "not connected" in error_msg.lower():
                error_msg = "Não foi possível conectar à Ethereum. Verifique sua conexão."
            return jsonify({"success": False, "error": error_msg}), 500
    
    # =============================================================================
    # ROTAS: TESTE 3 - PROOF-OF-LOCK ZK
    # =============================================================================
    
    @app.route('/test/proof-of-lock/status', methods=['GET'])
    @limit_if_available("60 per hour")
    def test_proof_of_lock_status():
        """Status do PoC Proof-of-Lock"""
        try:
            if not poc_lock:
                return jsonify({
                    "success": False,
                    "available": False,
                    "error": "Sistema não disponível"
                }), 503
            
            return jsonify({
                "success": True,
                "available": True,
                "status": "active",
                "description": "Proof-of-Lock criptográfico com ZK Proofs",
                "endpoints": {
                    "create": "/test/proof-of-lock (POST)",
                    "status": "/test/proof-of-lock/status (GET)"
                },
                "features": [
                    "Bloqueio de tokens",
                    "ZK Proofs para validação",
                    "Atomicidade garantida",
                    "Testado em redes de teste"
                ]
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/test/proof-of-lock', methods=['POST'])
    @limit_if_available("10 per hour")
    def test_proof_of_lock():
        """Teste de proof-of-lock com ZK Proofs"""
        try:
            if not poc_lock:
                return jsonify({"success": False, "error": "Sistema não disponível"}), 503
            
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "Dados JSON obrigatórios"}), 400
            
            source_chain = data.get('source_chain', 'polygon')
            target_chain = data.get('target_chain', 'ethereum')
            amount = float(data.get('amount', 0.1))
            token_symbol = data.get('token_symbol', 'MATIC')
            recipient_address = data.get('recipient_address', '').strip()
            
            # Validar chains
            valid_chains = ['polygon', 'ethereum', 'bsc', 'base']
            if source_chain not in valid_chains:
                return jsonify({"success": False, "error": f"Chain origem inválida. Use: {', '.join(valid_chains)}"}), 400
            if target_chain not in valid_chains:
                return jsonify({"success": False, "error": f"Chain destino inválida. Use: {', '.join(valid_chains)}"}), 400
            
            if source_chain == target_chain:
                return jsonify({"success": False, "error": "Chain origem e destino devem ser diferentes"}), 400
            
            # Validar amount
            if amount <= 0 or amount > 1000:
                return jsonify({"success": False, "error": "Quantidade deve estar entre 0 e 1000"}), 400
            
            # Validar endereço
            if not recipient_address:
                return jsonify({"success": False, "error": "Endereço do destinatário obrigatório"}), 400
            
            # Validar formato de endereço EVM (básico)
            if target_chain in ['ethereum', 'polygon', 'bsc', 'base']:
                if not recipient_address.startswith('0x') or len(recipient_address) != 42:
                    return jsonify({"success": False, "error": "Endereço EVM inválido (deve começar com 0x e ter 42 caracteres)"}), 400
            
            result = poc_lock.create_lock(
                source_chain=source_chain,
                amount=amount,
                token_symbol=token_symbol,
                target_chain=target_chain,
                recipient_address=recipient_address
            )
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Erro no teste proof-of-lock: {e}")
            error_msg = str(e)
            if "not connected" in error_msg.lower():
                error_msg = "Não foi possível conectar às blockchains. Verifique sua conexão."
            elif "invalid" in error_msg.lower():
                error_msg = "Dados inválidos. Verifique os parâmetros fornecidos."
            return jsonify({"success": False, "error": error_msg}), 500
    
    logger.info("✅ Rotas de teste inicializadas")
    print("🧪 TEST ROUTES: Rotas de teste carregadas!")
    print("   • GET  /test - Página de testes")
    print("   • POST /test/validation/bitcoin - Teste Bitcoin")
    print("   • POST /test/validation/solana - Teste Solana")
    print("   • GET  /test/gas/current - Gas atual")
    print("   • POST /test/gas/predict - Prever spike")
    print("   • POST /test/proof-of-lock - Teste proof-of-lock")

