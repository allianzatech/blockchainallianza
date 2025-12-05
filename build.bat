@echo off
REM Script de build para Windows
echo 🚀 Iniciando build do projeto Allianza Blockchain...

REM Verificar se Node.js está instalado
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js não encontrado. Por favor, instale Node.js primeiro.
    exit /b 1
)

REM Verificar se npm está instalado
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ NPM não encontrado. Por favor, instale NPM primeiro.
    exit /b 1
)

echo ✅ Node.js e NPM encontrados

REM Instalar dependências se necessário
if not exist "node_modules" (
    echo 📦 Instalando dependências do NPM...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao instalar dependências
        exit /b 1
    )
)

REM Compilar CSS
echo 🎨 Compilando CSS do Tailwind...
call npm run build-css
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar CSS
    exit /b 1
)

echo ✅ Build concluído com sucesso!
echo 📁 CSS compilado em: static\css\output.css

