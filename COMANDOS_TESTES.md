# 🧪 Comandos para Executar Testes - Allianza Blockchain

**Data:** 2025-12-08

---

## 📋 Pré-requisitos

### Instalar Dependências (se necessário)
```bash
pip install qiskit qiskit-aer
```

---

## 🧪 Testes Disponíveis

### 1. Testes de Ataques Quânticos

**Comando:**
```bash
python tests/quantum_attack_simulations.py
```

**O que testa:**
- ✅ Simulação de ataque de Shor em ECDSA
- ✅ Resistência QRS-3 a ataques quânticos
- ✅ Benchmark QRS-3 vs ECDSA

**Resultados salvos em:** `proofs/quantum_attack_simulations/quantum_attack_simulation_*.json`

---

### 2. Testes de Cross-Chain Recovery

**Comando:**
```bash
python tests/cross_chain_recovery.py
```

**O que testa:**
- ✅ Simulação de falhas de chain
- ✅ Mecanismos de recuperação automática
- ✅ Atomicidade em falhas multi-chain

**Resultados salvos em:** `proofs/recovery_tests/cross_chain_recovery_*.json`

---

### 3. Benchmarks Independentes

**Comando:**
```bash
python tests/benchmark_independent.py
```

**O que testa:**
- ✅ TPS (Transactions Per Second)
- ✅ Latência
- ✅ Throughput
- ✅ Batch Verification
- ✅ Comparação com outras blockchains

**Resultados salvos em:** `proofs/benchmarks/independent_benchmark_*.json`

---

## 🚀 Executar Todos os Testes

### Windows (PowerShell)
```powershell
cd "C:\Users\notebook\Downloads\Allianza Blockchain"
python tests/quantum_attack_simulations.py
python tests/cross_chain_recovery.py
python tests/benchmark_independent.py
```

### Linux/Mac
```bash
cd "C:\Users\notebook\Downloads\Allianza Blockchain"
python tests/quantum_attack_simulations.py
python tests/cross_chain_recovery.py
python tests/benchmark_independent.py
```

---

## 📊 Resultados Esperados

### Teste 1: Ataques Quânticos
```
✅ Teste 1: Simulando ataque de Shor em ECDSA... PASSOU
✅ Teste 2: Testando resistência QRS-3... PASSOU
✅ Teste 3: Benchmark QRS-3 vs ECDSA... PASSOU
```

### Teste 2: Cross-Chain Recovery
```
✅ Teste 1: Falha de rede... PASSOU
✅ Teste 2: Mecanismo de recuperação... PASSOU (500ms)
✅ Teste 3: Falha de atomicidade... PASSOU
```

### Teste 3: Benchmarks
```
✅ TPS: ~605 transações/segundo
✅ Latência: ~0.62ms
✅ Throughput: ~96 MB/s
✅ Melhoria batch: ~20%
```

---

## 🔍 Verificar Resultados

### Ver JSON Gerado
```bash
# Windows
type proofs\quantum_attack_simulations\quantum_attack_simulation_*.json
type proofs\recovery_tests\cross_chain_recovery_*.json
type proofs\benchmarks\independent_benchmark_*.json
```

### Linux/Mac
```bash
cat proofs/quantum_attack_simulations/quantum_attack_simulation_*.json
cat proofs/recovery_tests/cross_chain_recovery_*.json
cat proofs/benchmarks/independent_benchmark_*.json
```

---

## ⚠️ Troubleshooting

### Erro: "Qiskit não disponível"
```bash
pip install qiskit qiskit-aer
```

### Erro: "QuantumSecuritySystem não disponível"
- Verificar se está no diretório correto
- Verificar se `quantum_security.py` existe

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

---

## 📝 Notas

- Todos os testes geram arquivos JSON com resultados detalhados
- Os testes podem levar alguns segundos para executar
- Qiskit é opcional, mas recomendado para testes completos

---

**Última atualização:** 2025-12-08
