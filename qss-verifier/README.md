# @allianza/qss-verifier

🔐 Verificador open-source de provas QSS (Quantum Security Service)

Verifica provas quânticas geradas pela Allianza Blockchain **sem depender de APIs ou confiar em servidores**.

## 🚀 Instalação

```bash
npm install
```

## 📖 Uso

### Verificar arquivo JSON

```bash
node verify.js proof.json
```

### Verificar por proof_id (via API)

```bash
node verify.js qss-2025-00001234
```

## ✅ O que é verificado

1. **Schema Version** - Versão do formato da prova
2. **Campos Obrigatórios** - Todos os campos necessários presentes
3. **Proof Hash** - Hash canônico (RFC8785) confere
4. **Merkle Proof** - Caminho Merkle reconstruído corretamente
5. **Assinatura Quântica** - Assinatura ML-DSA válida
6. **Block Information** - Block height e hash válidos
7. **Timestamp** - Prova não muito antiga (<1 ano)

## 📊 Exemplo de Saída

```
🔍 Verificando prova QSS...

Proof ID: qss-2025-00001234
Chain: bitcoin
TX: 89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb

📊 Resultados da Verificação:

✅ schema_version: VÁLIDO
✅ proof_hash: VÁLIDO
✅ merkle_proof: VÁLIDO
✅ quantum_signature: VÁLIDO
✅ block_height: VÁLIDO
✅ timestamp: VÁLIDO

============================================================
✅ PROVA VÁLIDA
============================================================
```

## 🔗 Links

- **Repositório**: https://github.com/allianza-blockchain/qss-verifier
- **Documentação**: https://docs.allianza.tech/qss/verification
- **API QSS**: https://testnet.allianza.tech/api/qss

## 📄 Licença

MIT

