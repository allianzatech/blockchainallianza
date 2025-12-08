# 📋 Documentação Completa para Registro no INPI
## Allianza Blockchain - Tecnologias e Inovações Únicas

**Data:** 03/12/2025  
**Titular:** [Nome da Empresa/Pessoa]  
**Status:** Preparação para Depósito

---

## 📑 ÍNDICE

1. [Resumo Executivo](#resumo-executivo)
2. [Tecnologias Únicas Identificadas](#tecnologias-únicas-identificadas)
3. [Patentes de Invenção (PI)](#patentes-de-invenção-pi)
4. [Registro de Programa de Computador](#registro-de-programa-de-computador)
5. [Documentos Necessários](#documentos-necessários)
6. [Checklist de Depósito](#checklist-de-depósito)

---

## 🎯 RESUMO EXECUTIVO

A **Allianza Blockchain** desenvolveu tecnologias únicas e inovadoras no campo de interoperabilidade cross-chain e segurança quântica, que representam avanços significativos no estado da arte. Este documento identifica as tecnologias passíveis de proteção via:

- **Patentes de Invenção (PI)**: Para métodos, processos e sistemas inovadores
- **Registro de Programa de Computador**: Para o código fonte e implementações

### Tecnologias Principais

1. **Sistema ALZ-NIEV** - Interoperabilidade sem intermediários
2. **QRS-3** - Sistema de tripla redundância quântica
3. **Quantum Security Service Layer (QSS)** - Serviço de segurança quântica para outras blockchains
4. **Bridge Cross-Chain Real** - Transferências reais entre blockchains heterogêneas

---

## 🔬 TECNOLOGIAS ÚNICAS IDENTIFICADAS

### 1. Sistema ALZ-NIEV (Non-Intermediate Execution Validation)

**Status:** ✅ Implementado e Operacional  
**Unicidade:** Primeiro sistema do mundo com estas características

#### Descrição Técnica

O ALZ-NIEV é um sistema de interoperabilidade cross-chain composto por **5 camadas únicas**:

#### **Camada 1: ELNI (Execution-Level Native Interop)**
- **Inovação:** Execução nativa de funções em blockchains de destino sem transferir ativos
- **Diferencial:** Não usa bridges, tokens sintéticos, lock-and-mint, ou wrapping
- **Arquivo:** `alz_niev_interoperability.py` (classe `ELNI`)

#### **Camada 2: ZKEF (Zero-Knowledge External Functions)**
- **Inovação:** Funções externas provadas via Zero-Knowledge direto
- **Diferencial:** Sem relayers, sem assinaturas externas, zero confiança humana
- **Arquivo:** `alz_niev_interoperability.py` (classe `ZKEF`)

#### **Camada 3: UP-NMT (Universal Proof Normalized Merkle Tunneling)**
- **Inovação:** Túnel universal de provas padronizado, independente de consenso e VM
- **Diferencial:** Pipeline de normalização em Merkle-Proof universal para blockchains heterogêneas
- **Arquivo:** `alz_niev_interoperability.py` (classe `UPNMT`)

#### **Camada 4: MCL (Multi-Consensus Layer)**
- **Inovação:** Suporte a múltiplos tipos de consenso (PoW, PoS, BFT, Tendermint)
- **Diferencial:** Normalização de provas de consenso para diferentes blockchains
- **Arquivo:** `alz_niev_interoperability.py` (classe `MCL`)

#### **Camada 5: AES (Atomic Execution Sync)**
- **Inovação:** Execução atômica multi-chain com rollback automático
- **Diferencial:** Garantia de atomicidade "all-or-nothing" com reversão automática em caso de falha
- **Arquivo:** `alz_niev_interoperability.py` (classe `AES`)

**Evidência de Unicidade:**
- Nenhuma blockchain existente possui estas 5 camadas integradas
- Sistema operacional em testnet com provas de conceito validadas
- Whitepaper técnico completo documentando a arquitetura

---

### 2. QRS-3 (Quantum Redundancy System - Triple)

**Status:** ✅ Implementado e Operacional  
**Unicidade:** Primeiro sistema do mundo com tripla redundância quântica

#### Descrição Técnica

O QRS-3 é um sistema de assinatura digital que combina **3 algoritmos simultaneamente**:

1. **ECDSA (secp256k1)** - Compatibilidade com blockchains existentes
2. **ML-DSA (Dilithium)** - Padrão NIST PQC para assinaturas quântico-seguras
3. **SPHINCS+** - Assinaturas hash-based como redundância adicional

#### Características Únicas

- **Tripla Redundância:** Três assinaturas independentes para cada transação
- **Fallback Inteligente:** Se SPHINCS+ não estiver disponível, usa QRS-2 (ECDSA + ML-DSA)
- **Adaptativo:** Ajusta o nível de redundância baseado na disponibilidade de algoritmos
- **Híbrido Inteligente:** Seleciona algoritmo baseado no valor da transação

**Arquivo:** `quantum_security.py` (método `generate_qrs3_keypair()`)

**Evidência de Unicidade:**
- Nenhuma blockchain existente possui sistema de tripla redundância quântica
- Implementação funcional com testes validados
- Integração com padrões NIST PQC

---

### 3. Quantum Security Service Layer (QSS)

**Status:** ✅ Implementado e Operacional  
**Unicidade:** Primeiro serviço do mundo que oferece segurança quântica para outras blockchains

#### Descrição Técnica

O QSS permite que **qualquer blockchain** (Bitcoin, Ethereum, Polygon, etc.) use segurança quântica da Allianza sem modificar seu código ou consenso.

#### Características Únicas

- **API REST:** Endpoint `/api/qss/generate-proof` para gerar provas quânticas
- **Verificação Pública:** Endpoint `/verify-proof` para verificação independente
- **Ancoragem Cross-Chain:** Suporte para ancorar provas em Bitcoin (OP_RETURN) e EVM (Smart Contracts)
- **Canonicalização RFC8785:** Hash canônico para garantir consistência

**Arquivo:** `qss_api_service.py`

**Evidência de Unicidade:**
- Nenhum serviço existente oferece segurança quântica como serviço para outras blockchains
- SDK JavaScript disponível (`qss-sdk/`)
- Verificador open-source independente (`qss-verifier/`)

---

### 4. Bridge Cross-Chain Real

**Status:** ✅ Implementado e Operacional  
**Unicidade:** Transferências reais entre blockchains completamente diferentes

#### Descrição Técnica

Sistema que permite transferências **reais** (não sintéticas) entre blockchains heterogêneas:

- **Bitcoin ↔ Polygon:** Transferências reais BTC ↔ MATIC
- **Ethereum ↔ Bitcoin:** Transferências reais ETH ↔ BTC
- **Conversão Automática:** Taxas de câmbio em tempo real via CoinGecko API
- **Provas Criptográficas:** ZK Proofs, Merkle Proofs, Consensus Proofs

**Arquivo:** `real_cross_chain_bridge.py`

**Evidência de Unicidade:**
- Transferências reais (não wrapped tokens)
- Suporte para blockchains com modelos diferentes (UTXO vs Account)
- Provas de conceito validadas em testnet

---

## 📜 PATENTES DE INVENÇÃO (PI)

### PI-1: Sistema ALZ-NIEV para Interoperabilidade Cross-Chain

**Título:** "Sistema e Método de Interoperabilidade Cross-Chain sem Intermediários Utilizando Validação de Execução Não-Intermediária (ALZ-NIEV)"

**Reivindicações Principais:**

1. Sistema de interoperabilidade cross-chain composto por 5 camadas:
   - ELNI (Execution-Level Native Interop)
   - ZKEF (Zero-Knowledge External Functions)
   - UP-NMT (Universal Proof Normalized Merkle Tunneling)
   - MCL (Multi-Consensus Layer)
   - AES (Atomic Execution Sync)

2. Método de execução nativa de funções em blockchains de destino sem transferir ativos

3. Método de normalização de provas Merkle para blockchains heterogêneas

4. Método de execução atômica multi-chain com rollback automático

**Documentos Necessários:**
- Descrição detalhada do sistema
- Reivindicações
- Desenhos/Diagramas
- Resumo

---

### PI-2: Sistema QRS-3 de Tripla Redundância Quântica

**Título:** "Sistema e Método de Assinatura Digital com Tripla Redundância Quântica (QRS-3) Combinando ECDSA, ML-DSA e SPHINCS+"

**Reivindicações Principais:**

1. Sistema de assinatura digital que combina simultaneamente:
   - ECDSA (secp256k1)
   - ML-DSA (Dilithium - NIST PQC)
   - SPHINCS+ (Hash-based - NIST PQC)

2. Método de geração de par de chaves com tripla redundância

3. Método de assinatura adaptativa baseada no valor da transação

4. Método de fallback inteligente para QRS-2 quando SPHINCS+ não disponível

**Documentos Necessários:**
- Descrição detalhada do algoritmo
- Reivindicações
- Diagramas de fluxo
- Resumo

---

### PI-3: Quantum Security Service Layer (QSS)

**Título:** "Sistema e Método de Serviço de Segurança Quântica para Blockchains Heterogêneas (QSS)"

**Reivindicações Principais:**

1. Sistema de serviço que permite blockchains sem suporte nativo a PQC usarem segurança quântica

2. Método de geração de provas quânticas verificáveis para transações de outras blockchains

3. Método de ancoragem de provas quânticas em blockchains de destino (OP_RETURN, Smart Contracts)

4. Método de verificação pública e independente de provas quânticas

**Documentos Necessários:**
- Descrição detalhada do serviço
- Reivindicações
- Diagramas de arquitetura
- Resumo

---

## 💻 REGISTRO DE PROGRAMA DE COMPUTADOR

### RPC-1: Sistema ALZ-NIEV

**Nome:** "Sistema ALZ-NIEV - Interoperabilidade Cross-Chain sem Intermediários"

**Arquivos Principais:**
- `alz_niev_interoperability.py` (785+ linhas)
- `real_cross_chain_bridge.py` (integração)
- `test_atomicity_failure.py` (testes)
- `test_write_cross_chain.py` (testes)

**Linguagem:** Python 3.x

**Funcionalidades:**
- 5 camadas de interoperabilidade
- Execução cross-chain
- Provas criptográficas (ZK, Merkle, Consensus)
- Execução atômica com rollback

**Documentos Necessários:**
- Código fonte completo
- Manual do usuário
- Manual técnico
- Formulário de depósito

---

### RPC-2: Sistema de Segurança Quântica

**Nome:** "Sistema de Segurança Quântica Allianza - QRS-3 e PQC"

**Arquivos Principais:**
- `quantum_security.py` (835+ linhas)
- `quantum_security_REAL.py` (implementação real com liboqs-python)
- `quantum_multi_sig_wallet.py` (multi-sig quântico-segura)

**Linguagem:** Python 3.x

**Funcionalidades:**
- QRS-3 (tripla redundância)
- ML-DSA, ML-KEM, SPHINCS+
- Multi-signature quântico-segura
- Integração com padrões NIST PQC

**Documentos Necessários:**
- Código fonte completo
- Manual do usuário
- Manual técnico
- Formulário de depósito

---

### RPC-3: Quantum Security Service (QSS)

**Nome:** "Quantum Security Service Layer - API e SDK"

**Arquivos Principais:**
- `qss_api_service.py` (API REST)
- `qss-sdk/` (SDK JavaScript/TypeScript)
- `qss-verifier/` (verificador open-source)

**Linguagens:** Python 3.x, TypeScript/JavaScript

**Funcionalidades:**
- API REST para geração de provas quânticas
- SDK JavaScript para desenvolvedores
- Verificador independente
- Canonicalização RFC8785

**Documentos Necessários:**
- Código fonte completo
- Manual do desenvolvedor
- Manual técnico
- Formulário de depósito

---

### RPC-4: Bridge Cross-Chain Real

**Nome:** "Sistema de Bridge Cross-Chain Real - Transferências entre Blockchains Heterogêneas"

**Arquivos Principais:**
- `real_cross_chain_bridge.py` (implementação principal)
- Integração com BlockCypher, Blockstream, Web3

**Linguagem:** Python 3.x

**Funcionalidades:**
- Transferências reais Bitcoin ↔ EVM
- Conversão automática de valores
- Provas criptográficas
- Suporte para múltiplas blockchains

**Documentos Necessários:**
- Código fonte completo
- Manual do usuário
- Manual técnico
- Formulário de depósito

---

## 📄 DOCUMENTOS NECESSÁRIOS

### Para Patentes de Invenção (PI)

1. **Petição de Depósito**
   - Formulário do INPI
   - Taxa de depósito

2. **Descrição**
   - Campo técnico
   - Estado da arte
   - Descrição detalhada da invenção
   - Modo de realização
   - Exemplos

3. **Reivindicações**
   - Reivindicação principal
   - Reivindicações dependentes

4. **Desenhos/Diagramas**
   - Diagramas de arquitetura
   - Fluxogramas
   - Esquemas

5. **Resumo**
   - Resumo da invenção (até 200 palavras)
   - Figura representativa

6. **Comprovante de Pagamento**
   - Taxa de depósito

---

### Para Registro de Programa de Computador (RPC)

1. **Formulário de Depósito**
   - Formulário do INPI
   - Taxa de depósito

2. **Código Fonte**
   - Código completo
   - Comentários explicativos
   - Estrutura de diretórios

3. **Manual do Usuário**
   - Instruções de uso
   - Exemplos práticos
   - Screenshots (se aplicável)

4. **Manual Técnico**
   - Arquitetura do sistema
   - Especificações técnicas
   - Diagramas

5. **Comprovante de Pagamento**
   - Taxa de depósito

---

## ✅ CHECKLIST DE DEPÓSITO

### Patentes de Invenção

- [ ] PI-1: Sistema ALZ-NIEV
  - [ ] Descrição completa
  - [ ] Reivindicações
  - [ ] Diagramas
  - [ ] Resumo
  - [ ] Taxa paga

- [ ] PI-2: Sistema QRS-3
  - [ ] Descrição completa
  - [ ] Reivindicações
  - [ ] Diagramas
  - [ ] Resumo
  - [ ] Taxa paga

- [ ] PI-3: Quantum Security Service Layer
  - [ ] Descrição completa
  - [ ] Reivindicações
  - [ ] Diagramas
  - [ ] Resumo
  - [ ] Taxa paga

### Registro de Programa de Computador

- [ ] RPC-1: Sistema ALZ-NIEV
  - [ ] Código fonte completo
  - [ ] Manual do usuário
  - [ ] Manual técnico
  - [ ] Taxa paga

- [ ] RPC-2: Sistema de Segurança Quântica
  - [ ] Código fonte completo
  - [ ] Manual do usuário
  - [ ] Manual técnico
  - [ ] Taxa paga

- [ ] RPC-3: Quantum Security Service
  - [ ] Código fonte completo
  - [ ] Manual do desenvolvedor
  - [ ] Manual técnico
  - [ ] Taxa paga

- [ ] RPC-4: Bridge Cross-Chain Real
  - [ ] Código fonte completo
  - [ ] Manual do usuário
  - [ ] Manual técnico
  - [ ] Taxa paga

---

## 💰 CUSTOS ESTIMADOS (INPI - 2025)

### Patentes de Invenção (PI)
- **Taxa de Depósito:** R$ 70,00 (microempresa) / R$ 140,00 (pequena empresa) / R$ 280,00 (demais)
- **Exame Técnico:** R$ 350,00 (microempresa) / R$ 700,00 (pequena empresa) / R$ 1.400,00 (demais)
- **Anuidades:** Anuais, valores progressivos

### Registro de Programa de Computador (RPC)
- **Taxa de Depósito:** R$ 175,00 (microempresa) / R$ 350,00 (pequena empresa) / R$ 700,00 (demais)
- **Sem anuidades**

**Total Estimado (4 RPCs):**
- Microempresa: R$ 700,00
- Pequena Empresa: R$ 1.400,00
- Demais: R$ 2.800,00

**Total Estimado (3 PIs):**
- Microempresa: R$ 210,00 (depósito) + R$ 1.050,00 (exame) = R$ 1.260,00
- Pequena Empresa: R$ 420,00 (depósito) + R$ 2.100,00 (exame) = R$ 2.520,00
- Demais: R$ 840,00 (depósito) + R$ 4.200,00 (exame) = R$ 5.040,00

---

## 📞 PRÓXIMOS PASSOS

1. **Revisar Documentação**
   - Revisar este documento
   - Confirmar tecnologias a proteger
   - Priorizar depósitos

2. **Preparar Documentos Técnicos**
   - Descrições detalhadas para PIs
   - Código fonte organizado para RPCs
   - Manuais técnicos

3. **Consultar Especialista**
   - Advogado especializado em Propriedade Intelectual
   - Revisão de reivindicações
   - Estratégia de depósito

4. **Depositar no INPI**
   - Acessar portal do INPI
   - Preencher formulários
   - Pagar taxas
   - Acompanhar processo

---

## 📚 REFERÊNCIAS

- **INPI:** https://www.gov.br/inpi/pt-br
- **Portal de Serviços:** https://www.gov.br/inpi/pt-br/servicos
- **Manual de Patentes:** https://www.gov.br/inpi/pt-br/servicos/patentes
- **Manual de Programas de Computador:** https://www.gov.br/inpi/pt-br/servicos/programas-de-computador

---

**🎯 Este documento serve como base para o registro no INPI. Recomenda-se consulta com especialista em Propriedade Intelectual antes do depósito.**



