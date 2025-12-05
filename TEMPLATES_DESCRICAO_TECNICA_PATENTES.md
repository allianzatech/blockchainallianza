# 📋 Templates de Descrição Técnica para Patentes
## Allianza Blockchain - INPI

**Data:** 03/12/2025  
**Versão:** 1.0

---

## 📜 PATENTE 1: Sistema ALZ-NIEV

### TÍTULO
"Sistema e Método de Interoperabilidade Cross-Chain sem Intermediários Utilizando Validação de Execução Não-Intermediária (ALZ-NIEV)"

---

### CAMPO TÉCNICO

A presente invenção refere-se ao campo de interoperabilidade entre blockchains, mais especificamente a um sistema e método para execução de funções cross-chain sem necessidade de intermediários, bridges tradicionais, tokens sintéticos ou mecanismos de lock-and-mint.

---

### ESTADO DA TÉCNICA

As soluções atuais de interoperabilidade cross-chain apresentam limitações significativas:

1. **Bridges Tradicionais:** Requerem lock-and-mint ou wrapped tokens, introduzindo riscos de custódia e pontos únicos de falha.

2. **Oráculos:** Dependem de confiança em terceiros para validar informações entre blockchains.

3. **Relayers:** Exigem assinaturas externas e validação humana, comprometendo a descentralização.

4. **Tokens Sintéticos:** Criam ativos não-nativos que não representam transferências reais.

A presente invenção resolve essas limitações através de um sistema inovador de 5 camadas que permite execução nativa de funções entre blockchains heterogêneas sem intermediários.

---

### DESCRIÇÃO DETALHADA DA INVENÇÃO

#### Objetivo da Invenção

O objetivo da presente invenção é fornecer um sistema e método de interoperabilidade cross-chain que:

1. Permita execução nativa de funções em blockchains de destino sem transferir ativos
2. Elimine a necessidade de intermediários, bridges, oráculos ou relayers
3. Garanta atomicidade através de execução síncrona com rollback automático
4. Suporte múltiplos tipos de consenso e modelos de blockchain (UTXO, Account, etc.)
5. Forneça provas criptográficas verificáveis (ZK, Merkle, Consensus)

#### Estrutura do Sistema

O sistema ALZ-NIEV é composto por **5 camadas integradas**:

##### **Camada 1: ELNI (Execution-Level Native Interop)**

A camada ELNI permite execução nativa de funções em blockchains de destino sem transferir ativos ou usar tokens sintéticos.

**Funcionamento:**
1. Recebe requisição de execução cross-chain (chain origem, chain destino, função, parâmetros)
2. Gera prova criptográfica da intenção de execução
3. Executa função na blockchain de destino usando provas verificáveis
4. Retorna resultado com provas de execução

**Características Únicas:**
- Não transfere ativos entre blockchains
- Não cria tokens sintéticos
- Não requer lock-and-mint
- Execução direta usando provas criptográficas

##### **Camada 2: ZKEF (Zero-Knowledge External Functions)**

A camada ZKEF fornece funções externas provadas via Zero-Knowledge, eliminando necessidade de relayers ou assinaturas externas.

**Funcionamento:**
1. Gera prova zk-SNARK ou zk-STARK da função a ser executada
2. Cria circuito de verificação para a função
3. Gera prova de conhecimento zero
4. Valida prova na blockchain de destino antes da execução

**Características Únicas:**
- Zero confiança humana
- Sem relayers externos
- Provas verificáveis matematicamente
- Privacidade preservada

##### **Camada 3: UP-NMT (Universal Proof Normalized Merkle Tunneling)**

A camada UP-NMT normaliza provas Merkle para blockchains heterogêneas, criando um túnel universal de provas.

**Funcionamento:**
1. Recebe Merkle Proof de blockchain origem (formato específico)
2. Normaliza para formato universal independente de consenso e VM
3. Adapta para formato da blockchain destino
4. Valida prova normalizada

**Características Únicas:**
- Suporta blockchains com modelos diferentes (UTXO vs Account)
- Independente de tipo de consenso (PoW, PoS, BFT, etc.)
- Pipeline de normalização automático
- Compatível com qualquer blockchain

##### **Camada 4: MCL (Multi-Consensus Layer)**

A camada MCL suporta múltiplos tipos de consenso e normaliza provas de consenso.

**Funcionamento:**
1. Identifica tipo de consenso da blockchain origem
2. Gera prova de consenso específica (PoW, PoS, BFT, etc.)
3. Normaliza para formato universal
4. Valida na blockchain destino

