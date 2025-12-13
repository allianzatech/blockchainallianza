# uec_routes.py - ROTAS UEC COMPLETAS COM INTEROPERABILIDADE REAL
from flask import jsonify, request
import time
import hashlib
import secrets
import random
from datetime import datetime, timedelta

# Esta variável será inicializada no main
uec_system = None

def init_uec_routes(app, blockchain):
    """Inicializa rotas UEC no Flask"""
    global uec_system
    
    try:
        from uec_integration import AllianzaUEC
        uec_system = AllianzaUEC(blockchain)
        print("✅ UEC Routes: Sistema UEC inicializado com interoperabilidade REAL")
    except Exception as e:
        print(f"❌ UEC Routes: Erro ao inicializar UEC: {e}")
        return

    # =============================================================================
    # 🆕 NOVAS ROTAS PARA CONEXÕES REAIS
    # =============================================================================

    @app.route('/uec/real/balance', methods=['POST', 'OPTIONS'])
    def uec_real_balance():
        """💰 Consulta saldo REAL na blockchain"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            
            if not data or "address" not in data or "chain" not in data:
                return jsonify({"success": False, "error": "Campos 'address' e 'chain' são obrigatórios"}), 400
                
            address = data["address"]
            chain = data["chain"]
            
            print(f"🔍 Consultando saldo REAL: {chain} - {address}")
            
            if uec_system:
                balance_result = uec_system.get_real_balance(address, chain)
                return jsonify(balance_result)
            else:
                return jsonify({"success": False, "error": "Sistema UEC não disponível"}), 400
                
        except Exception as e:
            print(f"❌ Erro ao consultar saldo real: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/real/transactions', methods=['POST', 'OPTIONS'])
    def uec_real_transactions():
        """📜 Obtém transações REALs da blockchain"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            
            if not data or "address" not in data or "chain" not in data:
                return jsonify({"success": False, "error": "Campos 'address' e 'chain' são obrigatórios"}), 400
                
            address = data["address"]
            chain = data["chain"]
            limit = data.get("limit", 10)
            
            print(f"📜 Consultando transações REALs: {chain} - {address}")
            
            if uec_system:
                tx_result = uec_system.get_real_transactions(address, chain, limit)
                return jsonify(tx_result)
            else:
                return jsonify({"success": False, "error": "Sistema UEC não disponível"}), 400
                
        except Exception as e:
            print(f"❌ Erro ao obter transações reais: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/real/network/status', methods=['GET', 'OPTIONS'])
    def uec_real_network_status():
        """🔗 Status das redes blockchain reais"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            print("🔗 Consultando status das redes reais...")
            
            if uec_system:
                status_result = uec_system.get_network_status_real()
                return jsonify(status_result)
            else:
                return jsonify({"success": False, "error": "Sistema UEC não disponível"}), 400
                
        except Exception as e:
            print(f"❌ Erro ao obter status da rede real: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/real/connector/status', methods=['GET', 'OPTIONS'])
    def uec_real_connector_status():
        """🔧 Status do connector real"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            from uec_integration import check_real_connector_status
            status = check_real_connector_status()
            print(f"🔧 Status do connector real: {status.get('available', False)}")
            return jsonify(status)
        except Exception as e:
            print(f"❌ Erro ao verificar status do connector: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    # =============================================================================
    # ROTAS DE INTEROPERABILIDADE REAL
    # =============================================================================

    @app.route('/uec/convert/deposit', methods=['POST', 'OPTIONS'])
    def uec_convert_deposit():
        """🔄 Converte moeda REAL para token ponte na Allianza"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            
            # Validação de campos obrigatórios
            required_fields = ["real_chain", "amount", "token_id", "user_address"]
            if not data:
                return jsonify({"success": False, "error": "Nenhum dado JSON fornecido"}), 400
                
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "success": False,
                    "error": f"Campos obrigatórios faltando: {missing_fields}",
                    "required_fields": required_fields
                }), 400
            
            real_chain = data["real_chain"]  # "bitcoin" ou "ethereum"
            real_amount = float(data["amount"])
            token_id = data["token_id"]      # "BTCa" ou "ETHa" 
            user_address = data["user_address"]
            
            print(f"🔄 ROTA: Conversão REAL→TOKEN iniciada")
            print(f"   Chain: {real_chain}, Amount: {real_amount}")
            print(f"   Token: {token_id}, User: {user_address}")
            
            # Processar conversão
            result = uec_system.convert_real_to_token(
                real_chain, real_amount, token_id, user_address
            )
            
            return jsonify(result)
            
        except Exception as e:
            print(f"❌ Erro na conversão depósito: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/convert/withdraw', methods=['POST', 'OPTIONS'])
    def uec_convert_withdraw():
        """🔄 Converte token ponte para moeda REAL"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            
            # Validação de campos obrigatórios
            required_fields = ["token_id", "amount", "real_chain", "real_address", "private_key"]
            if not data:
                return jsonify({"success": False, "error": "Nenhum dado JSON fornecido"}), 400
                
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "success": False,
                    "error": f"Campos obrigatórios faltando: {missing_fields}",
                    "required_fields": required_fields
                }), 400
            
            token_id = data["token_id"]
            token_amount = float(data["amount"]) 
            real_chain = data["real_chain"]
            real_address = data["real_address"]
            private_key_pem = data["private_key"]
            
            print(f"🔄 ROTA: Conversão TOKEN→REAL iniciada")
            print(f"   Token: {token_id}, Amount: {token_amount}")
            print(f"   Chain: {real_chain}, Address: {real_address}")
            
            # Converter chave privada
            private_key = uec_system.pqc_crypto.pem_to_private_key(private_key_pem)
            
            # Processar conversão
            result = uec_system.convert_token_to_real(
                token_id, token_amount, real_chain, real_address, private_key
            )
            
            return jsonify(result)
            
        except Exception as e:
            print(f"❌ Erro na conversão saque: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/reserve/status', methods=['GET', 'OPTIONS'])
    def uec_reserve_status():
        """💰 Retorna status das reservas de interoperabilidade"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            if uec_system:
                reserve_status = uec_system.get_reserve_status()
                return jsonify({
                    "success": True,
                    "reserves": reserve_status,
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Sistema UEC não disponível"
                }), 400
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/wallet/balance/<address>/<token_id>', methods=['GET', 'OPTIONS'])
    def uec_wallet_token_balance(address, token_id):
        """💳 Retorna saldo específico de token na wallet UEC"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            if uec_system:
                balance = uec_system.get_token_balance(address, token_id)
                return jsonify({
                    "success": True,
                    "address": address,
                    "token": token_id,
                    "balance": balance,
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Sistema UEC não disponível"
                }), 400
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # =============================================================================
    # ROTAS UEC ORIGINAIS (MANTIDAS PARA COMPATIBILIDADE)
    # =============================================================================

    @app.route('/uec/create_wallet', methods=['POST'])
    def uec_create_wallet():
        try:
            data = request.get_json()
            blockchain_source = data.get("blockchain_source", "allianza")
            
            address, private_key = uec_system.create_uec_wallet(blockchain_source)
            
            return jsonify({
                "address": address,
                "private_key": uec_system.pqc_crypto.private_key_to_pem(private_key),
                "bitcoin_address": uec_system.blockchain.wallets[address]["bitcoin_address"],
                "uec_enabled": True
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/uec/bridge/transfer', methods=['POST'])
    def uec_bridge_transfer():
        try:
            data = request.get_json()
            
            required_fields = ["token_id", "amount", "external_address", "target_chain", "private_key"]
            if not data:
                return jsonify({"error": "Nenhum dado JSON fornecido"}), 400
                
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "error": f"Campos obrigatórios faltando: {missing_fields}",
                    "required_fields": required_fields,
                    "received_fields": list(data.keys())
                }), 400
            
            token_id = data["token_id"]
            amount = float(data["amount"])
            external_address = data["external_address"]
            target_chain = data["target_chain"]
            private_key_pem = data["private_key"]
            
            print(f"🔧 UEC Bridge: Processando {amount} {token_id} -> {target_chain}")
            print(f"🔧 UEC Bridge: Endereço destino: {external_address}")
            
            private_key = uec_system.pqc_crypto.pem_to_private_key(private_key_pem)
            
            bridge_tx = uec_system.transfer_to_external_chain(
                token_id, amount, external_address, target_chain, private_key
            )
            
            return jsonify({
                "bridge_transaction": bridge_tx,
                "message": "Transferência de bridge iniciada com sucesso"
            })
            
        except Exception as e:
            print(f"❌ Erro na bridge UEC: {e}")
            return jsonify({"error": str(e)}), 400

    @app.route('/uec/bridge/status/<bridge_id>')
    def uec_bridge_status(bridge_id):
        try:
            status = uec_system.get_bridge_status(bridge_id)
            if status:
                return jsonify({"status": status})
            else:
                return jsonify({"error": "Bridge ID não encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/uec/tokens')
    def uec_list_tokens():
        try:
            tokens = uec_system.get_supported_tokens()
            tokens_metadata = {}
            for token_id in tokens:
                tokens_metadata[token_id] = uec_system.get_token_metadata(token_id)
            
            return jsonify({"tokens": tokens_metadata})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/uec/validate_address', methods=['POST'])
    def uec_validate_address():
        try:
            data = request.get_json()
            
            if not data or "address" not in data or "chain" not in data:
                return jsonify({"error": "Campos 'address' e 'chain' são obrigatórios"}), 400
                
            address = data["address"]
            chain = data["chain"]
            
            is_valid = uec_system.validate_external_address(address, chain)
            
            return jsonify({
                "address": address,
                "chain": chain,
                "is_valid": is_valid
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/uec/system/status')
    def uec_system_status():
        try:
            status = {
                "uec_version": "2.0.0",
                "status": "online",
                "pqc_enabled": True,
                "clm_available": ["bitcoin"],
                "supported_tokens": uec_system.get_supported_tokens(),
                "supported_chains": uec_system.cross_chain_bridge["supported_chains"],
                "pending_transfers": len(uec_system.cross_chain_bridge["pending_transfers"]),
                "completed_transfers": len(uec_system.cross_chain_bridge["completed_transfers"]),
                "total_wallets_uec": len([w for w in uec_system.blockchain.wallets.values() if w.get('uec_enabled', False)]),
                "real_interoperability": True,
                "reserve_status": uec_system.get_reserve_status(),
                "real_connector_available": uec_system.real_connector is not None
            }
            return jsonify(status)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/uec/bridge/complete/<bridge_id>', methods=['POST'])
    def uec_complete_bridge(bridge_id):
        """Completa uma transferência de bridge (para testes)"""
        try:
            completed = uec_system.complete_bridge_transfer(bridge_id)
            if completed:
                return jsonify({"completed_transaction": completed})
            else:
                return jsonify({"error": "Bridge ID não encontrado ou já completado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # =============================================================================
    # ROTAS COMPATÍVEIS COM O FRONTEND
    # =============================================================================

    @app.route('/uec/supported_tokens', methods=['GET', 'OPTIONS'])
    def uec_supported_tokens():
        """Rota compatível com frontend - retorna tokens suportados"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            if uec_system:
                tokens = uec_system.get_supported_tokens()
                tokens_metadata = {}
                for token_id in tokens:
                    tokens_metadata[token_id] = uec_system.get_token_metadata(token_id)
                
                return jsonify({"tokens": tokens_metadata, "success": True})
            else:
                # Fallback para tokens simulados
                tokens_metadata = {
                    "BTCa": {
                        "symbol": "BTCa",
                        "name": "Bitcoin Allianza",
                        "decimals": 8,
                        "bridge_supported": True,
                        "price": 45000.0,
                        "real_interoperability": True
                    },
                    "ETHa": {
                        "symbol": "ETHa",
                        "name": "Ethereum Allianza", 
                        "decimals": 18,
                        "bridge_supported": True,
                        "price": 3000.0,
                        "real_interoperability": True
                    },
                    "USDa": {
                        "symbol": "USDa",
                        "name": "USD Allianza",
                        "decimals": 6,
                        "bridge_supported": True,
                        "price": 1.0,
                        "real_interoperability": True
                    }
                }
                return jsonify({"tokens": tokens_metadata, "success": True})
                
        except Exception as e:
            print(f"❌ Erro ao obter tokens: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/transfer', methods=['POST', 'OPTIONS'])
    def uec_transfer():
        """Rota alternativa para /uec/bridge_transfer"""
        return uec_bridge_transfer_compat()
    
    @app.route('/uec/bridge_transfer', methods=['POST', 'OPTIONS'])
    def uec_bridge_transfer_compat():
        """Rota compatível com frontend - transferência bridge"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            
            required_fields = ["token", "amount", "external_address", "target_chain", "private_key"]
            if not data:
                return jsonify({"success": False, "error": "Nenhum dado JSON fornecido"}), 400
                
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "success": False,
                    "error": f"Campos obrigatórios faltando: {missing_fields}",
                    "required_fields": required_fields,
                    "received_fields": list(data.keys())
                }), 400
            
            token = data["token"]
            amount = float(data["amount"])
            external_address = data["external_address"]
            target_chain = data["target_chain"]
            private_key_pem = data["private_key"]
            
            print(f"🌉 UEC Bridge Transfer: {amount} {token} -> {target_chain}")
            print(f"📍 Endereço destino: {external_address}")
            
            if uec_system:
                token_id = token
                private_key = uec_system.pqc_crypto.pem_to_private_key(private_key_pem)
                
                bridge_tx = uec_system.transfer_to_external_chain(
                    token_id, amount, external_address, target_chain, private_key
                )
                
                return jsonify({
                    "success": True,
                    "bridge_transaction": bridge_tx,
                    "message": "Transferência de bridge iniciada com sucesso"
                })
            else:
                # Simular transferência bridge
                bridge_id = f"bridge_{int(time.time())}_{secrets.token_hex(4)}"
                
                bridge_tx = {
                    "bridge_id": bridge_id,
                    "token": token,
                    "amount": amount,
                    "external_address": external_address,
                    "target_chain": target_chain,
                    "status": "pending",
                    "tx_hash": f"0x{secrets.token_hex(32)}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "estimated_completion": (datetime.utcnow() + timedelta(minutes=2)).isoformat()
                }
                
                return jsonify({
                    "success": True,
                    "bridge_transaction": bridge_tx,
                    "message": "Transferência de bridge simulada com sucesso"
                })
            
        except Exception as e:
            print(f"❌ Erro na bridge UEC: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/bridge_status/<bridge_id>', methods=['GET', 'OPTIONS'])
    def uec_bridge_status_compat(bridge_id):
        """Rota compatível com frontend - status da bridge"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            if uec_system:
                status = uec_system.get_bridge_status(bridge_id)
                if status:
                    return jsonify({"success": True, "status": status})
                else:
                    return jsonify({"success": False, "error": "Bridge ID não encontrado"}), 404
            else:
                # Simular status
                statuses = ["pending", "confirmed", "completed", "failed"]
                status = random.choice(statuses)
                
                return jsonify({
                    "success": True,
                    "bridge_id": bridge_id,
                    "status": status,
                    "confirmations": random.randint(0, 10) if status != "pending" else 0,
                    "estimated_completion": (datetime.utcnow() + timedelta(minutes=5)).isoformat() if status == "pending" else None
                })
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/create_wallet', methods=['POST', 'OPTIONS'])
    def uec_create_wallet_compat():
        """Rota compatível com frontend - criar wallet UEC"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            user_id = data.get("user_id", f"user_{int(time.time())}")
            blockchain_source = data.get("blockchain_source", "allianza")
            
            print(f"👛 Criando wallet UEC para: {user_id}")
            
            if uec_system:
                address, private_key = uec_system.create_uec_wallet(blockchain_source)
                
                bitcoin_address = uec_system.blockchain.wallets[address].get("bitcoin_address", "")
                
                response_data = {
                    "success": True,
                    "address": address,
                    "private_key": uec_system.pqc_crypto.private_key_to_pem(private_key),
                    "bitcoin_address": bitcoin_address,
                    "uec_enabled": True,
                    "user_id": user_id
                }
            else:
                # Simular criação de wallet
                address = f"1{secrets.token_hex(20)}"
                private_key_simulated = f"private_key_simulated_{secrets.token_hex(32)}"
                bitcoin_address = f"1{secrets.token_hex(20)}"
                
                response_data = {
                    "success": True,
                    "address": address,
                    "private_key": private_key_simulated,
                    "bitcoin_address": bitcoin_address,
                    "uec_enabled": True,
                    "user_id": user_id,
                    "simulated": True
                }
            
            print(f"✅ Wallet UEC criada: {address}")
            return jsonify(response_data)
            
        except Exception as e:
            print(f"❌ Erro ao criar wallet UEC: {e}")
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/uec/validate_address', methods=['POST', 'OPTIONS'])
    def uec_validate_address_compat():
        """Rota compatível com frontend - validar endereço"""
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            data = request.get_json()
            
            if not data or "address" not in data or "chain" not in data:
                return jsonify({"success": False, "error": "Campos 'address' e 'chain' são obrigatórios"}), 400
                
            address = data["address"]
            chain = data["chain"]
            
            if uec_system:
                is_valid = uec_system.validate_external_address(address, chain)
            else:
                # Simular validação
                if chain == "bitcoin":
                    is_valid = address.startswith("1") or address.startswith("3") or address.startswith("bc1")
                elif chain == "ethereum":
                    is_valid = address.startswith("0x") and len(address) == 42
                else:
                    is_valid = len(address) > 10
            
            return jsonify({
                "success": True,
                "address": address,
                "chain": chain,
                "is_valid": is_valid
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # =============================================================================
    # ROTAS ADICIONAIS DE SUPORTE
    # =============================================================================

    @app.route('/uec/health', methods=['GET'])
    def uec_health():
        """Health check da UEC"""
        return jsonify({
            "status": "healthy",
            "uec_available": uec_system is not None,
            "real_interoperability": True,
            "timestamp": datetime.utcnow().isoformat()
        })

    @app.route('/uec/wallet_info/<address>', methods=['GET'])
    def uec_wallet_info(address):
        """Informações da wallet UEC"""
        try:
            if uec_system and address in uec_system.blockchain.wallets:
                wallet = uec_system.blockchain.wallets[address]
                return jsonify({
                    "success": True,
                    "address": address,
                    "balance": wallet.get("ALZ", 0),
                    "uec_enabled": wallet.get("uec_enabled", False),
                    "bitcoin_address": wallet.get("bitcoin_address", ""),
                    "blockchain_source": wallet.get("blockchain_source", "allianza"),
                    # 🆕 CAMPOS DE TOKENS
                    "BTCa": wallet.get("BTCa", 0),
                    "ETHa": wallet.get("ETHa", 0),
                    "USDa": wallet.get("USDa", 0)
                })
            else:
                return jsonify({"success": False, "error": "Wallet não encontrada"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    print("✅ UEC Routes: ATUALIZADO - INTEROPERABILIDADE REAL COMPLETA")
    print("🔗 Rotas principais:")
    print("   - POST /uec/convert/deposit     🔄 REAL → TOKEN")
    print("   - POST /uec/convert/withdraw    🔄 TOKEN → REAL") 
    print("   - GET  /uec/reserve/status      💰 Status reservas")
    print("   - GET  /uec/wallet/balance/<addr>/<token> 💳 Saldo token")
    print("   - POST /uec/real/balance        💰 Saldo REAL")
    print("   - POST /uec/real/transactions   📜 Transações REAIS")
    print("   - GET  /uec/real/network/status 🔗 Status redes")
    print("   - GET  /uec/real/connector/status 🔧 Status connector")
    print("   - GET  /uec/supported_tokens    🎯 Tokens suportados")
    print("   - POST /uec/bridge_transfer     🌉 Transferência bridge")
    print("   - POST /uec/create_wallet       👛 Criar wallet")

# Função para verificar se UEC está disponível
def is_uec_available():
    return uec_system is not None

def get_uec_system():
    return uec_system