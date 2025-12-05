@echo off

title Reiniciar Compilacao liboqs - Allianza Blockchain

echo ======================================================================
echo       🔄 REINICIANDO COMPILAÇÃO LIBOQS
echo ======================================================================
echo.

REM Verificar se liboqs existe
IF NOT EXIST "liboqs" (
    echo ❌ Diretório liboqs não encontrado.
    echo    Execute primeiro: compilar_liboqs.bat
    pause
    exit /b 1
)

cd liboqs

REM Limpar build anterior (opcional - comentado para não perder progresso)
echo 🔍 Verificando estado do build...
IF EXIST "build" (
    echo    Diretório build encontrado.
    echo.
    echo    ⚠️  OPÇÕES:
    echo    1. Limpar e recompilar do zero (mais seguro)
    echo    2. Continuar compilação existente (pode ter problemas)
    echo.
    set /p OPCAO="   Escolha (1 ou 2): "
    
    IF /I "%OPCAO%"=="1" (
        echo.
        echo 🗑️  Limpando build anterior...
        rmdir /s /q build
        mkdir build
    ) ELSE IF /I "%OPCAO%"=="2" (
        echo.
        echo ⏭️  Continuando compilação existente...
    ) ELSE (
        echo.
        echo ❌ Opção inválida. Cancelando.
        cd ..
        pause
        exit /b 1
    )
) ELSE (
    echo    Criando diretório build...
    mkdir build
)

cd build

REM Configurar ambiente Visual Studio
echo.
echo 🔧 Configurando ambiente Visual Studio...
for /f "delims=" %%i in ('powershell -Command "$paths = @('C:\Program Files\Microsoft Visual Studio\2022\BuildTools', 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools'); $found = $null; foreach ($p in $paths) { $f = Join-Path $p 'VC\Auxiliary\Build\vcvars64.bat'; if (Test-Path $f) { $found = $f; break } }; if ($found) { Write-Output $found }"') do (
    call "%%i"
    goto :vs_ok
)

:vs_ok
where cl >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Compilador C++ não encontrado.
    echo    Execute: instalar_build_tools.bat
    cd ..\..
    pause
    exit /b 1
)

echo ✅ Ambiente Visual Studio configurado!

REM Configurar CMake (sempre reconfigurar)
echo.
echo 🔨 Configurando CMake para liboqs...
IF EXIST "build.ninja" (
    echo    Arquivo build.ninja encontrado. Reconfigurando...
) ELSE (
    echo    Configurando do zero...
)

cmake -GNinja .. -DOQS_BUILD_ONLY_SHARED_LIBS=ON

IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Erro ao configurar CMake com Ninja. Tentando sem Ninja...
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
echo ======================================================================
echo 🔨 COMPILANDO LIBOQS
echo ======================================================================
echo    Isso pode levar 10-30 minutos.
echo    Por favor, aguarde e NÃO feche este terminal...
echo.
echo    💡 DICA: Você pode executar em outro terminal:
echo       verificar_progresso_compilacao.bat
echo ======================================================================
echo.

cmake --build . --config Release

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erro ao compilar liboqs.
    echo.
    echo 💡 TENTATIVAS DE SOLUÇÃO:
    echo    1. Verifique se há espaço em disco suficiente
    echo    2. Feche outros programas para liberar memória
    echo    3. Execute: verificar_build_tools.bat
    echo    4. Tente limpar e recompilar (opção 1)
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
echo.
echo ======================================================================
echo 🔍 VERIFICANDO RESULTADO...
echo ======================================================================

IF EXIST "liboqs\build\liboqs.dll" (
    echo.
    echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO!
    echo    DLL encontrada: liboqs\build\liboqs.dll
    echo.
    echo 📋 PRÓXIMO PASSO:
    echo    Execute: compilar_liboqs_python.bat
) ELSE IF EXIST "liboqs\build\liboqs.lib" (
    echo.
    echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO!
    echo    LIB encontrada: liboqs\build\liboqs.lib
    echo.
    echo 📋 PRÓXIMO PASSO:
    echo    Execute: compilar_liboqs_python.bat
) ELSE (
    echo.
    echo ⚠️  Compilação concluída, mas DLL/LIB não encontrada.
    echo.
    echo 🔍 Verificando arquivos gerados...
    dir /b /s "liboqs\build\*.dll" 2>nul
    dir /b /s "liboqs\build\*.lib" 2>nul
    echo.
    echo 💡 Se não encontrar arquivos, tente limpar e recompilar.
)

echo.
pause









