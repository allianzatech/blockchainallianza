@echo off

echo ======================================================================
echo       🔍 VERIFICANDO INSTALAÇÃO SPHINCS+ REAL
echo ======================================================================
echo.

REM Verificar se liboqs foi compilado
echo 📦 Verificando liboqs...
IF EXIST "liboqs\build\liboqs.dll" (
    echo ✅ liboqs.dll encontrado - Compilação concluída!
) ELSE IF EXIST "liboqs\build\liboqs.so" (
    echo ✅ liboqs.so encontrado - Compilação concluída!
) ELSE IF EXIST "liboqs\build" (
    echo ⏳ liboqs em compilação (diretório build existe mas DLL não encontrada)
    echo    Isso é normal se ainda estiver compilando...
) ELSE (
    echo ❌ liboqs não foi compilado ainda
)

echo.

REM Verificar se liboqs-python foi instalado
echo 🐍 Verificando liboqs-python...
python -c "import oqs; print('✅ liboqs-python instalado!')" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ liboqs-python não está instalado ou não está funcionando
) ELSE (
    echo.
    echo 🧪 Testando SPHINCS+ real...
    python - << END
try:
    from oqs import Signature
    
    alg = "SPHINCS+-SHAKE-128f"
    sig = Signature(alg)
    
    public_key = sig.generate_keypair()
    message = b"Allianza Blockchain - Quantum Test"
    signature = sig.sign(message)
    valid = sig.verify(message, signature, public_key)
    
    if valid:
        print("✅✅✅ SPHINCS+ REAL FUNCIONANDO PERFEITAMENTE!")
        print("   Algoritmo:", alg)
        print("   Status: PRONTO PARA USO")
    else:
        print("❌ SPHINCS+ instalado mas teste falhou")
except ImportError as e:
    print("❌ Erro ao importar oqs:", e)
except Exception as e:
    print("❌ Erro no teste:", e)
END
)

echo.
echo ======================================================================
echo 📋 PRÓXIMOS PASSOS:
echo    1. Se SPHINCS+ está funcionando, execute:
echo       python PROVA_PILAR_2_SEGURANCA_QUANTICA.py
echo.
echo    2. Verifique se o output mostra:
echo       - Implementation: real
echo       - Redundancy Level: 3
echo       - SPHINCS+ Available: True
echo ======================================================================
pause









