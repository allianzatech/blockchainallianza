# QRS-3 - Post-Quantum Cryptography

## 📋 Description

QRS-3 (Quantum-Resistant Signature v3) implementation using standard PQC (Post-Quantum Cryptography) algorithms.

## 🔧 Main Files

- `pqc_crypto.py` - Post-quantum cryptography implementation
- `quantum_security.py` - Quantum security service
- `qrs3_complete_verification.py` - Complete QRS-3 verification

## 🔐 Supported Algorithms

- **ML-DSA** (Module-Lattice-based Digital Signature Algorithm)
- **SPHINCS+** (Stateless Hash-Based Signatures)

## 🚀 Features

- ✅ Post-quantum signatures
- ✅ Batch verification
- ✅ Integration with liboqs-python
- ✅ Compatibility with classical algorithms

## 📖 Documentation

See [docs/QRS3_IMPLEMENTATION.md](../../docs/QRS3_IMPLEMENTATION.md) for complete documentation.

## 🧪 Tests

Run tests:
```bash
python tests/public/test_qrs3_verification.py
```
