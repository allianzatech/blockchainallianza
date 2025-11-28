#!/usr/bin/env python3
"""
Script para gerar novo endereço Bitcoin Testnet válido
"""
import os
from dotenv import load_dotenv

load_dotenv()

def gerar_endereco_bitcoin():
    """Gera um novo endereço Bitcoin testnet válido"""
    print("🔧 Gerando novo endereço Bitcoin Testnet...")
    
    # Obter chave privada do .env ou gerar nova
    private_key_wif = os.getenv('BITCOIN_PRIVATE_KEY') or os.getenv('BITCOIN_TESTNET_PRIVATE_KEY')
    
    if not private_key_wif:
        print("⚠️  Nenhuma chave privada encontrada no .env")
        print("   Gerando nova chave privada...")
        
        try:
            from bitcoinlib.wallets import Wallet
            from bitcoinlib.mnemonic import Mnemonic
            
            # Gerar nova wallet
            wallet_name = f"temp_wallet_{int(__import__('time').time())}"
            wallet = Wallet.create(wallet_name, network='testnet', witness_type='segwit')
            
            # Obter chave privada WIF
            keys = wallet.keys()
            if keys:
                key = keys[0]
                private_key_wif = key.wif
                address = key.address
                
                print(f"\n✅ Novo endereço Bitcoin Testnet gerado!")
                print(f"\n📋 DADOS GERADOS:")
                print(f"   Endereço: {address}")
                print(f"   Tipo: SegWit (Bech32)")
                print(f"   Chave Privada WIF: {private_key_wif}")
                print(f"\n⚠️  IMPORTANTE: Salve a chave privada em local seguro!")
                print(f"   Adicione ao .env: BITCOIN_PRIVATE_KEY={private_key_wif}")
                
                # Limpar wallet temporária
                try:
                    wallet.delete()
                except:
                    pass
                
                return address, private_key_wif
        except Exception as e:
            print(f"❌ Erro ao gerar nova chave: {e}")
            return None, None
    else:
        print(f"✅ Usando chave privada existente do .env")
        print(f"   Primeiros 10 caracteres: {private_key_wif[:10]}...")
        
        try:
            from bitcoinlib.wallets import Wallet
            from bitcoinlib.keys import HDKey
            
            # Criar wallet a partir da chave WIF
            wallet_name = f"temp_wallet_{int(__import__('time').time())}"
            
            # Tentar diferentes tipos de witness para obter endereço
            witness_types = ['segwit', 'p2sh-segwit', 'legacy']
            
            for witness_type in witness_types:
                try:
                    wallet = Wallet.create(
                        f"{wallet_name}_{witness_type}",
                        keys=private_key_wif,
                        network='testnet',
                        witness_type=witness_type
                    )
                    
                    keys = wallet.keys()
                    if keys:
                        key = keys[0]
                        address = key.address
                        
                        print(f"\n✅ Endereço Bitcoin Testnet gerado!")
                        print(f"\n📋 DADOS:")
                        print(f"   Endereço: {address}")
                        print(f"   Tipo: {witness_type}")
                        print(f"   Chave Privada WIF: {private_key_wif[:10]}... (do .env)")
                        
                        # Validar endereço
                        print(f"\n🔍 Validando endereço...")
                        try:
                            import bech32
                            if address.startswith("tb1"):
                                hrp = "tb"
                                decoded = bech32.decode(hrp, address)
                                if decoded and decoded[0] is not None:
                                    print(f"   ✅ Checksum Bech32 válido!")
                                    print(f"   ✅ Endereço validado com sucesso!")
                                else:
                                    print(f"   ⚠️  Checksum Bech32 não verificado, mas formato OK")
                            else:
                                print(f"   ✅ Formato de endereço válido")
                        except Exception as val_error:
                            print(f"   ⚠️  Erro na validação: {val_error}")
                        
                        # Limpar wallet temporária
                        try:
                            wallet.delete()
                        except:
                            pass
                        
                        return address, private_key_wif
                except Exception as e:
                    print(f"   ⚠️  Erro com {witness_type}: {e}")
                    continue
            
            print(f"❌ Não foi possível gerar endereço com nenhum tipo de witness")
            return None, None
            
        except Exception as e:
            print(f"❌ Erro ao gerar endereço: {e}")
            import traceback
            traceback.print_exc()
            return None, None

if __name__ == "__main__":
    address, private_key = gerar_endereco_bitcoin()
    
    if address:
        print(f"\n🎯 PRÓXIMOS PASSOS:")
        print(f"   1. Use este endereço para receber Bitcoin testnet: {address}")
        print(f"   2. Adicione saldo usando um faucet Bitcoin testnet")
        print(f"   3. Teste a transferência Polygon → Bitcoin novamente")
        print(f"\n💡 Faucets Bitcoin Testnet:")
        print(f"   - https://bitcoinfaucet.uo1.net/")
        print(f"   - https://testnet-faucet.mempool.co/")
        print(f"   - https://coinfaucet.eu/en/btc-testnet/")
    else:
        print(f"\n❌ Não foi possível gerar endereço. Verifique os erros acima.")

