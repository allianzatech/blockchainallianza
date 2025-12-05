# 🧪 Tests - Allianza Blockchain

This directory contains test scripts and validation for the public repository.

## 📋 Files

### `run_all_demos.py` - Unified Test Runner

Runs all demos in `examples/` and generates a complete report.

**Usage:**
```bash
python tests/run_all_demos.py
```

**Output:**
- JSON Report: `tests/demo_test_report_YYYYMMDD_HHMMSS.json`
- Text Summary: `tests/demo_test_summary_YYYYMMDD_HHMMSS.txt`

**What it tests:**
- ✅ `examples/qss_demo.py` - Quantum Security Service
- ✅ `examples/qrs3_demo.py` - Quantum Redundancy System
- ✅ `examples/alz_niev_demo.py` - ALZ-NIEV Interoperability
- ✅ `examples/interoperability_demo.py` - Practical examples

**Example Report:**
```json
{
  "test_suite": "Allianza Blockchain - Demo Tests",
  "summary": {
    "total_demos": 4,
    "successful": 4,
    "failed": 0,
    "success_rate": 100.0,
    "total_execution_time_ms": 1234.56
  },
  "results": [...]
}
```

## 🎯 Use Cases

### For Developers
- Validate that all examples work
- Check compatibility after changes
- Prepare for contributions

### For Audits
- End-to-end functionality proof
- Structured reports for analysis
- Validation of all technologies

### For CI/CD
- Continuous integration (future)
- Automatic PR validation
- Quality reports

## 📊 Metrics

The test runner provides:
- ✅ Success rate
- ⏱️ Execution time
- 📝 Complete output from each demo
- ❌ Detailed errors (if any)

## 🔗 Related Links

- [Examples](../examples/README.md)
- [Documentation](../docs/API_REFERENCE.md)
- [Testnet](https://testnet.allianza.tech)

---

**Last updated:** 2025-12-05
