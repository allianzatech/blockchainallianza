# QRS-3 - Post-Quantum Cryptography

## 📋 Descrição

Implementação QRS-3 (Quantum-Resistant Signature v3) usando algoritmos PQC (Post-Quantum Cryptography) padrão.

## 🔧 Arquivos Principais

- `pqc_crypto.py` - Implementação de criptografia pós-quântica
- `quantum_security.py` - Serviço de segurança quântica
- `qrs3_complete_verification.py` - Verificação completa QRS-3

## 🔐 Algoritmos Suportados

- **ML-DSA** (Module-Lattice-based Digital Signature Algorithm)
- **SPHINCS+** (Stateless Hash-Based Signatures)

## 🚀 Características

- ✅ Assinaturas pós-quânticas
- ✅ Batch verification
- ✅ Integração com liboqs-python
- ✅ Compatibilidade com algoritmos clássicos

## 📖 Documentação

Veja [docs/QRS3_IMPLEMENTATION.md](../../docs/QRS3_IMPLEMENTATION.md) para documentação completa.

## 🧪 Testes

Execute os testes:
```bash
python tests/public/test_qrs3_verification.py
```

