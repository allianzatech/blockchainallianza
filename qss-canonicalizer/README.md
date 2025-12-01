# @allianza/qss-canonicalizer

🔐 Canonicalizador de provas QSS conforme RFC8785

Gera `proof_hash` canônico para ancoragem on-chain (OP_RETURN, Smart Contracts).

## 🚀 Uso

### Canonicalizar prova padrão

```bash
node canonicalize.js proof.json
```

### Especificar campos canônicos

```bash
node canonicalize.js proof.json --fields=asset_chain,asset_tx,merkle_root,block_hash,timestamp
```

## 📊 Exemplo de Saída

```
🔐 Canonicalizando prova QSS...

📊 Resultado:

Proof Hash: c1b2c8a6ecf44cb930791c953a9572fe70891aa3f2b7d9c49f6b47a72e9b28f3

Campos canônicos usados:
   - asset_chain: bitcoin
   - asset_tx: 89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb
   - merkle_root: 8c8af09c3927ab564dd8289c2a8c7b4cd549a6887218d8a4d105444667c3a9d8
   - block_hash: (não definido)
   - timestamp: 1764547146.9580045

JSON Canônico (RFC8785):
{"asset_chain":"bitcoin","asset_tx":"89b6d1b46c2a1f93bd1d9ccc95dd25b46a81c7f37cb7b2a11abbebd29ddafaeb","merkle_root":"8c8af09c3927ab564dd8289c2a8c7b4cd549a6887218d8a4d105444667c3a9d8","timestamp":1764547146.9580045}

📡 Payload para OP_RETURN (Bitcoin):
ALZ:c1b2c8a6ecf44cb930791c953a9572fe70891aa3f2b7d9c49f6b47a72e9b28f3
Tamanho: 73 bytes
```

## 🔗 Links

- **RFC8785**: https://tools.ietf.org/html/rfc8785
- **Repositório**: https://github.com/allianza-blockchain/qss-canonicalizer

## 📄 Licença

MIT

