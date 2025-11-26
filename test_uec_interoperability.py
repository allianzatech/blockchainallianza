# test_uec_interoperability.py
import requests
import json
import time

BASE_URL = "http://localhost:5008"

class UECTester:
    def __init__(self):
        self.session = requests.Session()
        self.wallet_address = None
        self.private_key = None
    
    def print_step(self, message):
        print(f"\n{'='*50}")
        print(f"🔧 {message}")
        print(f"{'='*50}")
    
    def test_system_status(self):
        """Teste 1: Status do sistema"""
        self.print_step("TESTE 1 - Status do Sistema")
        try:
            response = self.session.get(f"{BASE_URL}/uec/system/status")
            data = response.json()
            print("✅ Sistema UEC Online!")
            print(f"📊 Versão: {data.get('uec_version', 'N/A')}")
            print(f"🌉 Interoperabilidade: {data.get('real_interoperability', False)}")
            print(f"💰 Reservas: {data.get('reserve_status', {})}")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def test_create_wallet(self):
        """Teste 2: Criar wallet UEC"""
        self.print_step("TESTE 2 - Criar Wallet UEC")
        try:
            payload = {
                "blockchain_source": "allianza",
                "user_id": f"test_user_{int(time.time())}"
            }
            response = self.session.post(f"{BASE_URL}/uec/create_wallet", json=payload)
            data = response.json()
            
            if data.get("success") and "address" in data:
                self.wallet_address = data["address"]
                self.private_key = data["private_key"]
                print(f"✅ Wallet criada: {self.wallet_address}")
                print(f"🔑 Private Key: {self.private_key[:50]}...")
                print(f"₿ Bitcoin Address: {data.get('bitcoin_address', 'N/A')}")
                return True
            else:
                print(f"❌ Erro: {data.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def test_reserve_status(self):
        """Teste 3: Status das reservas"""
        self.print_step("TESTE 3 - Status das Reservas")
        try:
            response = self.session.get(f"{BASE_URL}/uec/reserve/status")
            data = response.json()
            
            if data.get("success"):
                reserves = data.get("reserves", {})
                print("💰 Status das Reservas:")
                print(f"   ₿ Bitcoin: {reserves.get('bitcoin', 0)} BTC")
                print(f"   ⬨ Ethereum: {reserves.get('ethereum', 0)} ETH")
                print(f"   🪙 BTCa em circulação: {reserves.get('btca_supply', 0)}")
                print(f"   🪙 ETHa em circulação: {reserves.get('etha_supply', 0)}")
                return True
            else:
                print(f"❌ Erro: {data.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def test_deposit_conversion(self):
        """Teste 4: Conversão REAL → TOKEN"""
        self.print_step("TESTE 4 - Conversão REAL → TOKEN (Depósito)")
        try:
            payload = {
                "real_chain": "bitcoin",
                "amount": 0.1,
                "token_id": "BTCa",
                "user_address": self.wallet_address
            }
            response = self.session.post(f"{BASE_URL}/uec/convert/deposit", json=payload)
            data = response.json()
            
            if data.get("success"):
                print("✅ Depósito realizado com sucesso!")
                print(f"📥 Endereço de depósito: {data.get('deposit_address')}")
                print(f"📝 Memo: {data.get('memo')}")
                print(f"🪙 Token recebido: {data.get('token_received')}")
                print(f"💰 Quantidade: {data.get('amount_received')}")
                return True
            else:
                print(f"❌ Erro: {data.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def test_token_balance(self):
        """Teste 5: Verificar saldo de tokens"""
        self.print_step("TESTE 5 - Verificar Saldo de Tokens")
        try:
            # Ver saldo BTCa
            response_btc = self.session.get(f"{BASE_URL}/uec/wallet/balance/{self.wallet_address}/BTCa")
            data_btc = response_btc.json()
            
            # Ver saldo ETHa
            response_eth = self.session.get(f"{BASE_URL}/uec/wallet/balance/{self.wallet_address}/ETHa")
            data_eth = response_eth.json()
            
            print("💰 Saldos da Wallet:")
            if data_btc.get("success"):
                print(f"   ₿ BTCa: {data_btc.get('balance', 0)}")
            if data_eth.get("success"):
                print(f"   ⬨ ETHa: {data_eth.get('balance', 0)}")
            
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def test_withdrawal_conversion(self):
        """Teste 6: Conversão TOKEN → REAL (Saque)"""
        self.print_step("TESTE 6 - Conversão TOKEN → REAL (Saque)")
        try:
            payload = {
                "token_id": "BTCa",
                "amount": 0.05,
                "real_chain": "bitcoin",
                "real_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Genesis BTC address
                "private_key": self.private_key
            }
            response = self.session.post(f"{BASE_URL}/uec/convert/withdraw", json=payload)
            data = response.json()
            
            if data.get("success"):
                print("✅ Saque realizado com sucesso!")
                print(f"🪙 Token queimado: {data.get('token_burned')} BTCa")
                print(f"💰 Real enviado: {data.get('real_sent')} BTC")
                print(f"📤 Transação: {data.get('real_transaction', {}).get('txid', 'N/A')}")
                print(f"🎯 Endereço destino: {data.get('real_address')}")
                return True
            else:
                print(f"❌ Erro: {data.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def test_validate_address(self):
        """Teste 7: Validação de endereços"""
        self.print_step("TESTE 7 - Validação de Endereços")
        try:
            test_cases = [
                {"address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "chain": "bitcoin"},
                {"address": "0x742d35Cc6634C0532925a3b8Df6B5e5B5C5b5E5e", "chain": "ethereum"},
                {"address": "invalid_address", "chain": "bitcoin"}
            ]
            
            for test in test_cases:
                response = self.session.post(f"{BASE_URL}/uec/validate_address", json=test)
                data = response.json()
                print(f"📍 {test['address'][:20]}... ({test['chain']}): {data.get('is_valid', False)}")
            
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTES DE INTEROPERABILIDADE UEC")
        print("📍 URL Base:", BASE_URL)
        
        tests = [
            self.test_system_status,
            self.test_create_wallet,
            self.test_reserve_status,
            self.test_deposit_conversion, 
            self.test_token_balance,
            self.test_withdrawal_conversion,
            self.test_validate_address
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                time.sleep(1)  # Pequena pausa entre testes
            except Exception as e:
                print(f"❌ Teste falhou: {e}")
                results.append(False)
        
        # Resumo final
        self.print_step("RESUMO DOS TESTES")
        passed = sum(results)
        total = len(results)
        print(f"✅ Testes passados: {passed}/{total}")
        print(f"📊 Sucesso: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM! Sistema de interoperabilidade funcionando!")
        else:
            print("⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    tester = UECTester()
    tester.run_all_tests()