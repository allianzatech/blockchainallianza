@echo off
echo 🚀 EXECUTANDO TESTES UEC - ALLIANZA BLOCKCHAIN
echo ==========================================

python uec_test.py

if %errorlevel% == 0 (
    echo.
    echo ✅ TESTES CONCLUÍDOS COM SUCESSO!
    echo 🌌 UEC PRONTA PARA USO!
    pause
) else (
    echo.
    echo ❌ ALGUNS TESTES FALHARAM
    echo 🔧 VERIFIQUE OS ERROS ACIMA
    pause
)