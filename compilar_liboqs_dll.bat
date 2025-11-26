@echo off

title Compilar liboqs com DLL - Allianza Blockchain

echo ======================================================================
echo       🔨 COMPILANDO LIBOQS COM DLL (SOLUÇÃO ALTERNATIVA)
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

REM Limpar build anterior se existir
IF EXIST "build" (
    echo 🧹 Limpando build anterior...
    rmdir /s /q build
)

REM Criar diretório build
mkdir build
cd build

REM Configurar CMake para gerar DLL (sem -DOQS_BUILD_ONLY_SHARED_LIBS)
echo.
echo 🔨 Configurando CMake para gerar DLL...
echo    Usando gerador Visual Studio (não Ninja) para garantir DLL...
cmake -G "Visual Studio 17 2022" -A x64 .. -DBUILD_SHARED_LIBS=ON

IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Tentando gerador alternativo...
    cmake -G "Visual Studio 16 2019" -A x64 .. -DBUILD_SHARED_LIBS=ON
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ⚠️  Tentando sem especificar gerador...
        cmake .. -DBUILD_SHARED_LIBS=ON
        
        IF %ERRORLEVEL% NEQ 0 (
            echo ❌ Erro ao configurar CMake.
            cd ..\..
            pause
            exit /b 1
        )
    )
)

REM Compilar
echo.
echo 🔨 Compilando liboqs em modo Release (isso pode levar 10-30 minutos)...
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
cmake --install . --config Release

cd ..\..

REM Verificar se DLL foi criada (pode estar em bin/ ou lib/)
echo.
echo 🔍 Verificando onde a DLL foi criada...

IF EXIST "liboqs\build\bin\oqs.dll" (
    echo ✅ DLL encontrada em: liboqs\build\bin\oqs.dll
    copy "liboqs\build\bin\oqs.dll" "liboqs\build\oqs.dll" >nul 2>&1
    echo    Copiada para: liboqs\build\oqs.dll
) ELSE IF EXIST "liboqs\build\bin\liboqs.dll" (
    echo ✅ DLL encontrada em: liboqs\build\bin\liboqs.dll
    copy "liboqs\build\bin\liboqs.dll" "liboqs\build\liboqs.dll" >nul 2>&1
    echo    Copiada para: liboqs\build\liboqs.dll
) ELSE IF EXIST "liboqs\build\lib\oqs.dll" (
    echo ✅ DLL encontrada em: liboqs\build\lib\oqs.dll
    copy "liboqs\build\lib\oqs.dll" "liboqs\build\oqs.dll" >nul 2>&1
    echo    Copiada para: liboqs\build\oqs.dll
) ELSE IF EXIST "liboqs\build\Release\oqs.dll" (
    echo ✅ DLL encontrada em: liboqs\build\Release\oqs.dll
    copy "liboqs\build\Release\oqs.dll" "liboqs\build\oqs.dll" >nul 2>&1
    echo    Copiada para: liboqs\build\oqs.dll
) ELSE (
    echo ⚠️  DLL não encontrada nos locais esperados.
    echo    Procurando em todos os diretórios...
    for /r "liboqs\build" %%f in (*.dll) do (
        echo    ✅ DLL encontrada: %%f
        goto :dll_found
    )
    echo    ❌ Nenhuma DLL encontrada.
    echo    Mas a biblioteca .lib foi compilada, então podemos tentar usar ela.
    goto :try_lib
)

:dll_found
echo.
echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO (DLL ENCONTRADA)!
echo.
echo 📋 PRÓXIMO PASSO:
echo    Execute: compilar_liboqs_python.bat
goto :end

:try_lib
echo.
echo ⚠️  DLL não encontrada, mas .lib foi compilada.
echo    Vamos tentar usar a biblioteca estática ou configurar liboqs-python
echo    para usar o diretório build diretamente.
echo.
echo ✅✅✅ LIBOQS COMPILADO (modo estático)!
echo.
echo 📋 PRÓXIMO PASSO:
echo    Execute: compilar_liboqs_python_alternativo.bat

:end
echo.
pause







