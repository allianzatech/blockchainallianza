@echo off
REM ======================================================================
REM Script para executar testes individuais do Allianza Blockchain
REM ======================================================================

:menu
cls
echo ======================================================================
echo 🧪 MENU DE TESTES - ALLIANZA BLOCKCHAIN
echo ======================================================================
echo.
echo 1. PILAR 1: Interoperabilidade
echo 2. PILAR 2: Segurança Quântica
echo 3. Performance e Escalabilidade PQC
echo 4. Batch Verification
echo 5. FALCON - Alternativa Compacta
echo 6. Compressão de Assinaturas
echo 7. Teste de Stress QRS-3
echo 8. Todas as Inovações
echo 9. Provas Completas (POCs)
echo 10. EXECUTAR TODOS OS TESTES
echo 0. SAIR
echo.
set /p choice="Escolha uma opção (0-10): "

if "%choice%"=="1" goto test1
if "%choice%"=="2" goto test2
if "%choice%"=="3" goto test3
if "%choice%"=="4" goto test4
if "%choice%"=="5" goto test5
if "%choice%"=="6" goto test6
if "%choice%"=="7" goto test7
if "%choice%"=="8" goto test8
if "%choice%"=="9" goto test9
if "%choice%"=="10" goto test_all
if "%choice%"=="0" goto end
goto menu

:test1
echo.
echo ======================================================================
echo 🧪 TESTE 1: PILAR 1 - INTEROPERABILIDADE
echo ======================================================================
python PROVA_PILAR_1_INTEROPERABILIDADE_REAL.py
pause
goto menu

:test2
echo.
echo ======================================================================
echo 🧪 TESTE 2: PILAR 2 - SEGURANÇA QUÂNTICA
echo ======================================================================
python PROVA_PILAR_2_SEGURANCA_QUANTICA.py
pause
goto menu

:test3
echo.
echo ======================================================================
echo 🧪 TESTE 3: PERFORMANCE E ESCALABILIDADE PQC
echo ======================================================================
python TESTE_PERFORMANCE_PQC.py
pause
goto menu

:test4
echo.
echo ======================================================================
echo 🧪 TESTE 4: BATCH VERIFICATION
echo ======================================================================
python TESTE_BATCH_VERIFICATION.py
pause
goto menu

:test5
echo.
echo ======================================================================
echo 🧪 TESTE 5: FALCON - ALTERNATIVA COMPACTA
echo ======================================================================
python TESTE_FALCON_COMPACTO.py
pause
goto menu

:test6
echo.
echo ======================================================================
echo 🧪 TESTE 6: COMPRESSÃO DE ASSINATURAS
echo ======================================================================
python TESTE_COMPRESSAO_ASSINATURAS.py
pause
goto menu

:test7
echo.
echo ======================================================================
echo 🧪 TESTE 7: TESTE DE STRESS QRS-3
echo ======================================================================
echo ⚠️  Este teste pode levar ~5-6 minutos...
python TESTE_STRESS_QRS3.py
pause
goto menu

:test8
echo.
echo ======================================================================
echo 🧪 TESTE 8: TODAS AS INOVAÇÕES
echo ======================================================================
python TESTE_TODAS_INOVACOES.py
pause
goto menu

:test9
echo.
echo ======================================================================
echo 🧪 TESTE 9: PROVAS COMPLETAS (POCs)
echo ======================================================================
echo ⚠️  Este teste salva em pasta com data/hora (ex: proofs/2025-11-17_13-21-19/)
python generate_complete_proof.py
pause
goto menu

:test_all
echo.
echo ======================================================================
echo 🚀 EXECUTANDO TODOS OS TESTES
echo ======================================================================
python GERAR_PROVAS_INVESTIDORES.py
pause
goto menu

:end
echo.
echo ✅ Saindo...
exit /b 0

