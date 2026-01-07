# ✅ Checklist Pré-Push - Repositório Público

Use este checklist antes de fazer push para o repositório público.

## 🔍 Verificação Rápida

### 1. Executar Script de Verificação

```bash
python scripts/verify_public_repo.py
```

O script verifica:
- ✅ Arquivos comerciais não estão incluídos
- ✅ Arquivos de produção não estão incluídos
- ✅ Arquivos testnet não estão incluídos
- ✅ .gitignore está atualizado

### 2. Verificar Git Status

```bash
git status
```

Verificar se aparecem:
- ❌ `commercial_repo/`
- ❌ `deploy/`
- ❌ Arquivos `testnet_*.py`
- ❌ Arquivos de deploy (`wsgi.py`, `Procfile`, etc.)
- ❌ Arquivos `.db`, `.log`
- ❌ Arquivos de secrets

### 3. Verificar .gitignore

```bash
cat .gitignore
```

Confirmar que:
- ✅ `commercial_repo/` está listado
- ✅ `deploy/` está listado
- ✅ `testnet_*.py` está listado
- ✅ Arquivos de produção estão listados

---

## 📋 Checklist Manual

### Diretórios Comerciais
- [ ] `commercial_repo/` **NÃO** está no commit
- [ ] `deploy/` **NÃO** está no commit

### Arquivos Comerciais
- [ ] `real_cross_chain_bridge.py` **NÃO** está no commit
- [ ] `allianza_bridge_config.py` **NÃO** está no commit
- [ ] `db_manager.py` **NÃO** está no commit
- [ ] `bridge_free_interop.py` (raiz) **NÃO** está no commit

### Arquivos Testnet
- [ ] Nenhum arquivo `testnet_*.py` está no commit

### Arquivos de Deploy
- [ ] `wsgi.py` **NÃO** está no commit
- [ ] `wsgi_optimized.py` **NÃO** está no commit
- [ ] `Procfile` **NÃO** está no commit
- [ ] `render.yaml` **NÃO** está no commit
- [ ] `Dockerfile` **NÃO** está no commit
- [ ] `docker-compose.yml` **NÃO** está no commit

### Arquivos de Dados
- [ ] Nenhum arquivo `.db` está no commit
- [ ] Nenhum arquivo `.log` está no commit
- [ ] `secrets/` **NÃO** está no commit
- [ ] `.env` **NÃO** está no commit

### Documentação
- [ ] `README.md` está atualizado
- [ ] `LICENSE` está presente
- [ ] Documentação está completa

---

## ✅ O que DEVE estar no Commit

### Código do Protocolo
- ✅ `core/` - Protocolo core
- ✅ `contracts/` - Contratos (open core)
- ✅ Arquivos principais do protocolo

### Documentação
- ✅ `README.md`
- ✅ `LICENSE`
- ✅ `CONTRIBUTING.md`
- ✅ `SECURITY.md`
- ✅ `ROADMAP.md`
- ✅ `docs/`
- ✅ Todos os arquivos `.md` de documentação

### Provas
- ✅ `proofs/` - Provas verificáveis

### Exemplos
- ✅ `examples/` (se existir)
- ✅ `cli/` - Ferramentas CLI
- ✅ `api/` - Exemplos de API

### Configuração
- ✅ `requirements.txt`
- ✅ `.gitignore`

---

## 🚨 Se Encontrar Problemas

### Arquivo Comercial no Commit

1. **Remover do Stage**
   ```bash
   git reset HEAD arquivo_comercial.py
   ```

2. **Adicionar ao .gitignore**
   ```bash
   echo "arquivo_comercial.py" >> .gitignore
   ```

3. **Commit .gitignore**
   ```bash
   git add .gitignore
   git commit -m "Update: adicionar arquivo comercial ao .gitignore"
   ```

### Diretório Comercial no Commit

1. **Remover do Stage**
   ```bash
   git reset HEAD commercial_repo/
   ```

2. **Verificar .gitignore**
   - Confirmar que `commercial_repo/` está listado

3. **Se necessário, atualizar .gitignore**
   ```bash
   echo "commercial_repo/" >> .gitignore
   git add .gitignore
   git commit -m "Update: adicionar diretório comercial ao .gitignore"
   ```

---

## 📝 Comandos Úteis

### Ver o que está staged
```bash
git diff --cached --name-only
```

### Ver o que será commitado
```bash
git status --short
```

### Remover arquivo do stage
```bash
git reset HEAD arquivo.py
```

### Verificar se arquivo está no .gitignore
```bash
git check-ignore -v arquivo.py
```

---

## ✅ Checklist Final

Antes de fazer push:

- [ ] Script de verificação passou (`python scripts/verify_public_repo.py`)
- [ ] Git status não mostra arquivos comerciais
- [ ] .gitignore está atualizado
- [ ] Checklist manual completo
- [ ] Documentação está atualizada
- [ ] README.md está correto

---

## 🔄 Após Push

1. **Verificar no GitHub**
   - Confirmar que arquivos comerciais não aparecem
   - Verificar que estrutura está correta

2. **Testar Links**
   - Verificar links no README
   - Testar links de documentação

3. **Notificar Equipe**
   - Informar sobre atualizações importantes

---

**Use este checklist toda vez antes de fazer push para o repositório público!**

