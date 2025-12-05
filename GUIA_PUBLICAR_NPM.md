# 📦 Guia: Como Publicar no npm

## 🎯 Objetivo

Publicar o pacote `@allianza/qss-js` no npm para que desenvolvedores possam instalar com:
```bash
npm install @allianza/qss-js
```

---

## ✅ Pré-requisitos

1. **Conta npm** (criar em: https://www.npmjs.com/signup)
2. **Node.js instalado** (versão 18+)
3. **SDK compilado** (já feito ✅)

---

## 🚀 Passo a Passo

### **1. Criar Conta npm (se ainda não tiver)**

1. Acesse: https://www.npmjs.com/signup
2. Preencha:
   - Username: `allianza-blockchain` (ou seu username)
   - Email: Seu email
   - Password: Senha segura
3. Verifique o email
4. ✅ Conta criada!

### **2. Fazer Login no npm**

Abra o terminal na pasta `qss-sdk`:

```bash
cd qss-sdk
npm login
```

**Informações solicitadas:**
- Username: `allianza-blockchain` (ou seu username)
- Password: Sua senha
- Email: Seu email
- OTP (se tiver 2FA): Código do app autenticador

### **3. Verificar se está Logado**

```bash
npm whoami
```

**Deve mostrar:** Seu username do npm

### **4. Verificar se o Pacote Está Pronto**

```bash
npm run build
```

**Deve compilar sem erros**

### **5. Verificar package.json**

Certifique-se que tem:
- ✅ `name`: `@allianza/qss-js`
- ✅ `version`: `1.0.0`
- ✅ `files`: `["dist", "README.md", "LICENSE"]`

### **6. Testar Publicação (Dry Run)**

```bash
npm publish --dry-run
```

**Isso mostra o que será publicado SEM publicar de verdade**

### **7. Publicar no npm**

```bash
npm publish --access public
```

**Importante:** `--access public` é necessário para pacotes com escopo (`@allianza/`)

### **8. Verificar Publicação**

1. Acesse: https://www.npmjs.com/package/@allianza/qss-js
2. Deve aparecer o pacote publicado!

### **9. Testar Instalação**

Em outro projeto ou pasta:

```bash
npm install @allianza/qss-js
```

**Deve instalar sem erros!**

---

## 🔧 Comandos Completos

```bash
# 1. Ir para pasta do SDK
cd qss-sdk

# 2. Fazer login
npm login

# 3. Compilar
npm run build

# 4. Verificar (dry run)
npm publish --dry-run

# 5. Publicar
npm publish --access public

# 6. Verificar
npm view @allianza/qss-js
```

---

## ⚠️ Problemas Comuns

### **Erro: "You must verify your email"**

**Solução:**
1. Verifique seu email no npm
2. Acesse o link de verificação
3. Tente novamente

### **Erro: "Package name already exists"**

**Solução:**
- Alguém já publicou esse nome
- Use outro nome ou verifique se você já publicou

### **Erro: "You do not have permission"**

**Solução:**
- Para pacotes com escopo (`@allianza/`), você precisa:
  1. Criar organização no npm: https://www.npmjs.com/org/create
  2. Ou usar `--access public`

### **Erro: "Access token expired"**

**Solução:**
```bash
npm logout
npm login
```

---

## 📝 Atualizar Versão

Quando quiser atualizar o pacote:

1. **Editar `package.json`:**
   ```json
   {
     "version": "1.0.1"  // Incrementar versão
   }
   ```

2. **Compilar:**
   ```bash
   npm run build
   ```

3. **Publicar:**
   ```bash
   npm publish --access public
   ```

---

## 🎯 Checklist Final

- [ ] Conta npm criada
- [ ] Email verificado
- [ ] Login feito (`npm login`)
- [ ] Build compilado (`npm run build`)
- [ ] Dry run testado (`npm publish --dry-run`)
- [ ] Publicado (`npm publish --access public`)
- [ ] Verificado no site npm
- [ ] Testado instalação (`npm install @allianza/qss-js`)

---

## ✅ Após Publicar

1. **Atualizar Developer Hub** (já feito ✅)
2. **Compartilhar link:** https://www.npmjs.com/package/@allianza/qss-js
3. **Adicionar badge no README:**
   ```markdown
   [![npm version](https://img.shields.io/npm/v/@allianza/qss-js)](https://www.npmjs.com/package/@allianza/qss-js)
   ```

---

**🚀 Pronto! Agora desenvolvedores podem instalar com `npm install @allianza/qss-js`**

