@echo off

title Compilar liboqs - Allianza Blockchain

echo ======================================================================
echo       🔨 COMPILANDO LIBOQS (Passo 1 de 2)
echo ======================================================================
echo.

REM Configurar ambiente Visual Studio
echo 🔧 Configurando ambiente Visual Studio...
for /f "delims=" %%i in ('powershell -Command "$paths = @('C:\Program Files\Microsoft Visual Studio\2022\BuildTools', 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools'); $found = $null; foreach ($p in $paths) { $f = Join-Path $p 'VC\Auxiliary\Build\vcvars64.bat'; if (Test-Path $f) { $found = $f; break } }; if ($found) { Write-Output $found }"') do (
    call "%%i"
    goto :vs_ok
)

:vs_ok
where cl >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Compilador C++ não encontrado. Configure o ambiente VS primeiro.
    pause
    exit /b 1
)

echo ✅ Ambiente Visual Studio configurado!

REM Verificar se liboqs já foi clonado
IF NOT EXIST "liboqs" (
    echo 📥 Clonando liboqs...
    git clone https://github.com/open-quantum-safe/liboqs.git
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao clonar liboqs.
        pause
        exit /b 1
    )
)

cd liboqs

REM Criar diretório build se não existir
IF NOT EXIST "build" (
    mkdir build
)

cd build

REM Configurar CMake
echo.
echo 🔨 Configurando CMake para liboqs...
cmake -GNinja .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON

IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Erro ao configurar CMake. Tentando sem Ninja...
    cmake .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao configurar CMake.
        cd ..\..
        pause
        exit /b 1
    )
)

REM Compilar
echo.
echo 🔨 Compilando liboqs (isso pode levar 10-30 minutos)...
echo    Por favor, aguarde...
cmake --build . --config Release

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar liboqs.
    cd ..\..
    pause
    exit /b 1
)

REM Instalar
echo.
echo 📦 Instalando liboqs...
cmake --install .

cd ..\..

REM Verificar se DLL foi criada
IF EXIST "liboqs\build\liboqs.dll" (
    echo.
    echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO!
    echo.
    echo 📋 PRÓXIMO PASSO:
    echo    Execute: compilar_liboqs_python.bat
) ELSE IF EXIST "liboqs\build\liboqs.lib" (
    echo.
    echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO!
    echo    (arquivo .lib encontrado)
    echo.
    echo 📋 PRÓXIMO PASSO:
    echo    Execute: compilar_liboqs_python.bat
) ELSE (
    echo.
    echo ⚠️  Compilação concluída, mas DLL não encontrada.
    echo    Verifique o diretório liboqs\build\
)

echo.
pause







