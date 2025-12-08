# 🔧 Correções para Deploy no Render

## ❌ Problemas Identificados nos Logs

### 1. **Módulo `psycopg2` não encontrado**
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Causa:** O `requirements.txt` tem `psycopg[binary]==3.2.11` (psycopg3), mas o código usa `psycopg2`.

**Solução:** Adicionar `psycopg2-binary==2.9.9` ao `requirements.txt`

---

### 2. **Token não está sendo carregado**
```
🔑 SITE_ADMIN_TOKEN: 'allianza_super_admin_2024_CdE25$$$'
```

**Causa:** A variável `VITE_SITE_ADMIN_TOKEN` não está sendo carregada do ambiente.

**Solução:** 
- Adicionar `load_dotenv()` no início do `admin_routes.py`
- Adicionar debug para verificar se o token está sendo carregado

---

## ✅ Correções Aplicadas

### 1. `requirements.txt`
**Adicionado:**
```
psycopg2-binary==2.9.9
```

### 2. `admin_routes.py`
**Adicionado:**
- `load_dotenv()` no início do arquivo
- Debug para verificar se o token está sendo carregado

---

## 📁 Arquivos para Atualizar no GitHub

### 1. `backend/requirements.txt`
**Mudança:**
- Adicionar linha: `psycopg2-binary==2.9.9`

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/requirements.txt

---

### 2. `backend/admin_routes.py`
**Mudanças:**
- Adicionar após linha 2:
  ```python
  # ✅ CARREGAR VARIÁVEIS DE AMBIENTE PRIMEIRO
  from dotenv import load_dotenv
  load_dotenv()
  ```

- Substituir linha 28:
  ```python
  # ✅ CARREGAR TOKEN DA VARIÁVEL DE AMBIENTE (com debug)
  _env_token = os.getenv('VITE_SITE_ADMIN_TOKEN')
  if _env_token:
      SITE_ADMIN_TOKEN = _env_token
      print(f"✅ VITE_SITE_ADMIN_TOKEN carregado: {_env_token[:10]}... (comprimento: {len(_env_token)})")
  else:
      SITE_ADMIN_TOKEN = 'allianza_super_admin_2024_CdE25$$$'
      print(f"⚠️  VITE_SITE_ADMIN_TOKEN não encontrado, usando valor padrão: {SITE_ADMIN_TOKEN[:10]}...")
  ```

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/admin_routes.py

---

### 3. `backend/backend_wallet_integration.py`
**Mudança:**
- Linha 272: Mudar de `/admin` para `/api/site`
- Linha 208: Adicionar OPTIONS para debug-token-info

**URL:** https://github.com/brunosmaach-spec/allianza-wallet-backend/blob/main/backend/backend_wallet_integration.py

---

## 🚀 Ordem de Atualização

1. **Atualizar `requirements.txt`** (adicionar psycopg2-binary)
2. **Atualizar `admin_routes.py`** (adicionar load_dotenv e debug)
3. **Atualizar `backend_wallet_integration.py`** (corrigir prefixo)
4. **Fazer deploy no Render** (Clear build cache & deploy)
5. **Verificar logs** para confirmar que o token está sendo carregado

---

## ✅ Verificação Após Deploy

Nos logs do Render, você deve ver:
```
✅ VITE_SITE_ADMIN_TOKEN carregado: vNFkVqGDZ4... (comprimento: 64)
```

**NÃO deve aparecer:**
```
⚠️  VITE_SITE_ADMIN_TOKEN não encontrado, usando valor padrão
```

---

## 📋 Checklist

- [ ] `requirements.txt` atualizado (psycopg2-binary adicionado)
- [ ] `admin_routes.py` atualizado (load_dotenv e debug adicionados)
- [ ] `backend_wallet_integration.py` atualizado (prefixo corrigido)
- [ ] Deploy feito no Render
- [ ] Logs mostram token sendo carregado corretamente
- [ ] Admin panel funcionando

---

**Última atualização:** 2025-01-XX



