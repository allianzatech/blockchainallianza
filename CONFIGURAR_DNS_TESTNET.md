# 🔧 CONFIGURAR DNS PARA TESTNET (Passo a Passo)

## ✅ SITUAÇÃO ATUAL

Vejo que você já tem um registro **ALIAS** para `testnet`:
```
ALIAS	testnet	0	testnet.allianza.tech.cdn.hstgr.net	300
```

Precisamos **modificar** isso para apontar para o Render.

---

## 🚀 PASSO 1: CONFIGURAR NO RENDER (PRIMEIRO!)

**IMPORTANTE:** Faça isso ANTES de configurar o DNS!

1. Acesse: https://dashboard.render.com
2. Vá até seu serviço **allianzablockchain**
3. Clique em **Settings → Custom Domains**
4. Clique em **"Add Custom Domain"**
5. Digite: `testnet.allianza.tech`
6. Clique em **"Save"**

O Render vai mostrar algo como:
```
Para configurar testnet.allianza.tech, adicione um registro CNAME:
Nome: testnet
Valor: allianzablockchain.onrender.com
```

**Anote essas informações!**

---

## 🔧 PASSO 2: CONFIGURAR DNS NA HOSTINGER

### Opção A: Modificar o registro existente (RECOMENDADO)

1. Na lista de registros DNS, encontre:
   ```
   ALIAS	testnet	0	testnet.allianza.tech.cdn.hstgr.net	300
   ```

2. Clique em **"Editar"** nesse registro

3. **Altere para:**
   - **Tipo:** `CNAME` (mude de ALIAS para CNAME)
   - **Nome:** `testnet` (mantém)
   - **Prioridade:** `0` (mantém ou deixe vazio)
   - **Conteúdo:** `allianzablockchain.onrender.com` (mude para o valor do Render)
   - **TTL:** `300` (ou `3600` se preferir)

4. Clique em **"Salvar"** ou **"Atualizar"**

### Opção B: Adicionar novo registro (se não conseguir editar)

1. Clique em **"Adicionar registro"**

2. Preencha:
   - **Tipo:** `CNAME`
   - **Nome:** `testnet`
   - **Prioridade:** `0` (ou deixe vazio)
   - **Conteúdo:** `allianzablockchain.onrender.com`
   - **TTL:** `300` (ou `3600`)

3. Clique em **"Salvar"**

4. **Depois, remova o registro ALIAS antigo** (se existir)

---

## ⏱️ PASSO 3: AGUARDAR PROPAGAÇÃO

- **Tempo:** 5-30 minutos (às vezes até 1 hora)
- O Render detectará automaticamente quando o DNS estiver configurado
- SSL será configurado automaticamente pelo Render

---

## ✅ PASSO 4: VERIFICAR

Após aguardar a propagação, teste:

1. **No Render:** Verifique se o domínio aparece como "Verified" em Custom Domains
2. **No navegador:** Acesse `https://testnet.allianza.tech`
3. **Deve funcionar!** ✅

---

## 📋 RESUMO DO QUE FAZER

### No Render:
1. Settings → Custom Domains
2. Add Custom Domain
3. Digite: `testnet.allianza.tech`
4. Anote o valor do CNAME (geralmente `allianzablockchain.onrender.com`)

### Na Hostinger:
1. Encontre o registro ALIAS `testnet`
2. Clique em "Editar"
3. Mude:
   - **Tipo:** `CNAME`
   - **Conteúdo:** `allianzablockchain.onrender.com`
4. Salve

### Aguardar:
- 5-30 minutos para propagação DNS
- Render configurará SSL automaticamente

---

## 🎯 RESULTADO FINAL

Após configurar:

- ✅ `allianza.tech` → Site principal (Hostinger)
- ✅ `testnet.allianza.tech` → Testnet completa (Render)
- ✅ SSL automático em ambos
- ✅ Tudo funcionando! 🚀

---

## ⚠️ IMPORTANTE

1. **Configure primeiro no Render** (antes do DNS)
2. **Use CNAME, não ALIAS** (ALIAS é específico da Hostinger)
3. **Aguarde a propagação** antes de testar
4. **Não remova outros registros DNS** (só modifique o `testnet`)

---

**Siga esses passos e em 30 minutos você terá `testnet.allianza.tech` funcionando!** 🎉

