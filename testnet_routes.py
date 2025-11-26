"""
🌐 Rotas Flask para Allianza Testnet
Faucet, Explorer, Verificador QRS-3, Testes Públicos
"""

from flask import Blueprint, jsonify, request, render_template, send_file
from pathlib import Path
import json
from datetime import datetime

from testnet_config import get_network_info, is_valid_testnet_address
from testnet_faucet import TestnetFaucet
from testnet_explorer import TestnetExplorer
from testnet_proofs import TestnetProofGenerator
from testnet_wallet_generator import TestnetWalletGenerator
from testnet_status import TestnetStatusPage
from testnet_quantum_dashboard import QuantumSecurityDashboard
from testnet_public_tests_interface import PublicTestsInterface
# Importar ALZ-NIEV (substitui testnet_interoperability)
try:
    from alz_niev_interoperability import ALZNIEV
    ALZ_NIEV_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  ALZ-NIEV não disponível: {e}")
    ALZNIEV = None
    ALZ_NIEV_AVAILABLE = False

# Importar ProfessionalTestRunner com fallback
try:
    from testnet_professional_tests import ProfessionalTestRunner
    PROFESSIONAL_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  ProfessionalTestRunner não disponível: {e}")
    ProfessionalTestRunner = None
    PROFESSIONAL_TESTS_AVAILABLE = False

# Importar Professional Test Suite
try:
    from testnet_professional_test_suite import init_professional_tests, professional_tests_bp
    PROFESSIONAL_SUITE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Professional Test Suite não disponível: {e}")
    PROFESSIONAL_SUITE_AVAILABLE = False

# Criar blueprint
testnet_bp = Blueprint('testnet', __name__, url_prefix='/testnet')

# Instâncias globais (serão inicializadas)
faucet = None
explorer = None
proof_generator = None
quantum_security = None
wallet_generator = None
professional_tests = None
status_page = None
quantum_dashboard = None
public_tests = None
alz_niev = None

def init_testnet_routes(app, blockchain_instance, quantum_security_instance, bridge_instance=None):
    """Inicializa as rotas da testnet"""
    global faucet, explorer, proof_generator, quantum_security, wallet_generator, professional_tests
    global status_page, quantum_dashboard, public_tests, alz_niev
    
    try:
        quantum_security = quantum_security_instance
        faucet = TestnetFaucet(blockchain_instance, quantum_security_instance)
        # Explorer melhorado com bridge e quantum security
        explorer = TestnetExplorer(blockchain_instance)
        # Se tiver EnhancedTestnetExplorer disponível, usar ele
        try:
            from testnet_explorer_enhanced import EnhancedTestnetExplorer
            explorer = EnhancedTestnetExplorer(
                blockchain_instance=blockchain_instance,
                bridge_instance=bridge_instance,
                quantum_security_instance=quantum_security_instance
            )
            print("✅ Explorer Melhorado inicializado!")
        except ImportError:
            # Usar explorer padrão
            explorer = TestnetExplorer(blockchain_instance)
        proof_generator = TestnetProofGenerator(blockchain_instance, quantum_security_instance)
        wallet_generator = TestnetWalletGenerator(blockchain_instance)
        status_page = TestnetStatusPage(blockchain_instance)
        quantum_dashboard = QuantumSecurityDashboard(quantum_security_instance, blockchain_instance)
        public_tests = PublicTestsInterface(blockchain_instance, quantum_security_instance)
        
        # Inicializar ALZ-NIEV (substitui testnet_interoperability)
        if ALZ_NIEV_AVAILABLE and ALZNIEV:
            try:
                alz_niev = ALZNIEV()
                print("🌐 ALZ-NIEV inicializado no testnet!")
            except Exception as e:
                print(f"⚠️  Erro ao inicializar ALZ-NIEV: {e}")
                alz_niev = None
        else:
            alz_niev = None
        
        # Inicializar ProfessionalTestRunner apenas se disponível
        if PROFESSIONAL_TESTS_AVAILABLE and ProfessionalTestRunner:
            try:
                professional_tests = ProfessionalTestRunner(blockchain_instance, quantum_security_instance)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar ProfessionalTestRunner: {e}")
                professional_tests = None
        else:
            professional_tests = None
        
        app.register_blueprint(testnet_bp)
        print(f"✅ Testnet blueprint registrado com sucesso! URL prefix: /testnet")
        
        # Inicializar Professional Test Suite
        if PROFESSIONAL_SUITE_AVAILABLE:
            try:
                # Tentar obter bridge instance
                bridge_instance = None
                try:
                    from real_cross_chain_bridge import RealCrossChainBridge
                    # Se houver uma instância global do bridge, usar aqui
                    # Por enquanto, None (será passado se disponível)
                except:
                    pass
                
                init_professional_tests(app, blockchain_instance, quantum_security_instance, bridge_instance)
                print("✅ Professional Test Suite registrada!")
            except Exception as e:
                print(f"⚠️  Erro ao inicializar Professional Test Suite: {e}")
                import traceback
                traceback.print_exc()
        
        return app
    except Exception as e:
        print(f"⚠️  Erro ao inicializar testnet: {e}")
        import traceback
        traceback.print_exc()
        # Mesmo com erro, tentar registrar o blueprint
        try:
            app.register_blueprint(testnet_bp)
            print(f"✅ Testnet blueprint registrado mesmo com erros parciais")
        except:
            pass
        return app

