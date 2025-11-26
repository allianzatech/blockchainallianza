@echo off
echo ========================================
echo 🚀 BUILD E DEPLOY - ALLIANZA BLOCKCHAIN
echo ========================================
echo.

REM Limpar arquivos temporários
echo 📌 Limpando arquivos temporários...
if exist __pycache__ (
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
)
del /q *.pyc 2>nul
if exist .pytest_cache rmdir /s /q .pytest_cache 2>nul

REM Criar diretório de deploy
echo 📌 Criando diretório de deploy...
if exist deploy rmdir /s /q deploy
mkdir deploy

REM Copiar arquivos Python
echo 📌 Copiando arquivos Python...
for %%f in (*.py) do (
    if not "%%f"=="build_deploy.bat" copy "%%f" "deploy\" >nul
)

REM Copiar diretórios necessários
echo 📌 Copiando diretórios...
if exist templates xcopy /E /I /Y templates deploy\templates >nul
if exist static xcopy /E /I /Y static deploy\static >nul
if exist contracts xcopy /E /I /Y contracts deploy\contracts >nul
if exist proofs xcopy /E /I /Y proofs deploy\proofs >nul
if exist templates xcopy /E /I /Y templates deploy\templates >nul

REM Copiar arquivos de configuração
echo 📌 Copiando arquivos de configuração...
if exist requirements.txt copy requirements.txt deploy\ >nul
if exist .env.production (
    copy .env.production deploy\.env >nul
) else if exist .env (
    copy .env deploy\.env >nul
)
if exist wsgi.py copy wsgi.py deploy\ >nul
if exist nginx_allianza.conf copy nginx_allianza.conf deploy\ >nul

REM Criar .htaccess para Hostinger usando Python (evita problemas com caracteres especiais)
echo 📌 Criando .htaccess...
python criar_htaccess.py

REM Criar arquivo de inicialização usando Python (evita problemas com caracteres especiais)
echo 📌 Criando start_server.sh...
python criar_start_server.py

echo.
echo ========================================
echo ✅ BUILD CONCLUÍDO!
echo ========================================
echo.
echo 📦 Diretório 'deploy' criado com sucesso!
echo.
echo 📋 Próximos passos:
echo    1. Compactar: powershell Compress-Archive -Path deploy -DestinationPath allianza_deploy.zip
echo    2. Enviar para Hostinger via FTP/SFTP
echo    3. Extrair no servidor
echo    4. Configurar e iniciar servidor
echo.
pause

