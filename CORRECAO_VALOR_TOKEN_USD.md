# 💰 Correção: Valor do Token Atualizado para USD

## ✅ Mudança Implementada

**Valor do token mudou:**
- ❌ **Antes**: 1 ALZ = R$ 0,10 (Reais)
- ✅ **Agora**: 1 ALZ = $0,10 USD (Dólares)

---

## 🔧 Correções Aplicadas

### 1. **Backend - Constantes e Funções**

**`admin_routes.py`:**
```python
# ✅ ATUALIZADO
ALZ_PRICE_USD = 0.10  # 1 ALZ = $0,10 USD
ALZ_PRICE_BRL = 0.10  # Mantido para compatibilidade

def calculate_alz_from_usd(amount_usd):
    """Calcula ALZ a partir de USD (método preferido)"""
    return float(amount_usd) / ALZ_PRICE_USD  # 1 ALZ = $0,10 USD

def calculate_alz_from_brl(amount_brl):
    """Calcula ALZ a partir de BRL (compatibilidade)"""
    usd_to_brl_rate = 5.50
    amount_usd = float(amount_brl) / usd_to_brl_rate
    return amount_usd / ALZ_PRICE_USD
```

**`backend_wallet_integration.py`:**
```python
# ✅ CORRIGIDO
# 1 ALZ = $0,10 USD
amount_usd = amount_alz * 0.10  # 1 ALZ = $0,10 USD
usd_to_brl_rate = 5.50
amount_brl = amount_usd * usd_to_brl_rate  # Para registro no banco
```

### 2. **Frontend - Buy.jsx**

**Cálculo Correto:**
```javascript
// ✅ CORRIGIDO: Usuário digita em USD
const priceAmountUSD = parseFloat(amount); // $5 USD
const alzAmount = priceAmountUSD / 0.10; // $5 / 0.10 = 50 ALZ

// Para NowPayments
const payload = {
    price_amount: priceAmountUSD, // ✅ CORRETO: $5 USD
    price_currency: 'usd',
    pay_currency: selectedNetwork
};
```

**Função de Cálculo:**
```javascript
const calculateDisplayAmounts = () => {
    const usdAmount = parseFloat(amount);
    const alzAmount = usdAmount / 0.10; // 1 ALZ = $0,10 USD
    const brlAmount = usdAmount * usdToBrlRate; // Para exibição
    return { brlAmount, alzAmount, usdAmount };
};
```

### 3. **Frontend - AdminDashboard.jsx**

**Cálculo Atualizado:**
```javascript
const calculateAlzAmount = (payment) => {
    // Verificar metadata primeiro (mais confiável)
    if (payment.metadata?.alz_amount) {
        return parseFloat(payment.metadata.alz_amount);
    }
    
    // Se amount está em BRL, converter: BRL → USD → ALZ
    const usd_to_brl_rate = 5.50;
    const amount_usd = amount / usd_to_brl_rate;
    return amount_usd / 0.10; // 1 ALZ = $0,10 USD
};

const calculateUSDAmount = (payment) => {
    const alzAmount = calculateAlzAmount(payment);
    return alzAmount * 0.10; // 1 ALZ = $0,10 USD
};

const calculateBRLAmount = (payment) => {
    const usdAmount = calculateUSDAmount(payment);
    return usdAmount * 5.50; // USD → BRL
};
```

---

## 📊 Exemplo de Conversão

### Antes (R$ 0,10):
- Usuário digita: R$ 5,00
- ALZ = R$ 5,00 / 0,10 = **50 ALZ**

### Agora ($0,10 USD):
- Usuário digita: $5,00 USD
- ALZ = $5,00 / 0,10 = **50 ALZ**
- BRL equivalente = $5,00 × 5,50 = R$ 27,50 (apenas para exibição)

---

## 🔧 Correções Adicionais

### 1. **Wallet Address** ✅
- Backend agora recebe e salva `wallet_address` do request
- Campo `wallet_address` incluído no INSERT
- Se usuário fornece wallet própria, usa ela

### 2. **Status Badge** ✅
- Layout ajustado com ícones e texto organizados
- Ícones separados do texto
- Melhor espaçamento

### 3. **NowPayments Valor** ✅
- Agora envia valor correto em USD
- $5 USD = 50 ALZ (correto)
- Não mais calculando errado

---

## 📁 Arquivos para Atualizar no GitHub

### Backend
1. `backend/admin_routes.py`
   - Constante `ALZ_PRICE_USD`
   - Funções de cálculo atualizadas
   - Import opcional de `payment_expiration`

2. `backend/backend_wallet_integration.py`
   - Cálculo USD correto
   - Salvar `wallet_address` do request
   - Metadata com `amount_usd`

3. `backend/payment_expiration.py` (verificar se existe no GitHub)

### Frontend
4. `Site/src/components/sections/Buy.jsx`
   - Cálculo correto: USD → ALZ
   - Enviar `wallet_address` no request
   - Enviar `amount_usd` para referência

5. `Site/src/components/sections/AdminDashboard.jsx`
   - Funções de cálculo atualizadas
   - Layout do status badge ajustado

---

## ✅ Checklist

- [ ] Atualizar `ALZ_PRICE_USD` em todos os arquivos
- [ ] Corrigir cálculo NowPayments (USD direto)
- [ ] Salvar `wallet_address` do request
- [ ] Ajustar layout do status badge
- [ ] Testar conversão $5 USD → 50 ALZ
- [ ] Verificar se `payment_expiration.py` está no GitHub

---

**Última atualização:** 2025-01-XX

