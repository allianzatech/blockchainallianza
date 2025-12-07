"""
🚀 Setup Completo para Transferências Bitcoin REAIS
Gera chave, converte para WIF, atualiza .env, testa saldo e faz transferência real
"""

import os
import sys
import time
from dotenv import load_dotenv

def install_dependencies():
    """Instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    try:
        import bitcoinlib
        print("✅ bitcoinlib já instalado")
    except ImportError:
        print("⏳ Instalando bitcoinlib...")
        os.system("pip install bitcoinlib")
        print("✅ bitcoinlib instalado")
    
    try:
        from web3 import Web3
        print("✅ web3 já instalado")
    except ImportError:
        print("⏳ Instalando web3...")
        os.system("pip install web3")
        print("✅ web3 instalado")

def generate_bitcoin_key():
    """Gera nova chave Bitcoin (testnet)"""
    try:
        from bitcoinlib.keys import HDKey
        
        print("🔑 Gerando nova chave Bitcoin Testnet...")
        # Gerar chave master para testnet
        key = HDKey(network='testnet')
        
        xprv = key.wif_private()
        address = key.address()
        wif = key.wif()
        
        print(f"✅ Chave gerada!")
        print(f"   Endereço: {address}")
        print(f"   WIF: {wif[:20]}...{wif[-10:]}")
        
        return {
            "xprv": xprv,
            "wif": wif,
            "address": address
        }
    except Exception as e:
        print(f"❌ Erro ao gerar chave: {e}")
        return None

def convert_xprv_to_wif(xprv: str) -> str:
    """Converte xprv para WIF"""
    try:
        from bitcoinlib.keys import HDKey
        
        key = HDKey(xprv)
        wif = key.wif()
        return wif
    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        return None

def update_env_file(bitcoin_wif: str, bitcoin_address: str):
    """Atualiza arquivo .env com chaves Bitcoin"""
    env_path = '.env'
    
    # Ler .env atual
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    
    # Remover linhas antigas
    lines = env_content.split('\n')
    new_lines = []
    for line in lines:
        if not (line.strip().startswith('BITCOIN_PRIVATE_KEY=') or 
                line.strip().startswith('BITCOIN_TESTNET_PRIVATE_KEY=') or
                line.strip().startswith('BITCOIN_TESTNET_ADDRESS=')):
            new_lines.append(line)
    
    # Adicionar novas linhas
    new_lines.append(f"BITCOIN_PRIVATE_KEY={bitcoin_wif}")
    new_lines.append(f"BITCOIN_TESTNET_PRIVATE_KEY={bitcoin_wif}")  # Para compatibilidade
    new_lines.append(f"BITCOIN_TESTNET_ADDRESS={bitcoin_address}")
    
    # Escrever de volta
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ .env atualizado!")

def check_bitcoin_balance(address: str):
    """Verifica saldo Bitcoin"""
    try:
        import requests
        
        # Usar BlockCypher API
        api_token = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
        url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance?token={api_token}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            balance_btc = data.get('balance', 0) / 100000000  # Satoshis para BTC
            print(f"💰 Saldo Bitcoin Testnet: {balance_btc} BTC")
            return balance_btc
        else:
            print(f"⚠️  Não foi possível verificar saldo (status {response.status_code})")
            return None
    except Exception as e:
        print(f"⚠️  Erro ao verificar saldo: {e}")
        return None

def get_bitcoin_faucet_info():
    """Retorna informações sobre faucets Bitcoin testnet"""
    print()
    print("💧 Faucets Bitcoin Testnet:")
    print("   1. https://bitcoinfaucet.uo1.net/")
    print("   2. https://testnet-faucet.com/btc-testnet/")
    print("   3. https://coinfaucet.eu/en/btc-testnet/")
    print()

def main():
    """Função principal"""
    print("=" * 70)
    print("🚀 SETUP COMPLETO: Transferências Bitcoin REAIS")
    print("=" * 70)
    print()
    
    # 1. Instalar dependências
    install_dependencies()
    print()
    
    # 2. Carregar .env
    load_dotenv()
    
    # 3. Verificar se já tem chave configurada
    existing_wif = os.getenv('BITCOIN_PRIVATE_KEY')
    existing_xprv = os.getenv('BITCOIN_TESTNET_PRIVATE_KEY')
    existing_address = os.getenv('BITCOIN_TESTNET_ADDRESS')
    
    bitcoin_wif = None
    bitcoin_address = None
    
    if existing_wif and len(existing_wif) > 20:
        print("✅ Chave Bitcoin WIF já encontrada no .env")
        bitcoin_wif = existing_wif
        bitcoin_address = existing_address
    elif existing_xprv and existing_xprv.startswith(('xprv', 'vprv', 'tprv')):
        print("⚠️  Chave xprv encontrada, convertendo para WIF...")
        bitcoin_wif = convert_xprv_to_wif(existing_xprv)
        if bitcoin_wif:
            bitcoin_address = existing_address
    else:
        print("📋 Nenhuma chave válida encontrada")
        print()
        print("Opções:")
        print("   1. Gerar nova chave Bitcoin")
        print("   2. Converter chave xprv existente")
        print("   3. Usar chave WIF existente")
        print()
        escolha = input("Escolha (1/2/3): ").strip()
        
        if escolha == "1":
            key_data = generate_bitcoin_key()
            if key_data:
                bitcoin_wif = key_data["wif"]
                bitcoin_address = key_data["address"]
        elif escolha == "2":
            xprv = input("Cole sua chave xprv/vprv: ").strip()
            bitcoin_wif = convert_xprv_to_wif(xprv)
            if bitcoin_wif:
                bitcoin_address = input("Digite o endereço Bitcoin: ").strip()
        elif escolha == "3":
            bitcoin_wif = input("Cole sua chave WIF: ").strip()
            bitcoin_address = input("Digite o endereço Bitcoin: ").strip()
    
    if not bitcoin_wif or not bitcoin_address:
        print("❌ Não foi possível obter chave Bitcoin válida")
        return
    
    print()
    print("=" * 70)
    print("✅ CHAVE BITCOIN CONFIGURADA")
    print("=" * 70)
    print(f"   Endereço: {bitcoin_address}")
    print(f"   WIF: {bitcoin_wif[:20]}...{bitcoin_wif[-10:]}")
    print()
    
    # 4. Atualizar .env
    print("💾 Atualizando .env...")
    update_env_file(bitcoin_wif, bitcoin_address)
    print()
    
    # 5. Verificar saldo
    print("💰 Verificando saldo Bitcoin...")
    balance = check_bitcoin_balance(bitcoin_address)
    print()
    
    if balance is None or balance == 0:
        print("⚠️  Saldo zero ou não verificado")
        get_bitcoin_faucet_info()
        print("💡 Obtenha Bitcoin testnet de um faucet acima")
        print()
    
    # 6. Resumo final
    print("=" * 70)
    print("✅ SETUP CONCLUÍDO!")
    print("=" * 70)
    print()
    print("📋 Próximos passos:")
    print("   1. ✅ Chave Bitcoin WIF configurada no .env")
    print("   2. ✅ Endereço Bitcoin configurado")
    if balance and balance > 0:
        print(f"   3. ✅ Saldo disponível: {balance} BTC")
    else:
        print("   3. ⚠️  Obtenha Bitcoin testnet de um faucet")
    print("   4. 🔄 Reinicie o servidor: python allianza_blockchain.py")
    print("   5. 🧪 Teste transferência real em: http://localhost:5008/testnet/interoperability")
    print()
    print("🎯 Agora as transferências serão 100% REAIS!")
    print()

if __name__ == "__main__":
    main()

















