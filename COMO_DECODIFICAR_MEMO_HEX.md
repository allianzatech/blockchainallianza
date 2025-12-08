# 🔧 Como Decodificar o Memo Hex da Transação

**Data:** 2025-12-08

---

## 📋 Memo Hex da Transação Real

**TX Hash:** `e4980edd048bb92f14cd688ffa4aaccd805cff2f1ea915683cbfe0c25cc00885`

**Memo Hex:**
```
7b22616c7a5f6e6965765f76657273696f6e223a2022312e30222c2022616d6f756e74223a20302e30312c2022736f757263655f636861696e223a2022706f6c79676f6e222c20227461726765745f636861696e223a2022657468657265756d222c202274696d657374616d70223a2022323032352d31322d30385432313a33363a31372e313534393930222c202274797065223a202263726f73735f636861696e5f7472616e73666572222c202275636861696e5f6964223a202255434841494e2d6333306433666364333764663636376634383664363462326131313233323166222c20227a6b5f70726f6f66223a207b2270726f6f665f6964223a20227a6b5f70726f6f665f313736353232393737365f64663465353162326366643632323261222c202273746174655f68617368223a202234313431373463633161353063323636316238646465633137303037363334343737633364383765653636366663663839636532393963346233613138623436222c20227665726966696564223a20747275657d7d
```

---

## 🔧 Método 1: Python

```python
import json

# Hex do memo (sem 0x)
memo_hex = "7b22616c7a5f6e6965765f76657273696f6e223a2022312e30222c2022616d6f756e74223a20302e30312c2022736f757263655f636861696e223a2022706f6c79676f6e222c20227461726765745f636861696e223a2022657468657265756d222c202274696d657374616d70223a2022323032352d31322d30385432313a33363a31372e313534393930222c202274797065223a202263726f73735f636861696e5f7472616e73666572222c202275636861696e5f6964223a202255434841494e2d6333306433666364333764663636376634383664363462326131313233323166222c20227a6b5f70726f6f66223a207b2270726f6f665f6964223a20227a6b5f70726f6f665f313736353232393737365f64663465353162326366643632323261222c202273746174655f68617368223a202234313431373463633161353063323636316238646465633137303037363334343737633364383765653636366663663839636532393963346233613138623436222c20227665726966696564223a20747275657d7d"

# Converter hex para bytes
memo_bytes = bytes.fromhex(memo_hex)

# Decodificar UTF-8
memo_text = memo_bytes.decode('utf-8')

# Parse JSON
memo_json = json.loads(memo_text)

# Imprimir formatado
print(json.dumps(memo_json, indent=2))
```

**Resultado:**
```json
{
  "alz_niev_version": "1.0",
  "amount": 0.01,
  "source_chain": "polygon",
  "target_chain": "ethereum",
  "timestamp": "2025-12-08T21:36:17.154990",
  "type": "cross_chain_transfer",
  "uchain_id": "UCHAIN-c30d3fcd37df667f486d64b2a112321f",
  "zk_proof": {
    "proof_id": "zk_proof_1765229776_df4e51b2cfd6222a",
    "state_hash": "414174cc1a50c2661b8ddec17007634477c3d87ee666fcf89ce299c4b3a18b46",
    "verified": true
  }
}
```

---

## 🔧 Método 2: JavaScript (Node.js)

```javascript
const memoHex = "7b22616c7a5f6e6965765f76657273696f6e223a2022312e30222c2022616d6f756e74223a20302e30312c2022736f757263655f636861696e223a2022706f6c79676f6e222c20227461726765745f636861696e223a2022657468657265756d222c202274696d657374616d70223a2022323032352d31322d30385432313a33363a31372e313534393930222c202274797065223a202263726f73735f636861696e5f7472616e73666572222c202275636861696e5f6964223a202255434841494e2d6333306433666364333764663636376634383664363462326131313233323166222c20227a6b5f70726f6f66223a207b2270726f6f665f6964223a20227a6b5f70726f6f665f313736353232393737365f64663465353162326366643632323261222c202273746174655f68617368223a202234313431373463633161353063323636316238646465633137303037363334343737633364383765653636366663663839636532393963346233613138623436222c20227665726966696564223a20747275657d7d";

// Converter hex para Buffer
const memoBytes = Buffer.from(memoHex, 'hex');

// Decodificar UTF-8
const memoText = memoBytes.toString('utf-8');

// Parse JSON
const memoJson = JSON.parse(memoText);

// Imprimir formatado
console.log(JSON.stringify(memoJson, null, 2));
```

---

## 🔧 Método 3: Online Tools

