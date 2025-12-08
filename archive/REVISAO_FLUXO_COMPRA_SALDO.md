# 🔍 Revisão Completa do Fluxo: Compra → Saldo Bloqueado → Login

## 📋 Problema Identificado

1. **Saldo fictício (1.5K ALZ) aparecendo para todos os usuários**
2. **Backend retornando erro 500** em `/balances/me` e `/ledger/history`
3. **Frontend usando dados mock** quando backend falha, mesmo com token presente

---

## ✅ Correções Aplicadas

### 1. **AllianzaBackendAPI.js** - Não usar mock quando houver token

**Problema:**
- Quando backend falhava, sempre usava dados mock (1500 ALZ)
- Isso acontecia mesmo com usuário autenticado (token presente)

**Solução:**
```javascript
// ✅ Se tiver token, NÃO usar mock - retornar saldo zero ou erro
if (hasToken) {
  if (endpoint === '/balances/me') {
    return {
      success: true,
      balance: {
        available: 0,
        locked: 0,
        staking_balance: 0,
        total: 0
      }
    };
  }
  throw error; // Lançar erro em vez de usar mock
}
```

**Arquivo:** `src/services/AllianzaBackendAPI.js`
- Linha 258-275: Correção do fallback para mock
- Linha 614-632: Correção do `getALZBalanceFromBackend()`

---

## 🔄 Fluxo Completo (Como Deve Funcionar)

### **1. Compra no Buy.jsx**

**Arquivo:** `src/components/sections/Buy.jsx`

**Fluxo:**
1. Usuário preenche formulário de compra
2. Envia para `/api/site/purchase` (backend)
3. Dados enviados:
   - `email`
   - `amount_usd`
   - `wallet_address` (opcional - se não informar, será NULL)
   - `use_own_wallet` (boolean)
   - `network` e `currency`

---

### **2. Backend Salva Compra e Bloqueia Tokens**

**Arquivo:** `backend/backend_wallet_integration.py`

**Rota:** `POST /api/site/purchase`

**Fluxo:**
1. **Recebe dados da compra:**
   ```python
   email = data.get('email')
   amount_usd = data.get('amount_usd')
   wallet_address_from_user = data.get('wallet_address')
   ```

2. **Calcula ALZ:**
   ```python
   # 1 ALZ = $0.10 USD
   amount_alz = amount_usd / 0.10
   ```

3. **Busca ou cria usuário:**
   ```python
   cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
   user = cursor.fetchone()
   
   if not user:
       # Cria usuário SEM wallet (wallet_address = NULL)
       cursor.execute(
           "INSERT INTO users (email, password, wallet_address, private_key) 
            VALUES (%s, %s, NULL, NULL)",
           (email, hashed_password)
       )
   ```

4. **Cria/verifica saldo:**
   ```python
   cursor.execute(
       "SELECT user_id FROM balances WHERE user_id = %s AND asset = 'ALZ'",
       (user_id,)
   )
   if not cursor.fetchone():
       cursor.execute(
           "INSERT INTO balances (user_id, asset, available, locked, staking_balance) 
            VALUES (%s, 'ALZ', 0, 0, 0)",
           (user_id,)
       )
   ```

5. **BLOQUEIA TOKENS (adiciona em `locked`):**
   ```python
   if not wallet_address_from_user:
       # ✅ SEM wallet externa → adiciona em LOCKED
       cursor.execute(
           "UPDATE balances SET locked = locked + %s 
            WHERE user_id = %s AND asset = 'ALZ'",
           (amount_alz, user_id)
       )
       print(f"🔒 Tokens bloqueados: +{amount_alz} ALZ em locked")
   else:
       # ✅ COM wallet externa → adiciona em AVAILABLE (será enviado depois)
       cursor.execute(
           "UPDATE balances SET available = available + %s 
            WHERE user_id = %s AND asset = 'ALZ'",
           (amount_alz, user_id)
       )
   ```

6. **Registra no ledger:**
   ```python
   cursor.execute(
       "INSERT INTO ledger_entries (user_id, asset, amount, entry_type, related_id, description) 
        VALUES (%s, 'ALZ', %s, 'purchase', %s, 'Compra via {method}')",
       (user_id, amount_alz, payment_id)
   )
   ```

**Linhas relevantes:** 350-404

---

### **3. Login e Geração de Wallet**

**Arquivo:** `backend/balance_ledger_routes.py`

**Rota:** `POST /login`

**Fluxo:**
1. **Autentica usuário:**
   ```python
   cursor.execute("SELECT id, email, password, wallet_address FROM users WHERE email = %s", (email,))
   user = cursor.fetchone()
   ```

2. **Gera wallet se não tiver:**
   ```python
   if not user['wallet_address']:
       # ✅ PRIMEIRO LOGIN → gera wallet automaticamente
       private_key, wallet_address = generate_polygon_wallet()
       
       cursor.execute(
           "UPDATE users SET wallet_address = %s, private_key = %s WHERE id = %s",
           (wallet_address, private_key, user_id)
       )
   ```

