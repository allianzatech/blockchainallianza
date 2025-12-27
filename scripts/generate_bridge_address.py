#!/usr/bin/env python3
"""
🌉 Script para gerar endereço Allianza Bridge
Gera um endereço Allianza com saldo inicial para uso como bridge
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from allianza_blockchain import AllianzaBlockchain
from allianza_bridge_config import AllianzaBridgeConfig
from base58_utils import validate_allianza_address

def main():
    print("🌉 Gerador de Endereço Allianza Bridge")
    print("=" * 60)
    
    # Inicializar blockchain
    print("\n📦 Inicializando blockchain...")
    blockchain = AllianzaBlockchain()
    
    # Inicializar bridge config
    print("🔧 Inicializando bridge config...")
    bridge_config = AllianzaBridgeConfig(blockchain)
    
    # Obter ou criar endereço bridge
    print("\n🔑 Gerando endereço bridge...")
    bridge_address = bridge_config.get_or_create_bridge_address()
    bridge_balance = bridge_config.get_bridge_balance()
    
    print("\n" + "=" * 60)
    print("✅ Bridge Address gerado com sucesso!")
    print("=" * 60)
    print(f"\n📍 Endereço Bridge: {bridge_address}")
    print(f"💰 Saldo: {bridge_balance} ALZ")
    
    # Verificar se é válido
    if validate_allianza_address(bridge_address):
        print("✅ Endereço válido!")
    else:
        print("⚠️  Endereço pode ser inválido")
    
    # Mostrar informações de configuração
    config_info = bridge_config.get_config_info()
    print(f"\n📊 Informações de Configuração:")
    print(f"   • Configurado via .env: {config_info['configured']}")
    print(f"   • Tem chave privada: {config_info['has_private_key']}")
    print(f"   • Saldo inicial configurado: {config_info['initial_balance']} ALZ")
    
    # Instruções para adicionar ao .env
    print("\n" + "=" * 60)
    print("📝 Adicione ao seu .env:")
    print("=" * 60)
    print(f"\nALLIANZA_BRIDGE_ADDRESS={bridge_address}")
    print(f"ALLIANZA_BRIDGE_INITIAL_BALANCE={config_info['initial_balance']}")
    print("\n💡 Dica: Se quiser usar uma chave privada específica, adicione:")
    print("   ALLIANZA_BRIDGE_PRIVATE_KEY=<sua_chave_privada_pem>")
    
    # Instruções para Render
    print("\n" + "=" * 60)
    print("🚀 Para usar no Render:")
    print("=" * 60)
    print("\n1. Acesse o Render Dashboard")
    print("2. Vá em Environment Variables")
    print(f"3. Adicione: ALLIANZA_BRIDGE_ADDRESS = {bridge_address}")
    print(f"4. Adicione: ALLIANZA_BRIDGE_INITIAL_BALANCE = {config_info['initial_balance']}")
    print("\n✅ Pronto! O bridge usará este endereço automaticamente.")
    
    # Atualizar arquivo .env automaticamente
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from scripts.update_env import update_env_file
        update_env_file(bridge_address, str(config_info['initial_balance']))
        print("\n" + "=" * 60)
        print("✅ Arquivo .env atualizado automaticamente!")
        print("=" * 60)
    except Exception as e:
        print(f"\n⚠️  Não foi possível atualizar .env automaticamente: {e}")
        print("   Você pode atualizar manualmente usando:")
        print(f"   python scripts/update_env.py {bridge_address} {config_info['initial_balance']}")
    
    print("\n" + "=" * 60)
    print("✨ Concluído!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