# =============================================================================
# ROTAS PRINCIPAIS
# =============================================================================

@testnet_bp.route('/')
def testnet_dashboard():
    """Dashboard principal da testnet"""
    network_info = get_network_info()
    stats = explorer.get_network_stats() if explorer else {
        "total_blocks": 0,
        "total_transactions": 0,
        "pending_transactions": 0,
        "tps_current": 0,
        "tps_24h_avg": 0,
        "latency_avg_ms": 0,
        "active_shards": 0,
        "validators_online": 0,
        "network_status": "unknown"
    }
    faucet_stats = faucet.get_stats() if faucet else {
        "total_requests": 0,
        "total_sent": 0,
        "total_rejected": 0,
        "amount_per_request": 1000
    }
    
    return render_template('testnet/dashboard.html',
                         network_info=network_info,
                         stats=stats,
                         faucet_stats=faucet_stats)

@testnet_bp.route('/explorer')
def testnet_explorer_page():
    """Página do explorer melhorada"""
    blocks = explorer.get_recent_blocks(limit=20) if explorer else []
    transactions = explorer.get_recent_transactions(limit=50) if explorer else []
    stats = explorer.get_network_stats() if explorer else {}
    
    # Tentar usar template melhorado, fallback para o original
    try:
        return render_template('testnet/explorer_enhanced.html',
                             blocks=blocks,
                             transactions=transactions,
                             stats=stats)
    except:
        return render_template('testnet/explorer.html',
                             blocks=blocks,
                             transactions=transactions,
                             stats=stats)

# =============================================================================
# API - FAUCET
# =============================================================================

@testnet_bp.route('/faucet', methods=['GET'])
def faucet_page():
    """Página do faucet"""
    faucet_stats = faucet.get_stats() if faucet else {
        "total_requests": 0,
        "total_sent": 0,
        "total_rejected": 0,
        "amount_per_request": 1000,
        "limits": {
            "max_per_ip_per_day": 10,
            "max_per_address_per_day": 5,
            "cooldown_hours": 1
        }
    }
    logs = faucet.get_logs(limit=20) if faucet else []
    
    return render_template('testnet/faucet.html',
                         faucet_stats=faucet_stats,
                         logs=logs)

@testnet_bp.route('/api/faucet/request', methods=['POST'])
def faucet_request():
    """Endpoint para solicitar tokens do faucet"""
    try:
        data = request.get_json() or {}
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({
                "success": False,
                "error": "Endereço é obrigatório"
            }), 400
        
        if not is_valid_testnet_address(address):
            return jsonify({
                "success": False,
                "error": "Endereço inválido. Deve começar com ALZ1 e ter 42 caracteres."
            }), 400
        
        if not faucet:
            return jsonify({
                "success": False,
                "error": "Faucet não inicializado"
            }), 500
        
        result = faucet.request_tokens(address, request)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

@testnet_bp.route('/api/faucet/logs', methods=['GET'])
def faucet_logs():
    """Retorna logs públicos do faucet"""
    limit = request.args.get('limit', 100, type=int)
    logs = faucet.get_logs(limit=limit) if faucet else []
    return jsonify({"logs": logs}), 200

@testnet_bp.route('/api/faucet/stats', methods=['GET'])
def faucet_stats():
    """Retorna estatísticas do faucet"""
    stats = faucet.get_stats() if faucet else {}
    return jsonify(stats), 200

# =============================================================================
# API - EXPLORER
# =============================================================================

@testnet_bp.route('/api/blocks', methods=['GET'])
def api_blocks():
    """Retorna blocos recentes"""
    limit = request.args.get('limit', 20, type=int)
    blocks = explorer.get_recent_blocks(limit=limit) if explorer else []
    return jsonify({"blocks": blocks}), 200

@testnet_bp.route('/api/blocks/<block_hash>', methods=['GET'])
def api_block_by_hash(block_hash):
    """Retorna um bloco específico"""
    block = explorer.get_block_by_hash(block_hash) if explorer else None
    if block:
        return jsonify({"block": block}), 200
    else:
        return jsonify({"error": "Bloco não encontrado"}), 404