**Tipos de Consenso Suportados:**
- Proof of Work (Bitcoin)
- Proof of Stake (Ethereum, Polygon)
- Byzantine Fault Tolerant
- Tendermint (Cosmos)
- Parallel Execution (Solana)

##### **Camada 5: AES (Atomic Execution Sync)**

A camada AES garante execução atômica multi-chain com rollback automático em caso de falha.

**Funcionamento:**
1. Recebe lista de execuções a serem realizadas em múltiplas blockchains
2. Executa todas as execuções em paralelo
3. Valida todas as provas antes de confirmar
4. Se qualquer execução falhar, reverte todas as execuções anteriores (rollback)
5. Garante atomicidade "all-or-nothing"

**Características Únicas:**
- Execução atômica garantida
- Rollback automático em caso de falha
- Suporte para múltiplas blockchains simultaneamente
- Sem estado inconsistente

#### Fluxo de Execução

1. **Requisição:** Usuário solicita execução cross-chain
2. **ELNI:** Prepara execução nativa na blockchain destino
3. **ZKEF:** Gera prova Zero-Knowledge da função
4. **UP-NMT:** Normaliza Merkle Proof para formato universal
5. **MCL:** Gera prova de consenso
6. **AES:** Executa atomicamente com validação de todas as provas
7. **Resultado:** Retorna resultado com todas as provas criptográficas

---

### REIVINDICAÇÕES

**Reivindicação 1:** Sistema de interoperabilidade cross-chain caracterizado por ser composto por 5 camadas integradas: ELNI (Execution-Level Native Interop), ZKEF (Zero-Knowledge External Functions), UP-NMT (Universal Proof Normalized Merkle Tunneling), MCL (Multi-Consensus Layer) e AES (Atomic Execution Sync).

**Reivindicação 2:** Método de execução nativa de funções em blockchains de destino sem transferir ativos, caracterizado por usar provas criptográficas verificáveis em vez de bridges ou tokens sintéticos.

**Reivindicação 3:** Método de normalização de provas Merkle para blockchains heterogêneas, caracterizado por criar um formato universal independente de consenso e modelo de blockchain (UTXO vs Account).

**Reivindicação 4:** Método de execução atômica multi-chain com rollback automático, caracterizado por garantir atomicidade "all-or-nothing" através de reversão automática de todas as execuções em caso de falha de qualquer uma.

**Reivindicação 5:** Sistema conforme reivindicação 1, caracterizado por suportar múltiplos tipos de consenso incluindo Proof of Work, Proof of Stake, Byzantine Fault Tolerant, Tendermint e Parallel Execution.

---

### RESUMO

A presente invenção refere-se a um sistema e método de interoperabilidade cross-chain sem intermediários, composto por 5 camadas integradas que permitem execução nativa de funções entre blockchains heterogêneas usando provas criptográficas verificáveis, garantindo atomicidade e eliminando necessidade de bridges, tokens sintéticos ou intermediários.

---

## 📜 PATENTE 2: Sistema QRS-3

### TÍTULO
"Sistema e Método de Assinatura Digital com Tripla Redundância Quântica (QRS-3) Combinando ECDSA, ML-DSA e SPHINCS+"

---

### CAMPO TÉCNICO

A presente invenção refere-se ao campo de criptografia pós-quântica e assinaturas digitais, mais especificamente a um sistema e método de assinatura digital com tripla redundância quântica que combina algoritmos clássicos e pós-quânticos.

---

### ESTADO DA TÉCNICA

As soluções atuais de assinatura digital apresentam limitações:

1. **Algoritmos Clássicos (ECDSA):** Vulneráveis a computadores quânticos futuros
2. **Algoritmos Pós-Quânticos Individuais:** Podem ter vulnerabilidades não descobertas
3. **Falta de Redundância:** Sistemas com apenas um algoritmo são pontos únicos de falha

A presente invenção resolve essas limitações através de um sistema de tripla redundância que combina ECDSA, ML-DSA e SPHINCS+ simultaneamente.

---

### DESCRIÇÃO DETALHADA DA INVENÇÃO

#### Objetivo da Invenção

O objetivo da presente invenção é fornecer um sistema e método de assinatura digital que:

1. Combine simultaneamente 3 algoritmos de assinatura (ECDSA, ML-DSA, SPHINCS+)
2. Forneça redundância tripla para máxima segurança
3. Seja compatível com blockchains existentes (via ECDSA)
4. Seja resistente a computadores quânticos (via ML-DSA e SPHINCS+)
5. Implemente fallback inteligente quando um algoritmo não estiver disponível

