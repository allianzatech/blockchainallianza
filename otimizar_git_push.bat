@echo off
echo ========================================
echo ⚡ OTIMIZANDO GIT PUSH
echo ========================================
echo.

echo 📌 Removendo arquivos grandes do Git...
echo.

REM Remover liboqs (muito grande)
if exist liboqs (
    echo Removendo liboqs...
    git rm -r --cached liboqs
)

if exist liboqs-python (
    echo Removendo liboqs-python...
    git rm -r --cached liboqs-python
)

REM Remover databases
echo Removendo databases...
for %%f in (*.db) do git rm --cached "%%f" 2>nul
for %%f in (*.sqlite) do git rm --cached "%%f" 2>nul
for %%f in (*.sqlite3) do git rm --cached "%%f" 2>nul

REM Remover logs
echo Removendo logs...
for %%f in (*.log) do git rm --cached "%%f" 2>nul

REM Remover zips
echo Removendo arquivos zip...
for %%f in (*.zip) do git rm --cached "%%f" 2>nul

REM Adicionar .gitignore atualizado
echo Atualizando .gitignore...
git add .gitignore

echo.
echo ========================================
echo ✅ OTIMIZAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo 📋 Próximos passos:
echo    1. git commit -m "Otimizar: remover arquivos grandes"
echo    2. git push -u origin main
echo.
echo ⚡ O push será MUITO mais rápido agora!
echo.
pause

