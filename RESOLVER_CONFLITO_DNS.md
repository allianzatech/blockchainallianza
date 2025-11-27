# 🔧 RESOLVER CONFLITO DNS - testnet

## ❌ PROBLEMA

Erro: "O registro de recurso DNS não é válido ou está em conflito com outro registro de recurso"

## 🔍 CAUSA

Provavelmente você já tem um registro para `testnet` que está conflitando:
- Pode ser um registro **ALIAS** (que você viu antes)
- Pode ser um registro **A** ou **AAAA**
- Pode ser outro **CNAME**

## ✅ SOLUÇÃO

### OPÇÃO 1: Remover o registro antigo primeiro (RECOMENDADO)

1. **Na lista de registros DNS, encontre TODOS os registros com nome `testnet`:**
   - Procure por: `ALIAS testnet`, `CNAME testnet`, `A testnet`, `AAAA testnet`

2. **Remova TODOS os registros antigos:**
   - Clique em **"Remover"** ou **"Editar"** → **"Remover"** em cada um
   - Confirme a remoção

3. **Aguarde 1-2 minutos**

4. **Adicione o novo registro CNAME:**
   - Clique em **"Adicionar registro"**
   - **Tipo:** `CNAME`
   - **Nome:** `testnet`
   - **Destino:** `allianzablockchain.onrender.com`
   - **TTL:** `300` ou `3600`
   - Clique em **"Salvar"**

### OPÇÃO 2: Editar o registro existente

Se você viu um registro **ALIAS testnet** antes:

1. **Encontre o registro ALIAS:**
   ```
   ALIAS	testnet	0	testnet.allianza.tech.cdn.hstgr.net	300
   ```

2. **Clique em "Editar"**

3. **Altere:**
   - **Tipo:** Mude de `ALIAS` para `CNAME`
   - **Nome:** `testnet` (mantém)
   - **Destino:** `allianzablockchain.onrender.com` (mude)
   - **TTL:** `300` (pode manter)

4. **Clique em "Atualizar"**

### OPÇÃO 3: Se ainda não funcionar

Alguns provedores não permitem CNAME se já existe ALIAS. Nesse caso:

1. **Remova TODOS os registros `testnet`**
2. **Aguarde 5 minutos**
3. **Adicione o CNAME novo**

---

## 📋 CHECKLIST

- [ ] Verificar se existe registro ALIAS para `testnet`
- [ ] Verificar se existe registro A para `testnet`
- [ ] Verificar se existe registro AAAA para `testnet`
- [ ] Verificar se existe outro CNAME para `testnet`
- [ ] Remover TODOS os registros antigos de `testnet`
- [ ] Aguardar 1-2 minutos
- [ ] Adicionar novo CNAME: `testnet` → `allianzablockchain.onrender.com`

---

## 🎯 O QUE PROCURAR NA LISTA

Procure por qualquer linha que tenha `testnet` na coluna "Nome":

```
ALIAS	testnet	...
CNAME	testnet	...
A	testnet	...
AAAA	testnet	...
```

**Remova TODOS antes de adicionar o novo!**

---

## ⚠️ IMPORTANTE

- **Não pode ter dois registros com o mesmo nome** (exceto MX que pode ter prioridades diferentes)
- **CNAME não pode coexistir com A, AAAA ou ALIAS** para o mesmo nome
- **Remova o antigo antes de adicionar o novo**

---

**Remova o registro antigo primeiro, depois adicione o novo CNAME!** ✅