#### Estrutura do Sistema

O sistema QRS-3 gera **3 pares de chaves simultaneamente**:

1. **Chave ECDSA (secp256k1):** Compatibilidade com blockchains existentes
2. **Chave ML-DSA (Dilithium):** Padrão NIST PQC para assinaturas quântico-seguras
3. **Chave SPHINCS+:** Assinaturas hash-based como redundância adicional

#### Processo de Assinatura

1. **Geração de Chaves:**
   - Gera par de chaves ECDSA (secp256k1)
   - Gera par de chaves ML-DSA (Dilithium - NIST FIPS 204)
   - Gera par de chaves SPHINCS+ (NIST FIPS 205)

2. **Assinatura:**
   - Assina mensagem com ECDSA
   - Assina mensagem com ML-DSA
   - Assina mensagem com SPHINCS+ (se disponível)
   - Combina as 3 assinaturas em um único objeto

3. **Verificação:**
   - Verifica assinatura ECDSA
   - Verifica assinatura ML-DSA
   - Verifica assinatura SPHINCS+ (se presente)
   - Considera válida se pelo menos 2 das 3 assinaturas forem válidas

#### Fallback Inteligente

Se SPHINCS+ não estiver disponível, o sistema automaticamente usa **QRS-2** (dupla redundância: ECDSA + ML-DSA).

#### Assinatura Adaptativa

O sistema seleciona o algoritmo baseado no valor da transação:
- **Micro-transações:** Apenas ML-DSA (mais rápido)
- **Transações normais:** QRS-2 (ECDSA + ML-DSA)
- **Transações críticas:** QRS-3 (ECDSA + ML-DSA + SPHINCS+)

---

### REIVINDICAÇÕES

**Reivindicação 1:** Sistema de assinatura digital caracterizado por combinar simultaneamente três algoritmos de assinatura: ECDSA (secp256k1), ML-DSA (Dilithium - NIST FIPS 204) e SPHINCS+ (NIST FIPS 205).

**Reivindicação 2:** Método de geração de par de chaves com tripla redundância, caracterizado por gerar simultaneamente chaves ECDSA, ML-DSA e SPHINCS+ para o mesmo usuário.

**Reivindicação 3:** Método de assinatura digital com tripla redundância, caracterizado por assinar a mesma mensagem com três algoritmos diferentes e combinar as assinaturas em um único objeto.

**Reivindicação 4:** Método de verificação de assinatura com tripla redundância, caracterizado por verificar as três assinaturas e considerar válida se pelo menos duas das três forem válidas.

**Reivindicação 5:** Sistema conforme reivindicação 1, caracterizado por implementar fallback inteligente para QRS-2 (dupla redundância) quando SPHINCS+ não estiver disponível.

**Reivindicação 6:** Método de assinatura adaptativa, caracterizado por selecionar o nível de redundância (ML-DSA apenas, QRS-2 ou QRS-3) baseado no valor da transação.

---

### RESUMO

A presente invenção refere-se a um sistema e método de assinatura digital com tripla redundância quântica que combina simultaneamente ECDSA, ML-DSA e SPHINCS+, fornecendo máxima segurança através de redundância e compatibilidade com blockchains existentes, com fallback inteligente e assinatura adaptativa baseada no valor da transação.

---

## 📜 PATENTE 3: Quantum Security Service Layer (QSS)

### TÍTULO
"Sistema e Método de Serviço de Segurança Quântica para Blockchains Heterogêneas (QSS)"

---

### CAMPO TÉCNICO

A presente invenção refere-se ao campo de segurança quântica e serviços de blockchain, mais especificamente a um sistema e método que permite blockchains sem suporte nativo a criptografia pós-quântica usarem segurança quântica através de um serviço externo verificável.

---

### ESTADO DA TÉCNICA

As blockchains existentes (Bitcoin, Ethereum, etc.) não possuem suporte nativo a criptografia pós-quântica (PQC), tornando-as vulneráveis a computadores quânticos futuros. Não existe atualmente um serviço que permita essas blockchains usarem segurança quântica sem modificar seu código ou consenso.

A presente invenção resolve essa limitação através de um serviço que gera provas quânticas verificáveis para transações de outras blockchains, permitindo ancoragem dessas provas na blockchain original.

---

### DESCRIÇÃO DETALHADA DA INVENÇÃO

#### Objetivo da Invenção

O objetivo da presente invenção é fornecer um sistema e método que:

