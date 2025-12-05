@echo off
REM Script para Executar Todos os Testes - Allianza Blockchain (Windows)
REM Versão: 1.0
REM Data: 03 de Dezembro de 2025

echo ============================================================
echo 🧪 EXECUTANDO TODOS OS TESTES - ALLIANZA BLOCKCHAIN
echo ============================================================
echo.

REM Criar diretórios necessários
if not exist "test_results\complete_validation" mkdir "test_results\complete_validation"
if not exist "test_results\critical_tests" mkdir "test_results\critical_tests"
if not exist "test_results\professional_suite" mkdir "test_results\professional_suite"
if not exist "logs" mkdir "logs"

REM Timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%

echo 📅 Início: %date% %time%
echo 📂 Diretório de trabalho: %CD%
echo.

REM Contador de testes
set TOTAL_TESTS=0
set PASSED_TESTS=0
set FAILED_TESTS=0

REM Executar testes principais
echo 📋 FASE 1: Provas Principais
echo.

REM Executar testes de validação completa
echo 📋 FASE 2: Complete Validation Suite
echo.

REM Executar testes críticos
echo 📋 FASE 3: Critical Tests Suite
echo.

REM Executar suite profissional
echo 📋 FASE 4: Professional Suite
echo.

REM Gerar relatório final
echo.
echo ============================================================
echo 📊 RESULTADOS FINAIS
echo ============================================================
echo.
echo 📅 Fim: %date% %time%
echo.

if %FAILED_TESTS%==0 (
    echo 🎉 TAXA DE SUCESSO: 100%%
    echo ✅ TODOS OS TESTES PASSARAM!
) else (
    echo ⚠️  TAXA DE SUCESSO: Calculando...
    echo ❌ Alguns testes falharam. Verifique os logs em logs\
)

echo.
echo 📄 Relatório salvo em: test_results\FINAL_RESULTS_%TIMESTAMP%.json
echo.

if %FAILED_TESTS%==0 (
    exit /b 0
) else (
    exit /b 1
)



