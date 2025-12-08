# 🧪 Testing Guide - Allianza Blockchain

This guide explains how to run public tests and reproduce the results of technical proofs.

## 📋 Prerequisites

### 1. Environment Setup

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt

# Install liboqs-python (optional, but recommended)
# See INSTALAR_LIBOQS.md for detailed instructions
```

### 2. Configuration

Create a `.env` file in the project root (will not be committed):

```env
# Example - DO NOT commit real values
ALLIANZA_ENCRYPTION_KEY=your_encryption_key_here
DATABASE_URL=sqlite:///allianza_test.db
```

**⚠️ IMPORTANT**: The `.env` file is in `.gitignore` and will not be committed.

## 🚀 Running Tests

### Basic Verification Tests

```bash
# Run basic verification suite
python tests/public/run_verification_tests.py
```

This script runs:
- ✅ QRS-3 (PQC) verification
- ✅ Interoperability test
- ✅ Consensus test
- ✅ Transaction validation

### Complete Tests (Reproduce Technical Proofs)

```bash
# Run all tests that generated COMPLETE_TECHNICAL_PROOFS_FINAL.json
python tests/public/run_all_tests.py
```

This script:
- Executes all technical tests
- Generates consolidated report
- Saves results in `proofs/testnet/public_tests/`

### Specific Tests

#### 1. QRS-3 (PQC) Test

```bash
python tests/public/test_qrs3_verification.py
```

**What it tests:**
- ML-DSA key generation
- SPHINCS+ signature and verification
- Batch verification
- PQC performance

**Expected result:**
```json
{
  "test": "QRS-3 Verification",
  "status": "PASSED",
  "ml_dsa_keygen": "✅",
  "sphincs_signature": "✅",
  "batch_verification": "✅"
}
```

#### 2. Interoperability Test

```bash
python tests/public/test_interoperability.py
```

**What it tests:**
- Cross-chain transfers
- Proof-of-Lock
- Bridge-free routing
- Atomic swaps

**Expected result:**
- Transactions created on testnet
- Transaction hashes returned
- Status: "success"

#### 3. Consensus (ALZ-NIEV) Test

```bash
python tests/public/test_consensus.py
```

**What it tests:**
- Block creation
- Transaction validation
- Sharding
- Consensus adaptability

#### 4. Performance Test

```bash
python tests/public/test_performance.py
```

**What it tests:**
- Throughput (TPS)
- Latency
- Batch verification time
- Memory usage

## 📊 Comparing Results

### 1. Verify Test Results

After running tests, compare with `COMPLETE_TECHNICAL_PROOFS_FINAL.json`:

```bash
# Verify if results are consistent
python tests/public/verify_results.py
```

### 2. Verify on Testnet

1. Access https://testnet.allianza.tech/explorer
2. Search for transaction hashes returned by tests
3. Verify that transactions appear in the explorer

### 3. Verify Logs

Execution logs are saved in:
- `logs/test_execution_YYYY-MM-DD.log`
- `proofs/testnet/` (individual proofs)

## 🔍 Interpreting Results

### Test Status

- ✅ **PASSED**: Test passed successfully
- ⚠️ **WARNING**: Test passed but with warnings
- ❌ **FAILED**: Test failed
- ⏭️ **SKIPPED**: Test skipped (dependency not available)

### Important Metrics

#### QRS-3 Performance

```json
{
  "ml_dsa_keygen_time_ms": 45.2,
  "sphincs_sign_time_ms": 12.8,
  "batch_verification_100_txs_ms": 234.5
}
```

**Interpretation:**
- `keygen_time < 100ms`: ✅ Excellent
- `sign_time < 50ms`: ✅ Good
- `batch_verification < 500ms` (100 txs): ✅ Efficient

#### Interoperability

```json
{
  "cross_chain_transfers": 10,
  "successful": 10,
  "failed": 0,
  "avg_time_seconds": 3.2
}
```

**Interpretation:**
- `success_rate = 100%`: ✅ Perfect
- `avg_time < 5s`: ✅ Fast

#### Consensus

```json
{
  "blocks_created": 50,
  "avg_block_time_seconds": 2.1,
  "tps": 19.8
}
```

**Interpretation:**
- `tps > 15`: ✅ Good throughput
- `block_time < 3s`: ✅ Fast

## 🐛 Troubleshooting

### Error: "liboqs not found"

**Solution:**
```bash
# Install liboqs-python
pip install liboqs-python

# Or follow INSTALAR_LIBOQS.md
```

### Error: "Database connection failed"

**Solution:**
```bash
# Create .env file with DATABASE_URL
echo "DATABASE_URL=sqlite:///allianza_test.db" > .env
```

### Error: "Testnet connection timeout"

**Solution:**
- Check internet connection
- Verify testnet is online: https://testnet.allianza.tech
- Try again after a few seconds

### Tests failing randomly

**Possible causes:**
- Testnet temporarily unavailable
- Rate limiting
- Dependencies not installed

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Run tests again
python tests/public/run_verification_tests.py
```

## 📝 Generating Reports

### Complete Report

```bash
python tests/public/run_all_tests.py
```

Generates report in: `proofs/testnet/public_tests/YYYYMMDD_HHMMSS_report.json`

### Performance Report

```bash
python tests/public/test_performance.py --report
```

Generates report in: `proofs/testnet/performance_report_YYYY-MM-DD.json`

## 🔗 Next Steps

1. ✅ Run basic tests
2. ✅ Compare with `COMPLETE_TECHNICAL_PROOFS_FINAL.json`
3. ✅ Verify transactions on testnet
4. 📖 Read [VERIFICATION.md](VERIFICATION.md) for independent verification
5. 🐛 Report issues in [SECURITY.md](SECURITY.md)

## 📚 References

- [VERIFICATION.md](VERIFICATION.md) - Independent verification guide
- [SECURITY.md](SECURITY.md) - Security policy
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API reference
- [INSTALAR_LIBOQS.md](INSTALAR_LIBOQS.md) - liboqs installation

---

**Last updated**: 2025-12-07
