@echo off
REM Run All Demos - Allianza Blockchain (Windows)
REM This script runs all available demos in sequence

echo ==========================================
echo 🚀 ALLIANZA BLOCKCHAIN - ALL DEMOS
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check if we're in the right directory
if not exist "examples\qrs3_demo.py" (
    echo ❌ Please run this script from the repository root
    exit /b 1
)

echo 📋 Running all available demos...
echo.

REM Demo 1: QRS-3 Signature
echo 1. QRS-3 Signature Demo
echo    Demonstrating quantum-safe signatures...
python examples\qrs3_signature.py
echo.

REM Demo 2: QRS-3 Demo
echo 2. QRS-3 Demo
echo    Demonstrating QRS-3 implementation...
python examples\qrs3_demo.py
echo.

REM Demo 3: QSS Demo
echo 3. QSS (Quantum Security Service) Demo
echo    Demonstrating quantum security service...
python examples\qss_demo.py
echo.

REM Demo 4: ALZ-NIEV Demo
echo 4. ALZ-NIEV Protocol Demo
echo    Demonstrating bridge-free interoperability...
python examples\alz_niev_demo.py
echo.

REM Demo 5: Interoperability Demo
echo 5. Interoperability Demo
echo    Demonstrating cross-chain interoperability...
python examples\interoperability_demo.py
echo.

REM Demo 6: Cross-Chain Transfer
echo 6. Cross-Chain Transfer Demo
echo    Demonstrating bridge-free cross-chain transfers...
python examples\cross_chain_transfer.py
echo.

REM Demo 7: Basic Wallet
echo 7. Basic Wallet Demo
echo    Demonstrating wallet operations...
python examples\basic_wallet.py
echo.

echo ==========================================
echo ✅ All demos completed!
echo ==========================================
echo.
echo 📚 Next steps:
echo    • Read GETTING_STARTED.md for detailed instructions
echo    • Run verification scripts: python scripts\verify_technical_proofs.py
echo    • Access testnet: https://testnet.allianza.tech
echo.

pause
