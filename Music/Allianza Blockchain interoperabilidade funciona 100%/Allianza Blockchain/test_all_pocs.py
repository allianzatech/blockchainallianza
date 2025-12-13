# test_all_pocs.py
# 🧪 TESTE AUTOMATIZADO: TODAS AS POCs
# Valida funcionalidades das 3 PoCs finalizadas

import sys
import os
import time
import json
from typing import Dict, List
from datetime import datetime, timedelta

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("🧪 TESTE AUTOMATIZADO: TODAS AS POCs")
print("="*70)

# Contadores de testes
total_tests = 0
passed_tests = 0
failed_tests = 0

def test_result(test_name: str, passed: bool, details: str = ""):
    """Registrar resultado de teste"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if passed:
        passed_tests += 1
        print(f"✅ {test_name}")
        if details:
            print(f"   {details}")
    else:
        failed_tests += 1
        print(f"❌ {test_name}")
        if details:
            print(f"   {details}")

# =============================================================================
# TESTE 1: POC_VALIDACAO_UNIVERSAL_FINAL
# =============================================================================

print("\n" + "="*70)
print("📝 TESTE 1: POC_VALIDACAO_UNIVERSAL_FINAL")
print("="*70)

try:
    from POC_VALIDACAO_UNIVERSAL_FINAL import UniversalSignatureValidationPOC
    
    # Testar inicialização
    try:
        poc_validacao = UniversalSignatureValidationPOC()
        test_result("Inicialização da PoC de Validação", True, "Classe instanciada com sucesso")
    except Exception as e:
        test_result("Inicialização da PoC de Validação", False, f"Erro: {str(e)}")
        poc_validacao = None
    
    if poc_validacao:
        # Testar conexões
        try:
            has_connections = (
                hasattr(poc_validacao, 'blockcypher_token') and
                hasattr(poc_validacao, 'solana_rpc') and
                hasattr(poc_validacao, 'eth_w3')
            )
            test_result("Configuração de conexões", has_connections, "BlockCypher, Solana RPC, Web3 configurados")
        except Exception as e:
            test_result("Configuração de conexões", False, f"Erro: {str(e)}")
        
        # Testar método de validação Bitcoin (estrutural)
        try:
            # Teste com hash inválido (deve retornar erro)
            result = poc_validacao.validate_bitcoin_utxo_signature("invalid_hash_123")
            is_valid = result.get('valid') == False  # Deve ser inválido
            test_result("Validação Bitcoin (hash inválido)", is_valid, "Detecta hash inválido corretamente")
        except Exception as e:
            test_result("Validação Bitcoin (hash inválido)", False, f"Erro: {str(e)}")
        
        # Testar método de validação Solana (estrutural)
        try:
            # Teste com assinatura inválida (deve retornar erro)
            result = poc_validacao.validate_solana_ed25519_signature(
                signature="invalid_sig",
                message=b"test",
                public_key="invalid_key"
            )
            is_valid = result.get('valid') == False  # Deve ser inválido
            test_result("Validação Solana (assinatura inválida)", is_valid, "Detecta assinatura inválida corretamente")
        except Exception as e:
            test_result("Validação Solana (assinatura inválida)", False, f"Erro: {str(e)}")
        
        # Testar método de validação de transação Solana (estrutural)
        try:
            result = poc_validacao.validate_solana_transaction("invalid_signature")
            is_valid = result.get('valid') == False  # Deve ser inválido
            test_result("Validação Transação Solana (inválida)", is_valid, "Detecta transação inválida corretamente")
        except Exception as e:
            test_result("Validação Transação Solana (inválida)", False, f"Erro: {str(e)}")
    
except ImportError as e:
    test_result("Importação da PoC de Validação", False, f"Erro: {str(e)}")
except Exception as e:
    test_result("Teste da PoC de Validação", False, f"Erro: {str(e)}")

# =============================================================================
# TESTE 2: POC_PREDICAO_GAS_80_PRECISAO
# =============================================================================

print("\n" + "="*70)
print("📝 TESTE 2: POC_PREDICAO_GAS_80_PRECISAO")
print("="*70)

try:
    from POC_PREDICAO_GAS_80_PRECISAO import GasPricePredictionPOC
    
    # Testar inicialização
    try:
        poc_gas = GasPricePredictionPOC()
        test_result("Inicialização da PoC de Predição de Gas", True, "Classe instanciada com sucesso")
    except Exception as e:
        test_result("Inicialização da PoC de Predição de Gas", False, f"Erro: {str(e)}")
        poc_gas = None
    
    if poc_gas:
        # Testar conexão Web3
        try:
            is_connected = poc_gas.w3 is not None and poc_gas.w3.is_connected()
            test_result("Conexão Web3", is_connected, "Conectado à Ethereum Sepolia" if is_connected else "Não conectado")
        except Exception as e:
            test_result("Conexão Web3", False, f"Erro: {str(e)}")
        
        # Testar obtenção de gas price atual
        try:
            gas_data = poc_gas.get_current_gas_price()
            has_data = gas_data is not None and 'gas_price_gwei' in gas_data
            test_result("Obtenção de Gas Price Atual", has_data, f"Gas: {gas_data.get('gas_price_gwei', 'N/A')} Gwei" if has_data else "Falhou")
        except Exception as e:
            test_result("Obtenção de Gas Price Atual", False, f"Erro: {str(e)}")
        
        # Testar análise de padrões (com dados simulados)
        try:
            # Criar histórico simulado
            from datetime import datetime
            simulated_history = []
            base_time = datetime.now()
            for i in range(20):
                simulated_history.append({
                    'gas_price_gwei': 10.0 + (i % 5),
                    'datetime': base_time.replace(second=0, microsecond=0) if i == 0 else (base_time.replace(second=0, microsecond=0) + timedelta(minutes=i))
                })
            
            # Adicionar ao histórico
            for h in simulated_history:
                poc_gas.gas_history.append(h)
            
            patterns = poc_gas.analyze_patterns(list(poc_gas.gas_history))
            has_patterns = 'statistics' in patterns and 'spikes' in patterns
            test_result("Análise de Padrões", has_patterns, f"Média: {patterns.get('statistics', {}).get('mean', 'N/A'):.2f} Gwei" if has_patterns else "Falhou")
        except Exception as e:
            test_result("Análise de Padrões", False, f"Erro: {str(e)}")
        
        # Testar predição de gas spike
        try:
            prediction = poc_gas.predict_gas_spike(minutes_ahead=5, confidence_threshold=0.8)
            has_prediction = prediction.get('success') is not None
            test_result("Predição de Gas Spike", has_prediction, f"Confiança: {prediction.get('confidence_percentage', 'N/A'):.2f}%" if has_prediction else "Falhou")
        except Exception as e:
            test_result("Predição de Gas Spike", False, f"Erro: {str(e)}")
    
except ImportError as e:
    test_result("Importação da PoC de Predição de Gas", False, f"Erro: {str(e)}")
except Exception as e:
    test_result("Teste da PoC de Predição de Gas", False, f"Erro: {str(e)}")

# =============================================================================
# TESTE 3: POC_PROOF_OF_LOCK_ZK
# =============================================================================

print("\n" + "="*70)
print("📝 TESTE 3: POC_PROOF_OF_LOCK_ZK")
print("="*70)

try:
    from POC_PROOF_OF_LOCK_ZK import ProofOfLockZKPOC
    
    # Testar inicialização
    try:
        poc_lock = ProofOfLockZKPOC()
        test_result("Inicialização da PoC de Proof-of-Lock", True, "Classe instanciada com sucesso")
    except Exception as e:
        test_result("Inicialização da PoC de Proof-of-Lock", False, f"Erro: {str(e)}")
        poc_lock = None
    
    if poc_lock:
        # Testar conexões Web3
        try:
            eth_connected = poc_lock.eth_w3 is not None and poc_lock.eth_w3.is_connected()
            polygon_connected = poc_lock.polygon_w3 is not None and poc_lock.polygon_w3.is_connected()
            test_result("Conexões Web3", eth_connected or polygon_connected, 
                       f"Ethereum: {'✅' if eth_connected else '❌'}, Polygon: {'✅' if polygon_connected else '❌'}")
        except Exception as e:
            test_result("Conexões Web3", False, f"Erro: {str(e)}")
        
        # Testar criação de lock
        try:
            lock_result = poc_lock.create_lock(
                source_chain="polygon",
                amount=0.1,
                token_symbol="MATIC",
                target_chain="ethereum",
                recipient_address="0x48Ec8b17B7af735AB329fA07075247FAf3a09599"
            )
            lock_success = lock_result.get('success') == True
            test_result("Criação de Lock", lock_success, f"Lock ID: {lock_result.get('lock_id', 'N/A')}" if lock_success else "Falhou")
            
            if lock_success:
                lock_id = lock_result.get('lock_id')
                
                # Testar verificação de proof-of-lock
                try:
                    verification = poc_lock.verify_lock_proof(lock_id)
                    verify_success = verification.get('valid') == True
                    test_result("Verificação de Proof-of-Lock", verify_success, "ZK Proof válido" if verify_success else "Falhou")
                except Exception as e:
                    test_result("Verificação de Proof-of-Lock", False, f"Erro: {str(e)}")
                
                # Testar unlock
                try:
                    unlock_result = poc_lock.unlock_tokens(lock_id, "ethereum")
                    unlock_success = unlock_result.get('success') == True
                    test_result("Unlock de Tokens", unlock_success, f"TX: {unlock_result.get('unlock_tx_hash', 'N/A')}" if unlock_success else "Falhou")
                except Exception as e:
                    test_result("Unlock de Tokens", False, f"Erro: {str(e)}")
        
        except Exception as e:
            test_result("Criação de Lock", False, f"Erro: {str(e)}")
        
        # Testar criação de ZK Proof diretamente
        try:
            test_lock_data = {
                "source_chain": "polygon",
                "amount": 0.1,
                "token_symbol": "MATIC",
                "target_chain": "ethereum",
                "timestamp": time.time()
            }
            zk_result = poc_lock.create_zk_proof(test_lock_data)
            zk_success = zk_result.get('success') == True
            test_result("Criação de ZK Proof", zk_success, f"Proof ID: {zk_result.get('proof_id', 'N/A')}" if zk_success else "Falhou")
            
            if zk_success:
                # Testar verificação de ZK Proof
                try:
                    verify_zk = poc_lock.verify_zk_proof(zk_result['zk_proof'], test_lock_data)
                    verify_zk_success = verify_zk.get('valid') == True
                    test_result("Verificação de ZK Proof", verify_zk_success, "ZK Proof válido" if verify_zk_success else "Falhou")
                except Exception as e:
                    test_result("Verificação de ZK Proof", False, f"Erro: {str(e)}")
        
        except Exception as e:
            test_result("Criação de ZK Proof", False, f"Erro: {str(e)}")
    
except ImportError as e:
    test_result("Importação da PoC de Proof-of-Lock", False, f"Erro: {str(e)}")
except Exception as e:
    test_result("Teste da PoC de Proof-of-Lock", False, f"Erro: {str(e)}")

# =============================================================================
# RESUMO FINAL
# =============================================================================

print("\n" + "="*70)
print("📊 RESUMO DOS TESTES")
print("="*70)
print(f"Total de Testes: {total_tests}")
print(f"✅ Passou: {passed_tests}")
print(f"❌ Falhou: {failed_tests}")
print(f"Taxa de Sucesso: {(passed_tests/total_tests*100) if total_tests > 0 else 0:.2f}%")
print("="*70)

if failed_tests == 0:
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    sys.exit(0)
else:
    print(f"\n⚠️  {failed_tests} teste(s) falharam. Verifique os erros acima.")
    sys.exit(1)