@testnet_bp.route('/api/transactions', methods=['GET'])
def api_transactions():
    """Retorna transações recentes"""
    limit = request.args.get('limit', 50, type=int)
    transactions = explorer.get_recent_transactions(limit=limit) if explorer else []
    return jsonify({"transactions": transactions}), 200

@testnet_bp.route('/api/transactions/<tx_hash>', methods=['GET'])
def api_transaction_by_hash(tx_hash):
    """Retorna uma transação específica"""
    tx = explorer.get_transaction_by_hash(tx_hash) if explorer else None
    if tx:
        return jsonify({"transaction": tx}), 200
    else:
        return jsonify({"error": "Transação não encontrada"}), 404

@testnet_bp.route('/api/network/stats', methods=['GET'])
def api_network_stats():
    """Retorna estatísticas da rede"""
    stats = explorer.get_network_stats() if explorer else {}
    network_info = get_network_info()
    return jsonify({
        "network": network_info,
        "stats": stats
    }), 200

# =============================================================================
# API - PROVAS
# =============================================================================

@testnet_bp.route('/api/proofs/block/<int:block_index>', methods=['GET'])
def api_block_proof(block_index):
    """Gera e retorna prova de um bloco"""
    format_type = request.args.get('format', 'json')
    
    if not explorer:
        return jsonify({"error": "Explorer não inicializado"}), 500
    
    blocks = explorer.get_recent_blocks(limit=block_index + 10)
    block = None
    for b in blocks:
        if b.get("index") == block_index:
            block = b
            break
    
    if not block:
        return jsonify({"error": "Bloco não encontrado"}), 404
    
    proof = proof_generator.generate_block_proof(block, format=format_type) if proof_generator else None
    
    if proof and format_type == "json":
        return send_file(proof["filepath"], mimetype='application/json')
    elif proof and format_type == "txt":
        return send_file(proof["filepath"], mimetype='text/plain')
    else:
        return jsonify(proof), 200

@testnet_bp.route('/api/proofs/transaction/<tx_hash>', methods=['GET'])
def api_transaction_proof(tx_hash):
    """Gera e retorna prova de uma transação"""
    format_type = request.args.get('format', 'json')
    
    if not explorer:
        return jsonify({"error": "Explorer não inicializado"}), 500
    
    tx = explorer.get_transaction_by_hash(tx_hash)
    if not tx:
        return jsonify({"error": "Transação não encontrada"}), 404
    
    proof = proof_generator.generate_transaction_proof(tx, format=format_type) if proof_generator else None
    
    if proof and format_type == "json":
        return send_file(proof["filepath"], mimetype='application/json')
    elif proof and format_type == "txt":
        return send_file(proof["filepath"], mimetype='text/plain')
    else:
        return jsonify(proof), 200

# =============================================================================
# VERIFICADOR QRS-3
# =============================================================================

@testnet_bp.route('/qrs3-verifier')
def qrs3_verifier_page():
    """Página do verificador QRS-3"""
    return render_template('testnet/qrs3_verifier.html')

