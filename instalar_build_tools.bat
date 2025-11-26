@echo off

echo ================================================================
echo  INSTALANDO MICROSOFT C++ BUILD TOOLS (AUTO)
echo ================================================================
echo.

echo Baixando instalador...
curl -L "https://aka.ms/vs/17/release/vs_BuildTools.exe" -o buildtools.exe

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao baixar instalador.
    echo    Tentando método alternativo...
    powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vs_BuildTools.exe' -OutFile 'buildtools.exe'"
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao baixar instalador via PowerShell também.
        echo    Por favor, baixe manualmente: https://visualstudio.microsoft.com/downloads/
        pause
        exit /b 1
    )
)

echo ✅ Instalador baixado com sucesso!
echo.

echo ================================================================
echo Iniciando instalacao silenciosa...
echo ================================================================
echo.

buildtools.exe --quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo ✅ INSTALACAO CONCLUIDA COM SUCESSO!
    echo ================================================================
    echo.
    echo 📋 PRÓXIMOS PASSOS:
    echo    1. Feche e reabra este terminal
    echo    2. Execute: instalar_sphincs_com_vs.bat
    echo.
) ELSE (
    echo.
    echo ================================================================
    echo ⚠️  INSTALACAO PODE TER FALHADO
    echo ================================================================
    echo.
    echo    Código de saída: %ERRORLEVEL%
    echo    Verifique se o Build Tools foi instalado corretamente.
    echo    Você pode tentar executar: instalar_sphincs_com_vs.bat
    echo    Ou instalar manualmente: https://visualstudio.microsoft.com/downloads/
    echo.
)

REM Limpar instalador temporário
IF EXIST buildtools.exe (
    echo Limpando arquivo temporário...
    del buildtools.exe
)

pause







