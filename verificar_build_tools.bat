@echo off

echo ======================================================================
echo       🔍 VERIFICANDO MICROSOFT C++ BUILD TOOLS
echo ======================================================================
echo.

echo Procurando vcvars64.bat em locais comuns...

IF EXIST "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    echo ✅ ENCONTRADO: Build Tools 2022
    echo    Caminho: C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat
    goto :found
)

IF EXIST "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    echo ✅ ENCONTRADO: Build Tools 2022 (x86)
    echo    Caminho: C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat
    goto :found
)

IF EXIST "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (
    echo ✅ ENCONTRADO: Visual Studio 2022 Community
    echo    Caminho: C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat
    goto :found
)

IF EXIST "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat" (
    echo ✅ ENCONTRADO: Visual Studio 2022 Professional
    echo    Caminho: C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat
    goto :found
)

IF EXIST "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat" (
    echo ✅ ENCONTRADO: Visual Studio 2022 Enterprise
    echo    Caminho: C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat
    goto :found
)

echo ⚠️  Não encontrado nos locais padrão.
echo.
echo Procurando em todo o sistema (pode demorar)...
for /f "delims=" %%i in ('powershell -Command "Get-ChildItem 'C:\Program Files*' -Recurse -Filter 'vcvars64.bat' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName"') do (
    echo ✅ ENCONTRADO em: %%i
    goto :found
)

echo ❌ Build Tools não encontrado!
echo.
echo 📋 OPÇÕES:
echo    1. A instalação pode ainda estar em andamento (aguarde alguns minutos)
echo    2. Verifique se há processos "vs_BuildTools.exe" ou "vs_installer.exe" rodando
echo    3. Tente instalar manualmente: https://visualstudio.microsoft.com/downloads/
echo    4. Ou abra "Developer Command Prompt for VS 2022" no menu Iniciar
echo.
goto :end

:found
echo.
echo ✅ Build Tools está instalado!
echo.
echo 📋 PRÓXIMO PASSO:
echo    Execute: instalar_sphincs_com_vs.bat
echo.

:end
pause







