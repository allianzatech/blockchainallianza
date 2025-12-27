#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Chain Transfer Example - Allianza Blockchain
Demonstrates bridge-free cross-chain interoperability
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    """Demonstrate cross-chain transfer"""
    print("=" * 70)
    print("🌉 Allianza Blockchain - Cross-Chain Transfer Example")
    print("=" * 70)
    print()
    
    try:
        from core.interoperability.bridge_free_interop import BridgeFreeInterop
        
        print("📝 Initializing bridge-free interoperability...")
        interop = BridgeFreeInterop()
        
        print()
        print("💡 Example: Transfer from Polygon to Ethereum")
        print("-" * 70)
        print()
        print("This example demonstrates how to transfer tokens cross-chain")
        print("without traditional bridges or wrapped tokens.")
        print()
        print("Required parameters:")
        print("  - source_chain: 'polygon'")
        print("  - target_chain: 'ethereum'")
        print("  - amount: 100.0")
        print("  - recipient: '0x...' (Ethereum address)")
        print("  - source_private_key: 'your_polygon_private_key'")
        print()
        print("⚠️  Note: This is a demonstration. For actual transfers,")
        print("   configure your private keys and recipient addresses.")
        print()
        print("📖 See docs/INTEROPERABILITY.md for complete documentation")
        print()
        
        # Example code (commented out for safety)
        example_code = """
# Example cross-chain transfer
result = interop.transfer_cross_chain(
    source_chain="polygon",
    target_chain="ethereum",
    amount=100.0,
    recipient="0xYourEthereumAddress",
    source_private_key="your_polygon_private_key"
)

if result.get("success"):
    print(f"✅ Transfer initiated: {result['transfer_id']}")
    print(f"   Proof-of-Lock: {result['proof_of_lock']}")
else:
    print(f"❌ Error: {result.get('error')}")
"""
        
        print("Example code:")
        print(example_code)
        
    except ImportError as e:
        print(f"⚠️  Error: {e}")
        print("💡 Some dependencies may not be available")
        return 1
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

