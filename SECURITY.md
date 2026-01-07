# 🔒 Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

### How to Report

If you discover a security vulnerability, please **DO NOT** open a public issue. Instead, report it privately:

1. **Email:** [contact@allianza.tech](mailto:contact@allianza.tech)
2. **Subject:** `[SECURITY] Brief description of vulnerability`
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Suggested fix (if you have one)

### What to Expect

- **Response Time:** We aim to respond within 48 hours
- **Update Frequency:** We will provide updates every 7 days until resolution
- **Disclosure:** We will coordinate public disclosure after a fix is available

### Security Severity Levels

- **Critical:** Remote code execution, authentication bypass, data breach
- **High:** Privilege escalation, sensitive data exposure
- **Medium:** Information disclosure, denial of service
- **Low:** Minor information leakage, best practice violations

---

## Security Features

### Implemented Security Measures

✅ **Path Traversal Protection** - Secure file download validation  
✅ **CSRF Protection** - Applied to all critical POST routes  
✅ **Rate Limiting** - Global DDoS protection  
✅ **Input Validation** - Comprehensive sanitization  
✅ **Security Headers** - CSP, COEP, COOP  
✅ **SECRET_KEY Validation** - Production environment checks  
✅ **Audit Logging** - Complete transaction traceability  
✅ **Quantum-Safe Cryptography** - NIST PQC standards (ML-DSA, ML-KEM, SPHINCS+)  
✅ **Zero-Knowledge Proofs** - Cryptographic verification of state transitions  

### Security Audit

A comprehensive security audit has been performed. See:
- **[Security Audit Report](docs/SECURITY_AUDIT_REPORT.md)** - Full vulnerability analysis
- **[Dependency Vulnerabilities Report](docs/DEPENDENCY_VULNERABILITIES_REPORT.md)** - Dependency security status

---

## Security Best Practices

### For Developers

1. **Never commit secrets** - Use `.env` files (already in `.gitignore`)
2. **Use testnet keys only** - Never use mainnet keys in development
3. **Validate all inputs** - Always sanitize user input
4. **Keep dependencies updated** - Run `pip-audit` regularly
5. **Follow secure coding practices** - See [CONTRIBUTING.md](CONTRIBUTING.md)

### For Production Deployments

1. **Use strong SECRET_KEY** - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
2. **Enable HTTPS** - Always use TLS/SSL in production
3. **Configure security headers** - CSP, COEP, COOP are already implemented
4. **Monitor logs** - Set up alerting for suspicious activity
5. **Regular security updates** - Keep dependencies and system updated

---

## Dependency Security

### Checking for Vulnerabilities

```bash
# Using pip-audit (recommended)
pip install pip-audit
pip-audit

# Using our custom script
python scripts/check_dependencies_security.py
```

### Known Vulnerabilities

We maintain a list of known vulnerabilities and their status in:
- **[Dependency Vulnerabilities Report](docs/DEPENDENCY_VULNERABILITIES_REPORT.md)**

---

## Security Disclosure Timeline

1. **Discovery** - Vulnerability discovered
2. **Report** - Private report to contact@allianza.tech
3. **Acknowledgment** - Response within 48 hours
4. **Investigation** - Analysis and fix development
5. **Fix** - Patch developed and tested
6. **Disclosure** - Coordinated public disclosure after fix

---

## Security Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged (with permission) in our security acknowledgments.

---

## Contact

- **Contact:** [contact@allianza.tech](mailto:contact@allianza.tech)

---

**Last Updated:** 2025-01-27






