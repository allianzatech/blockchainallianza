@echo off
REM Setup script for local development (Windows)

echo 🚀 Setting up Allianza Blockchain development environment...

REM Check Python
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Install development dependencies
echo 🛠️  Installing development dependencies...
pip install black flake8 mypy isort pytest pytest-cov pre-commit

REM Install pre-commit hooks
echo 🔧 Installing pre-commit hooks...
pre-commit install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    if exist ".env.example" (
        copy .env.example .env
    ) else (
        echo # Environment variables > .env
    )
    echo ⚠️  Please configure .env file with your settings
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "data" mkdir data
if not exist "secrets" mkdir secrets
if not exist "logs" mkdir logs
if not exist "proofs\testnet" mkdir proofs\testnet

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Configure .env file with your settings
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Run tests: python tests\public\run_verification_tests.py
echo 4. Start development server: python allianza_blockchain.py
echo.
echo Or use Docker Compose:
echo   docker-compose up -d

pause

