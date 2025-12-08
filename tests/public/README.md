# 🧪 Testes Públicos - Allianza Blockchain

Este diretório contém scripts de teste públicos que podem ser executados para verificar as funcionalidades da Allianza Blockchain.

## 📋 Scripts Disponíveis

### `run_verification_tests.py`
Script principal que executa todos os testes básicos de verificação.

**Uso:**
```bash
python tests/public/run_verification_tests.py
```

**O que testa:**
- ✅ Verificação QRS-3 (PQC)
- ✅ Funcionalidades básicas da blockchain
- ✅ Interoperabilidade básica

### Scripts Específicos

Scripts adicionais podem ser adicionados aqui para testes mais específicos:
- `test_qrs3_verification.py` - Testes detalhados de QRS-3
- `test_interoperability.py` - Testes de interoperabilidade
- `test_consensus.py` - Testes de consenso
- `test_performance.py` - Testes de performance

## 🔒 Segurança

**⚠️ IMPORTANTE**: Estes scripts são públicos e **NÃO** devem:
- ❌ Expor chaves privadas
- ❌ Usar credenciais reais
- ❌ Acessar mainnet
- ❌ Modificar dados de produção

Todos os testes usam:
- ✅ Testnet apenas
- ✅ Wallets temporárias
- ✅ Dados de teste
- ✅ Sem segredos hardcoded

## 📊 Resultados

Os resultados dos testes são salvos em:
- `proofs/testnet/verification_YYYYMMDD_HHMMSS.json`

## 🔗 Ver Também

- [TESTING.md](../../TESTING.md) - Guia completo de testes
- [VERIFICATION.md](../../VERIFICATION.md) - Guia de verificação independente

