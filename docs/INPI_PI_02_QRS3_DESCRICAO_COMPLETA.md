# PATENTE DE INVENÇÃO - PI-02
## Sistema e Método de Assinatura Digital com Tripla Redundância Quântica (QRS-3) Combinando ECDSA, ML-DSA e SPHINCS+

**Titular:** [NOME DO TITULAR]  
**Inventores:** [NOMES DOS INVENTORES]  
**Data de Depósito:** [DATA]  
**Número do Pedido:** [A SER PREENCHIDO PELO INPI]

---

## 1. CAMPO TÉCNICO

A presente invenção refere-se ao campo de criptografia pós-quântica e assinaturas digitais, mais especificamente a um sistema e método de assinatura digital com tripla redundância quântica que combina simultaneamente algoritmos clássicos (ECDSA) e algoritmos pós-quânticos (ML-DSA e SPHINCS+) para fornecer máxima segurança através de redundância e compatibilidade com blockchains existentes.

---

## 2. ESTADO DA TÉCNICA

### 2.1 Limitações das Soluções Existentes

As soluções atuais de assinatura digital apresentam limitações significativas:

**2.1.1 Algoritmos Clássicos (ECDSA)**
- Vulneráveis a computadores quânticos futuros
- Algoritmo de Shor pode quebrar ECDSA em tempo polinomial
- Não oferecem proteção contra ataques quânticos

**2.1.2 Algoritmos Pós-Quânticos Individuais**
- Podem ter vulnerabilidades não descobertas
- Implementações podem conter bugs
- Falta de redundância cria pontos únicos de falha

**2.1.3 Sistemas Híbridos Simples**
- Combinam apenas 2 algoritmos (clássico + PQC)
- Não oferecem redundância suficiente
- Não implementam fallback inteligente

### 2.2 Necessidade da Invenção

A presente invenção resolve essas limitações através de um sistema de tripla redundância que combina simultaneamente ECDSA, ML-DSA e SPHINCS+, fornecendo máxima segurança através de redundância e compatibilidade com blockchains existentes, com fallback inteligente e assinatura adaptativa baseada no valor da transação.

---

## 3. DESCRIÇÃO DETALHADA DA INVENÇÃO

### 3.1 Objetivo da Invenção

O objetivo da presente invenção é fornecer um sistema e método de assinatura digital que:

1. Combine simultaneamente 3 algoritmos de assinatura (ECDSA, ML-DSA, SPHINCS+)
2. Forneça redundância tripla para máxima segurança
3. Seja compatível com blockchains existentes (via ECDSA)
4. Seja resistente a computadores quânticos (via ML-DSA e SPHINCS+)
5. Implemente fallback inteligente quando um algoritmo não estiver disponível
6. Selecione nível de redundância baseado no valor da transação

### 3.2 Estrutura do Sistema QRS-3

O sistema QRS-3 (Quantum Redundancy System - Triple) gera **3 pares de chaves simultaneamente**:

#### 3.2.1 Chave ECDSA (secp256k1)

**Propósito:** Compatibilidade com blockchains existentes

**Características:**
- Algoritmo clássico amplamente adotado
- Compatível com Bitcoin, Ethereum e outras blockchains
- Tamanho de chave: 256 bits
- Tamanho de assinatura: 64 bytes

**Geração:**
```python
# Geração de chave ECDSA
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
public_key = private_key.public_key()
```

#### 3.2.2 Chave ML-DSA (Dilithium)

**Propósito:** Assinaturas quântico-seguras (NIST PQC Standard)

**Características:**
- Padrão: NIST FIPS 204
- Algoritmo baseado em lattice (Module-Lattice)
- Resistente a computadores quânticos
- Tamanho de chave pública: ~1.3 KB (Dilithium3)
- Tamanho de assinatura: ~2.7 KB (Dilithium3)

**Geração:**
```python
# Geração de chave ML-DSA
def generate_ml_dsa_keypair(security_level=3):
    """
    Gera par de chaves ML-DSA (Dilithium)
    security_level: 2, 3, 5 (recomendado: 3)
    """
    # Usando liboqs-python ou implementação funcional
    keypair = ml_dsa_keygen(security_level)
    return {
        "public_key": keypair.public_key,
        "private_key": keypair.private_key,
        "algorithm": "ML-DSA",
        "security_level": security_level
    }
```

