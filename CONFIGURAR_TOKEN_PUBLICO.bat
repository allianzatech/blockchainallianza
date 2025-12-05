@echo off
chcp 65001 >nul
title Configurar Token para Push Automático

echo.
echo ======================================================================
echo   CONFIGURAR TOKEN PARA PUSH AUTOMÁTICO
echo ======================================================================
echo.
echo   Este script configura um token para fazer push automático
echo   do repositório público.
echo.
echo ======================================================================
echo.

echo IMPORTANTE:
echo 1. Você precisa criar um token da conta allianzatoken-png
echo 2. Acesse: https://github.com/settings/tokens
echo 3. Generate new token (classic)
echo 4. Marque 'repo' (tudo)
echo 5. Copie o token
echo.
echo ======================================================================
echo.

set /p TOKEN="Cole o Personal Access Token aqui: "

if "%TOKEN%"=="" (
    echo.
    echo ❌ Token não fornecido!
    pause
    exit /b 1
)

echo.
echo Configurando variável de ambiente...
setx GITHUB_TOKEN_PUBLIC "%TOKEN%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo   ✅ TOKEN CONFIGURADO COM SUCESSO!
    echo ======================================================================
    echo.
    echo   Agora você pode executar:
    echo   .\sincronizar_automatico.bat
    echo.
    echo   O push será feito automaticamente!
    echo.
    echo   ⚠️  IMPORTANTE: Reinicie o terminal para a variável funcionar
    echo.
) else (
    echo.
    echo ❌ Erro ao configurar token
    echo.
    echo Tente manualmente:
    echo setx GITHUB_TOKEN_PUBLIC "seu_token"
)

pause

