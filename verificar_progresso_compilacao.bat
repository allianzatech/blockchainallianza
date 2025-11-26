@echo off

echo ======================================================================
echo       📊 VERIFICANDO PROGRESSO DA COMPILAÇÃO LIBOQS
echo ======================================================================
echo.

REM Verificar se liboqs está sendo compilado
IF EXIST "liboqs\build" (
    echo 📁 Diretório build encontrado
    echo.
    
    REM Contar arquivos .obj compilados (aproximação do progresso)
    echo 📊 Contando objetos compilados...
    for /f %%i in ('dir /b /s "liboqs\build\*.obj" 2^>nul ^| find /c /v ""') do set OBJ_COUNT=%%i
    echo    Objetos compilados: %OBJ_COUNT%
    echo.
    
    REM Verificar se DLL já foi gerada
    IF EXIST "liboqs\build\liboqs.dll" (
        echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO!
        echo    DLL encontrada: liboqs\build\liboqs.dll
        echo.
        echo 📋 PRÓXIMO PASSO:
        echo    Execute: compilar_liboqs_python.bat
    ) ELSE IF EXIST "liboqs\build\liboqs.lib" (
        echo ✅✅✅ LIBOQS COMPILADO COM SUCESSO!
        echo    LIB encontrada: liboqs\build\liboqs.lib
        echo.
        echo 📋 PRÓXIMO PASSO:
        echo    Execute: compilar_liboqs_python.bat
    ) ELSE (
        echo ⏳ Compilação em andamento...
        echo    Total esperado: ~1346 objetos
        echo    Compilados até agora: %OBJ_COUNT%
        echo.
        echo 💡 DICA: A compilação pode levar 10-30 minutos.
        echo    Aguarde até ver a mensagem de sucesso no terminal.
    )
) ELSE (
    echo ❌ Diretório build não encontrado.
    echo    Execute primeiro: compilar_liboqs.bat
)

echo.
pause







