# 📋 Guia: Como Preencher o Resumo Digital Hash no INPI

## 📌 O que é o Resumo Digital Hash?

Conforme o **§1º e Incisos VI e VII do §2º do Art. 2º da Instrução Normativa do INPI**, o **resumo digital hash** é a transformação dos trechos do programa de computador e demais dados considerados suficientes para identificação e caracterização do software.

**Você é o responsável único** pela geração e guarda desses hashes.

---

## 🔐 Algoritmo Utilizado

A Allianza Blockchain utiliza **SHA-256** (Secure Hash Algorithm 256 bits) para gerar os resumos digitais.

---

## 📝 Como Preencher no Formulário do INPI

### **✅ Opção Recomendada: Hash Consolidado (UM HASH POR PROGRAMA)**

**Esta é a opção mais simples e prática!** Um único hash representa todos os arquivos do programa.

1. **Abra o arquivo `HASHES_CONSOLIDADOS_INPI.txt`**
2. **Copie o hash consolidado** do programa que você está registrando
3. **Cole no campo "Resumo Digital Hash"** do formulário do INPI

**Exemplo - RPC-1 (ALZ-NIEV):**
```
Hash Consolidado: 38c2e6711f3fc7350c0988613c8cd6fb0661cb37814ea9d60ead25474c4ffcc5
```

**Exemplo - RPC-2 (Quantum Security):**
```
Hash Consolidado: cede285ea5ba679ad17771497270ba2bb347a79e5bea46b6c4adc13afc4c6656
```

**Exemplo - RPC-3 (QSS):**
```
Hash Consolidado: 7de14be7a1e2a9c4ea578a54b10bb8e959c94221b13ce3deed5dbb99d3686258
```

**Exemplo - RPC-4 (Bridge):**
```
Hash Consolidado: 5a5bd2c4cd66558747a0da8dee81a9c6eb67cbf6e00d1ccb917035a614ec1263
```

### **Opção Alternativa: Hash Individual por Arquivo**

Se o formulário exigir um hash por arquivo:

1. **Copie o hash SHA256** de cada arquivo do arquivo `HASHES_INPI_RESUMO.txt`
2. **Cole no campo "Resumo Digital Hash"** do formulário do INPI
3. **Repetir para cada arquivo** que compõe o programa

**⚠️ Importante:** Verifique no formulário do INPI qual formato é aceito. A maioria aceita o hash consolidado.

---

## 📂 Arquivos de Referência

Você tem três arquivos gerados automaticamente:

### 1. **HASHES_CONSOLIDADOS_INPI.txt** ⭐ **USE ESTE!**
- Contém **um único hash por programa** (mais simples para o formulário)
- Formato direto e fácil de copiar
- **Este é o arquivo recomendado para preencher o formulário do INPI**

### 2. **HASHES_INPI_RESUMO.txt**
- Contém os hashes individuais de cada arquivo
- Organizado por categoria (Patentes, RPCs, Documentação)
- Inclui também os hashes consolidados no final
- Útil se precisar dos hashes individuais

### 3. **HASHES_INPI_COMPLETO.json**
- Contém todos os hashes em formato JSON estruturado
- Inclui metadados (data de geração, tamanho dos arquivos)
- Útil para referência técnica e auditoria

---

## 📋 Hashes por Programa de Computador (RPC)

### **RPC-1: Sistema ALZ-NIEV**

```
alz_niev_interoperability.py
Hash: a6292046d8c401ac41e2b953b620be80ca30d2fb85671a79ea0187219ff0fdf3

real_cross_chain_bridge.py
Hash: 3091d59d199872e3821288e2c1565a307030a06bfd4283955bc92baf815fee9a

test_atomicity_failure.py
Hash: 3ad3734538b01507f75a36f5b06208f463197acecb51770e694899f1c2f203c7

test_write_cross_chain.py
Hash: afcded32c9d824766d92b8d90d2464fa47d87df07fc3018d0a9b08f3fd3a5691
```

### **RPC-2: Sistema de Segurança Quântica**

```
quantum_security.py
Hash: a0b4430824f371880faba9306a93f5fefad62bf56b103b46cef47600ef870dcf

quantum_security_REAL.py
Hash: c62ba6863ac6160a3d7f1f9b610e5c7ee2592492d6472b5a7ecb28e42b464c5f

quantum_multi_sig_wallet.py
Hash: 60c93f10ae3bbc45048bd3206fd97a2451e90ead1bd45e0100d8a4419836760a
```

### **RPC-3: Quantum Security Service (QSS)**

```
qss_api_service.py
Hash: 892653e6b29d834903ae5cb76cd6dccbae543d798ad57b5ecfd5d512f4d74b58

qss-sdk/src/index.ts
Hash: 0f8795051d611344d37bb0ffe19b1c4120d71215204fdc0f3067bd5353613041

qss-verifier/verify.js
Hash: 3830b1230a44997743daf71bc62da16e26904923e441f3f71493b148d0e3cf6b
```

### **RPC-4: Bridge Cross-Chain**

```
real_cross_chain_bridge.py
Hash: 3091d59d199872e3821288e2c1565a307030a06bfd4283955bc92baf815fee9a
```

---

## ⚠️ Observações Importantes

1. **Guarde os arquivos originais:** Você é responsável pela guarda dos arquivos originais que geraram esses hashes
2. **Não altere os arquivos:** Qualquer alteração nos arquivos gerará hashes diferentes
3. **Data de geração:** Os hashes foram gerados em: **2025-12-04T21:32:39**
4. **Algoritmo:** SHA-256 (padrão aceito pelo INPI)

---

## 🔄 Como Regenerar os Hashes (se necessário)

Se você precisar regenerar os hashes (por exemplo, após fazer alterações nos arquivos), execute:

```bash
python gerar_hashes_inpi.py
```

Isso gerará novos arquivos `HASHES_INPI_COMPLETO.json` e `HASHES_INPI_RESUMO.txt` com os hashes atualizados.

---

## 📞 Suporte

Se tiver dúvidas sobre qual hash usar ou como preencher o formulário, consulte:
- A documentação oficial do INPI
- O arquivo `GUIA_PASSO_A_PASSO_DEPOSITO_INPI.md` para instruções detalhadas sobre o depósito

---

**✅ Status:** Hashes gerados e prontos para uso no formulário do INPI
**📅 Data de Geração:** 2025-12-04T21:32:39
**🔐 Algoritmo:** SHA-256

