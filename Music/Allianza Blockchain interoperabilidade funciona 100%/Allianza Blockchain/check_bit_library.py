#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script para verificar e instalar biblioteca 'bit' se necessário
"""

import sys
import subprocess

def check_bit_library():
    """Verificar se biblioteca 'bit' está instalada"""
    try:
        from bit import PrivateKey
        from bit.network import NetworkAPI
        print("✅ Biblioteca 'bit' está instalada e funcionando!")
        return True
    except ImportError as e:
        print(f"❌ Biblioteca 'bit' não está instalada: {e}")
        print(f"\n💡 Para instalar, execute:")
        print(f"   pip install bit")
        return False
    except Exception as e:
        print(f"⚠️  Erro ao importar biblioteca 'bit': {e}")
        return False

def install_bit_library():
    """Tentar instalar biblioteca 'bit'"""
    try:
        print("📦 Tentando instalar biblioteca 'bit'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "bit>=0.8.0"])
        print("✅ Biblioteca 'bit' instalada com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar biblioteca 'bit': {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🔍 VERIFICAÇÃO DA BIBLIOTECA 'bit'")
    print("="*60)
    
    if check_bit_library():
        print("\n✅ Tudo OK! Biblioteca 'bit' está disponível.")
        sys.exit(0)
    else:
        print("\n❌ Biblioteca 'bit' não está disponível.")
        response = input("\nDeseja instalar agora? (s/n): ")
        if response.lower() == 's':
            if install_bit_library():
                print("\n✅ Instalação concluída! Testando novamente...")
                if check_bit_library():
                    print("\n✅✅✅ Biblioteca 'bit' instalada e funcionando!")
                    sys.exit(0)
                else:
                    print("\n⚠️  Biblioteca instalada mas ainda há problemas.")
                    sys.exit(1)
            else:
                print("\n❌ Falha na instalação. Tente instalar manualmente:")
                print("   pip install bit")
                sys.exit(1)
        else:
            print("\n⚠️  Instalação cancelada. Execute manualmente:")
            print("   pip install bit")
            sys.exit(1)

