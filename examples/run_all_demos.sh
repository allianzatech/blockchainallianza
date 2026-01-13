#!/bin/bash
# Run All Demos - Allianza Blockchain
# This script runs all available demos in sequence

set -e  # Exit on error

echo "=========================================="
echo "🚀 ALLIANZA BLOCKCHAIN - ALL DEMOS"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "examples/qrs3_demo.py" ]; then
    echo "❌ Please run this script from the repository root"
    exit 1
fi

echo -e "${BLUE}📋 Running all available demos...${NC}"
echo ""

# Demo 1: QRS-3 Signature
echo -e "${GREEN}1. QRS-3 Signature Demo${NC}"
echo "   Demonstrating quantum-safe signatures..."
python examples/qrs3_signature.py
echo ""

# Demo 2: QRS-3 Demo
echo -e "${GREEN}2. QRS-3 Demo${NC}"
echo "   Demonstrating QRS-3 implementation..."
python examples/qrs3_demo.py
echo ""

# Demo 3: QSS Demo
echo -e "${GREEN}3. QSS (Quantum Security Service) Demo${NC}"
echo "   Demonstrating quantum security service..."
python examples/qss_demo.py
echo ""

# Demo 4: ALZ-NIEV Demo
echo -e "${GREEN}4. ALZ-NIEV Protocol Demo${NC}"
echo "   Demonstrating bridge-free interoperability..."
python examples/alz_niev_demo.py
echo ""

# Demo 5: Interoperability Demo
echo -e "${GREEN}5. Interoperability Demo${NC}"
echo "   Demonstrating cross-chain interoperability..."
python examples/interoperability_demo.py
echo ""

# Demo 6: Cross-Chain Transfer
echo -e "${GREEN}6. Cross-Chain Transfer Demo${NC}"
echo "   Demonstrating bridge-free cross-chain transfers..."
python examples/cross_chain_transfer.py
echo ""

# Demo 7: Basic Wallet
echo -e "${GREEN}7. Basic Wallet Demo${NC}"
echo "   Demonstrating wallet operations..."
python examples/basic_wallet.py
echo ""

echo "=========================================="
echo -e "${GREEN}✅ All demos completed!${NC}"
echo "=========================================="
echo ""
echo "📚 Next steps:"
echo "   • Read GETTING_STARTED.md for detailed instructions"
echo "   • Run verification scripts: python scripts/verify_technical_proofs.py"
echo "   • Access testnet: https://testnet.allianza.tech"
echo ""