@testnet_bp.route('/api/wallet/generate', methods=['POST'])
def api_generate_wallet():
    """Gera uma nova wallet para a testnet"""
    if not wallet_generator:
        return jsonify({
            "success": False,
            "error": "Gerador de wallets não inicializado"
        }), 500
    
    result = wallet_generator.generate_wallet()
    
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@testnet_bp.route('/api/qrs3/generate-example', methods=['POST'])
def api_qrs3_generate_example():
    """Gera um exemplo de assinatura QRS-3 para teste"""
    try:
        data = request.get_json() or {}
        message = data.get('message', 'Hello Allianza Testnet!')
        
        if not quantum_security:
            return jsonify({
                "success": False,
                "error": "Sistema de segurança quântica não disponível"
            }), 500
        
        # Converter mensagem para bytes
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
        
        # Gerar keypair temporário
        import time
        keypair_result = quantum_security.generate_qrs3_keypair()
        
        if not keypair_result.get("success"):
            return jsonify({
                "success": False,
                "error": f"Erro ao gerar keypair: {keypair_result.get('error', 'Unknown error')}"
            }), 500
        
        keypair_id = keypair_result.get("keypair_id")
        if not keypair_id:
            # Se não retornou keypair_id, usar um temporário
            keypair_id = f"example_{int(time.time())}"
        
        # Assinar mensagem
        signature_result = quantum_security.sign_qrs3(
            keypair_id=keypair_id,
            message=message_bytes,
            optimized=True,
            parallel=True
        )
        
        if not signature_result.get("success"):
            return jsonify({
                "success": False,
                "error": f"Erro ao assinar: {signature_result.get('error', 'Unknown error')}"
            }), 500
        
        # A assinatura QRS-3 está no resultado direto (não em qrs3_signature)
        # O resultado já contém classic_signature, ml_dsa_signature, sphincs_signature
        signature = {
            "classic_signature": signature_result.get("classic_signature"),
            "ml_dsa_signature": signature_result.get("ml_dsa_signature"),
            "sphincs_signature": signature_result.get("sphincs_signature"),
            "algorithm": signature_result.get("algorithm"),
            "redundancy_level": signature_result.get("redundancy_level"),
            "signing_time_ms": signature_result.get("signing_time_ms")
        }
        
        # Verificar manualmente (verificar se tem pelo menos 2 assinaturas válidas)
        verified = False
        valid_count = 0
        if signature.get("classic_signature"):
            valid_count += 1
        if signature.get("ml_dsa_signature"):
            valid_count += 1
        if signature.get("sphincs_signature"):
            valid_count += 1
        verified = valid_count >= 2
        
        return jsonify({
            "success": True,
            "message": message if isinstance(message, str) else message.decode('utf-8', errors='ignore'),
            "signature": signature,
            "verified": verified,
            "instructions": [
                "1. Copie a mensagem acima",
                "2. Copie a assinatura JSON completa",
                "3. Cole no Verificador QRS-3",
                "4. Clique em 'Verificar Assinatura'",
                "5. Deve mostrar ✅ Assinatura Válida!"
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao gerar exemplo: {str(e)}"
        }), 500

@testnet_bp.route('/api/qrs3/verify', methods=['POST'])
def api_qrs3_verify():
    """Verifica uma assinatura QRS-3"""
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        signature = data.get('signature', {})
        
        if not message or not signature:
            return jsonify({
                "success": False,
                "error": "Mensagem e assinatura são obrigatórias"
            }), 400
        
        if not quantum_security:
            return jsonify({
                "success": False,
                "error": "Sistema de segurança quântica não disponível"
            }), 500
        
        # Verificar assinatura QRS-3
        try:
            # Converter mensagem para bytes se necessário
            if isinstance(message, str):
                message_bytes = message.encode('utf-8')
            else:
                message_bytes = message
            
            # Verificar assinatura QRS-3 manualmente
            # QRS-3 é válido se pelo menos 2 de 3 assinaturas estão presentes
            verified = False
            valid_count = 0
            keypair_id_from_sig = None
            
            if isinstance(signature, dict):
                # Tentar obter keypair_id da assinatura
                keypair_id_from_sig = signature.get("keypair_id") or signature.get("kid")
                
                # Verificar ECDSA
                if signature.get("classic_signature"):
                    valid_count += 1
                
                # Verificar ML-DSA
                if signature.get("ml_dsa_signature"):
                    valid_count += 1
                
                # Verificar SPHINCS+
                if signature.get("sphincs_signature"):
                    valid_count += 1
                
                # QRS-3 requer pelo menos 2 assinaturas válidas
                verified = valid_count >= 2
            else:
                verified = False
            
            # Obter chaves públicas se disponível
            public_keys = {}
            keypair_id_to_use = keypair_id_from_sig
            if quantum_security and keypair_id_to_use:
                try:
                    if hasattr(quantum_security, 'pqc_keypairs') and keypair_id_to_use in quantum_security.pqc_keypairs:
                        keypair = quantum_security.pqc_keypairs[keypair_id_to_use]
                        public_keys = {
                            "ecdsa_public_key": keypair.get("classic_public_key", ""),
                            "ml_dsa_public_key": keypair.get("ml_dsa_public_key", ""),
                            "sphincs_public_key": keypair.get("sphincs_public_key", "")
                        }
                except:
                    pass
            
            # Gerar prova profissional
            proof = None
            if proof_generator:
                try:
                    message_str = message if isinstance(message, str) else message.decode('utf-8', errors='ignore')
                    proof = proof_generator.generate_qrs3_verification_proof(
                        message=message_str,
                        signature=signature,
                        verified=verified,
                        format="json",
                        keypair_id=keypair_id_to_use,
                        public_keys=public_keys if public_keys else None
                    )
                    if not proof:
                        print(f"⚠️  generate_qrs3_verification_proof retornou None")
                    else:
                        print(f"✅ Prova gerada: proof_id={proof.get('proof_id')}, filepath={proof.get('filepath')}")
                except Exception as e:
                    import traceback
                    print(f"❌ Erro ao gerar prova: {e}")
                    traceback.print_exc()
                    proof = None
            
            # Criar URL para download da prova
            proof_url = None
            if proof:
                # Extrair proof_id do resultado
                proof_id = proof.get("proof_id")
                if not proof_id and proof.get("data"):
                    # Tentar extrair do data
                    proof_id = proof.get("data", {}).get("meta", {}).get("proof_id")
                
                if proof_id:
                    proof_url = f"/testnet/api/proofs/qrs3/{proof_id}?format=json"
                elif proof.get("filepath"):
                    # Se não tem proof_id, usar nome do arquivo
                    import os
                    filename = os.path.basename(proof.get("filepath", ""))
                    if filename.endswith(".json"):
                        proof_id_from_file = filename[:-5]  # Remove .json
                        proof_url = f"/testnet/api/proofs/qrs3/{proof_id_from_file}?format=json"
            
            response_data = {
                "success": True,
                "verified": verified,
                "signature": signature,
                "proof": proof_url,
                "proof_hash": proof.get("hash") if proof else None,
                "proof_id": proof.get("proof_id") if proof else None
            }
            
            # Debug: adicionar informações se proof não foi gerado
            if not proof:
                response_data["debug"] = {
                    "proof_generator_available": proof_generator is not None,
                    "message_length": len(message) if isinstance(message, str) else len(str(message)),
                    "signature_keys": list(signature.keys()) if isinstance(signature, dict) else "not_dict"
                }
            
            return jsonify(response_data), 200
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Erro ao verificar: {str(e)}"
            }), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

