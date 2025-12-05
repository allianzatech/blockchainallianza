@echo off

title Continuar Instalação SPHINCS+ Real - Allianza Blockchain

echo ======================================================================
echo       🔄 CONTINUANDO INSTALAÇÃO SPHINCS+ REAL
echo ======================================================================
echo.

REM Verificar se precisa configurar ambiente VS
where cl >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 🔧 Configurando ambiente Visual Studio...
    for /f "delims=" %%i in ('powershell -Command "$paths = @('C:\Program Files\Microsoft Visual Studio\2022\BuildTools', 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools'); $found = $null; foreach ($p in $paths) { $f = Join-Path $p 'VC\Auxiliary\Build\vcvars64.bat'; if (Test-Path $f) { $found = $f; break } }; if ($found) { Write-Output $found }"') do (
        call "%%i"
        goto :vs_configured
    )
    :vs_configured
)

REM Verificar se liboqs precisa ser compilado
echo 📦 Verificando liboqs...
IF NOT EXIST "liboqs\build\liboqs.dll" (
    IF NOT EXIST "liboqs\build\liboqs.lib" (
        echo 🔨 Compilando liboqs (isso pode levar 10-30 minutos)...
        cd liboqs\build
        
        echo    Iniciando compilação...
        cmake --build . --config Release
        
        IF %ERRORLEVEL% NEQ 0 (
            echo ❌ Erro ao compilar liboqs.
            cd ..\..
            pause
            exit /b 1
        )
        
        echo 📦 Instalando liboqs...
        cmake --install .
        
        cd ..\..
        echo ✅ liboqs compilado com sucesso!
    ) ELSE (
        echo ✅ liboqs já foi compilado (arquivo .lib encontrado)
    )
) ELSE (
    echo ✅ liboqs já foi compilado (DLL encontrada)
)

REM Verificar se liboqs-python precisa ser compilado
echo.
echo 🐍 Verificando liboqs-python...
python -c "import oqs" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    IF NOT EXIST "liboqs-python" (
        echo 📥 Clonando liboqs-python...
        git clone https://github.com/open-quantum-safe/liboqs-python.git
        
        IF %ERRORLEVEL% NEQ 0 (
            echo ❌ Erro ao clonar liboqs-python.
            pause
            exit /b 1
        )
    )
    
    cd liboqs-python
    
    echo 🔨 Compilando liboqs-python...
    python setup.py build
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao compilar liboqs-python.
        cd ..
        pause
        exit /b 1
    )
    
    echo 📦 Instalando liboqs-python...
    python setup.py install
    
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Erro ao instalar liboqs-python.
        cd ..
        pause
        exit /b 1
    )
    
    cd ..
    echo ✅ liboqs-python instalado com sucesso!
) ELSE (
    echo ✅ liboqs-python já está instalado
)

REM Testar SPHINCS+
echo.
echo ======================================================================
echo 🧪 TESTANDO SPHINCS+ REAL...
echo ======================================================================

python - << END
try:
    from oqs import Signature
    
    alg = "SPHINCS+-SHAKE-128f"
    sig = Signature(alg)
    
    public_key = sig.generate_keypair()
    message = b"Allianza Blockchain - Quantum Test"
    signature = sig.sign(message)
    valid = sig.verify(message, signature, public_key)
    
    print("====================================================")
    print("🔐 SPHINCS+ REAL TEST")
    print("Algoritmo:", alg)
    print("Válido?:", valid)
    print("====================================================")
    
    if valid:
        print("✅✅✅ SPHINCS+ REAL FUNCIONANDO PERFEITAMENTE!")
        print()
        print("🎉 INSTALAÇÃO COMPLETA!")
        print()
        print("📋 PRÓXIMOS PASSOS:")
        print("   1. Execute: python PROVA_PILAR_2_SEGURANCA_QUANTICA.py")
        print("   2. Verifique se SPHINCS+ está em modo 'real'")
        print("   3. Confirme que QRS-3 está com Redundancy Level: 3")
    else:
        print("❌ Erro: Assinatura inválida")
except ImportError as e:
    print("❌ Erro ao importar oqs:", e)
    print("   Verifique se liboqs-python foi instalado corretamente.")
    import traceback
    traceback.print_exc()
except Exception as e:
    print("❌ Erro no teste:", e)
    import traceback
    traceback.print_exc()
END

echo.
pause









