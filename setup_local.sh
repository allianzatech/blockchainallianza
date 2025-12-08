#!/bin/bash
# Setup script for local development

set -e

echo "🚀 Setting up Allianza Blockchain development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "🛠️  Installing development dependencies..."
pip install black flake8 mypy isort pytest pytest-cov pre-commit

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env 2>/dev/null || echo "# Environment variables" > .env
    echo "⚠️  Please configure .env file with your settings"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data secrets logs proofs/testnet

# Run initial tests
echo "🧪 Running initial tests..."
python tests/public/run_verification_tests.py || echo "⚠️  Some tests may have failed, but setup is complete"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure .env file with your settings"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run tests: python tests/public/run_verification_tests.py"
echo "4. Start development server: python allianza_blockchain.py"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up -d"