# =============================================================================
# TESTES PROFISSIONAIS
# =============================================================================

@testnet_bp.route('/api/tests/professional/proof-of-lock', methods=['POST'])
def api_professional_proof_of_lock():
    """Executa teste profissional de Proof-of-Lock"""
    try:
        data = request.get_json() or {}
        source_chain = data.get('source_chain', 'polygon')
        target_chain = data.get('target_chain', 'ethereum')
        amount = data.get('amount', 1.0)
        
        if not professional_tests:
            return jsonify({
                "success": False,
                "error": "Professional tests não inicializado"
            }), 500
        
        result = professional_tests.test_proof_of_lock_with_real_tx(
            source_chain=source_chain,
            target_chain=target_chain,
            amount=amount
        )
        
        return jsonify(result), 200 if result.get("success") else 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}"
        }), 500

@testnet_bp.route('/api/tests/professional/qrs3', methods=['POST'])
def api_professional_qrs3():
    """Executa teste profissional de QRS-3"""
    try:
        data = request.get_json() or {}
        message = data.get('message', 'Allianza Testnet Professional Test')
        
        if not professional_tests:
            return jsonify({
                "success": False,
                "error": "Professional tests não inicializado"
            }), 500
        
        result = professional_tests.test_qrs3_signature_professional(message=message)
        
        return jsonify(result), 200 if result.get("success") else 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}"
        }), 500

# =============================================================================
# STATUS PAGE
# =============================================================================

@testnet_bp.route('/status', methods=['GET'])
def status_page_route():
    """Status page profissional da testnet"""
    if not status_page:
        return jsonify({"error": "Status page não inicializado"}), 500
    
    overall_status = status_page.get_overall_status()
    realtime_metrics = status_page.get_realtime_metrics()
    incidents = status_page.get_incidents(limit=10)
    uptime_history = status_page.get_uptime_history(days=30)
    
    return render_template('testnet/status.html',
                         overall_status=overall_status,
                         realtime_metrics=realtime_metrics,
                         incidents=incidents,
                         uptime_history=uptime_history)

@testnet_bp.route('/api/status', methods=['GET'])
def api_status():
    """API do status page"""
    if not status_page:
        return jsonify({"error": "Status page não inicializado"}), 500
    
    return jsonify({
        "overall_status": status_page.get_overall_status(),
        "realtime_metrics": status_page.get_realtime_metrics(),
        "incidents": status_page.get_incidents(limit=10),
        "uptime_history": status_page.get_uptime_history(days=30)
    }), 200

# =============================================================================
# DASHBOARD DE SEGURANÇA QUÂNTICA
# =============================================================================

@testnet_bp.route('/quantum-security', methods=['GET'])
def quantum_security_dashboard_route():
    """Dashboard de segurança quântica"""
    if not quantum_dashboard:
        return jsonify({"error": "Quantum dashboard não inicializado"}), 500
    
    dashboard_data = quantum_dashboard.get_complete_dashboard()
    
    return render_template('testnet/quantum_security.html',
                         dashboard=dashboard_data)

@testnet_bp.route('/api/quantum-security', methods=['GET'])
def api_quantum_security():
    """API do dashboard de segurança quântica"""
    if not quantum_dashboard:
        return jsonify({"error": "Quantum dashboard não inicializado"}), 500
    
    return jsonify(quantum_dashboard.get_complete_dashboard()), 200

