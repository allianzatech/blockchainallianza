# 🔄 Sincronização Automática Completa - Privado → Público

## 🎯 Visão Geral

Sincronização automática do repositório **privado** para o **público**, com commit e push automático.

---

## 🚀 Como Usar

### **Método 1: Script Batch (Mais Fácil)**

Execute no repositório privado:

```bash
cd "C:\Users\notebook\Downloads\Allianza Blockchain"
.\sincronizar_automatico.bat
```

O script:
1. ✅ Sincroniza arquivos seguros
2. ✅ Faz commit automático
3. ✅ Tenta fazer push (se token configurado)

---

### **Método 2: Python Direto**

```bash
cd "C:\Users\notebook\Downloads\Allianza Blockchain"
python sincronizar_repositorio_publico.py
```

---

## 🔐 Configurar Token para Push Automático

### **Opção 1: Variável de Ambiente (Recomendado)**

1. **Crie um token** da conta `allianzatoken-png`:
   - https://github.com/settings/tokens
   - Marque `repo` (tudo)
   - Copie o token

2. **Configure variável de ambiente:**

**No Windows (CMD):**
```bash
setx GITHUB_TOKEN_PUBLIC "seu_token_aqui"
```

**No PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN_PUBLIC", "seu_token_aqui", "User")
```

3. **Reinicie o terminal** e execute o script novamente

---

### **Opção 2: Arquivo .env (Alternativa)**

Crie um arquivo `.env` no repositório privado:

```
GITHUB_TOKEN_PUBLIC=seu_token_aqui
```

O script vai ler automaticamente.

---

## 📋 O Que É Sincronizado

### ✅ **Sempre Sincronizado:**
- `examples/` - Demos Python
- `qss-sdk/` - SDK TypeScript
- `docs/` - Documentação
- `tests/` - Testes
- `templates/testnet/` - Templates HTML
- `README.md`, `CHANGELOG.md`, etc.
- `.github/workflows/` - CI/CD

### ❌ **Nunca Sincronizado:**
- Core da blockchain (ALZ-NIEV, QRS-3)
- Chaves privadas e senhas
- `.env` e configurações sensíveis
- Bancos de dados

---

## 🔄 Fluxo Automático

```
Repositório Privado
    ↓
Script sincronizar_repositorio_publico.py
    ↓
Repositório Público (local)
    ↓
Git Commit
    ↓
Git Push (com token)
    ↓
GitHub Público ✅
```

---

## 🎯 Agendar Sincronização Automática

### **Opção 1: Agendador de Tarefas do Windows**

1. Abra **Agendador de Tarefas**
2. **Criar Tarefa Básica**
3. Configure:
   - **Nome:** "Sync Allianza Public Repo"
   - **Gatilho:** Diariamente (ou quando preferir)
   - **Ação:** Iniciar programa
   - **Programa:** `C:\Users\notebook\Downloads\Allianza Blockchain\sincronizar_automatico.bat`

### **Opção 2: GitHub Actions (No Repositório Privado)**

Crie `.github/workflows/sync-public.yml`:

```yaml
name: Sync to Public Repo

on:
  push:
    branches: [ main ]
    paths:
      - 'examples/**'
      - 'docs/**'
      - 'qss-sdk/**'
      - 'tests/**'
      - 'README.md'
      - 'CHANGELOG.md'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Sync to public repo
        run: |
          # Script de sincronização
          python sincronizar_repositorio_publico.py
```

---

## ✅ Verificação

Depois da sincronização:

1. Acesse: https://github.com/allianzatoken-png/allianzablockchain
2. Verifique:
   - ✅ README em inglês
   - ✅ Commits recentes
   - ✅ Arquivos atualizados

---

## 🔗 Arquivos Relacionados

- **Script:** `sincronizar_repositorio_publico.py`
- **Batch:** `sincronizar_automatico.bat`
- **Guia:** `ESTRATEGIA_DOIS_REPOSITORIOS.md`

---

**Agora você pode sincronizar automaticamente do privado para o público!** 🚀

