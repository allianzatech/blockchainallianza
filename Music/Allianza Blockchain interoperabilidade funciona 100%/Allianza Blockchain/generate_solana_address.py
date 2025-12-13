#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 Script para gerar novo endereço Solana (Testnet)
"""

import os
import base58
from dotenv import load_dotenv

load_dotenv()

def generate_solana_address():
    """Gerar novo endereço Solana"""
    
    print(f"{'='*70}")
    print(f"🔑 GERANDO NOVO ENDEREÇO SOLANA (TESTNET)")
    print(f"{'='*70}\n")
    
    try:
        # Tentar usar bibliotecas Solana se disponíveis
        try:
            from solders.keypair import Keypair
            
            # Gerar novo keypair
            keypair = Keypair()
            
            # Obter endereço público (Base58)
            public_key = str(keypair.pubkey())
            
            # Obter chave privada (bytes)
            private_key_bytes = bytes(keypair)
            
            # Converter chave privada para Base58
            private_key_base58 = base58.b58encode(private_key_bytes).decode('utf-8')
            
            print("✅ Endereço gerado usando biblioteca Solana!\n")
            
        except ImportError:
            # Método alternativo: gerar chave privada aleatória e derivar endereço
            import secrets
            
            print("⚠️  Bibliotecas Solana não disponíveis, usando método alternativo...")
            print("   (Recomendado: pip install solana solders para melhor segurança)\n")
            
            # Gerar 32 bytes aleatórios para chave privada
            private_key_bytes = secrets.token_bytes(32)
            
            # Converter para Base58
            private_key_base58 = base58.b58encode(private_key_bytes).decode('utf-8')
            
            # Para obter o endereço público, precisamos derivar da chave privada
            # Como não temos as bibliotecas, vamos usar uma abordagem simplificada
            # Em produção, sempre use as bibliotecas oficiais!
            
            # Nota: Sem as bibliotecas, não podemos derivar o endereço público corretamente
            # Vamos gerar um endereço temporário que precisa ser validado
            print("⚠️  ATENÇÃO: Sem bibliotecas Solana, não é possível derivar o endereço público.")
            print("   Instale as bibliotecas para gerar um endereço válido:")
            print("   pip install solana solders\n")
            
            # Retornar apenas a chave privada
            return {
                "success": False,
                "error": "Bibliotecas Solana necessárias para gerar endereço completo",
                "private_key_base58": private_key_base58,
                "note": "Instale: pip install solana solders"
            }
        
        print(f"📍 ENDEREÇO PÚBLICO (PUBLIC KEY):")
        print(f"   {public_key}\n")
        
        print(f"🔑 CHAVE PRIVADA (PRIVATE KEY - BASE58):")
        print(f"   {private_key_base58}\n")
        
        print(f"⚠️  IMPORTANTE:")
        print(f"   • Guarde a chave privada em local SEGURO!")
        print(f"   • NUNCA compartilhe a chave privada!")
        print(f"   • Use apenas em TESTNET para testes\n")
        
        print(f"📋 PARA ADICIONAR NO .env:")
        print(f"   SOLANA_ADDRESS={public_key}")
        print(f"   SOLANA_PRIVATE_KEY={private_key_base58}\n")
        
        print(f"🔗 FAUCETS SOLANA TESTNET:")
        print(f"   • https://faucet.solana.com/")
        print(f"   • https://solfaucet.com/")
        print(f"   • https://faucet.triangleplatform.com/solana/testnet\n")
        
        print(f"💡 Para verificar o saldo depois:")
        print(f"   python check_solana_balance.py\n")
        
        return {
            "success": True,
            "address": public_key,
            "private_key": private_key_base58,
            "network": "testnet"
        }
        
    except Exception as e:
        print(f"\n❌ Erro ao gerar endereço: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    result = generate_solana_address()
    
    if not result.get("success"):
        print(f"\n❌ Falha ao gerar endereço: {result.get('error')}")
        if result.get("note"):
            print(f"   💡 {result.get('note')}")