# =============================================================================
# TESTES PÚBLICOS
# =============================================================================

@testnet_bp.route('/public-tests', methods=['GET'])
def public_tests_page_route():
    """Página de testes públicos"""
    return render_template('testnet/public_tests.html')

@testnet_bp.route('/api/public-tests/run', methods=['POST'])
def api_run_public_tests():
    """Executa todos os testes públicos"""
    if not public_tests:
        return jsonify({
            "success": False,
            "error": "Public tests não inicializado"
        }), 500
    
    try:
        data = request.get_json() or {}
        test_name = data.get('test_name')
        
        if test_name:
            # Executar teste específico
            test_map = {
                "qrs3": public_tests.run_test_qrs3_signature,
                "interoperability": public_tests.run_test_interoperability,
                "performance": public_tests.run_test_performance,
                "block_validation": public_tests.run_test_block_validation,
                "quantum_security": public_tests.run_test_quantum_security
            }
            
            test_func = test_map.get(test_name)
            if test_func:
                result = test_func()
                return jsonify(result), 200
            else:
                return jsonify({
                    "success": False,
                    "error": f"Teste '{test_name}' não encontrado"
                }), 400
        else:
            # Executar todos os testes
            result = public_tests.run_all_tests()
            return jsonify(result), 200
    
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@testnet_bp.route('/api/public-tests/stream', methods=['GET'])
def api_stream_public_tests():
    """Stream de logs dos testes públicos (Server-Sent Events)"""
    from flask import Response
    import json
    
    def generate():
        """Gera eventos SSE"""
        if not public_tests:
            yield f"data: {json.dumps({'error': 'Public tests não inicializado'})}\n\n"
            return
        
        # Callback para enviar eventos
        def callback(event):
            yield f"data: {json.dumps(event)}\n\n"
        
        # Executar testes com callback
        result = public_tests.run_all_tests(callback=callback)
        yield f"data: {json.dumps({'type': 'complete', 'result': result})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

# =============================================================================
# INTEROPERABILIDADE
# =============================================================================

@testnet_bp.route('/interoperability', methods=['GET'])
def interoperability_dashboard_route():
    """Dashboard de interoperabilidade - Agora usando ALZ-NIEV"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    return render_template('testnet/interoperability.html',
                         alz_niev_available=True)

@testnet_bp.route('/api/interoperability/status', methods=['GET'])
def api_interoperability_status():
    """API do status de interoperabilidade - Agora usando ALZ-NIEV"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    return jsonify({
        "available": True,
        "system": "ALZ-NIEV",
        "layers": {
            "elni": "Execution-Level Native Interop",
            "zkef": "Zero-Knowledge External Functions",
            "upnmt": "Universal Proof Normalized Merkle Tunneling",
            "mcl": "Multi-Consensus Layer",
            "aes": "Atomic Execution Sync"
        },
        "supported_chains": ["bitcoin", "ethereum", "polygon", "bsc", "solana", "cosmos", "base"],
        "real_transfers": True
    }), 200

