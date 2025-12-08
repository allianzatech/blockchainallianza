# ⏰ Sistema de Expiração de Pagamentos - 10 Dias

## 📋 Visão Geral

Sistema que automaticamente expira pagamentos pendentes após 10 dias, devolvendo o saldo ao supply total de 1 bilhão de ALZ.

---

## 🔧 Funcionalidades Implementadas

### 1. **Expiração Automática** ✅

- Pagamentos pendentes expiram automaticamente após **10 dias**
- Status muda de `pending` para `expired`
- Saldo é devolvido ao supply total (não conta mais em `pending_distribution`)

### 2. **Job Periódico** ✅

- Executa automaticamente a cada **1 hora**
- Verifica pagamentos expirados
- Atualiza status e devolve saldo

### 3. **Filtros no Frontend** ✅

- Filtro por status: **Todos**, **Pendentes**, **Concluídos**, **Expirados**
- Exibição visual diferenciada para cada status
- Card de estatísticas para pagamentos expirados

---

## 📁 Arquivos Modificados/Criados

### Backend

1. **`payment_expiration.py`** (já existia)
   - Função `expire_old_payments()` - Expira pagamentos antigos
   - Função `set_payment_expiration()` - Define data de expiração
   - Função `add_expires_at_column()` - Adiciona coluna no banco

2. **`payment_expiration_job.py`** (NOVO)
   - Job periódico que executa `expire_old_payments()`
   - Scheduler em background
   - Executa a cada 1 hora

3. **`main.py`** (ATUALIZADO)
   - Inicia scheduler de expiração ao iniciar o servidor

4. **`backend_wallet_integration.py`** (já tinha)
   - Define `expires_at = created_at + 10 dias` ao criar pagamento

5. **`admin_routes.py`** (ATUALIZADO)
   - Query de pagamentos inclui `expires_at`
   - Estatísticas incluem `expired_payments`
   - `pending_distribution` exclui pagamentos expirados

### Frontend

1. **`AdminDashboard.jsx`** (ATUALIZADO)
   - Filtro de status inclui "Expirados"
   - Exibição visual para status `expired`
   - Card de estatísticas para expirados

---

## 🔄 Fluxo de Funcionamento

### 1. Criação de Pagamento

```python
# backend_wallet_integration.py
expires_at = datetime.now(timezone.utc) + timedelta(days=10)
cursor.execute(
    "INSERT INTO payments (..., expires_at) VALUES (..., %s)",
    (..., expires_at)
)
```

**Resultado:**
- Pagamento criado com `status = 'pending'`
- `expires_at` definido para 10 dias no futuro
- Saldo diminui do supply (conta em `pending_distribution`)

---

### 2. Job de Expiração (a cada 1 hora)

```python
# payment_expiration_job.py
def run_expiration_job():
    # Buscar pagamentos pendentes expirados
    expired_payments = buscar_pagamentos_expirados()
    
    # Atualizar status para 'expired'
    atualizar_status_para_expired(expired_payments)
    
    # Saldo é automaticamente devolvido (não conta mais em pending_distribution)
```

**Resultado:**
- Status muda de `pending` → `expired`
- Saldo devolvido ao supply total
- Não conta mais em `pending_distribution`

---

### 3. Cálculo de Supply

```python
# admin_routes.py
# ✅ PAGAMENTOS PENDENTES (apenas não expirados)
cursor.execute("""
    SELECT SUM(amount) as pending_brl 
    FROM payments 
    WHERE status = 'pending' 
    AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
""")

# Supply Reserve = TOTAL_SUPPLY - circulating - pending_alz
# Quando expira, pending_alz diminui, reserve aumenta
```

---

## 🎨 Interface do Frontend

### Filtro de Status

```jsx
<select value={filterStatus} onChange={...}>
    <option value="all">📋 Todos os status</option>
    <option value="pending">⏳ Pendentes</option>
    <option value="completed">✅ Concluídos</option>
    <option value="expired">⏰ Expirados</option>
</select>
```

### Exibição Visual

- **Pendente**: Badge amarelo `⏳ Pendente`
- **Concluído**: Badge verde `✅ Concluído`
- **Expirado**: Badge vermelho `⏰ Expirado`

### Card de Estatísticas

Quando há pagamentos expirados, aparece um card:
- Ícone: ⏰
- Cor: Vermelho
- Texto: "Saldo devolvido ao supply total"

---

## 📊 Estrutura do Banco de Dados

### Tabela `payments`

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    amount DECIMAL(10,2),
    method VARCHAR(50),
    status VARCHAR(50),  -- 'pending', 'completed', 'expired'
    created_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,  -- ✅ NOVA COLUNA
    ...
);
```

---

## 🚀 Como Funciona

1. **Pagamento Criado:**
   - `status = 'pending'`
   - `expires_at = created_at + 10 dias`
   - Saldo diminui do supply

2. **Após 10 dias:**
   - Job detecta pagamento expirado
   - `status = 'expired'`
   - Saldo devolvido (não conta mais em `pending_distribution`)

3. **No Frontend:**
   - Filtro permite ver apenas expirados
   - Card mostra quantidade de expirados
   - Badge vermelho indica status expirado

---

## ✅ Benefícios

1. **Gestão Automática**: Não precisa expirar manualmente
2. **Saldo Correto**: Supply sempre reflete apenas pagamentos válidos
3. **Transparência**: Usuário vê claramente pagamentos expirados
4. **Organização**: Filtros facilitam gestão

---

## 📝 Notas Importantes

- ⏰ **Prazo**: 10 dias (configurável em `payment_expiration.py`)
- 🔄 **Frequência do Job**: 1 hora (configurável em `main.py`)
- 💰 **Saldo**: Automaticamente devolvido quando expira
- 📊 **Estatísticas**: Incluem contagem de expirados

---

**Última atualização:** 2025-01-XX