#### 3.2.3 Chave SPHINCS+ (Hash-based)

**Propósito:** Redundância adicional com assinaturas hash-based

**Características:**
- Padrão: NIST FIPS 205
- Algoritmo baseado em hash (Hash-based signatures)
- Resistente a computadores quânticos
- Tamanho de chave pública: ~32 bytes
- Tamanho de assinatura: ~7.8 KB (SPHINCS+-SHAKE-128f)

**Geração:**
```python
# Geração de chave SPHINCS+
def generate_sphincs_keypair(variant="sha256-128f"):
    """
    Gera par de chaves SPHINCS+
    variant: sha256-128f, sha256-192f, sha256-256f
    """
    keypair = sphincs_keygen(variant)
    return {
        "public_key": keypair.public_key,
        "private_key": keypair.private_key,
        "algorithm": "SPHINCS+",
        "variant": variant
    }
```

### 3.3 Processo de Geração de Chaves QRS-3

O processo de geração de chaves QRS-3 segue os seguintes passos:

1. **Geração de Chave ECDSA:**
   - Gera par de chaves ECDSA (secp256k1)
   - Armazena chave privada de forma segura
   - Exporta chave pública em formato PEM

2. **Geração de Chave ML-DSA:**
   - Gera par de chaves ML-DSA (Dilithium)
   - Seleciona nível de segurança (recomendado: 3)
   - Armazena chave privada de forma segura

3. **Geração de Chave SPHINCS+:**
   - Tenta gerar par de chaves SPHINCS+
   - Testa múltiplas variantes se necessário
   - Se falhar, continua com QRS-2 (dupla redundância)

4. **Consolidação:**
   - Cria objeto QRS-3 com as 3 chaves
   - Gera ID único do keypair
   - Armazena metadados (algoritmos, timestamps)

**Exemplo de Implementação:**

```python
def generate_qrs3_keypair() -> Dict:
    """
    Gerar par de chaves QRS-3 (Tripla Redundância Quântica)
    """
    # 1. Chave clássica (ECDSA)
    classic_private = ec.generate_private_key(ec.SECP256K1(), default_backend())
    classic_public = classic_private.public_key()
    
    # 2. Chave ML-DSA (Dilithium)
    ml_dsa_result = generate_ml_dsa_keypair(security_level=3)
    if not ml_dsa_result["success"]:
        return ml_dsa_result
    
    # 3. Chave SPHINCS+ (Hash-based)
    sphincs_result = None
    sphincs_available = False
    
    # Tentar múltiplas variantes
    for variant in ["sha256-192f", "sha256-128f", "sha256-256f"]:
        try:
            sphincs_result = generate_sphincs_keypair(variant=variant)
            if sphincs_result.get("success", False):
                sphincs_available = True
                break
        except:
            continue
    
    # Se SPHINCS+ falhar, usar QRS-2
    if not sphincs_available:
        return generate_qrs2_keypair(classic_private, ml_dsa_result)
    
    # 4. Consolidar QRS-3
    keypair_id = f"qrs3_{int(time.time())}_{secrets.token_hex(8)}"
    
    return {
        "success": True,
        "keypair_id": keypair_id,
        "redundancy_level": 3,
        "algorithms": ["ECDSA", "ML-DSA", "SPHINCS+"],
        "ecdsa_key": classic_public,
        "ml_dsa_key": ml_dsa_result["public_key"],
        "sphincs_key": sphincs_result["public_key"]
    }
```

### 3.4 Processo de Assinatura QRS-3

O processo de assinatura QRS-3 segue os seguintes passos:

1. **Preparação da Mensagem:**
   - Recebe mensagem a ser assinada
   - Gera hash da mensagem (SHA-256)
   - Prepara dados para assinatura

2. **Assinatura com ECDSA:**
   - Assina hash da mensagem com chave ECDSA
   - Gera assinatura de 64 bytes
   - Valida assinatura gerada

3. **Assinatura com ML-DSA:**
   - Assina hash da mensagem com chave ML-DSA
   - Gera assinatura de ~2.7 KB
   - Valida assinatura gerada

