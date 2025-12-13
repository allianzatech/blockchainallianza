#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic Wallet Example - Allianza Blockchain
Demonstrates how to create a wallet and generate an address
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from allianza_blockchain import AllianzaBlockchain

def main():
    """Create a new wallet and display address"""
    print("=" * 70)
    print("👛 Allianza Blockchain - Basic Wallet Example")
    print("=" * 70)
    print()
    
    # Initialize blockchain
    print("📝 Initializing blockchain...")
    blockchain = AllianzaBlockchain()
    
    # Create wallet
    print("🔑 Creating new wallet...")
    address, private_key = blockchain.create_wallet()
    
    # Display results
    print()
    print("✅ Wallet created successfully!")
    print()
    print(f"📍 Address: {address}")
    print(f"🔐 Private Key: {private_key[:50]}...")
    print()
    print("⚠️  IMPORTANT: This is a TESTNET wallet.")
    print("   Never use this private key on mainnet!")
    print("   Keep your private key secure and never share it.")
    print()

if __name__ == "__main__":
    main()

