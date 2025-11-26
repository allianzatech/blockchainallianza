@echo off

title Compilar liboqs-python - Allianza Blockchain

echo ======================================================================
echo       🐍 COMPILANDO LIBOQS-PYTHON (Passo 2 de 2)
echo ======================================================================
echo.

REM Verificar se liboqs foi compilado (verificar DLL primeiro, depois LIB)
set "LIBOQS_DLL_FOUND=false"
set "LIBOQS_LIB_FOUND=false"

IF EXIST "liboqs\build\bin\Release\oqs.dll" (
    set "LIBOQS_DLL_FOUND=true"
    echo ✅ DLL encontrada em: liboqs\build\bin\Release\oqs.dll
    REM Copiar DLL para local padrão para facilitar acesso
    copy "liboqs\build\bin\Release\oqs.dll" "liboqs\build\oqs.dll" >nul 2>&1
    echo    Copiada para: liboqs\build\oqs.dll
) ELSE IF EXIST "liboqs\build\bin\oqs.dll" (
    set "LIBOQS_DLL_FOUND=true"
    echo ✅ DLL encontrada em: liboqs\build\bin\oqs.dll
) ELSE IF EXIST "liboqs\build\oqs.dll" (
    set "LIBOQS_DLL_FOUND=true"
    echo ✅ DLL encontrada em: liboqs\build\oqs.dll
)

IF EXIST "liboqs\build\lib\Release\oqs.lib" (
    set "LIBOQS_LIB_FOUND=true"
    echo ✅ LIB encontrada em: liboqs\build\lib\Release\oqs.lib
) ELSE IF EXIST "liboqs\build\lib\oqs.lib" (
    set "LIBOQS_LIB_FOUND=true"
    echo ✅ LIB encontrada em: liboqs\build\lib\oqs.lib
)

IF "%LIBOQS_DLL_FOUND%"=="false" (
    IF "%LIBOQS_LIB_FOUND%"=="false" (
        echo ❌ liboqs não foi compilado ainda!
        echo    Execute primeiro: compilar_liboqs_dll.bat
        pause
        exit /b 1
    ) ELSE (
        echo ⚠️  Apenas biblioteca estática (.lib) encontrada. DLL não encontrada.
        echo    Isso pode funcionar, mas SPHINCS+ pode não estar em modo real.
    )
)

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

REM Configurar variáveis de ambiente para liboqs-python encontrar liboqs
REM Definir caminhos baseados na localização da DLL/LIB
set "OQS_INSTALL_DIR=%CD%\..\liboqs\build"
set "OQS_LIB_DIR=%CD%\..\liboqs\build\lib\Release"
REM Headers estão em build/include após compilação
set "OQS_INCLUDE_DIR=%CD%\..\liboqs\build\include"
set "OQS_BIN_DIR=%CD%\..\liboqs\build\bin\Release"

REM Adicionar diretório DLL ao PATH para runtime
set "PATH=%OQS_BIN_DIR%;%PATH%"

echo.
echo 🔧 Configurando variáveis de ambiente...
echo    OQS_INSTALL_DIR=%OQS_INSTALL_DIR%
echo    OQS_LIB_DIR=%OQS_LIB_DIR%
echo    OQS_INCLUDE_DIR=%OQS_INCLUDE_DIR%
echo    OQS_BIN_DIR=%OQS_BIN_DIR%

echo.
echo 🔨 Compilando liboqs-python...
python setup.py build

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs-python.
    cd ..
    pause
    exit /b 1
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

python - << END
try:
    from oqs import Signature
    
    alg = "SPHINCS+-SHAKE-128f"
    sig = Signature(alg)
    
    public_key = sig.generate_keypair()
    message = b"Allianza Blockchain - Quantum Test"
    signature = sig.sign(message)
    valid = sig.verify(message, signature, public_key)
    
    print("====================================================")
    print("🔐 SPHINCS+ REAL TEST")
    print("Algoritmo:", alg)
    print("Válido?:", valid)
    print("====================================================")
    
    if valid:
        print("✅✅✅ SPHINCS+ REAL FUNCIONANDO PERFEITAMENTE!")
        print()
        print("🎉 INSTALAÇÃO COMPLETA!")
        print()
        print("📋 PRÓXIMOS PASSOS:")
        print("   1. Execute: python PROVA_PILAR_2_SEGURANCA_QUANTICA.py")
        print("   2. Verifique se SPHINCS+ está em modo 'real'")
        print("   3. Confirme que QRS-3 está com Redundancy Level: 3")
    else:
        print("❌ Erro: Assinatura inválida")
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

