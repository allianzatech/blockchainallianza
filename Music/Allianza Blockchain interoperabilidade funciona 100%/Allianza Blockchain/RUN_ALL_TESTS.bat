@echo off
REM ======================================================================
REM Script para executar todos os testes do Allianza Blockchain
REM ======================================================================

echo ======================================================================
echo 🚀 EXECUTANDO TODOS OS TESTES - ALLIANZA BLOCKCHAIN
echo ======================================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.x primeiro.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.

REM Executar script principal
echo Executando: python GERAR_PROVAS_INVESTIDORES.py
echo.
python GERAR_PROVAS_INVESTIDORES.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar os testes!
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo ✅ TODOS OS TESTES FORAM EXECUTADOS!
echo ======================================================================
echo.
echo 📁 Resultados salvos em: proofs\relatorio_investidores\
echo.
echo 📄 Para ver o relatório, execute:
echo    type RELATORIO_EXECUTIVO_INVESTIDORES.md
echo.
pause




