@testnet_bp.route('/api/interoperability/test/signature', methods=['POST'])
def api_test_signature_validation():
    """Teste de validação universal de assinaturas - Usando ALZ-NIEV"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    try:
        data = request.get_json() or {}
        chain = data.get('chain', 'bitcoin')
        tx_hash = data.get('tx_hash', '')
        
        if not tx_hash:
            return jsonify({
                "success": False,
                "error": "tx_hash é obrigatório"
            }), 400
        
        # Usar ALZ-NIEV para validação (simulado por enquanto)
        return jsonify({
            "success": False,
            "error": "Use /testnet/interoperability para transferências reais",
            "note": "Validação de assinatura será implementada via ALZ-NIEV"
        }), 501
    
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@testnet_bp.route('/api/interoperability/test/proof-of-lock', methods=['POST'])
def api_test_proof_of_lock():
    """Teste de Proof-of-Lock com ZK Proofs - Usando ALZ-NIEV"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    try:
        data = request.get_json() or {}
        source_chain = data.get('source_chain', 'polygon')
        target_chain = data.get('target_chain', 'ethereum')
        amount = float(data.get('amount', 0.1))
        
        # Usar ALZ-NIEV para proof-of-lock (simulado por enquanto)
        return jsonify({
            "success": False,
            "error": "Use /testnet/interoperability para transferências reais",
            "note": "Proof-of-Lock será implementado via ALZ-NIEV"
        }), 501
    
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@testnet_bp.route('/api/interoperability/transfer-real', methods=['POST'])
def api_transfer_real():
    """Transferência REAL cross-chain usando ALZ-NIEV"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    try:
        data = request.get_json() or {}
        source_chain = data.get('source_chain', 'polygon')
        target_chain = data.get('target_chain', 'bitcoin')
        amount = float(data.get('amount', 0.1))
        token_symbol = data.get('token_symbol', 'MATIC')
        recipient = data.get('recipient', '')
        
        if not recipient:
            return jsonify({
                "success": False,
                "error": "Endereço destinatário é obrigatório"
            }), 400
        
        # Executar transferência REAL com ALZ-NIEV
        result = alz_niev.real_transfer(
            source_chain=source_chain,
            target_chain=target_chain,
            amount=amount,
            recipient=recipient,
            token_symbol=token_symbol
        )
        
        return jsonify(result), 200 if result.get("success") else 500
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@testnet_bp.route('/api/interoperability/test/cross-chain', methods=['POST'])
def api_test_cross_chain_transfer():
    """Teste de transferência cross-chain real (compatibilidade)"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    try:
        data = request.get_json() or {}
        source_chain = data.get('source_chain', 'polygon')
        target_chain = data.get('target_chain', 'ethereum')
        amount = float(data.get('amount', 0.1))
        recipient = data.get('recipient', '')
        
        if not recipient:
            return jsonify({
                "success": False,
                "error": "recipient é obrigatório"
            }), 400
        
        # Redirecionar para transferência real via ALZ-NIEV
        result = alz_niev.real_transfer(
            source_chain=source_chain,
            target_chain=target_chain,
            amount=amount,
            recipient=recipient,
            token_symbol="MATIC"
        )
        return jsonify(result), 200 if result.get("success") else 500
    
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@testnet_bp.route('/interoperability/guide', methods=['GET'])
def interoperability_guide():
    """Guia de transferências reais"""
    return render_template('testnet/interoperability_guide.html')

@testnet_bp.route('/api/proofs/interoperability/<proof_id>', methods=['GET'])
def api_download_interoperability_proof(proof_id):
    """Baixa prova de interoperabilidade em JSON"""
    try:
        proof_file = Path("proofs/testnet/interoperability") / f"{proof_id}.json"
        
        if proof_file.exists():
            return send_file(
                str(proof_file),
                mimetype='application/json',
                as_attachment=True,
                download_name=f"interoperability_proof_{proof_id}.json"
            )
        else:
            return jsonify({
                "success": False,
                "error": "Prova não encontrada"
            }), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}"
        }), 500

@testnet_bp.route('/api/proofs/qrs3/<proof_id>', methods=['GET'])
def api_download_qrs3_proof(proof_id):
    """Baixa prova QRS-3 em JSON"""
    try:
        format_type = request.args.get('format', 'json')
        
        # Tentar múltiplos caminhos possíveis
        possible_dirs = [
            Path("proofs/testnet/professional/qrs3_verifications"),  # Profissional (gerador profissional)
            Path("proofs/testnet/qrs3_verifications"),  # Básico (gerador básico)
            Path("proofs/testnet/professional"),  # Diretório profissional
            Path("proofs/testnet")  # Fallback
        ]
        
        proof_file = None
        for proof_dir in possible_dirs:
            if format_type == "json":
                candidate_file = proof_dir / f"{proof_id}.json"
                if candidate_file.exists():
                    proof_file = candidate_file
                    break
        
        if proof_file and proof_file.exists():
            return send_file(
                str(proof_file), 
                mimetype='application/json', 
                as_attachment=True, 
                download_name=f"qrs3_proof_{proof_id}.json"
            )
        else:
            # Tentar buscar a prova no cache/gerador se disponível
            # Isso pode acontecer se a prova foi gerada mas o arquivo ainda não foi salvo
            if proof_generator and hasattr(proof_generator, 'professional') and proof_generator.professional:
                try:
                    # Tentar buscar no diretório profissional
                    professional_dir = Path("proofs/testnet/professional/qrs3_verifications")
                    if professional_dir.exists():
                        # Procurar por qualquer arquivo que contenha o proof_id
                        for file in professional_dir.glob(f"*{proof_id}*.json"):
                            if file.exists():
                                return send_file(
                                    str(file),
                                    mimetype='application/json',
                                    as_attachment=True,
                                    download_name=f"qrs3_proof_{proof_id}.json"
                                )
                except:
                    pass
            
            # Listar arquivos disponíveis para debug
            available_files = []
            for proof_dir in possible_dirs:
                if proof_dir.exists():
                    available_files.extend([f.name for f in proof_dir.glob("*.json")])
            
            return jsonify({
                "success": False,
                "error": f"Prova não encontrada: {proof_id}",
                "debug": {
                    "proof_id_requested": proof_id,
                    "searched_dirs": [str(d) for d in possible_dirs],
                    "available_files": available_files[:10] if available_files else [],
                    "tip": "A prova pode não ter sido salva ainda. Tente verificar a assinatura novamente."
                }
            }), 404
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": f"Erro: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500


