# ATIVAR_QRS3_COMPLETO.py
# 🔐 Script para ativar QRS-3 completo (SPHINCS+ real)
# Instala liboqs-python e valida QRS-3 completo

import subprocess
import sys
import os
from pathlib import Path

def install_liboqs():
    """Instalar liboqs-python"""
    print("="*70)
    print("🔐 INSTALAÇÃO: liboqs-python")
    print("="*70)
    print("\n📦 Instalando liboqs-python...")
    print("   (Isso pode levar alguns minutos)")
    
    try:
        # Tentar instalar
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "liboqs-python"],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutos timeout
        )
        
        if result.returncode == 0:
            print("✅ liboqs-python instalado com sucesso!")
            return True
        else:
            print(f"⚠️  Erro na instalação:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout na instalação (mais de 10 minutos)")
        return False
    except Exception as e:
        print(f"❌ Erro ao instalar: {e}")
        return False

def check_liboqs_installed():
    """Verificar se liboqs-python está instalado"""
    try:
        import oqs
        print("✅ liboqs-python está instalado e importável!")
        return True
    except ImportError:
        print("❌ liboqs-python não está instalado")
        return False

def test_qrs3_complete():
    """Testar QRS-3 completo após instalação"""
    print("\n" + "="*70)
    print("🔐🔐🔐 TESTE: QRS-3 COMPLETO (SPHINCS+ REAL)")
    print("="*70)
    
    try:
        from quantum_security import QuantumSecuritySystem
        
        system = QuantumSecuritySystem()
        
        # Gerar QRS-3
        print("\n1. Gerando QRS-3 keypair...")
        keypair_result = system.generate_qrs3_keypair()
        
        if not keypair_result.get("success"):
            print(f"❌ Erro ao gerar QRS-3: {keypair_result.get('error')}")
            return False
        
        keypair_id = keypair_result["keypair_id"]
        redundancy_level = keypair_result.get("redundancy_level", 0)
        sphincs_available = keypair_result.get("sphincs_available", False)
        
        print(f"   ✅ Keypair ID: {keypair_id}")
        print(f"   ✅ Redundancy Level: {redundancy_level}")
        print(f"   ✅ SPHINCS+ Available: {sphincs_available}")
        
        if redundancy_level == 3 and sphincs_available:
            print("\n✅✅✅ QRS-3 COMPLETO ATIVADO!")
            print("   • Redundancy Level: 3 (TRIPLA REDUNDÂNCIA)")
            print("   • SPHINCS+ REAL funcionando")
            print("   • ECDSA + ML-DSA + SPHINCS+ (REAL)")
        else:
            print(f"\n⚠️  QRS-3 ainda em modo QRS-2")
            print(f"   • Redundancy Level: {redundancy_level}")
            print(f"   • SPHINCS+ Available: {sphincs_available}")
            return False
        
        # Testar assinatura
        print("\n2. Testando assinatura QRS-3...")
        message = b"Test message for QRS-3 complete validation"
        sign_result = system.sign_qrs3(keypair_id, message)
        
        if not sign_result.get("success"):
            print(f"❌ Erro ao assinar: {sign_result.get('error')}")
            return False
        
        print("   ✅ Assinatura QRS-3 criada com sucesso!")
        print(f"   • Classic Signature: {sign_result.get('classic_signature', 'N/A')[:50]}...")
        print(f"   • ML-DSA Signature: {sign_result.get('ml_dsa_signature', 'N/A')[:50]}...")
        print(f"   • SPHINCS+ Signature: {sign_result.get('sphincs_signature', 'N/A')[:50]}...")
        print(f"   • Redundancy Level: {sign_result.get('redundancy_level', 0)}")
        
        if sign_result.get("redundancy_level") == 3:
            print("\n✅✅✅ QRS-3 COMPLETO VALIDADO!")
            return True
        else:
            print(f"\n⚠️  Redundancy Level: {sign_result.get('redundancy_level', 0)} (esperado: 3)")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("="*70)
    print("🔐 ATIVAÇÃO DO QRS-3 COMPLETO")
    print("="*70)
    print("\nEste script irá:")
    print("1. Verificar se liboqs-python está instalado")
    print("2. Instalar liboqs-python se necessário")
    print("3. Validar QRS-3 completo (Redundancy Level: 3)")
    print("="*70)
    
    # Passo 1: Verificar instalação
    print("\n📋 PASSO 1: Verificando instalação...")
    if check_liboqs_installed():
        print("✅ liboqs-python já está instalado!")
    else:
        print("⚠️  liboqs-python não está instalado")
        print("\n📋 PASSO 2: Instalando liboqs-python...")
        
        resposta = input("\nDeseja instalar liboqs-python agora? (s/n): ").strip().lower()
        if resposta != 's':
            print("❌ Instalação cancelada pelo usuário")
            return
        
        if not install_liboqs():
            print("\n❌ Falha na instalação de liboqs-python")
            print("   Você pode tentar instalar manualmente:")
            print("   pip install liboqs-python")
            return
        
        # Verificar novamente
        if not check_liboqs_installed():
            print("\n❌ liboqs-python instalado mas não importável")
            print("   Tente reiniciar o Python ou verificar a instalação")
            return
    
    # Passo 3: Testar QRS-3 completo
    print("\n📋 PASSO 3: Testando QRS-3 completo...")
    if test_qrs3_complete():
        print("\n" + "="*70)
        print("✅✅✅ QRS-3 COMPLETO ATIVADO E VALIDADO!")
        print("="*70)
        print("\n📊 Próximos passos:")
        print("   1. Execute: python PROVA_PILAR_2_SEGURANCA_QUANTICA.py")
        print("   2. Execute: python TESTE_PERFORMANCE_PQC.py")
        print("   3. Verifique que Redundancy Level: 3")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("⚠️  QRS-3 ainda não está completo")
        print("="*70)
        print("\nPossíveis causas:")
        print("   1. liboqs-python não está instalado corretamente")
        print("   2. SPHINCS+ não está disponível na biblioteca")
        print("   3. Reinicie o Python após instalação")
        print("\nTente:")
        print("   pip install liboqs-python")
        print("   (Reinicie o Python e execute novamente)")
        print("="*70)

if __name__ == "__main__":
    main()





















