# 🌐 INTEGRAR TESTNET NO SEU DOMÍNIO (allianza.tech)

## 📍 SITUAÇÃO ATUAL

- **Site principal:** `allianza.tech` (Hostinger)
- **Testnet:** `allianzablockchain.onrender.com` (Render)

## 🎯 OPÇÕES DE INTEGRAÇÃO

### ✅ OPÇÃO 1: Subdomínio (RECOMENDADO)

Criar `testnet.allianza.tech` apontando para o Render.

**Vantagens:**
- ✅ URL limpa: `testnet.allianza.tech`
- ✅ Fácil de configurar
- ✅ Não interfere no site principal
- ✅ SEO melhor

**Como fazer:**

#### Passo 1: Configurar no Render

1. No Render Dashboard, vá em **Settings → Custom Domains**
2. Clique em **"Add Custom Domain"**
3. Digite: `testnet.allianza.tech`
4. O Render vai mostrar instruções de DNS

#### Passo 2: Configurar DNS na Hostinger

1. Acesse o painel da Hostinger
2. Vá em **Domínios → Gerenciar DNS**
3. Adicione um registro **CNAME**:
   - **Nome/Host:** `testnet`
   - **Tipo:** `CNAME`
   - **Valor/Destino:** `allianzablockchain.onrender.com`
   - **TTL:** `3600` (ou padrão)

#### Passo 3: Aguardar Propagação

- Aguarde 5-30 minutos para propagação DNS
- O Render detectará automaticamente
- SSL será configurado automaticamente

**Resultado:**
- ✅ `testnet.allianza.tech` → Render (testnet completa)
- ✅ `allianza.tech` → Hostinger (site principal)

---

### ✅ OPÇÃO 2: Proxy Reverso na Hostinger

Configurar `/testnet` na Hostinger para redirecionar ao Render.

**Vantagens:**
- ✅ URL: `allianza.tech/testnet`
- ✅ Tudo no mesmo domínio

**Desvantagens:**
- ⚠️ Requer configuração avançada
- ⚠️ Pode ter problemas de CORS
- ⚠️ Mais complexo

**Como fazer (se Hostinger suportar):**

#### Se Hostinger tiver suporte a Proxy Reverso:

1. No painel Hostinger, configure um proxy reverso
2. `/testnet/*` → `https://allianzablockchain.onrender.com/testnet/*`

#### Se não tiver (solução alternativa):

Criar uma página em `allianza.tech/testnet` que redireciona:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=https://allianzablockchain.onrender.com/testnet">
    <title>Allianza Testnet - Redirecionando...</title>
</head>
<body>
    <p>Redirecionando para a testnet...</p>
    <script>
        window.location.href = "https://allianzablockchain.onrender.com/testnet";
    </script>
</body>
</html>
```

---

### ✅ OPÇÃO 3: Iframe (Mais Simples)

Criar uma página em `allianza.tech/testnet` com iframe.

**Vantagens:**
- ✅ Muito simples
- ✅ Funciona imediatamente

**Desvantagens:**
- ⚠️ URL do navegador não muda
- ⚠️ Alguns recursos podem não funcionar (cookies, localStorage)

**Como fazer:**

Crie um arquivo `testnet.html` na Hostinger:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Allianza Testnet</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        iframe {
            width: 100%;
            height: 100vh;
            border: none;
        }
    </style>
</head>
<body>
    <iframe 
        src="https://allianzablockchain.onrender.com/testnet" 
        frameborder="0"
        allowfullscreen>
    </iframe>
</body>
</html>
```

**Resultado:**
- `allianza.tech/testnet.html` mostra a testnet do Render em iframe

---

### ✅ OPÇÃO 4: Link Direto (Mais Simples)

Adicionar link na página principal apontando para o Render.

**Como fazer:**

Na página principal (`allianza.tech`), adicione:

```html
<a href="https://allianzablockchain.onrender.com/testnet" target="_blank">
    🌐 Acessar Testnet
</a>
```

Ou com botão estilizado:

```html
<div class="testnet-link">
    <a href="https://allianzablockchain.onrender.com/testnet" 
       target="_blank" 
       class="btn-testnet">
        🌐 Acessar Testnet Allianza
    </a>
</div>

<style>
.btn-testnet {
    display: inline-block;
    padding: 15px 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
    transition: transform 0.3s;
}
.btn-testnet:hover {
    transform: scale(1.05);
}
</style>
```

---

## 🎯 RECOMENDAÇÃO FINAL

**Use a OPÇÃO 1 (Subdomínio):**

1. ✅ Mais profissional
2. ✅ URL limpa: `testnet.allianza.tech`
3. ✅ Fácil de configurar
4. ✅ Não interfere no site principal
5. ✅ SSL automático do Render

**Passos rápidos:**

1. **No Render:** Settings → Custom Domains → Add `testnet.allianza.tech`
2. **Na Hostinger:** DNS → CNAME `testnet` → `allianzablockchain.onrender.com`
3. **Aguardar:** 5-30 minutos
4. **Pronto!** ✅ `testnet.allianza.tech` funcionando

---

## 📋 CHECKLIST

- [ ] Render configurado com domínio customizado
- [ ] DNS configurado na Hostinger (CNAME)
- [ ] Aguardar propagação DNS
- [ ] Testar `testnet.allianza.tech`
- [ ] Verificar SSL automático

---

## 🔗 LINKS ÚTEIS

- **Render Custom Domains:** https://render.com/docs/custom-domains
- **Hostinger DNS:** Painel → Domínios → Gerenciar DNS

---

**Qual opção você prefere? Recomendo a OPÇÃO 1 (Subdomínio)!** 🚀

