@echo off
echo ========================================
echo 🌌 ALLIANZA UEC - DEPLOY AUTOMATIZADO
echo ========================================
echo.

echo 🔄 Atualizando dependências UEC...
pip install -r requirements_uec.txt

echo.
echo 🧪 Executando testes UEC...
python uec_test.py

if %errorlevel% neq 0 (
    echo ❌ Testes UEC falharam! Verifique os erros acima.
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando Allianza Blockchain com UEC...
echo 📊 Acesse: http://localhost:5008
echo.

python run_simple.py

pause