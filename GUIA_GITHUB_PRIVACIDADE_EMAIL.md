# 🔒 Guia: Privacidade de Email no GitHub

## ❓ Sua Pergunta

"Eles não veem o email que criou a conta do GitHub?"

## ✅ Resposta

### **Opção 1: Email Pode Ser Privado (Recomendado)**

Você pode configurar o GitHub para **NÃO mostrar seu email público**:

1. **Configurações do GitHub:**
   - Settings → Emails
   - Marcar: **"Keep my email addresses private"**
   - Marcar: **"Block command line pushes that expose my email"**

2. **Email Público:**
   - GitHub gera um email "noreply" para você
   - Exemplo: `username@users.noreply.github.com`
   - Ninguém vê seu email real

### **Opção 2: Criar Conta Nova (Também Válido)**

Se preferir separar completamente:

✅ **Vantagens:**
- Conta profissional separada
- Email corporativo (ex: `dev@allianza.tech`)
- Mais profissional
- Separação clara entre pessoal/profissional

❌ **Desvantagens:**
- Mais uma conta para gerenciar
- Precisa verificar email novo

---

## 🎯 Recomendação: Criar Organização GitHub

### **Melhor Opção: Organização Profissional**

Criar uma **Organização GitHub** é a melhor escolha:

1. **Criar Organização:**
   - Nome: `allianza-blockchain`
   - Email: `dev@allianza.tech` (ou email profissional)
   - Visibilidade: Pública

2. **Vantagens:**
   - ✅ Mais profissional que conta pessoal
   - ✅ Pode ter múltiplos membros depois
   - ✅ Email da organização (não pessoal)
   - ✅ Melhor para projetos empresariais
   - ✅ Pode ter múltiplos repositórios

3. **Estrutura:**
   ```
   github.com/allianza-blockchain/
   ├── qss-sdk-js          (público)
   ├── qss-verifier         (público, futuro)
   └── [outros repositórios públicos]
   ```

---

## 📧 Opções de Email

### **Opção A: Email Profissional**
```
dev@allianza.tech
ou
github@allianza.tech
ou
contact@allianza.tech
```

### **Opção B: Email "noreply" do GitHub**
```
allianza-blockchain@users.noreply.github.com
```
- Gerado automaticamente
- Totalmente privado
- Ninguém vê seu email real

### **Opção C: Email Pessoal (com privacidade)**
```
seu-email@gmail.com
```
- Mas configurado como privado
- GitHub não mostra publicamente

---

## 🔐 Configuração de Privacidade

### **Passo a Passo:**

1. **Criar Conta/Organização:**
   - Acesse: https://github.com/join
   - Escolha: Conta pessoal OU Organização

2. **Configurar Email Privado:**
   ```
   Settings → Emails
   ✅ Keep my email addresses private
   ✅ Block command line pushes that expose my email
   ```

3. **Email Público:**
   - GitHub usa: `username@users.noreply.github.com`
   - Ninguém vê seu email real

---

## 🎯 Estrutura Recomendada

### **Cenário Ideal:**

```
Organização: allianza-blockchain
Email: dev@allianza.tech (ou noreply do GitHub)
Repositórios:
  - qss-sdk-js (público)
  - qss-verifier (público, futuro)
  - [core privado - não no GitHub]
```

### **Configuração:**

1. **Criar Organização:**
   - Nome: `allianza-blockchain`
   - Visibilidade: Pública
   - Email: Privado (noreply)

2. **Criar Repositório:**
   - Nome: `qss-sdk-js`
   - Visibilidade: Pública
   - Descrição: "Quantum Security Service SDK"

3. **Configurar Privacidade:**
   - Email: Privado
   - Profile: Profissional
   - Bio: "Allianza Blockchain - Quantum Security for All Blockchains"

---

## ✅ Checklist

- [ ] Decidir: Conta pessoal OU Organização
- [ ] Criar conta/organização no GitHub
- [ ] Configurar email como privado
- [ ] Verificar email (se necessário)
- [ ] Criar repositório `qss-sdk-js`
- [ ] Configurar descrição e links
- [ ] Fazer push do SDK
- [ ] Verificar que email não aparece publicamente

---

## 🔍 Como Verificar se Email Está Privado

1. **Acesse seu perfil:**
   ```
   https://github.com/allianza-blockchain
   ```

2. **Verifique commits:**
   - Clique em qualquer commit
   - Veja o email do autor
   - Deve aparecer: `username@users.noreply.github.com`

3. **Se aparecer email real:**
   - Vá em Settings → Emails
   - Ative "Keep my email addresses private"
   - Refaça commits (ou use `git commit --amend`)

---

## 💡 Dica Extra

### **Para Commits Antigos:**

Se você já fez commits com email público, pode corrigir:

```bash
# Corrigir email em commits antigos
git filter-branch --env-filter '
OLD_EMAIL="seu-email-antigo@exemplo.com"
CORRECT_NAME="Allianza Blockchain"
CORRECT_EMAIL="allianza-blockchain@users.noreply.github.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

---

## 🎯 Resposta Final

**Você tem 3 opções:**

1. ✅ **Usar conta existente com email privado** (mais fácil)
2. ✅ **Criar conta nova profissional** (mais organizado)
3. ✅ **Criar Organização GitHub** (mais profissional - RECOMENDADO)

**Recomendação:** Criar **Organização `allianza-blockchain`** com email privado (noreply do GitHub).

Assim você tem:
- ✅ Email não aparece publicamente
- ✅ Conta profissional separada
- ✅ Pode adicionar membros depois
- ✅ Mais credibilidade

---

**Quer que eu te ajude a configurar a Organização GitHub passo a passo?**

