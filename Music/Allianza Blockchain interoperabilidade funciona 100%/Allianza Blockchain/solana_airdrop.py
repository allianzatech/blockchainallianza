"""
💰 Solana Airdrop via Python
Faz airdrop de SOL na testnet/devnet sem precisar da CLI
"""

import requests
import json
import base58
import sys

def solana_airdrop(address: str, amount: float = 2.0, network: str = "testnet"):
    """
    Faz airdrop de SOL para um endereço
    
    Args:
        address: Endereço Solana (base58)
        amount: Quantidade de SOL (padrão: 2.0)
        network: "testnet" ou "devnet"
    """
    try:
        # RPC URLs
        rpc_urls = {
            "testnet": "https://api.testnet.solana.com",
            "devnet": "https://api.devnet.solana.com"
        }
        
        rpc_url = rpc_urls.get(network, rpc_urls["testnet"])
        
        print(f"💰 Solicitando {amount} SOL para {address}")
        print(f"🌐 Network: {network}")
        print(f"🔗 RPC: {rpc_url}")
        print()
        
        # Método 1: Tentar requestAirdrop via RPC
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "requestAirdrop",
            "params": [
                address,
                int(amount * 1e9)  # Converter para lamports
            ]
        }
        
        response = requests.post(rpc_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                signature = data["result"]
                print(f"✅ Airdrop solicitado com sucesso!")
                print(f"📝 Signature: {signature}")
                print(f"🔗 Explorer: https://explorer.solana.com/tx/{signature}?cluster={network}")
                print()
                print("⏳ Aguardando confirmação...")
                
                # Verificar status
                check_payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getSignatureStatuses",
                    "params": [[signature]]
                }
                
                import time
                for i in range(10):
                    time.sleep(2)
                    check_response = requests.post(rpc_url, json=check_payload, timeout=10)
                    if check_response.status_code == 200:
                        check_data = check_response.json()
                        if check_data.get("result") and check_data["result"].get("value"):
                            status = check_data["result"]["value"][0]
                            if status and status.get("confirmationStatus"):
                                print(f"✅ Status: {status['confirmationStatus']}")
                                if status.get("confirmationStatus") in ["confirmed", "finalized"]:
                                    print("✅ Airdrop confirmado!")
                                    return {
                                        "success": True,
                                        "signature": signature,
                                        "explorer": f"https://explorer.solana.com/tx/{signature}?cluster={network}"
                                    }
                
                return {
                    "success": True,
                    "signature": signature,
                    "note": "Airdrop solicitado, aguardando confirmação",
                    "explorer": f"https://explorer.solana.com/tx/{signature}?cluster={network}"
                }
            else:
                error = data.get("error", {})
                error_msg = error.get("message", "Erro desconhecido")
                print(f"❌ Erro: {error_msg}")
                return {"success": False, "error": error_msg}
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Função principal"""
    print("=" * 70)
    print("💰 SOLANA AIRDROP - TESTNET/DEVNET")
    print("=" * 70)
    print()
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        address = sys.argv[1]
        amount = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
        network = sys.argv[3] if len(sys.argv) > 3 else "testnet"
    else:
        # Modo interativo
        address = input("Digite o endereço Solana: ").strip()
        amount = input("Quantidade de SOL (padrão: 2.0): ").strip()
        amount = float(amount) if amount else 2.0
        network = input("Network (testnet/devnet, padrão: testnet): ").strip() or "testnet"
    
    if not address:
        print("❌ Endereço não fornecido")
        return
    
    print()
    result = solana_airdrop(address, amount, network)
    print()
    
    if result.get("success"):
        print("=" * 70)
        print("✅ AIRDROP CONCLUÍDO!")
        print("=" * 70)
        if result.get("explorer"):
            print(f"🔗 Ver no explorer: {result['explorer']}")
    else:
        print("=" * 70)
        print("❌ AIRDROP FALHOU")
        print("=" * 70)
        print(f"Erro: {result.get('error', 'Desconhecido')}")
        print()
        print("💡 Dicas:")
        print("   - Verifique se o endereço está correto")
        print("   - Tente usar devnet: python solana_airdrop.py <endereço> 2 devnet")
        print("   - Use faucets alternativos se necessário")

if __name__ == "__main__":
    main()

















