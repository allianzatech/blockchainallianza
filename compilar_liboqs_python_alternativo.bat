@echo off

title Compilar liboqs-python (Método Alternativo) - Allianza Blockchain

echo ======================================================================
echo       🐍 COMPILANDO LIBOQS-PYTHON (MÉTODO ALTERNATIVO)
echo ======================================================================
echo.

REM Verificar se liboqs foi compilado (aceita .lib ou .dll)
IF NOT EXIST "liboqs\build\lib\oqs.lib" (
    IF NOT EXIST "liboqs\build\oqs.lib" (
        IF NOT EXIST "liboqs\build\liboqs.lib" (
            IF NOT EXIST "liboqs\build\oqs.dll" (
                IF NOT EXIST "liboqs\build\liboqs.dll" (
                    echo ❌ liboqs não foi compilado ainda!
                    echo    Execute primeiro: compilar_liboqs_dll.bat
                    pause
                    exit /b 1
                )
            )
        )
    )
)

echo ✅ liboqs encontrado!

REM Verificar se liboqs-python já foi clonado
IF NOT EXIST "liboqs-python" (
    echo 📥 Clonando liboqs-python...
    git clone https://github.com/open-quantum-safe/liboqs-python.git
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao clonar liboqs-python.
        pause
        exit /b 1
    )
)

cd liboqs-python

REM Configurar variável de ambiente para liboqs encontrar as bibliotecas
echo.
echo 🔧 Configurando variáveis de ambiente...

REM Encontrar o diretório com as bibliotecas
SET LIBOQS_DIR=..\liboqs\build

IF EXIST "..\liboqs\build\bin" (
    SET LIBOQS_BIN_DIR=..\liboqs\build\bin
) ELSE (
    SET LIBOQS_BIN_DIR=..\liboqs\build\lib
)

IF EXIST "..\liboqs\build\lib" (
    SET LIBOQS_LIB_DIR=..\liboqs\build\lib
) ELSE (
    SET LIBOQS_LIB_DIR=..\liboqs\build
)

echo    LIBOQS_DIR: %LIBOQS_DIR%
echo    LIBOQS_BIN_DIR: %LIBOQS_BIN_DIR%
echo    LIBOQS_LIB_DIR: %LIBOQS_LIB_DIR%

REM Configurar variáveis de ambiente
SET CMAKE_PREFIX_PATH=%LIBOQS_DIR%
SET OQS_DIR=%LIBOQS_DIR%

echo.
echo 🔨 Compilando liboqs-python...
echo    Isso pode levar alguns minutos...
python setup.py build --cmake-args="-DOQS_DIR=%LIBOQS_DIR%"

IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Erro com cmake-args. Tentando sem argumentos...
    python setup.py build
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao compilar liboqs-python.
        cd ..
        pause
        exit /b 1
    )
)

echo.
echo 📦 Instalando liboqs-python...
python setup.py install

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao instalar liboqs-python.
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ======================================================================
echo 🧪 TESTANDO SPHINCS+ REAL...
echo ======================================================================

REM Adicionar diretório da DLL ao PATH temporariamente
SET PATH=%LIBOQS_BIN_DIR%;%PATH%

python - << END
import os
import sys

# Adicionar diretório da DLL ao PATH do Python
liboqs_bin = r"%LIBOQS_BIN_DIR%"
if liboqs_bin and os.path.exists(liboqs_bin):
    os.add_dll_directory(liboqs_bin)

try:
    from oqs import Signature
    
    # Tentar diferentes variantes de SPHINCS+
    algorithms = [
        "SPHINCS+-SHAKE-128f",
        "SPHINCS+-SHA256-128f",
        "SPHINCS+-SHAKE-192f"
    ]
    
    sig_mechanisms = Signature.get_enabled_sig_mechanisms()
    print(f"✅ Assinaturas disponíveis: {len(sig_mechanisms)}")
    
    for alg in algorithms:
        if alg in sig_mechanisms:
            print(f"\n🧪 Testando: {alg}")
            sig = Signature(alg)
            public_key = sig.generate_keypair()
            message = b"Allianza Blockchain - Quantum Test"
            signature = sig.sign(message)
            valid = sig.verify(message, signature, public_key)
            
            print("=" * 60)
            print("🔐 SPHINCS+ REAL TEST")
            print(f"Algoritmo: {alg}")
            print(f"Válido?: {valid}")
            print("=" * 60)
            
            if valid:
                print("✅✅✅ SPHINCS+ REAL FUNCIONANDO PERFEITAMENTE!")
                print()
                print("🎉 INSTALAÇÃO COMPLETA!")
                print()
                print("📋 PRÓXIMOS PASSOS:")
                print("   1. Execute: python PROVA_PILAR_2_SEGURANCA_QUANTICA.py")
                print("   2. Verifique se SPHINCS+ está em modo 'real'")
                print("   3. Confirme que QRS-3 está com Redundancy Level: 3")
                break
            else:
                print(f"❌ Erro: Assinatura inválida para {alg}")
    else:
        print("⚠️  Nenhuma variante de SPHINCS+ disponível")
        print("   Algoritmos disponíveis:", list(sig_mechanisms)[:10])
        
except ImportError as e:
    print("❌ Erro ao importar oqs:", e)
    print("   Verifique se liboqs-python foi instalado corretamente.")
    import traceback
    traceback.print_exc()
except Exception as e:
    print("❌ Erro no teste:", e)
    import traceback
    traceback.print_exc()
END

echo.
pause