4. **Assinatura com SPHINCS+:**
   - Assina hash da mensagem com chave SPHINCS+
   - Gera assinatura de ~7.8 KB
   - Valida assinatura gerada

5. **Consolidação:**
   - Combina as 3 assinaturas em um único objeto
   - Adiciona metadados (algoritmos, timestamps)
   - Retorna assinatura QRS-3 completa

**Exemplo de Implementação:**

```python
def sign_qrs3(keypair_id: str, message: bytes) -> Dict:
    """
    Assina mensagem com QRS-3 (tripla redundância)
    """
    # 1. Obter keypair
    keypair = get_qrs3_keypair(keypair_id)
    
    # 2. Gerar hash da mensagem
    message_hash = hashlib.sha256(message).digest()
    
    # 3. Assinar com ECDSA
    ecdsa_signature = sign_with_ecdsa(keypair["ecdsa_private"], message_hash)
    
    # 4. Assinar com ML-DSA
    ml_dsa_signature = sign_with_ml_dsa(keypair["ml_dsa_private"], message_hash)
    
    # 5. Assinar com SPHINCS+
    sphincs_signature = sign_with_sphincs(keypair["sphincs_private"], message_hash)
    
    # 6. Consolidar
    return {
        "success": True,
        "signature": {
            "ecdsa": ecdsa_signature,
            "ml_dsa": ml_dsa_signature,
            "sphincs": sphincs_signature
        },
        "algorithms": ["ECDSA", "ML-DSA", "SPHINCS+"],
        "redundancy_level": 3
    }
```

### 3.5 Processo de Verificação QRS-3

O processo de verificação QRS-3 segue os seguintes passos:

1. **Recebimento de Assinatura:**
   - Recebe assinatura QRS-3 completa
   - Extrai as 3 assinaturas (ECDSA, ML-DSA, SPHINCS+)
   - Valida formato

2. **Verificação Individual:**
   - Verifica assinatura ECDSA
   - Verifica assinatura ML-DSA
   - Verifica assinatura SPHINCS+

3. **Validação Final:**
   - Considera válida se pelo menos 2 das 3 assinaturas forem válidas
   - Retorna resultado detalhado
   - Registra estatísticas de verificação

**Exemplo de Implementação:**

```python
def verify_qrs3(
    public_key: Dict,
    message: bytes,
    signature: Dict
) -> Dict:
    """
    Verifica assinatura QRS-3
    """
    # 1. Gerar hash da mensagem
    message_hash = hashlib.sha256(message).digest()
    
    # 2. Verificar cada assinatura
    ecdsa_valid = verify_ecdsa(
        public_key["ecdsa"],
        message_hash,
        signature["ecdsa"]
    )
    
    ml_dsa_valid = verify_ml_dsa(
        public_key["ml_dsa"],
        message_hash,
        signature["ml_dsa"]
    )
    
    sphincs_valid = verify_sphincs(
        public_key["sphincs"],
        message_hash,
        signature["sphincs"]
    )
    
    # 3. Validar (pelo menos 2 de 3)
    valid_count = sum([ecdsa_valid, ml_dsa_valid, sphincs_valid])
    is_valid = valid_count >= 2
    
    return {
        "success": is_valid,
        "valid": is_valid,
        "ecdsa_valid": ecdsa_valid,
        "ml_dsa_valid": ml_dsa_valid,
        "sphincs_valid": sphincs_valid,
        "valid_count": valid_count,
        "redundancy_level": 3
    }
```

### 3.6 Fallback Inteligente (QRS-2)

Se SPHINCS+ não estiver disponível, o sistema automaticamente usa **QRS-2** (dupla redundância: ECDSA + ML-DSA).

**Características do QRS-2:**
- Combina ECDSA + ML-DSA
- Ainda oferece redundância significativa
- Compatível com blockchains existentes
- Resistente a computadores quânticos

### 3.7 Assinatura Adaptativa

O sistema seleciona o algoritmo baseado no valor da transação:

- **Micro-transações (< 0.001 ETH):** Apenas ML-DSA (mais rápido)
- **Transações normais (0.001 - 1 ETH):** QRS-2 (ECDSA + ML-DSA)
- **Transações críticas (> 1 ETH):** QRS-3 (ECDSA + ML-DSA + SPHINCS+)

**Exemplo de Implementação:**

