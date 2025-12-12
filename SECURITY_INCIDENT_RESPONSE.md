# 🚨 SECURITY INCIDENT RESPONSE - Chaves Privadas Expostas

## 📋 Resumo do Incidente

**Data:** 12 de dezembro de 2025  
**Tipo:** Segredo genérico de alta entropia exposto no GitHub  
**Detectado por:** GitGuardian  
**Severidade:** ALTA

## 🔍 Chaves Expostas Identificadas

As seguintes chaves privadas Bitcoin foram encontradas hardcoded em arquivos commitados:

1. **Chave WIF Testnet:** `cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN`
   - Endereço: `mft38vhDpoF4qEAFChbfxZ5UrUemSViHHh`
   - Arquivos afetados:
     - `check_render_keys.py` (removido)
     - `verify_final_setup.py` (removido)
     - `verify_new_address.py` (removido)
     - `real_cross_chain_bridge.py` (exemplos apenas - marcados)

2. **Chave WIF Testnet:** `cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ`
   - Arquivos afetados:
     - `check_render_keys.py` (removido)

## ✅ Ações Imediatas Realizadas

1. ✅ Removidas chaves hardcoded de todos os arquivos de teste
2. ✅ Substituídas por leitura de variáveis de ambiente
3. ✅ Adicionados arquivos de teste ao `.gitignore`
4. ✅ Marcados exemplos em mensagens de erro como "EXAMPLE"
5. ✅ Commit de segurança realizado

## 🚨 Ações Necessárias (URGENTE)

### 1. Rotacionar Chaves Expostas

**IMPORTANTE:** As chaves expostas ainda estão no histórico do Git. Mesmo que tenham sido removidas dos arquivos atuais, elas podem ser recuperadas do histórico.

#### Para Bitcoin Testnet:

1. **Gerar nova chave privada:**
   ```bash
   python generate_bitcoin_address.py
   ```

2. **Atualizar no Render:**
   - Dashboard → Environment Variables
   - Atualizar `BITCOIN_PRIVATE_KEY` com a nova chave
   - Atualizar `BITCOIN_TESTNET_ADDRESS` com o novo endereço

3. **Transferir fundos:**
   - Se houver fundos nas chaves antigas, transferir para as novas
   - Usar um faucet Bitcoin testnet para a nova chave

### 2. Limpar Histórico do Git (Opcional mas Recomendado)

**⚠️ ATENÇÃO:** Isso requer force push e pode afetar colaboradores.

```bash
# Usar BFG Repo-Cleaner (recomendado)
# ou git filter-branch

# Exemplo com git filter-branch:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch check_render_keys.py verify_final_setup.py verify_new_address.py" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (CUIDADO!)
git push origin --force --all
```

**Nota:** Force push pode quebrar forks e clones. Considere criar um novo repositório se necessário.

### 3. Verificar Outros Segredos

Execute varredura completa:

```bash
# Usar GitGuardian CLI
ggshield scan repo .

# Ou usar truffleHog
trufflehog git file://. --json
```

## 📝 Prevenção Futura

### 1. Pre-commit Hooks

Adicionar hook para detectar segredos antes de commit:

```bash
# Instalar detect-secrets
pip install detect-secrets

# Criar baseline
detect-secrets scan > .secrets.baseline

# Adicionar ao pre-commit
pre-commit install
```

### 2. GitGuardian Integration

- Configurar GitGuardian para monitorar o repositório
- Adicionar webhook para alertas em tempo real
- Configurar políticas de bloqueio de commits com segredos

### 3. Code Review

- Sempre revisar commits antes de merge
- Verificar se há chaves, tokens ou senhas hardcoded
- Usar ferramentas automatizadas de detecção

## 🔐 Boas Práticas

1. **NUNCA** commitar chaves privadas, tokens ou senhas
2. **SEMPRE** usar variáveis de ambiente para segredos
3. **SEMPRE** adicionar arquivos com segredos ao `.gitignore`
4. **SEMPRE** rotacionar chaves após exposição
5. **SEMPRE** usar ferramentas de detecção de segredos

## 📞 Contato

Em caso de dúvidas sobre este incidente, entre em contato com a equipe de segurança.

---

**Última atualização:** 12 de dezembro de 2025

