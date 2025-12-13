#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script para consultar saldo do endereço Solana
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_solana_balance():
    """Consultar saldo do endereço Solana"""
    
    # Obter endereço do .env ou usar o padrão
    address = os.getenv('SOLANA_ADDRESS', '5qzASbWFvFBhyAq8D9k9mvf3ubzHKYdA49saDgFNgvhk')
    rpc_url = os.getenv('SOLANA_RPC_URL', 'https://api.testnet.solana.com')
    
    print(f"{'='*70}")
    print(f"🔍 CONSULTANDO SALDO SOLANA")
    print(f"{'='*70}")
    print(f"📡 RPC URL: {rpc_url}")
    print(f"📍 Endereço: {address}")
    print()
    
    # Tentar usar solana_bridge se disponível
    try:
        from solana_bridge import SolanaBridge
        bridge = SolanaBridge()
        
        print("✅ Usando SolanaBridge...")
        result = bridge.get_balance(address)
        
        if result.get("success"):
            balance_sol = result.get("balance_sol", 0)
            balance_lamports = result.get("balance_lamports", 0)
            
            print(f"\n✅✅✅ SALDO ENCONTRADO!")
            print(f"   💰 {balance_sol:.9f} SOL")
            print(f"   💰 {balance_lamports:,} lamports")
            
            if balance_sol < 0.01:
                print(f"\n⚠️  AVISO: Saldo muito baixo!")
                print(f"   💡 Considere solicitar SOL de um faucet:")
                print(f"   🔗 https://faucet.solana.com/")
                print(f"   🔗 https://solfaucet.com/")
            else:
                print(f"\n✅ Saldo suficiente para transações!")
            
            return result
        else:
            error = result.get("error", "Erro desconhecido")
            print(f"\n❌ Erro ao consultar saldo: {error}")
            return result
            
    except ImportError:
        print("⚠️  SolanaBridge não disponível, usando API direta...")
        
        # Método alternativo: usar API REST diretamente
        import requests
        
        try:
            # Solana RPC API
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [address]
            }
            
            response = requests.post(rpc_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "result" in data:
                    balance_lamports = data["result"]["value"]
                    balance_sol = balance_lamports / 1e9
                    
                    print(f"\n✅✅✅ SALDO ENCONTRADO!")
                    print(f"   💰 {balance_sol:.9f} SOL")
                    print(f"   💰 {balance_lamports:,} lamports")
                    
                    if balance_sol < 0.01:
                        print(f"\n⚠️  AVISO: Saldo muito baixo!")
                        print(f"   💡 Considere solicitar SOL de um faucet:")
                        print(f"   🔗 https://faucet.solana.com/")
                        print(f"   🔗 https://solfaucet.com/")
                    else:
                        print(f"\n✅ Saldo suficiente para transações!")
                    
                    return {
                        "success": True,
                        "balance_sol": balance_sol,
                        "balance_lamports": balance_lamports,
                        "address": address
                    }
                else:
                    error = data.get("error", {}).get("message", "Erro desconhecido")
                    print(f"\n❌ Erro na resposta: {error}")
                    return {"success": False, "error": error}
            else:
                print(f"\n❌ Erro HTTP: {response.status_code}")
                print(f"   Resposta: {response.text[:200]}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"\n❌ Erro ao consultar saldo: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = check_solana_balance()
    sys.exit(0 if result.get("success") else 1)

