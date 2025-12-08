# 🚀 Getting Started - Allianza Blockchain

Welcome to Allianza Blockchain! This guide will help you get started quickly.

## 📋 Prerequisites

- **Python 3.8+** (3.11 recommended)
- **Git**
- **Docker & Docker Compose** (optional, for full stack)
- **liboqs-python** (optional, for real PQC implementation)

## ⚡ Quick Start

### Option 1: Local Setup (Recommended for Development)

```bash
# Clone repository
git clone https://github.com/dieisonmaach-lang/allianzablockchain.git
cd allianzablockchain

# Run setup script
# Linux/Mac:
bash setup_local.sh

# Windows:
setup_local.bat

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run tests
python tests/public/run_verification_tests.py

# Start development server
python allianza_blockchain.py
```

### Option 2: Docker Compose (Full Stack)

```bash
# Clone repository
git clone https://github.com/dieisonmaach-lang/allianzablockchain.git
cd allianzablockchain

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f allianza-blockchain

# Access services
# - Blockchain: http://localhost:5000
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
```

## 🧪 Running Tests

### Basic Verification
```bash
python tests/public/run_verification_tests.py
```

### Complete Test Suite
```bash
python tests/public/run_all_tests.py
```

### With Coverage
```bash
pytest tests/public/ --cov=core --cov-report=html
```

## 📚 Next Steps

1. **Read Documentation**
   - [Architecture](docs/ARCHITECTURE.md)
   - [API Reference](docs/API_REFERENCE.md)
   - [Glossary](GLOSSARIO.md)

2. **Explore Code**
   - [QRS-3 Implementation](core/crypto/quantum_security.py)
   - [ALZ-NIEV Protocol](core/consensus/alz_niev_interoperability.py)
   - [Interoperability](core/interoperability/)

3. **Access Testnet**
   - Dashboard: https://testnet.allianza.tech
   - Explorer: https://testnet.allianza.tech/explorer
   - Faucet: https://testnet.allianza.tech/faucet

4. **Contribute**
   - Read [CONTRIBUTING.md](CONTRIBUTING.md)
   - Check [Good First Issues](https://github.com/dieisonmaach-lang/allianzablockchain/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

## 🎥 Video Tutorial

📹 **Coming Soon** - Video tutorial on YouTube

## ❓ Need Help?

- 📖 [Documentation](docs/)
- 💬 [GitHub Discussions](https://github.com/dieisonmaach-lang/allianzablockchain/discussions)
- 🐛 [Report Issues](https://github.com/dieisonmaach-lang/allianzablockchain/issues)
- 📧 Email: support@allianza.tech

## 🔧 Troubleshooting

### liboqs-python Installation Issues

```bash
# Install system dependencies first
# Ubuntu/Debian:
sudo apt-get install build-essential cmake libssl-dev

# macOS:
brew install cmake openssl

# Then install liboqs-python
pip install liboqs-python
```

### Port Already in Use

```bash
# Change port in .env
FLASK_PORT=5001

# Or kill process using port 5000
# Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Issues

```bash
# Reset database
rm allianza_blockchain.db
python allianza_blockchain.py
```

---

**Ready to build the future of blockchain? Let's go! 🚀**

