# 🔧 Solução: Erro "Scope not found" no npm

## ❌ Problema

```
npm error 404 Scope not found
```

**Causa:** O escopo `@allianza` não existe no npm.

## ✅ Soluções

### **Opção 1: Criar Organização no npm (Recomendado)**

Para publicar `@allianza/qss-js`, você precisa criar uma organização:

1. **Acesse:** https://www.npmjs.com/org/create
2. **Criar Organização:**
   - Nome: `allianza`
   - Visibilidade: Pública
   - Plano: Free (gratuito)
3. **Adicionar membros:**
   - Adicione sua conta como membro
4. **Publicar novamente:**
   ```bash
   npm publish --access public
   ```

**Tempo:** 2 minutos  
**Custo:** Grátis

---

### **Opção 2: Publicar Sem Escopo (Temporário)**

Se quiser publicar rápido sem criar organização:

1. **Editar `package.json`:**
   ```json
   {
     "name": "allianza-qss-js",  // Sem @
     "version": "1.0.0"
   }
   ```

2. **Publicar:**
   ```bash
   npm publish
   ```

3. **Instalação será:**
   ```bash
   npm install allianza-qss-js
   ```

**Depois pode migrar para `@allianza/qss-js` quando criar a organização.**

---

## 🎯 Recomendação

**Criar Organização `allianza` no npm:**

### **Passo a Passo:**

1. **Acesse:** https://www.npmjs.com/org/create

2. **Preencha:**
   - Organization name: `allianza`
   - Organization URL: `https://allianza.tech` (ou deixe vazio)
   - Visibilidade: **Public**

3. **Plano:**
   - Escolha: **Free** (gratuito)
   - Permite publicar pacotes públicos ilimitados

4. **Adicionar Membros:**
   - Adicione sua conta pessoal como membro
   - Dê permissão de "Owner" ou "Admin"

5. **Publicar:**
   ```bash
   cd qss-sdk
   npm publish --access public
   ```

---

## 🔍 Verificar Organização

Após criar, verifique:

1. Acesse: https://www.npmjs.com/org/allianza
2. Deve mostrar sua organização
3. Agora pode publicar `@allianza/qss-js`

---

## ⚠️ Importante

### **Para Pacotes com Escopo:**

- ✅ **Organização criada:** Pode publicar `@allianza/qss-js`
- ❌ **Sem organização:** Erro "Scope not found"

### **Alternativas:**

1. **Criar organização** (recomendado - 2 min)
2. **Publicar sem escopo** (temporário - 1 min)
3. **Usar escopo pessoal** `@seu-username/qss-js` (não recomendado)

---

## 🚀 Após Criar Organização

```bash
# 1. Verificar login
npm whoami

# 2. Publicar
cd qss-sdk
npm publish --access public

# 3. Verificar
npm view @allianza/qss-js

# 4. Testar instalação
npm install @allianza/qss-js
```

---

## 📝 Checklist

- [ ] Criar organização `allianza` no npm
- [ ] Adicionar sua conta como membro
- [ ] Verificar organização criada
- [ ] Publicar: `npm publish --access public`
- [ ] Verificar no site: https://www.npmjs.com/package/@allianza/qss-js
- [ ] Testar instalação: `npm install @allianza/qss-js`

---

**🎯 Solução Rápida:** Criar organização `allianza` em https://www.npmjs.com/org/create (2 minutos, grátis)

