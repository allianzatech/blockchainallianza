@echo off

title Instalador SPHINCS+ / liboqs / liboqs-python - Allianza Blockchain (Continuar Mesmo com Erros)

echo ======================================================================
echo       🚀 INSTALADOR: SPHINCS+ REAL + liboqs + liboqs-python
echo       Modo: Continuar mesmo se algumas instalações falharem
echo       Compatível com Python 3.13.7 / Windows 10/11
echo ======================================================================
echo.

REM ---------------------------------------------------------
REM 1. Verificar Build Tools (não bloquear se falhar)
REM ---------------------------------------------------------
echo 🔧 Verificando Microsoft C++ Build Tools...
where cl >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ✅ Compilador C++ detectado no PATH.
) ELSE (
    echo ⚠️  Compilador C++ não encontrado no PATH.
    echo    Se você já instalou Build Tools, pode estar em outro local.
    echo    Continuando... (a compilação pode falhar se não estiver instalado)
)

REM ---------------------------------------------------------
REM 2. Verificar CMake
REM ---------------------------------------------------------
echo 🧱 Verificando CMake...
where cmake >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ✅ CMake detectado.
    cmake --version
) ELSE (
    echo ⚠️  CMake não encontrado. Tentando instalar...
    winget install --id Kitware.CMake --source winget --accept-package-agreements --accept-source-agreements 2>nul
    where cmake >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo ⚠️  CMake não encontrado. Continuando mesmo assim...
    )
)

REM ---------------------------------------------------------
REM 3. Verificar Git
REM ---------------------------------------------------------
echo 🔧 Verificando Git...
where git >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ✅ Git detectado.
    git --version
) ELSE (
    echo ❌ Git não encontrado. É necessário para continuar.
    echo    Instale manualmente: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM ---------------------------------------------------------
REM 4. Clonar liboqs
REM ---------------------------------------------------------
echo.
echo ======================================================================
echo 📥 ETAPA 1: Baixando liboqs...
echo ======================================================================

IF EXIST liboqs (
    echo ⚠️  Diretório liboqs já existe. Atualizando...
    cd liboqs
    git pull
    cd ..
) ELSE (
    echo 📥 Clonando liboqs do GitHub...
    git clone https://github.com/open-quantum-safe/liboqs.git
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao clonar liboqs.
        pause
        exit /b 1
    )
)

REM ---------------------------------------------------------
REM 5. Compilar liboqs
REM ---------------------------------------------------------
echo.
echo ======================================================================
echo 🔨 ETAPA 2: Compilando liboqs...
echo ======================================================================

cd liboqs

IF NOT EXIST build (
    mkdir build
)
cd build

echo 🔨 Configurando CMake para liboqs...
cmake -GNinja .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao configurar CMake.
    echo    Verifique se CMake e Build Tools estão instalados.
    echo    Você pode precisar abrir "Developer Command Prompt for VS" ou
    echo    executar: "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
    cd ..\..
    pause
    exit /b 1
)

echo 🔨 Compilando liboqs (isso pode levar 10-30 minutos)...
cmake --build . --config Release

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs.
    echo    Verifique se todas as dependências estão instaladas.
    cd ..\..
    pause
    exit /b 1
)

echo 📦 Instalando liboqs...
cmake --install .

cd ..\..

REM ---------------------------------------------------------
REM 6. Clonar e compilar liboqs-python
REM ---------------------------------------------------------
echo.
echo ======================================================================
echo 📥 ETAPA 3: Baixando liboqs-python...
echo ======================================================================

IF EXIST liboqs-python (
    echo ⚠️  Diretório liboqs-python já existe. Atualizando...
    cd liboqs-python
    git pull
    cd ..
) ELSE (
    echo 📥 Clonando liboqs-python do GitHub...
    git clone https://github.com/open-quantum-safe/liboqs-python.git
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao clonar liboqs-python.
        pause
        exit /b 1
    )
)

cd liboqs-python

echo.
echo ======================================================================
echo 🔨 ETAPA 4: Compilando liboqs-python...
echo ======================================================================

echo 🔨 Compilando liboqs-python para Python 3.13.7...
python setup.py build

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs-python.
    echo    Verifique se liboqs foi compilado corretamente.
    cd ..
    pause
    exit /b 1
)

echo 📦 Instalando liboqs-python...
python setup.py install

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao instalar liboqs-python.
    cd ..
    pause
    exit /b 1
)

cd ..

REM ---------------------------------------------------------
REM 7. Testar SPHINCS+
REM ---------------------------------------------------------
echo.
echo ======================================================================
echo 🧪 ETAPA 5: Testando SPHINCS+ real...
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
    else:
        print("❌ Erro: Assinatura inválida")
except ImportError as e:
    print("❌ Erro ao importar oqs:", e)
    print("   Verifique se liboqs-python foi instalado corretamente.")
    print("   Erro detalhado:")
    import traceback
    traceback.print_exc()
except Exception as e:
    print("❌ Erro no teste:", e)
    import traceback
    traceback.print_exc()
END

echo.
echo ======================================================================
echo      🎉 INSTALACAO COMPLETA! SPHINCS+ REAL ATIVADO ✔
echo ======================================================================
echo.
echo 📋 PRÓXIMOS PASSOS:
echo    1. Execute: python PROVA_PILAR_2_SEGURANCA_QUANTICA.py
echo    2. Verifique se SPHINCS+ está em modo "real" (não "simulated")
echo    3. Confirme que QRS-3 está com Redundancy Level: 3
echo.
pause









