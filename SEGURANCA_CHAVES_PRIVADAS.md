# 🔐 Segurança: Chaves Privadas e Senhas

## ⚠️ IMPORTANTE: Antes de Tornar o Repositório Público

### ✅ O que está PROTEGIDO pelo `.gitignore`:

- ✅ `.env` - Variáveis de ambiente
- ✅ `secrets/` - Diretório de segredos
- ✅ `*.key`, `*.pem`, `*.wif` - Chaves privadas
- ✅ `pqc_keys/` - Chaves PQC privadas
- ✅ `VARIAVEIS_RENDER_COPIAR_COLAR.txt` - Arquivo com chaves
- ✅ `*_token*`, `*_password*`, `*_secret*` - Tokens e senhas

### 🔒 Como Funciona:

1. **`.gitignore` protege automaticamente** - Arquivos listados NUNCA são commitados
2. **Variáveis de ambiente** - Use `.env` (não versionado) ou variáveis do sistema
3. **Chaves privadas** - Sempre em `secrets/` ou variáveis de ambiente

## ✅ Verificação ANTES de Tornar Público

### Passo 1: Verificar se há chaves commitadas

```bash
# Verificar se há chaves privadas no histórico
git log --all --full-history --source --pretty=format:"%H" -- "*.key" "*.pem" "*.env" "*secret*" "*password*" "*token*"

# Verificar arquivos que serão commitados
git status

# Verificar se arquivos sensíveis estão ignorados
git check-ignore VARIAVEIS_RENDER_COPIAR_COLAR.txt pqc_keys/
```

### Passo 2: Se encontrar chaves no histórico

**⚠️ ATENÇÃO:** Se você já commitou chaves privadas, elas estão no histórico do Git!

**Solução:**
1. **ROTACIONAR TODAS AS CHAVES** - As chaves antigas estão comprometidas
2. **Remover do histórico** (se necessário):
   ```bash
   # Usar git-filter-repo (recomendado)
   pip install git-filter-repo
   git filter-repo --path VARIAVEIS_RENDER_COPIAR_COLAR.txt --invert-paths
   git filter-repo --path pqc_keys/ --invert-paths
   ```

3. **OU criar novo repositório** limpo (mais seguro)

### Passo 3: Verificar arquivos sensíveis

```bash
# Listar arquivos que contêm palavras-chave sensíveis
grep -r "private_key\|password\|secret\|token" --include="*.py" --include="*.txt" | grep -v ".git" | grep -v "__pycache__"
```

## 🔐 Boas Práticas

### ✅ FAZER:

1. **Usar variáveis de ambiente:**
   ```python
   import os
   private_key = os.getenv('ETH_PRIVATE_KEY')  # ✅ Correto
   ```

2. **Usar arquivo `.env` (não versionado):**
   ```bash
   # .env (não commitado)
   ETH_PRIVATE_KEY=0x...
   POLYGON_PRIVATE_KEY=0x...
   ```

3. **Armazenar em `secrets/` (não versionado):**
   ```bash
   secrets/
     ├── encryption_key.key
     ├── ethereum_key.pem
     └── .gitkeep  # Apenas este arquivo pode ser commitado
   ```

### ❌ NUNCA FAZER:

1. ❌ Hardcode de chaves no código:
   ```python
   private_key = "0xabc123..."  # ❌ NUNCA!
   ```

2. ❌ Commitar arquivos `.env` com valores reais:
   ```bash
   # .env.example ✅ (pode ser commitado)
   ETH_PRIVATE_KEY=your_key_here
   
   # .env ❌ (NUNCA commitar)
   ETH_PRIVATE_KEY=0xabc123...
   ```

3. ❌ Commitar arquivos de chaves:
   ```bash
   # ❌ NUNCA commitar:
   - VARIAVEIS_RENDER_COPIAR_COLAR.txt
   - pqc_keys/*.pem
   - secrets/*.key
   ```

## 🛡️ Checklist ANTES de Tornar Público

- [ ] Verificar `.gitignore` está completo
- [ ] Verificar que `VARIAVEIS_RENDER_COPIAR_COLAR.txt` está ignorado
- [ ] Verificar que `pqc_keys/` está ignorado
- [ ] Verificar que `secrets/` está ignorado
- [ ] Verificar que `.env` está ignorado
- [ ] Verificar histórico do Git por chaves commitadas
- [ ] Se encontrou chaves no histórico: **ROTACIONAR TODAS AS CHAVES**
- [ ] Testar que arquivos sensíveis não aparecem em `git status`
- [ ] Verificar que código usa `os.getenv()` e não hardcode

## 🚨 Se Você Já Commitou Chaves:

1. **ROTACIONAR IMEDIATAMENTE:**
   - Todas as chaves privadas
   - Todos os tokens de API
   - Todas as senhas

2. **Remover do histórico** (se necessário)

3. **Atualizar `.gitignore`** para prevenir futuros commits

4. **Verificar** que não há mais chaves no repositório

## 📋 Arquivos que DEVEM estar no Repositório Público:

✅ **Código-fonte:**
- `core/crypto/quantum_security.py`
- `core/consensus/alz_niev_interoperability.py`
- `core/interoperability/`

✅ **Documentação:**
- `README.md`
- `TESTING.md`
- `VERIFICATION.md`

✅ **Exemplos (sem chaves reais):**
- `examples/`
- `.env.example` (com valores de exemplo)

## 📋 Arquivos que NUNCA devem estar no Repositório:

❌ **Chaves e Segredos:**
- `VARIAVEIS_RENDER_COPIAR_COLAR.txt`
- `pqc_keys/*.pem`
- `secrets/*.key`
- `.env` (com valores reais)
- Qualquer arquivo com chaves privadas

---

**Última atualização:** 2025-12-08
**Status:** ✅ `.gitignore` atualizado para proteger chaves privadas

