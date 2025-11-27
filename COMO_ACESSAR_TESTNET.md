# 🌐 COMO ACESSAR A TESTNET NO SEU SITE

## 🚀 URL Base do Seu Site

Seu site está disponível em:
```
https://allianzablockchain.onrender.com
```

---

## 📍 ROTAS DA TESTNET

### 🏠 Dashboard Principal
**URL:**
```
https://allianzablockchain.onrender.com/testnet
```

**O que você verá:**
- Dashboard completo da testnet
- Estatísticas da rede
- Blocos recentes
- Transações recentes
- Status dos sistemas

---

### 🔍 Explorer da Rede
**URL:**
```
https://allianzablockchain.onrender.com/testnet/explorer
```

**O que você verá:**
- Explorer completo da blockchain
- Busca de blocos, transações e endereços
- Histórico de transações
- Estatísticas em tempo real

---

### 💰 Faucet (Solicitar Tokens)
**URL:**
```
https://allianzablockchain.onrender.com/testnet/faucet
```

**O que você pode fazer:**
- Solicitar tokens ALZ para testar
- Ver histórico de solicitações
- Verificar saldo disponível no faucet

---

### 🔐 Verificador QRS-3
**URL:**
```
https://allianzablockchain.onrender.com/testnet/qrs3-verifier
```

**O que você pode fazer:**
- Verificar assinaturas QRS-3 (híbridas)
- Testar validação de assinaturas quânticas
- Verificar integridade de mensagens

---

### 🧪 Testes Profissionais
**URL:**
```
https://allianzablockchain.onrender.com/testnet/tests
```

**O que você pode fazer:**
- Executar testes profissionais
- Ver status de validação
- Ver relatórios de testes

---

## 🔗 LINKS RÁPIDOS

### Página Principal
```
https://allianzablockchain.onrender.com/
```

### Health Check
```
https://allianzablockchain.onrender.com/health
```

### Dashboard Testnet
```
https://allianzablockchain.onrender.com/testnet
```

### Explorer
```
https://allianzablockchain.onrender.com/testnet/explorer
```

### Faucet
```
https://allianzablockchain.onrender.com/testnet/faucet
```

---

## 📊 APIs DISPONÍVEIS

### Estatísticas da Rede
```
GET https://allianzablockchain.onrender.com/testnet/api/network/stats
```

### Lista de Blocos
```
GET https://allianzablockchain.onrender.com/testnet/api/blocks
```

### Lista de Transações
```
GET https://allianzablockchain.onrender.com/testnet/api/transactions
```

### Solicitar Tokens (Faucet)
```
POST https://allianzablockchain.onrender.com/testnet/api/faucet/request
Content-Type: application/json

{
  "address": "seu_endereco_aqui"
}
```

---

## 🎯 COMO ADICIONAR LINK NO SEU SITE

### Opção 1: Link Simples na Página Principal

Adicione um botão ou link na página inicial (`/`) apontando para:
```html
<a href="/testnet">🌐 Acessar Testnet</a>
```

### Opção 2: Menu de Navegação

Crie um menu com links para:
- `/` - Página Inicial
- `/testnet` - Dashboard Testnet
- `/testnet/explorer` - Explorer
- `/testnet/faucet` - Faucet
- `/health` - Health Check

### Opção 3: Cards na Página Principal

Crie cards visuais na página inicial com:
- 🏠 **Dashboard Testnet** → `/testnet`
- 🔍 **Explorer** → `/testnet/explorer`
- 💰 **Faucet** → `/testnet/faucet`
- 🔐 **Verificador QRS-3** → `/testnet/qrs3-verifier`

---

## 📱 EXEMPLO DE HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>Allianza Blockchain</title>
</head>
<body>
    <h1>🌐 Allianza Blockchain</h1>
    
    <div class="menu">
        <a href="/">🏠 Início</a>
        <a href="/testnet">🌐 Testnet</a>
        <a href="/testnet/explorer">🔍 Explorer</a>
        <a href="/testnet/faucet">💰 Faucet</a>
        <a href="/health">❤️ Health</a>
    </div>
    
    <div class="cards">
        <div class="card">
            <h2>🌐 Testnet Dashboard</h2>
            <p>Acesse o dashboard completo da testnet</p>
            <a href="/testnet">Acessar →</a>
        </div>
        
        <div class="card">
            <h2>🔍 Explorer</h2>
            <p>Explore blocos, transações e endereços</p>
            <a href="/testnet/explorer">Explorar →</a>
        </div>
        
        <div class="card">
            <h2>💰 Faucet</h2>
            <p>Solicite tokens ALZ para testar</p>
            <a href="/testnet/faucet">Solicitar →</a>
        </div>
    </div>
</body>
</html>
```

---

## ✅ CHECKLIST

- [ ] Site deployado: `https://allianzablockchain.onrender.com`
- [ ] Testnet acessível: `/testnet`
- [ ] Explorer funcionando: `/testnet/explorer`
- [ ] Faucet disponível: `/testnet/faucet`
- [ ] Health check: `/health`

---

## 🎨 DICA

Você pode criar uma página inicial (`/`) bonita que redirecione ou mostre links para todas essas funcionalidades da testnet!

**Tudo já está funcionando, só acessar as URLs!** 🚀

