@echo off

title Instalador SPHINCS+ com Visual Studio - Allianza Blockchain

echo ======================================================================
echo       🚀 INSTALADOR: SPHINCS+ REAL (com Visual Studio)
echo       Configura ambiente VS automaticamente
echo ======================================================================
echo.

REM ---------------------------------------------------------
REM Configurar ambiente Visual Studio
REM ---------------------------------------------------------
echo 🔧 Configurando ambiente Visual Studio...

REM Tentar encontrar vcvars64.bat usando PowerShell (evita problemas com parênteses)
echo 🔍 Procurando Visual Studio Build Tools...
set "VS_FOUND=0"
for /f "delims=" %%i in ('powershell -Command "$paths = @('C:\Program Files\Microsoft Visual Studio\2022\BuildTools', 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools', 'C:\Program Files\Microsoft Visual Studio\2022\Community', 'C:\Program Files\Microsoft Visual Studio\2022\Professional', 'C:\Program Files\Microsoft Visual Studio\2022\Enterprise'); $found = $null; foreach ($p in $paths) { $f = Join-Path $p 'VC\Auxiliary\Build\vcvars64.bat'; if (Test-Path $f) { $found = $f; break } }; if ($found) { Write-Output $found }"') do (
    echo ✅ Build Tools encontrado: %%i
    echo 🔧 Configurando ambiente Visual Studio...
    call "%%i"
    set "VS_FOUND=1"
    goto :vs_configured
)

:vs_configured
IF "%VS_FOUND%"=="0" (
    echo ⚠️  Visual Studio Build Tools não encontrado nos locais padrão.
    echo.
    echo    Tentando procurar em outros locais...
    
    REM Procurar usando PowerShell
    for /f "delims=" %%i in ('powershell -Command "Get-ChildItem 'C:\Program Files*' -Recurse -Filter 'vcvars64.bat' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName"') do set "VS_PATH=%%i"
    
    IF "%VS_PATH%"=="" (
        echo ❌ Visual Studio Build Tools não encontrado!
        echo.
        echo    A instalação pode ainda estar em andamento ou ter falhado.
        echo    Verifique:
        echo    1. Se a instalação do Build Tools foi concluída
        echo    2. Abra "Developer Command Prompt for VS 2022" no menu Iniciar
        echo    3. Ou instale manualmente: https://visualstudio.microsoft.com/downloads/
        echo.
        echo    Tentando continuar sem configurar ambiente VS...
        echo    (a compilação pode falhar se o compilador não estiver no PATH)
        goto :skip_vs_setup
    ) ELSE (
        echo ✅ Build Tools encontrado em: %VS_PATH%
    )
)

:skip_vs_setup
IF "%VS_FOUND%"=="0" (
    echo ⚠️  Continuando sem configurar ambiente VS.
    echo    Se a compilação falhar, abra "Developer Command Prompt for VS 2022"
    echo    e execute este script de lá.
) ELSE (
    REM Verificar se compilador está disponível
    where cl >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo ⚠️  Compilador C++ não encontrado após configurar ambiente.
        echo    Tentando continuar mesmo assim...
    ) ELSE (
        echo ✅ Ambiente Visual Studio configurado!
        cl 2>&1 | findstr /C:"Microsoft" >nul
        IF %ERRORLEVEL% EQU 0 (
            echo ✅ Compilador C++ disponível
        )
    )
)

REM ---------------------------------------------------------
REM Verificar/Instalar Ninja
REM ---------------------------------------------------------
echo.
echo 🔧 Verificando Ninja (gerador de build)...
set "USE_NINJA=0"
where ninja >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ✅ Ninja já está instalado.
    set "USE_NINJA=1"
) ELSE (
    echo 📥 Instalando Ninja via pip...
    pip install ninja >nul 2>&1
    
    where ninja >nul 2>&1
    IF %ERRORLEVEL% EQU 0 (
        echo ✅ Ninja instalado com sucesso.
        set "USE_NINJA=1"
    ) ELSE (
        echo ⚠️  Ninja não encontrado. Tentando continuar sem ele (usando NMake)...
        set "USE_NINJA=0"
    )
)

REM ---------------------------------------------------------
REM Verificar outras dependências
REM ---------------------------------------------------------
where cmake >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ CMake não encontrado. Instale: https://cmake.org/download/
    pause
    exit /b 1
) ELSE (
    echo ✅ CMake detectado.
    cmake --version
)

where git >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Git não encontrado. Instale: https://git-scm.com/download/win
    pause
    exit /b 1
) ELSE (
    echo ✅ Git detectado.
    git --version
)

REM ---------------------------------------------------------
REM Clonar liboqs
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
REM Compilar liboqs
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
IF "%USE_NINJA%"=="1" (
    echo    Usando Ninja como gerador de build...
    cmake -GNinja .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON
) ELSE (
    echo    Usando NMake como gerador de build...
    cmake .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON
)

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao configurar CMake.
    cd ..\..
    pause
    exit /b 1
)

echo 🔨 Compilando liboqs (isso pode levar 10-30 minutos)...
IF "%USE_NINJA%"=="1" (
    cmake --build . --config Release
) ELSE (
    cmake --build . --config Release
)

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs.
    cd ..\..
    pause
    exit /b 1
)

echo 📦 Instalando liboqs...
cmake --install .

cd ..\..

REM ---------------------------------------------------------
REM Clonar e compilar liboqs-python
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
REM Testar SPHINCS+
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

