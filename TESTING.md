# 🧪 Guia de Testes - Allianza Blockchain

Este guia explica como executar os testes públicos e reproduzir os resultados das provas técnicas.

## 📋 Pré-requisitos

### 1. Instalação do Ambiente

```bash
# Python 3.8 ou superior
python --version

# Instalar dependências
pip install -r requirements.txt

# Instalar liboqs-python (opcional, mas recomendado)
# Veja INSTALAR_LIBOQS.md para instruções detalhadas
```

### 2. Configuração

Crie um arquivo `.env` na raiz do projeto (não será commitado):

```env
# Exemplo - NÃO commitar valores reais
ALLIANZA_ENCRYPTION_KEY=your_encryption_key_here
DATABASE_URL=sqlite:///allianza_test.db
```

**⚠️ IMPORTANTE**: O arquivo `.env` está no `.gitignore` e não será commitado.

## 🚀 Executando Testes

### Testes Básicos de Verificação

```bash
# Executar suite de verificação básica
python tests/public/run_verification_tests.py
```

Este script executa:
- ✅ Verificação de QRS-3 (PQC)
- ✅ Teste de interoperabilidade
- ✅ Teste de consenso
- ✅ Validação de transações

### Testes Completos (Reproduzir Provas Técnicas)

```bash
# Executar todos os testes que geraram PROVAS_TECNICAS_COMPLETAS_FINAL.json
python EXECUTAR_TODOS_TESTES_INVESTIDORES.py
```

Este script:
- Executa todos os testes técnicos
- Gera relatório consolidado
- Salva resultados em `proofs/relatorio_investidores/`

### Testes Específicos

#### 1. Teste de QRS-3 (PQC)

```bash
python tests/public/test_qrs3_verification.py
```

**O que testa:**
- Geração de chaves ML-DSA
- Assinatura e verificação SPHINCS+
- Batch verification
- Performance PQC

**Resultado esperado:**
```json
{
  "test": "QRS-3 Verification",
  "status": "PASSED",
  "ml_dsa_keygen": "✅",
  "sphincs_signature": "✅",
  "batch_verification": "✅"
}
```

#### 2. Teste de Interoperabilidade

```bash
python tests/public/test_interoperability.py
```

**O que testa:**
- Transferências cross-chain
- Proof-of-Lock
- Bridge-free routing
- Atomic swaps

**Resultado esperado:**
- Transações criadas na testnet
- Hashes de transação retornados
- Status: "success"

#### 3. Teste de Consenso (ALZ-NIEV)

```bash
python tests/public/test_consensus.py
```

**O que testa:**
- Criação de blocos
- Validação de transações
- Sharding
- Adaptabilidade do consenso

#### 4. Teste de Performance

```bash
python tests/public/test_performance.py
```

**O que testa:**
- Throughput (TPS)
- Latência
- Tempo de batch verification
- Uso de memória

## 📊 Comparando Resultados

### 1. Verificar Resultados dos Testes

Após executar os testes, compare com `PROVAS_TECNICAS_COMPLETAS_FINAL.json`:

```bash
# Verificar se os resultados são consistentes
python tests/public/verify_results.py
```

### 2. Verificar na Testnet

1. Acesse https://testnet.allianza.tech/explorer
2. Procure pelos hashes de transação retornados pelos testes
3. Verifique que as transações aparecem no explorer

### 3. Verificar Logs

Os logs de execução são salvos em:
- `logs/test_execution_YYYY-MM-DD.log`
- `proofs/testnet/` (provas individuais)

## 🔍 Interpretando Resultados

### Status de Teste

- ✅ **PASSED**: Teste passou com sucesso
- ⚠️ **WARNING**: Teste passou mas com avisos
- ❌ **FAILED**: Teste falhou
- ⏭️ **SKIPPED**: Teste pulado (dependência não disponível)

### Métricas Importantes

#### QRS-3 Performance

```json
{
  "ml_dsa_keygen_time_ms": 45.2,
  "sphincs_sign_time_ms": 12.8,
  "batch_verification_100_txs_ms": 234.5
}
```

**Interpretação:**
- `keygen_time < 100ms`: ✅ Excelente
- `sign_time < 50ms`: ✅ Bom
- `batch_verification < 500ms` (100 txs): ✅ Eficiente

#### Interoperabilidade

```json
{
  "cross_chain_transfers": 10,
  "successful": 10,
  "failed": 0,
  "avg_time_seconds": 3.2
}
```

**Interpretação:**
- `success_rate = 100%`: ✅ Perfeito
- `avg_time < 5s`: ✅ Rápido

#### Consenso

```json
{
  "blocks_created": 50,
  "avg_block_time_seconds": 2.1,
  "tps": 19.8
}
```

**Interpretação:**
- `tps > 15`: ✅ Bom throughput
- `block_time < 3s`: ✅ Rápido

## 🐛 Troubleshooting

### Erro: "liboqs not found"

**Solução:**
```bash
# Instalar liboqs-python
pip install liboqs-python

# Ou seguir INSTALAR_LIBOQS.md
```

### Erro: "Database connection failed"

**Solução:**
```bash
# Criar arquivo .env com DATABASE_URL
echo "DATABASE_URL=sqlite:///allianza_test.db" > .env
```

### Erro: "Testnet connection timeout"

**Solução:**
- Verificar conexão com internet
- Verificar se testnet está online: https://testnet.allianza.tech
- Tentar novamente após alguns segundos

### Testes falhando aleatoriamente

**Possíveis causas:**
- Testnet temporariamente indisponível
- Rate limiting
- Dependências não instaladas

**Solução:**
```bash
# Reinstalar dependências
pip install -r requirements.txt --upgrade

# Executar testes novamente
python tests/public/run_verification_tests.py
```

## 📝 Gerando Relatórios

### Relatório Completo

```bash
python EXECUTAR_TODOS_TESTES_INVESTIDORES.py
```

Gera relatório em: `proofs/relatorio_investidores/YYYY-MM-DD_HH-MM-SS_report.json`

### Relatório de Performance

```bash
python tests/public/test_performance.py --report
```

Gera relatório em: `proofs/testnet/performance_report_YYYY-MM-DD.json`

## 🔗 Próximos Passos

1. ✅ Execute os testes básicos
2. ✅ Compare com `PROVAS_TECNICAS_COMPLETAS_FINAL.json`
3. ✅ Verifique transações na testnet
4. 📖 Leia [VERIFICATION.md](VERIFICATION.md) para verificação independente
5. 🐛 Reporte problemas em [SECURITY.md](SECURITY.md)

## 📚 Referências

- [VERIFICATION.md](VERIFICATION.md) - Guia de verificação independente
- [SECURITY.md](SECURITY.md) - Política de segurança
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Referência da API
- [INSTALAR_LIBOQS.md](INSTALAR_LIBOQS.md) - Instalação do liboqs

---

**Última atualização**: 2025-12-07

