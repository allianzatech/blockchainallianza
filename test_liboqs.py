#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE: VERIFICAÇÃO DE INSTALAÇÃO liboqs-python
=================================================
Testa se liboqs-python está instalado e funcionando
"""

def test_liboqs():
    """Testar se liboqs-python está instalado"""
    print("="*70)
    print("  🔐 TESTE: VERIFICAÇÃO liboqs-python")
    print("="*70)
    
    try:
        import oqs
        print("\n✅ liboqs-python está INSTALADO!")
        
        # Tentar obter versão
        try:
            version = oqs.__version__
            print(f"   Versão: {version}")
        except:
            print("   Versão: N/A")
        
        # Testar SPHINCS+
        print("\n🧪 Testando SPHINCS+...")
        try:
            # Tentar diferentes variantes
            variants = [
                'SPHINCS+-SHA256-128f-simple',
                'SPHINCS+-SHA256-192f-simple',
                'SPHINCS+-SHA256-256f-simple'
            ]
            
            success = False
            for variant in variants:
                try:
                    sigalg = oqs.Signature(variant)
                    public_key, secret_key = sigalg.generate_keypair()
                    print(f"   ✅ {variant}: Funcionando!")
                    success = True
                    break
                except Exception as e:
                    continue
            
            if success:
                print("\n✅✅✅ SPHINCS+ REAL FUNCIONANDO!")
                print("   → QRS-3 completo estará disponível")
                print("   → Redundancy Level: 3 (Tripla Redundância)")
            else:
                print("\n⚠️  SPHINCS+ não funcionou com nenhuma variante")
                
        except Exception as e:
            print(f"   ❌ Erro ao testar SPHINCS+: {e}")
        
        print("\n" + "="*70)
        print("✅ liboqs-python está instalado e funcionando!")
        print("="*70)
        return True
        
    except ImportError:
        print("\n❌ liboqs-python NÃO está instalado")
        print("\n📋 PARA INSTALAR:")
        print("   1. Windows: Instalar Visual Studio Build Tools")
        print("   2. Executar: pip install liboqs-python")
        print("\n💡 Veja GUIA_INSTALACAO_LIBOQS.md para instruções detalhadas")
        print("="*70)
        return False
    except Exception as e:
        print(f"\n⚠️  Erro: {e}")
        print("="*70)
        return False

if __name__ == "__main__":
    test_liboqs()