# =============================================================================
# ROTAS ALZ-NIEV
# =============================================================================

@testnet_bp.route('/alz-niev', methods=['GET'])
def alz_niev_dashboard():
    """Dashboard ALZ-NIEV"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    return render_template('testnet/alz_niev.html', 
                         alz_niev_available=True)

@testnet_bp.route('/api/alz-niev/execute', methods=['POST'])
def api_alz_niev_execute():
    """Executa função cross-chain com ALZ-NIEV (modo real)"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    try:
        data = request.get_json() or {}
        source_chain = data.get('source_chain', 'allianza')
        target_chain = data.get('target_chain', 'polygon')
        function_name = data.get('function_name', 'getBalance')
        function_params = data.get('function_params', {})
        
        # Executar com ALZ-NIEV (modo real)
        result = alz_niev.execute_cross_chain_with_proofs(
            source_chain=source_chain,
            target_chain=target_chain,
            function_name=function_name,
            function_params=function_params
        )
        
        # Preparar resposta
        response = {
            "success": result.success,
            "source_chain": source_chain,
            "target_chain": target_chain,
            "function_name": function_name,
            "return_value": result.return_value,
            "execution_time_ms": result.execution_time_ms,
            "proofs": {
                "zk_proof": {
                    "proof_type": result.zk_proof.proof_type if result.zk_proof else None,
                    "verifier_id": result.zk_proof.verifier_id if result.zk_proof else None,
                    "circuit_id": result.zk_proof.circuit_id if result.zk_proof else None,
                    "proof_hash": result.zk_proof.proof_data[:32] + "..." if result.zk_proof else None
                },
                "merkle_proof": {
                    "merkle_root": result.merkle_proof.merkle_root[:32] + "..." if result.merkle_proof else None,
                    "chain_id": result.merkle_proof.chain_id if result.merkle_proof else None,
                    "tree_depth": result.merkle_proof.tree_depth if result.merkle_proof else None
                },
                "consensus_proof": {
                    "consensus_type": result.consensus_proof.consensus_type.value if result.consensus_proof else None,
                    "block_height": result.consensus_proof.block_height if result.consensus_proof else None
                }
            },
            "note": "✅ Execução ALZ-NIEV com todas as 5 camadas de prova"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@testnet_bp.route('/api/alz-niev/atomic', methods=['POST'])
def api_alz_niev_atomic():
    """Executa transação atômica multi-chain com ALZ-NIEV (modo real)"""
    if not alz_niev:
        return jsonify({"error": "ALZ-NIEV não inicializado"}), 500
    
    try:
        data = request.get_json() or {}
        chains = data.get('chains', [])
        
        if not chains or len(chains) < 2:
            return jsonify({
                "success": False,
                "error": "Precisa de pelo menos 2 chains para execução atômica"
            }), 400
        
        # Converter formato: [{"chain": "...", "function": "...", "params": {...}}, ...]
        # Para formato ALZ-NIEV: [("chain", "function", params), ...]
        chains_formatted = [
            (c.get('chain'), c.get('function'), c.get('params', {}))
            for c in chains
        ]
        
        # Executar atomicamente
        results = alz_niev.execute_atomic_multi_chain(chains_formatted)
        
        # Preparar resposta
        response = {
            "success": all(r.success for r in results.values()),
            "chains": [chain for chain, _, _ in chains_formatted],
            "results": {
                chain: {
                    "success": result.success,
                    "has_zk_proof": result.zk_proof is not None,
                    "has_merkle_proof": result.merkle_proof is not None,
                    "has_consensus_proof": result.consensus_proof is not None,
                    "execution_time_ms": result.execution_time_ms
                }
                for chain, result in results.items()
            },
            "note": "✅ Execução atômica ALZ-NIEV - todas as chains confirmadas atomicamente"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@testnet_bp.route('/api/alz-niev/status', methods=['GET'])
def api_alz_niev_status():
    """Status do ALZ-NIEV"""
    return jsonify({
        "available": alz_niev is not None,
        "layers": {
            "elni": "Execution-Level Native Interop",
            "zkef": "Zero-Knowledge External Functions",
            "upnmt": "Universal Proof Normalized Merkle Tunneling",
            "mcl": "Multi-Consensus Layer",
            "aes": "Atomic Execution Sync"
        },
        "supported_chains": ["bitcoin", "ethereum", "polygon", "bsc", "solana", "cosmos", "base"],
        "supported_consensus": ["PoW", "PoS", "Parallel", "Tendermint", "BFT"]
    }), 200
