@echo off

title Instalador SPHINCS+ / liboqs / liboqs-python - Allianza Blockchain

echo ======================================================================
echo       🚀 INSTALADOR: SPHINCS+ REAL + liboqs + liboqs-python
echo       Compatível com Python 3.13.7 / Windows 10/11
echo ======================================================================
echo.

REM ---------------------------------------------------------
REM 1. Verificar/Instalar Microsoft Build Tools
REM ---------------------------------------------------------
echo 🔧 Verificando Microsoft C++ Build Tools...

REM Verificar se cl.exe (compilador C++) está disponível
where cl >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ✅ Compilador C++ já está disponível no PATH.
    cl 2>&1 | findstr /C:"Microsoft" >nul
    IF %ERRORLEVEL% EQU 0 (
        echo ✅ Microsoft C++ Build Tools detectado.
        goto :check_cmake
    )
)

REM Tentar instalar via winget
echo 🔧 Tentando instalar Microsoft C++ Build Tools via winget...
winget install --id Microsoft.VisualStudio.2022.BuildTools --source winget --accept-package-agreements --accept-source-agreements

REM Mesmo se falhar, verificar se já está instalado
where cl >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Aviso: Build Tools pode não estar no PATH.
    echo    Se a instalação falhou, você pode:
    echo    1. Instalar manualmente: https://visualstudio.microsoft.com/downloads/
    echo    2. Ou continuar - pode estar instalado mas não no PATH
    echo.
    echo    Continuando com a instalação (pode falhar na compilação se não estiver instalado)...
) ELSE (
    echo ✅ Compilador C++ detectado após instalação.
)

:check_cmake

REM ---------------------------------------------------------
REM 2. Verificar/Instalar CMake
REM ---------------------------------------------------------
echo 🧱 Verificando CMake...
where cmake >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ✅ CMake já está instalado.
    cmake --version
    goto :check_git
)

echo 🧱 Instalando CMake...
winget install --id Kitware.CMake --source winget --accept-package-agreements --accept-source-agreements

REM Verificar se CMake foi instalado
where cmake >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  CMake não encontrado após instalação.
    echo    Você pode instalar manualmente: https://cmake.org/download/
    echo    Continuando... (pode falhar na compilação se não estiver instalado)
) ELSE (
    echo ✅ CMake instalado com sucesso.
    cmake --version
)

:check_git

REM ---------------------------------------------------------
REM 3. Verificar Git
REM ---------------------------------------------------------
where git >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 🔧 Git não encontrado. Instalando Git...
    winget install --id Git.Git --source winget
    
    REM Verificar se Git foi instalado com sucesso
    where git >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo ⚠️  Git não foi encontrado após instalação. Verifique manualmente.
        echo    URL: https://git-scm.com/download/win
        echo    Após instalar, reinicie o terminal e execute este script novamente.
        pause
        exit /b 1
    )
    
    echo ✅ Git instalado com sucesso!
    echo ⚠️  IMPORTANTE: Reinicie o terminal e execute este script novamente.
    pause
    exit /b 0
) ELSE (
    echo ✅ Git já está instalado e disponível.
    git --version
)

REM ---------------------------------------------------------
REM 4. Clonar liboqs
REM ---------------------------------------------------------
echo 📥 Baixando liboqs...
IF EXIST liboqs (
    echo ⚠️  Diretório liboqs já existe. Pulando clone...
    cd liboqs
    git pull
    cd ..
) ELSE (
    git clone https://github.com/open-quantum-safe/liboqs.git
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao clonar liboqs.
        pause
        exit /b 1
    )
)

cd liboqs

IF NOT EXIST build (
    mkdir build
)
cd build

echo 🔨 Compilando liboqs...
cmake -GNinja .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao configurar CMake. Verifique se CMake e Ninja estão instalados.
    cd ..\..
    pause
    exit /b 1
)

cmake --build . --config Release

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs.
    cd ..\..
    pause
    exit /b 1
)

echo 📦 Instalando liboqs no sistema...
cmake --install .

IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Aviso: Erro ao instalar liboqs via CMake. Continuando...
)

cd ..\..

REM ---------------------------------------------------------
REM 5. Clonar liboqs-python compatível com Python 3.13.7
REM ---------------------------------------------------------
echo 📥 Baixando liboqs-python...
IF EXIST liboqs-python (
    echo ⚠️  Diretório liboqs-python já existe. Pulando clone...
    cd liboqs-python
    git pull
    cd ..
) ELSE (
    git clone https://github.com/open-quantum-safe/liboqs-python.git
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao clonar liboqs-python.
        pause
        exit /b 1
    )
)

cd liboqs-python

echo 🔨 Compilando liboqs-python para Python 3.13.7...
python setup.py build

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs-python.
    cd ..
    pause
    exit /b 1
)

python setup.py install

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao instalar liboqs-python.
    cd ..
    pause
    exit /b 1
)

cd ..

REM ---------------------------------------------------------
REM 6. Testar SPHINCS+
REM ---------------------------------------------------------
echo 🧪 Testando SPHINCS+ real...
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
except Exception as e:
    print("❌ Erro no teste:", e)
    import traceback
    traceback.print_exc()
END

IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Aviso: Teste de SPHINCS+ falhou. Verifique os logs acima.
)

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