### Opção 1: RapidTables
1. Acesse: https://www.rapidtables.com/convert/number/hex-to-ascii.html
2. Cole o hex (sem 0x)
3. Clique em "Convert"
4. Copie o resultado ASCII
5. Use um JSON formatter online para formatar

### Opção 2: Hex Decoder
1. Acesse: https://www.hexdictionary.com/hexdecoder/
2. Cole o hex
3. Selecione "ASCII" ou "UTF-8"
4. Clique em "Decode"

### Opção 3: CyberChef
1. Acesse: https://gchq.github.io/CyberChef/
2. Cole o hex no input
3. Adicione "From Hex" na receita
4. Adicione "To JSON" se necessário
5. Veja o resultado formatado

---

## 🔧 Método 4: Etherscan (Automático)

1. Acesse: https://sepolia.etherscan.io/tx/e4980edd048bb92f14cd688ffa4aaccd805cff2f1ea915683cbfe0c25cc00885
2. Clique em "Click to see more"
3. Clique em "Decode Input Data"
4. O Etherscan decodifica automaticamente se reconhecer o formato

---

## 📊 O Que o Memo Contém?

```json
{
  "alz_niev_version": "1.0",                    // Versão do protocolo ALZ-NIEV
  "amount": 0.01,                                // Quantidade transferida
  "source_chain": "polygon",                     // Chain de origem
  "target_chain": "ethereum",                    // Chain de destino
  "timestamp": "2025-12-08T21:36:17.154990",    // Timestamp ISO 8601
  "type": "cross_chain_transfer",                // Tipo de transação
  "uchain_id": "UCHAIN-c30d3fcd37df667f486d64b2a112321f",  // UChainID único
  "zk_proof": {
    "proof_id": "zk_proof_1765229776_df4e51b2cfd6222a",      // ID da prova ZK
    "state_hash": "414174cc1a50c2661b8ddec17007634477c3d87ee666fcf89ce299c4b3a18b46",  // Hash do estado
    "verified": true                              // Status de verificação
  }
}
```

---

## ✅ Verificação

1. **UChainID:** `UCHAIN-c30d3fcd37df667f486d64b2a112321f`
   - Busque na interface: https://testnet.allianza.tech/cross-chain-test
   - Ou via API: `GET /api/cross-chain/proof/UCHAIN-c30d3fcd37df667f486d64b2a112321f`

2. **ZK Proof ID:** `zk_proof_1765229776_df4e51b2cfd6222a`
   - Verificado: `true`
   - State Hash: `414174cc1a50c2661b8ddec17007634477c3d87ee666fcf89ce299c4b3a18b46`

3. **Timestamp:** `2025-12-08T21:36:17.154990`
   - Confere com o block timestamp

---

## 🎯 Script Python Completo

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decodificador de Memo Hex - Allianza Blockchain
Decodifica o memo hex de transações cross-chain
"""

import json
import sys

def decode_memo_hex(memo_hex: str) -> dict:
    """
    Decodifica memo hex para JSON
    """
    try:
        # Remover 0x se presente
        if memo_hex.startswith('0x'):
            memo_hex = memo_hex[2:]
        
        # Converter hex para bytes
        memo_bytes = bytes.fromhex(memo_hex)
        
        # Decodificar UTF-8
        memo_text = memo_bytes.decode('utf-8')
        
        # Parse JSON
        memo_json = json.loads(memo_text)
        
        return memo_json
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Memo hex da transação real
    memo_hex = "7b22616c7a5f6e6965765f76657273696f6e223a2022312e30222c2022616d6f756e74223a20302e30312c2022736f757263655f636861696e223a2022706f6c79676f6e222c20227461726765745f636861696e223a2022657468657265756d222c202274696d657374616d70223a2022323032352d31322d30385432313a33363a31372e313534393930222c202274797065223a202263726f73735f636861696e5f7472616e73666572222c202275636861696e5f6964223a202255434841494e2d6333306433666364333764663636376634383664363462326131313233323166222c20227a6b5f70726f6f66223a207b2270726f6f665f6964223a20227a6b5f70726f6f665f313736353232393737365f64663465353162326366643632323261222c202273746174655f68617368223a202234313431373463633161353063323636316238646465633137303037363334343737633364383765653636366663663839636532393963346233613138623436222c20227665726966696564223a20747275657d7d"
    
    if len(sys.argv) > 1:
        memo_hex = sys.argv[1]
    
    result = decode_memo_hex(memo_hex)
    
    print(json.dumps(result, indent=2))
```

**Uso:**
```bash
python decode_memo.py
# Ou com hex customizado:
python decode_memo.py "7b22616c7a5f6e6965765f76657273696f6e223a..."
```

---

**Última atualização:** 2025-12-08

