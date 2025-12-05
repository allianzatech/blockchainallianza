# 🔄 Estratégia: Dois Repositórios (Privado + Público)

## 🎯 Visão Geral

Manter **dois repositórios** sincronizados:
- **Privado:** Código completo do projeto (core, chaves, configurações)
- **Público:** Código para validação (SDK, demos, documentação)

---

## 📁 Estrutura dos Repositórios

### 🔒 Repositório Privado
```
allianza-blockchain/ (privado)
├── alz_niev_interoperability.py  ← Core (privado)
├── quantum_security.py           ← Core (privado)
├── allianza_blockchain.py        ← Core (privado)
├── .env                          ← Secrets (privado)
├── sincronizar_repositorio_publico.py  ← Script de sync
└── ... (código completo)
```

### 🌐 Repositório Público
```
allianzablockchain/ (público)
├── examples/                     ← Demos (público)
├── qss-sdk/                     ← SDK (público)
├── docs/                        ← Documentação (público)
├── tests/                       ← Testes (público)
├── templates/                   ← UI (público)
└── ... (apenas código seguro)
```

---

## 🔄 Fluxo de Sincronização

### **Opção 1: Script Manual** (Recomendado para Início)

```bash
# No repositório privado
python sincronizar_repositorio_publico.py
```

**O que faz:**
1. Copia arquivos seguros do privado para público
2. Exclui arquivos sensíveis automaticamente
3. Pergunta se deseja fazer commit e push

### **Opção 2: GitHub Actions** (Automático)

Configure um workflow que:
- Executa a cada 6 horas
- Ou manualmente via `workflow_dispatch`
- Sincroniza automaticamente

**Arquivo:** `.github/workflows/sync-from-private.yml`

### **Opção 3: Git Subtree** (Avançado)

```bash
# Adicionar subtree do público no privado
git subtree push --prefix=public-files origin public main
```

---

## 📋 O Que Sincronizar

### ✅ **Sempre Sincronizar:**
- `examples/` - Demos Python
- `qss-sdk/` - SDK TypeScript
- `docs/` - Documentação
- `tests/` - Testes
- `templates/testnet/` - Templates HTML
- `README.md` - Atualizado
- `CHANGELOG.md` - Histórico
- `CONTRIBUTING.md` - Guia
- `CODE_OF_CONDUCT.md` - Conduta
- `.github/workflows/` - CI/CD

### ❌ **Nunca Sincronizar:**
- `alz_niev_interoperability.py` - Core privado
- `quantum_security.py` - Core privado
- `allianza_blockchain.py` - Core privado
- `.env` - Variáveis de ambiente
- `*_PRIVATE_KEY*` - Chaves privadas
- `*.db` - Bancos de dados
- `node_modules/` - Dependências
- `__pycache__/` - Cache Python

---

## 🛠️ Configuração Inicial

### **1. Configurar Repositório Público**

```bash
cd ../allianzablockchain-public
git remote -v  # Verificar remote
git remote set-url origin https://github.com/allianzatoken-png/allianzablockchain.git
```

### **2. Executar Sincronização**

```bash
cd "C:\Users\notebook\Downloads\Allianza Blockchain"
python sincronizar_repositorio_publico.py
```

### **3. Verificar Mudanças**

```bash
cd ../allianzablockchain-public
git status
git diff
```

---

## 🔐 Segurança

### **Checklist Antes de Sincronizar:**

- [ ] Verificar que não há chaves privadas
- [ ] Verificar que não há senhas
- [ ] Verificar que não há API keys
- [ ] Verificar que não há arquivos `.env`
- [ ] Executar `sincronizar_repositorio_publico.py` (faz verificação automática)

### **Script de Verificação:**

```bash
# Verificar se há arquivos sensíveis
python -c "
import os
from pathlib import Path
sensitive = ['PRIVATE_KEY', 'password', '.env', 'secret']
for f in Path('.').rglob('*'):
    if any(s in str(f) for s in sensitive):
        print(f'⚠️  {f}')
"
```

---

## 📅 Frequência de Sincronização

### **Recomendação:**
- **Diária:** Para mudanças frequentes
- **Semanal:** Para mudanças esporádicas
- **Antes de releases:** Sempre sincronizar

### **Quando Sincronizar:**
- ✅ Adicionar novo demo
- ✅ Atualizar documentação
- ✅ Adicionar novos testes
- ✅ Atualizar SDK
- ✅ Criar nova release

---

## 🚀 Automação

### **GitHub Actions Workflow**

O arquivo `.github/workflows/sync-from-private.yml` pode ser configurado para:

1. **Execução Manual:** Via `workflow_dispatch`
2. **Execução Agendada:** A cada 6 horas
3. **Execução em Push:** Quando arquivos específicos mudam

### **Configurar Secret (se necessário):**

Se precisar acessar o repositório privado:
1. Settings → Secrets → Actions
2. Adicionar `PRIVATE_REPO_TOKEN`
3. Usar no workflow

---

## 📊 Monitoramento

### **Verificar Última Sincronização:**

```bash
cd ../allianzablockchain-public
git log --oneline -5
```

### **Ver Diferenças:**

```bash
# Ver o que mudou desde última sync
git diff HEAD~1
```

---

## 💡 Dicas

1. **Sempre teste localmente** antes de fazer push
2. **Revise as mudanças** antes de commitar
3. **Use commits descritivos** (Conventional Commits)
4. **Mantenha CHANGELOG.md atualizado**
5. **Documente mudanças importantes**

---

## 🔗 Links Úteis

- **Repositório Público:** https://github.com/allianzatoken-png/allianzablockchain
- **Script de Sync:** `sincronizar_repositorio_publico.py`
- **Workflow:** `.github/workflows/sync-from-private.yml`

---

**Última atualização:** 2025-12-05

