@echo off
chcp 65001 >nul
title Sincronização Automática - Privado para Público

echo.
echo ======================================================================
echo   SINCRONIZAÇÃO AUTOMÁTICA - REPOSITÓRIO PRIVADO PARA PÚBLICO
echo ======================================================================
echo.
echo   Este script sincroniza arquivos seguros do repositório privado
echo   para o público e faz push automático.
echo.
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/2] Sincronizando arquivos...
python sincronizar_repositorio_publico.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erro na sincronização
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo   ✅ SINCRONIZAÇÃO CONCLUÍDA!
echo ======================================================================
echo.
echo   Se o push automático não funcionou, use GitHub Desktop
echo   ou configure um token (veja SINCRONIZACAO_AUTOMATICA.md)
echo.

pause

