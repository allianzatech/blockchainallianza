@echo off
echo ========================================
echo TESTES ALLIANZA BLOCKCHAIN
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias...
pip install -q flask cryptography web3 requests base58 python-dotenv >nul 2>&1
if errorlevel 1 (
    echo AVISO: Algumas dependencias podem nao ter sido instaladas
    echo Continuando mesmo assim...
)
echo OK

echo.
echo [2/3] Executando testes basicos de verificacao...
echo.
python tests\public\run_verification_tests.py
if errorlevel 1 (
    echo.
    echo AVISO: Alguns testes falharam
    echo Isso pode ser normal se liboqs-python nao estiver instalado
)

echo.
echo [3/3] Executando suite completa de testes...
echo.
python tests\public\run_all_tests.py

echo.
echo ========================================
echo TESTES CONCLUIDOS
echo ========================================
pause

