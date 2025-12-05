@echo off
chcp 65001 >nul
echo ======================================================================
echo ⚡ TESTE RÁPIDO - ALLIANZA BLOCKCHAIN
echo ======================================================================
echo.

echo 🚀 Executando testes essenciais...
echo.

echo ======================================================================
echo 1️⃣ Verificando: Todas as 50 Melhorias
echo ======================================================================
python TESTE_TODAS_50_MELHORIAS.py
echo.

echo ======================================================================
echo 2️⃣ Verificando: Segurança Quântica (QRS-3)
echo ======================================================================
python PROVA_PILAR_2_SEGURANCA_QUANTICA.py
echo.

echo ======================================================================
echo ✅ TESTE RÁPIDO CONCLUÍDO!
echo ======================================================================
echo.
pause