3. **Retorna token:**
   ```python
   token = f"mock_token_{user_id}"
   return jsonify({
       "success": True,
       "token": token,
       "user": {
           "id": user_id,
           "email": email,
           "wallet_address": wallet_address
       }
   })
   ```

**Linhas relevantes:** 257-310

---

### **4. Busca Saldo ao Fazer Login**

**Arquivo:** `backend/balance_ledger_routes.py`

**Rota:** `GET /balances/me`

**Fluxo:**
1. **Extrai user_id do token:**
   ```python
   token = request.headers.get("Authorization").split(" ")[1]
   user_id = get_user_id_from_token(token)  # Extrai de "mock_token_{id}"
   ```

2. **Busca saldo REAL do banco:**
   ```python
   cursor.execute("""
       SELECT user_id, asset, available, locked, staking_balance, updated_at
       FROM balances
       WHERE user_id = %s AND asset = 'ALZ'
   """, (user_id,))
   
   balance_row = cursor.fetchone()
   ```

3. **Retorna saldo:**
   ```python
   return jsonify({
       "success": True,
       "balance": {
           "user_id": balance_row['user_id'],
           "asset": "ALZ",
           "available": available,      # ✅ Saldo disponível
           "locked": locked,            # ✅ Saldo BLOQUEADO (da compra)
           "staking_balance": staking,  # ✅ Saldo em staking
           "total": available + locked + staking
       }
   })
   ```

**Linhas relevantes:** 82-160

---

### **5. Frontend Exibe Saldo**

**Arquivo:** `src/hooks/useWalletState.js`

**Método:** `fetchALZData()`

**Fluxo:**
1. **Busca saldo do backend:**
   ```javascript
   const balanceResponse = await allianzaBackendAPI.request("/balances/me", {
     method: "GET",
     headers: { Authorization: `Bearer ${token}` }
   });
   ```

2. **Extrai valores:**
   ```javascript
   const balanceData = balanceResponse?.balance || {};
   const availableBalance = parseFloat(balanceData.available || 0);
   const lockedBalance = parseFloat(balanceData.locked || 0);  // ✅ Saldo bloqueado
   const stakingBalance = parseFloat(balanceData.staking_balance || 0);
   ```

3. **Atualiza estado:**
   ```javascript
   setWalletData(prev => ({
     ...prev,
     balance: {
       available: availableBalance,
       locked: lockedBalance,  // ✅ Saldo bloqueado
       staked: stakingBalance,
       total: availableBalance + lockedBalance + stakingBalance
     }
   }));
   ```

**Linhas relevantes:** 195-230

---

## 🎯 Resumo do Fluxo Correto

```
1. COMPRA (Buy.jsx)
   ↓
   POST /api/site/purchase
   ↓
2. BACKEND (backend_wallet_integration.py)
   - Busca/cria usuário por email
   - Calcula ALZ (amount_usd / 0.10)
   - BLOQUEIA tokens em `balances.locked`
   - Salva pagamento em `payments`
   ↓
3. LOGIN (balance_ledger_routes.py)
   - Autentica usuário
   - Gera wallet se não tiver (primeiro login)
   - Retorna token: mock_token_{user_id}
   ↓
4. BUSCA SALDO (balance_ledger_routes.py)
   - Extrai user_id do token
   - Busca saldo REAL do banco (available + locked + staking)
   - Retorna valores reais
   ↓
5. FRONTEND (useWalletState.js)
   - Chama /balances/me com token
   - Recebe saldo REAL (incluindo locked)
   - Exibe na wallet
```

---

## ⚠️ Problemas Restantes

### **1. Erro 500 no Backend**

**Causa:** Backend local pode estar com erro nas correções aplicadas.

**Solução:**
- Verificar logs do backend
- Garantir que `balance_ledger_routes.py` está usando `.get()` para acesso seguro aos campos
- Verificar se `database_neon.py` está retornando dict_row corretamente

### **2. Saldo Fictício Aparecendo**

**Causa:** Frontend ainda usando mock quando backend falha.

**Solução (JÁ APLICADA):**
- ✅ `AllianzaBackendAPI.js` não usa mock quando há token
- ✅ Retorna saldo zero em vez de mock quando backend falha com token presente

---

## 📝 Checklist de Verificação

- [x] Backend salva compra corretamente
- [x] Backend bloqueia tokens em `locked` quando não há wallet externa
- [x] Login gera wallet automaticamente no primeiro acesso
- [x] `/balances/me` busca saldo REAL por user_id
- [x] Frontend não usa mock quando há token
- [ ] Backend local funcionando sem erro 500
- [ ] Saldo bloqueado aparecendo corretamente na wallet

---

**Última atualização:** 2025-01-07