```python
def sign_hybrid_intelligent(
    keypair_id: str,
    message: bytes,
    transaction_value: float
) -> Dict:
    """
    Assina adaptativamente baseado no valor da transação
    """
    if transaction_value < 0.001:
        # Micro-transação: apenas ML-DSA
        return sign_ml_dsa_only(keypair_id, message)
    elif transaction_value < 1.0:
        # Transação normal: QRS-2
        return sign_qrs2(keypair_id, message)
    else:
        # Transação crítica: QRS-3
        return sign_qrs3(keypair_id, message)
```

### 3.8 Vantagens da Invenção

A presente invenção apresenta as seguintes vantagens:

1. **Máxima Segurança:** Tripla redundância elimina pontos únicos de falha
2. **Compatibilidade:** ECDSA garante compatibilidade com blockchains existentes
3. **Resistência Quântica:** ML-DSA e SPHINCS+ protegem contra computadores quânticos
4. **Fallback Inteligente:** QRS-2 quando SPHINCS+ não disponível
5. **Assinatura Adaptativa:** Seleciona nível de redundância baseado no valor
6. **Padrões NIST:** Usa algoritmos aprovados pelo NIST (FIPS 204, 205)

---

## 4. REIVINDICAÇÕES

**Reivindicação 1:** Sistema de assinatura digital caracterizado por combinar simultaneamente três algoritmos de assinatura: ECDSA (secp256k1) para compatibilidade com blockchains existentes, ML-DSA (Dilithium - NIST FIPS 204) para assinaturas quântico-seguras, e SPHINCS+ (NIST FIPS 205) para redundância adicional com assinaturas hash-based.

**Reivindicação 2:** Método de geração de par de chaves com tripla redundância, caracterizado por gerar simultaneamente chaves ECDSA, ML-DSA e SPHINCS+ para o mesmo usuário, compreendendo as etapas de: gerar par de chaves ECDSA (secp256k1), gerar par de chaves ML-DSA (Dilithium), tentar gerar par de chaves SPHINCS+, e consolidar as três chaves em um único objeto QRS-3.

**Reivindicação 3:** Método de assinatura digital com tripla redundância, caracterizado por assinar a mesma mensagem com três algoritmos diferentes e combinar as assinaturas em um único objeto, compreendendo as etapas de: gerar hash da mensagem, assinar hash com ECDSA, assinar hash com ML-DSA, assinar hash com SPHINCS+, e consolidar as três assinaturas.

**Reivindicação 4:** Método de verificação de assinatura com tripla redundância, caracterizado por verificar as três assinaturas independentemente e considerar válida se pelo menos duas das três forem válidas, compreendendo as etapas de: verificar assinatura ECDSA, verificar assinatura ML-DSA, verificar assinatura SPHINCS+, e validar se pelo menos duas das três são válidas.

**Reivindicação 5:** Sistema conforme reivindicação 1, caracterizado por implementar fallback inteligente para QRS-2 (dupla redundância: ECDSA + ML-DSA) quando SPHINCS+ não estiver disponível, mantendo compatibilidade e segurança.

**Reivindicação 6:** Método de assinatura adaptativa, caracterizado por selecionar o nível de redundância baseado no valor da transação, compreendendo: usar apenas ML-DSA para micro-transações, usar QRS-2 para transações normais, e usar QRS-3 para transações críticas.

**Reivindicação 7:** Sistema conforme reivindicação 1, caracterizado por usar algoritmos aprovados pelo NIST (FIPS 204 para ML-DSA e FIPS 205 para SPHINCS+), garantindo conformidade com padrões internacionais de segurança quântica.

---

## 5. RESUMO

A presente invenção refere-se a um sistema e método de assinatura digital com tripla redundância quântica que combina simultaneamente ECDSA, ML-DSA e SPHINCS+, fornecendo máxima segurança através de redundância e compatibilidade com blockchains existentes, com fallback inteligente para QRS-2 quando SPHINCS+ não estiver disponível e assinatura adaptativa baseada no valor da transação.

---

## 6. DESENHOS

[Inserir diagramas de fluxo, esquemas de chaves e assinaturas aqui]

---

**Documento gerado em:** 03/12/2025  
**Versão:** 1.0  
**Status:** Pronto para depósito no INPI



