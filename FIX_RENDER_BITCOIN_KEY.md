# 🔧 CORREÇÃO URGENTE: Chave Bitcoin no Render

## ❌ PROBLEMA IDENTIFICADO

No Render Dashboard você tem:
- `BITCOIN_PRIVATE_KEY` = `cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN` ❌ **ERRADA**
- `BITCOIN_TESTNET_ADDRESS` = `tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q` ✅ **CORRETO**

**A chave privada NÃO gera o endereço esperado!**

### Verificação:
- Chave `cPmkhTUA6E9Kwt7grHcf5b1F67k1iucDXDgqimnMDbJd4W5aE3MN` gera: `tb1qq07vwy340hwehxycr8zg33s3c4lmfjhz5mz5ef` (sem saldo)
- Endereço esperado: `tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q` (com 0.00313350 BTC)

## ✅ SOLUÇÃO

### Passo 1: Atualizar BITCOIN_PRIVATE_KEY no Render

1. Acesse **Render Dashboard** → Seu serviço → **Environment**
2. Encontre a variável `BITCOIN_PRIVATE_KEY`
3. **ALTERE** o valor para:
   ```
   cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ
   ```
4. Clique em **Save Changes**

### Passo 2: Verificar BITCOIN_TESTNET_ADDRESS

A variável `BITCOIN_TESTNET_ADDRESS` já está correta:
```
tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q
```
**NÃO PRECISA ALTERAR**

### Passo 3: Reiniciar o Serviço

Após salvar as alterações:
1. Vá em **Manual Deploy** → **Deploy latest commit**
2. OU aguarde o deploy automático (pode levar alguns minutos)

## ✅ VERIFICAÇÃO

Após atualizar, a chave `cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ` deve gerar:
- Endereço: `tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q` ✅
- Saldo: 0.00313350 BTC ✅

## 📋 RESUMO DAS VARIÁVEIS CORRETAS

```
BITCOIN_PRIVATE_KEY = cSamqcRz79BCXe5LWhqVSMhKo1bkxZA3EE6PTpy8hkYVVmofUXfJ
BITCOIN_TESTNET_ADDRESS = tb1q92s4pc5hxh0gmew4d026y7n5rtwc4astv3dn6q
```

## ⚠️ IMPORTANTE

- A chave privada deve ser uma chave **WIF** (começa com `c` para testnet)
- A chave deve gerar o endereço configurado em `BITCOIN_TESTNET_ADDRESS`
- Nunca compartilhe ou commite chaves privadas no código!

