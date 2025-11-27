# 🔧 CORRIGIR ERRO: "Private key não configurada para polygon"

## 🚨 PROBLEMA

O erro indica que `POLYGON_PRIVATE_KEY` não está sendo encontrada ou está **vazia** no Render.

---

## ✅ SOLUÇÃO PASSO A PASSO

### 1. Verificar se a variável está configurada

No Render Dashboard:
1. Vá em **Settings → Environment**
2. Procure por `POLYGON_PRIVATE_KEY`
3. **Clique para editar** e verifique o valor

### 2. Se a variável estiver vazia ou não existir:

**Adicione ou edite a variável:**

```
KEY: POLYGON_PRIVATE_KEY
VALUE: a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
```

**⚠️ IMPORTANTE:**
- **NÃO** adicione o prefixo `0x` (o código adiciona automaticamente)
- O valor deve ter **64 caracteres** (32 bytes em hex)
- **NÃO** deixe espaços antes ou depois

### 3. Verificar outras variáveis relacionadas

Certifique-se de que estas também estão configuradas:

```
POLYGON_PRIVATE_KEY=a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
REAL_POLY_PRIVATE_KEY=0xa2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
POLYGON_MASTER_PRIVATE_KEY=a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
```

### 4. Após adicionar/editar:

1. **Clique em "Save Changes"**
2. **Aguarde o redeploy automático** (ou clique em "Manual Deploy")
3. **Teste novamente** a transferência

---

## 🔍 VERIFICAÇÃO RÁPIDA

### No Render Dashboard:

1. **Settings → Environment**
2. **Procure por:** `POLYGON_PRIVATE_KEY`
3. **Verifique:**
   - ✅ Existe?
   - ✅ Tem valor?
   - ✅ Não está vazio?
   - ✅ Tem 64 caracteres (sem contar espaços)?

### Se estiver tudo OK mas ainda der erro:

1. **Verifique os logs** do Render
2. **Procure por:** "POLYGON_PRIVATE_KEY" nos logs
3. **Veja o debug** na resposta do erro (agora mostra quantos caracteres tem)

---

## 📋 VALORES CORRETOS (do seu .env)

Use estes valores exatos:

```
POLYGON_PRIVATE_KEY=a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
REAL_POLY_PRIVATE_KEY=0xa2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
POLYGON_MASTER_PRIVATE_KEY=a2b050a9ff78efabced4fd16bf5e51d204fd9a1bdab4b56418a5148fe70b4c28
```

**Nota:** `REAL_POLY_PRIVATE_KEY` pode ter `0x`, mas `POLYGON_PRIVATE_KEY` e `POLYGON_MASTER_PRIVATE_KEY` **NÃO devem ter**.

---

## 🎯 TESTE RÁPIDO

Após configurar, teste:

1. Acesse: `https://testnet.allianza.tech/testnet/interoperability`
2. Tente uma transferência: **Polygon → Bitcoin**
3. Se ainda der erro, **veja o debug** na resposta JSON

O novo código agora mostra:
- Quantos caracteres cada variável tem
- Quais variáveis foram testadas
- Se está vazia ou não configurada

---

## ✅ PRONTO!

Após seguir estes passos, a transferência deve funcionar! 🚀

