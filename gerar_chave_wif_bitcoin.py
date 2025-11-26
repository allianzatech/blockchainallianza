"""
Script para gerar uma chave WIF Bitcoin válida para testnet
"""
import os
from bitcoinlib.keys import HDKey
from bitcoinlib.mnemonic import Mnemonic
import secrets

def gerar_chave_wif():
    """Gera uma nova chave WIF Bitcoin válida"""
    print("=" * 70)
    print("🔑 GERADOR DE CHAVE WIF BITCOIN (TESTNET)")
    print("=" * 70)
    print()
    
    print("🔄 Gerando chave privada aleatória...")
    
    # Método 1: Gerar chave privada aleatória diretamente
    try:
        # Gerar 32 bytes aleatórios (chave privada)
        private_key_bytes = secrets.token_bytes(32)
        
        # Criar HDKey a partir dos bytes da chave privada
        # IMPORTANTE: passar os bytes diretamente e especificar que é privada
        hd_key = HDKey(private_key_bytes, network='testnet', compressed=True)
        
        # Verificar se é chave privada
        if not hd_key.is_private:
            # Se não for privada, criar novamente forçando privada
            # Usar método alternativo: criar wallet e extrair WIF
            from bitcoinlib.wallets import Wallet
            import time
            
            wallet_name = f"temp_wif_gen_{int(time.time())}"
            wallet = Wallet.create(wallet_name, network='testnet', witness_type='segwit')
            key = wallet.keys()[0]
            
            # Obter a chave privada em formato WIF
            # O bitcoinlib armazena como HDKey, precisamos acessar o WIF correto
            # Usar o método privado_key() ou acessar diretamente
            try:
                # Tentar obter WIF do HDKey subjacente
                hd_key_private = key.key()
                wif = hd_key_private.wif()
                address = hd_key_private.address()
            except:
                # Método alternativo: usar o método privado_key()
                private_key_obj = key.key()
                wif = private_key_obj.wif()
                address = private_key_obj.address()
            
            # Limpar wallet
            try:
                wallet.delete()
            except:
                pass
        else:
            # Obter WIF (Wallet Import Format) - é uma propriedade, não método
            wif = hd_key.wif if hasattr(hd_key, 'wif') and not callable(hd_key.wif) else hd_key.wif()
            address = hd_key.address if hasattr(hd_key, 'address') and not callable(hd_key.address) else hd_key.address()
            
            # Se ainda for extended key, usar método alternativo
            if wif.startswith(('xprv', 'vprv', 'tprv', 'xpub', 'vpub', 'tpub')):
                # Usar wallet para gerar WIF real
                from bitcoinlib.wallets import Wallet
                import time
                
                wallet_name = f"temp_wif_gen_{int(time.time())}"
                wallet = Wallet.create(wallet_name, network='testnet', witness_type='segwit')
                key = wallet.keys()[0]
                private_key_obj = key.key()
                wif = private_key_obj.wif()
                address = private_key_obj.address()
                
                try:
                    wallet.delete()
                except:
                    pass
        
        print("✅ Chave WIF gerada com sucesso!")
        print()
        print("=" * 70)
        print("📋 SUA NOVA CHAVE WIF")
        print("=" * 70)
        print()
        print(f"🔑 WIF (Private Key):")
        print(f"   {wif}")
        print()
        print(f"🏦 Endereço Bitcoin (Testnet):")
        print(f"   {address}")
        print()
        print("=" * 70)
        print("📝 ADICIONE AO SEU .env")
        print("=" * 70)
        print()
        print("Abra o arquivo .env e substitua:")
        print()
        print(f"BITCOIN_PRIVATE_KEY={wif}")
        print(f"BITCOIN_TESTNET_PRIVATE_KEY={wif}")
        print(f"BITCOIN_TESTNET_ADDRESS={address}")
        print()
        print("=" * 70)
        print("⚠️  IMPORTANTE")
        print("=" * 70)
        print()
        print("1. ✅ Guarde esta chave em local SEGURO")
        print("2. ✅ Esta é uma chave PRIVADA - NÃO compartilhe!")
        print("3. ✅ Use apenas em TESTNET (não use em mainnet)")
        print("4. ✅ Obtenha fundos de teste no faucet:")
        print(f"   - https://bitcoinfaucet.uo1.net/")
        print(f"   - https://testnet-faucet.mempool.co/")
        print(f"   - Endereço: {address}")
        print()
        print("5. ✅ Depois de atualizar o .env, execute:")
        print("   python validar_e_testar_chave_wif.py")
        print()
        
        # Perguntar se quer atualizar o .env automaticamente
        print("=" * 70)
        resposta = input("Deseja atualizar o arquivo .env automaticamente? (s/n): ").strip().lower()
        
        if resposta == 's':
            atualizar_env(wif, address)
        else:
            print()
            print("💡 Você pode atualizar o .env manualmente usando as informações acima.")
        
        return wif, address
        
    except Exception as e:
        print(f"❌ Erro ao gerar chave: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def atualizar_env(wif, address):
    """Atualiza o arquivo .env com a nova chave"""
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print(f"❌ Arquivo .env não encontrado em {os.path.abspath(env_path)}")
        print("💡 Crie o arquivo .env manualmente ou execute este script na raiz do projeto.")
        return False
    
    try:
        # Ler arquivo .env
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Atualizar ou adicionar linhas
        updated_keys = {
            'BITCOIN_PRIVATE_KEY': wif,
            'BITCOIN_TESTNET_PRIVATE_KEY': wif,
            'BITCOIN_TESTNET_ADDRESS': address
        }
        
        # Verificar quais linhas já existem
        existing_keys = set()
        for line in lines:
            for key in updated_keys:
                if line.strip().startswith(f'{key}='):
                    existing_keys.add(key)
        
        # Reescrever arquivo
        with open(env_path, 'w', encoding='utf-8') as f:
            for line in lines:
                updated = False
                for key, value in updated_keys.items():
                    if line.strip().startswith(f'{key}='):
                        f.write(f'{key}={value}\n')
                        updated = True
                        existing_keys.add(key)
                        break
                if not updated:
                    f.write(line)
            
            # Adicionar linhas que não existiam
            for key, value in updated_keys.items():
                if key not in existing_keys:
                    f.write(f'{key}={value}\n')
        
        print()
        print("✅ Arquivo .env atualizado com sucesso!")
        print()
        print("🔄 Próximos passos:")
        print("   1. Execute: python validar_e_testar_chave_wif.py")
        print("   2. Obtenha fundos de teste no faucet")
        print("   3. Reinicie o servidor")
        print("   4. Teste a transferência Polygon → Bitcoin")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar .env: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    gerar_chave_wif()

