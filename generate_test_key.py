#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Gerador de Chave Privada para Testnet
Gera uma chave privada segura para usar na testnet
"""

from eth_account import Account
import secrets

def gerar_chave_teste():
    """Gera uma chave privada e endereço para testnet"""
    
    # Gerar chave privada aleatória (64 caracteres hex)
    private_key = "0x" + secrets.token_hex(32)
    
    # Criar conta a partir da chave
    account = Account.from_key(private_key)
    
    print("=" * 70)
    print("🔐 CHAVE PRIVADA DE TESTE GERADA")
    print("=" * 70)
    print()
    print("⚠️  ATENÇÃO: Use APENAS para TESTNET!")
    print("   Nunca use esta chave com tokens reais!")
    print()
    print("📋 INFORMAÇÕES:")
    print(f"   Chave Privada: {private_key}")
    print(f"   Endereço: {account.address}")
    print()
    print("=" * 70)
    print("📝 CONFIGURAÇÃO NO RENDER:")
    print("=" * 70)
    print()
    print("1. Acesse: https://dashboard.render.com")
    print("2. Vá em: Settings → Environment")
    print("3. Adicione:")
    print()
    print(f"   KEY: POLYGON_PRIVATE_KEY")
    print(f"   VALUE: {private_key}")
    print()
    print("=" * 70)
    print("💰 PRÓXIMOS PASSOS:")
    print("=" * 70)
    print()
    print(f"1. Copie o endereço: {account.address}")
    print()
    print("2. Solicite tokens de teste nos faucets:")
    print("   • Polygon Amoy: https://faucet.polygon.technology/")
    print("   • Ethereum Sepolia: https://sepoliafaucet.com/")
    print("   • BSC Testnet: https://testnet.bnbchain.org/faucet-smart")
    print("   • Base Sepolia: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet")
    print()
    print("3. Aguarde o deploy no Render")
    print()
    print("4. Teste transferências em: https://testnet.allianza.tech/testnet/interoperability")
    print()
    print("=" * 70)
    print("✅ Pronto! Sua chave está gerada e pronta para usar!")
    print("=" * 70)
    
    return {
        "private_key": private_key,
        "address": account.address
    }

if __name__ == "__main__":
    gerar_chave_teste()

