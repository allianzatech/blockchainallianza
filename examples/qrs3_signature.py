#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QRS-3 Signature Example - Allianza Blockchain
Demonstrates post-quantum cryptography with ML-DSA and SPHINCS+
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    """Demonstrate QRS-3 signature generation and verification"""
    print("=" * 70)
    print("🔐 Allianza Blockchain - QRS-3 Signature Example")
    print("=" * 70)
    print()
    
    try:
        from core.crypto.pqc_crypto import MLDSAKeyPair, SPHINCSPlusKeyPair
        
        # Message to sign
        message = b"Hello, Allianza Blockchain! This is a post-quantum secure message."
        
        print("📝 Message to sign:")
        print(f"   {message.decode()}")
        print()
        
        # ML-DSA Example
        print("🔑 ML-DSA (Module-Lattice Digital Signature Algorithm)")
        print("-" * 70)
        mldsa = MLDSAKeyPair()
        mldsa_signature = mldsa.sign(message)
        mldsa_valid = mldsa.verify(message, mldsa_signature)
        
        print(f"✅ Signature generated: {mldsa_signature[:50]}...")
        print(f"✅ Verification: {'PASSED' if mldsa_valid else 'FAILED'}")
        print()
        
        # SPHINCS+ Example
        print("🔑 SPHINCS+ (Stateless Hash-Based Signatures)")
        print("-" * 70)
        sphincs = SPHINCSPlusKeyPair()
        sphincs_signature = sphincs.sign(message)
        sphincs_valid = sphincs.verify(message, sphincs_signature)
        
        print(f"✅ Signature generated: {sphincs_signature[:50]}...")
        print(f"✅ Verification: {'PASSED' if sphincs_valid else 'FAILED'}")
        print()
        
        print("=" * 70)
        if mldsa_valid and sphincs_valid:
            print("✅ All QRS-3 signatures verified successfully!")
        else:
            print("❌ Some signatures failed verification")
        print("=" * 70)
        
    except ImportError as e:
        print(f"⚠️  Error: {e}")
        print("💡 Install liboqs-python: pip install liboqs-python")
        print("   Or see INSTALAR_LIBOQS.md for installation instructions")
        return 1
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

