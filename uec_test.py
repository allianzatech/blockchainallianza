# uec_test.py - VERSÃO MAIS ROBUSTA
import pytest
import time
import sys
import os

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from uec_integration import AllianzaUEC

class MockBlockchain:
    """Mock da blockchain para testes"""
    def __init__(self):
        self.wallets = {}
        self.INITIAL_BALANCE = 1000

def test_uec_initialization():
    """Testa inicialização da UEC"""
    print("\n🔧 Testando inicialização UEC...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    assert uec.pqc_crypto is not None
    assert uec.bitcoin_clm is not None
    assert uec.token_factory is not None
    print("✅ UEC Initialization: PASSED")

def test_pqc_wallet_creation():
    """Testa criação de carteira PQC"""
    print("\n🔧 Testando criação de carteira PQC...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    address, private_key = uec.create_uec_wallet()
    
    assert address is not None
    assert private_key is not None
    assert len(address) >= 20  # Endereços PQC
    assert address in uec.blockchain.wallets
    assert "bitcoin_address" in uec.blockchain.wallets[address]
    print("✅ PQC Wallet Creation: PASSED")
    print(f"   Endereço: {address}")
    print(f"   Bitcoin Address: {uec.blockchain.wallets[address]['bitcoin_address']}")

def test_bitcoin_address_validation():
    """Testa validação de endereços Bitcoin"""
    print("\n🔧 Testando validação de endereços Bitcoin...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    # Endereços válidos
    valid_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Satoshi
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # P2SH
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"  # Bech32
    ]
    
    for address in valid_addresses:
        result = uec.bitcoin_clm.validate_bitcoin_address(address)
        assert result, f"Endereço válido rejeitado: {address}"
        print(f"   ✅ {address}")
    
    # Endereços inválidos
    invalid_addresses = [
        "invalid_address",
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfN",  # Muito curto
        "bc1invalid"
    ]
    
    for address in invalid_addresses:
        result = uec.bitcoin_clm.validate_bitcoin_address(address)
        assert not result, f"Endereço inválido aceito: {address}"
        print(f"   ✅ Rejeitou: {address}")
    
    print("✅ Bitcoin Address Validation: PASSED")

def test_metaprogrammable_tokens():
    """Testa tokens metaprogramáveis"""
    print("\n🔧 Testando tokens metaprogramáveis...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    tokens = uec.get_supported_tokens()
    print(f"   Tokens encontrados: {tokens}")
    
    # Verificar se os tokens principais existem
    assert "BTCa" in tokens, "BTCa não encontrado"
    assert "ETHa" in tokens, "ETHa não encontrado" 
    assert "USDa" in tokens, "USDa não encontrado"
    
    # Testar BTCa
    btc_metadata = uec.get_token_metadata("BTCa")
    assert btc_metadata is not None, "Metadados do BTCa são None"
    assert btc_metadata["token_id"] == "BTCa"
    assert "bitcoin" in btc_metadata["cross_logic_metadata"]
    print("   ✅ BTCa: OK")
    
    # Testar ETHa
    eth_metadata = uec.get_token_metadata("ETHa")
    assert eth_metadata is not None, "Metadados do ETHa são None"
    assert eth_metadata["token_id"] == "ETHa"
    assert "ethereum" in eth_metadata["cross_logic_metadata"]
    print("   ✅ ETHa: OK")
    
    # Testar USDa
    usd_metadata = uec.get_token_metadata("USDa")
    assert usd_metadata is not None, "Metadados do USDa são None"
    assert usd_metadata["token_id"] == "USDa"
    assert "multi_chain" in usd_metadata["cross_logic_metadata"]
    print("   ✅ USDa: OK")
    
    print("✅ Metaprogrammable Tokens: PASSED")

def test_bridge_transfer():
    """Testa transferência na bridge UEC"""
    print("\n🔧 Testando bridge UEC...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    # Criar wallet de teste
    address, private_key = uec.create_uec_wallet()
    
    # Testar transferência para Bitcoin
    bridge_tx = uec.transfer_to_external_chain(
        "BTCa", 0.001, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "bitcoin", private_key
    )
    
    assert bridge_tx["bridge_id"] is not None
    assert bridge_tx["status"] == "pending"
    assert bridge_tx["token"] == "BTCa"
    assert bridge_tx["to_chain"] == "bitcoin"
    
    # Verificar se está na lista de pendentes
    status = uec.get_bridge_status(bridge_tx["bridge_id"])
    assert status is not None
    assert status["status"] == "pending"
    
    print("✅ Bridge Transfer: PASSED")
    print(f"   Bridge ID: {bridge_tx['bridge_id']}")

def test_bridge_completion():
    """Testa conclusão da bridge"""
    print("\n🔧 Testando conclusão da bridge...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    # Criar wallet e transferência
    address, private_key = uec.create_uec_wallet()
    bridge_tx = uec.transfer_to_external_chain(
        "BTCa", 0.001, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "bitcoin", private_key
    )
    
    # Completar transferência
    completed = uec.complete_bridge_transfer(bridge_tx["bridge_id"])
    assert completed is not None
    assert completed["status"] == "completed"
    
    # Verificar se foi movida para completadas
    status = uec.get_bridge_status(bridge_tx["bridge_id"])
    assert status["status"] == "completed"
    
    print("✅ Bridge Completion: PASSED")

def test_token_validation():
    """Testa validação de operações com tokens"""
    print("\n🔧 Testando validação de tokens...")
    blockchain = MockBlockchain()
    uec = AllianzaUEC(blockchain)
    
    # Testar operação válida
    is_valid, message = uec.token_factory.validate_token_operation("BTCa", "cross_chain_transfer", "bitcoin")
    assert is_valid, f"Validação válida falhou: {message}"
    print("   ✅ BTCa → Bitcoin: VÁLIDO")
    
    # Testar operação inválida
    is_valid, message = uec.token_factory.validate_token_operation("BTCa", "cross_chain_transfer", "solana")
    assert not is_valid, "Validação inválida passou"
    print("   ✅ BTCa → Solana: INVÁLIDO (como esperado)")
    
    print("✅ Token Validation: PASSED")

if __name__ == "__main__":
    try:
        print("🚀 INICIANDO TESTES UEC COMPLETOS...")
        print("=" * 50)
        
        test_uec_initialization()
        test_pqc_wallet_creation() 
        test_bitcoin_address_validation()
        test_metaprogrammable_tokens()
        test_token_validation()
        test_bridge_transfer()
        test_bridge_completion()
        
        print("\n" + "=" * 50)
        print("🎉 TODOS OS TESTES UEC PASSARAM! 🎉")
        print("🌌 UEC PRONTA PARA IMPLANTAÇÃO!")
        print("🚀 AGORA VAMOS INTEGRAR COM O SISTEMA PRINCIPAL!")
        
    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}")
        import traceback
        traceback.print_exc()