1. Permita blockchains sem suporte nativo a PQC usarem segurança quântica
2. Gere provas quânticas verificáveis para transações de outras blockchains
3. Permita ancoragem de provas quânticas em blockchains de destino
4. Forneça verificação pública e independente de provas quânticas
5. Seja compatível com qualquer blockchain sem modificar seu código

#### Estrutura do Sistema

O sistema QSS é composto por:

1. **API REST:** Endpoint para receber requisições de geração de provas
2. **Gerador de Provas Quânticas:** Sistema que gera provas usando ML-DSA, Merkle Proofs e Consensus Proofs
3. **Canonicalizador RFC8785:** Sistema que gera hash canônico da prova
4. **Verificador Público:** Endpoint para verificação independente
5. **Sistema de Ancoragem:** Instruções para ancorar provas em diferentes blockchains

#### Processo de Geração de Prova

1. **Recebe Requisição:**
   - Hash da transação da blockchain origem
   - Metadados opcionais (block height, timestamp, etc.)

2. **Gera Prova Quântica:**
   - Assina com ML-DSA (Dilithium - NIST PQC)
   - Gera Merkle Proof da transação
   - Gera Consensus Proof da blockchain origem
   - Canonicaliza JSON usando RFC8785
   - Calcula proof_hash (SHA256 do JSON canônico)

3. **Retorna Prova:**
   - JSON com todas as provas
   - Public key URI para verificação
   - Instruções de ancoragem
   - URL de verificação pública

#### Processo de Ancoragem

**Bitcoin (via OP_RETURN):**
- Inclui proof_hash no OP_RETURN da próxima transação Bitcoin
- Cria link imutável entre transação Bitcoin e prova quântica

**Ethereum/Polygon (via Smart Contract):**
- Chama função `anchorProof()` no contrato QuantumSecurityAdapter
- Armazena proof_hash, assinatura quântica e merkle_root on-chain

#### Processo de Verificação

1. **Recebe Prova:** JSON com todas as provas
2. **Canonicaliza:** Gera JSON canônico usando RFC8785
3. **Valida Hash:** Verifica se proof_hash corresponde ao hash do JSON canônico
4. **Valida Assinatura:** Verifica assinatura ML-DSA usando public key
5. **Valida Merkle:** Verifica Merkle Proof
6. **Valida Consenso:** Verifica Consensus Proof
7. **Retorna Resultado:** Válido ou inválido com detalhes

---

### REIVINDICAÇÕES

**Reivindicação 1:** Sistema de serviço de segurança quântica caracterizado por permitir blockchains sem suporte nativo a criptografia pós-quântica usarem segurança quântica através de provas quânticas verificáveis geradas externamente.

**Reivindicação 2:** Método de geração de provas quânticas para transações de outras blockchains, caracterizado por assinar hash da transação com ML-DSA (Dilithium - NIST PQC), gerar Merkle Proof e Consensus Proof, e canonicalizar usando RFC8785.

**Reivindicação 3:** Método de ancoragem de provas quânticas em blockchains de destino, caracterizado por incluir proof_hash no OP_RETURN (Bitcoin) ou em Smart Contract (EVM), criando link imutável entre transação original e prova quântica.

**Reivindicação 4:** Método de verificação pública e independente de provas quânticas, caracterizado por verificar proof_hash, assinatura ML-DSA, Merkle Proof e Consensus Proof sem necessidade de confiar no serviço gerador.

**Reivindicação 5:** Sistema conforme reivindicação 1, caracterizado por fornecer SDK JavaScript/TypeScript para desenvolvedores integrarem o serviço em suas aplicações.

---

### RESUMO

A presente invenção refere-se a um sistema e método de serviço de segurança quântica que permite blockchains sem suporte nativo a criptografia pós-quântica usarem segurança quântica através de provas quânticas verificáveis geradas externamente, com ancoragem em blockchains de destino e verificação pública independente.

---

## 📝 NOTAS IMPORTANTES

1. **Consultar Especialista:** Estes templates devem ser revisados por advogado especializado em Propriedade Intelectual antes do depósito.

2. **Reivindicações:** As reivindicações devem ser cuidadosamente redigidas para maximizar o escopo de proteção.

3. **Prioridade:** Considerar depósito de pedido de patente com prioridade internacional (PCT) se houver interesse em proteção internacional.

4. **Novidade:** Verificar se as tecnologias não foram divulgadas publicamente antes do depósito (exceto em testnet, que geralmente não invalida novidade).

5. **Atividade Inventiva:** Destacar os aspectos inovadores e não óbvios das soluções.

---

**🎯 Estes templates servem como base para redação das descrições técnicas. Recomenda-se consulta com especialista antes do depósito no INPI.**



