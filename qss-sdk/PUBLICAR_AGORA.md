# 🚀 Publicar Agora (Sem Escopo)

## ✅ Solução Rápida

Mudei o `package.json` para publicar **sem escopo** temporariamente.

### **Publicar Agora:**

```bash
npm publish
```

**Instalação será:**
```bash
npm install allianza-qss-js
```

### **Depois (Quando Criar Organização):**

1. Criar organização `allianza` no npm
2. Mudar `package.json` de volta para `@allianza/qss-js`
3. Publicar nova versão
4. Deprecar versão antiga: `npm deprecate allianza-qss-js "Use @allianza/qss-js instead"`

---

## 📝 O Que Foi Mudado

**Antes:**
```json
"name": "@allianza/qss-js"
```

**Agora:**
```json
"name": "allianza-qss-js"
```

**Tudo mais permanece igual!**

---

## 🎯 Próximos Passos

1. **Publicar agora:**
   ```bash
   npm publish
   ```

2. **Testar instalação:**
   ```bash
   npm install allianza-qss-js
   ```

3. **Depois criar organização:**
   - Acesse: https://www.npmjs.com/org/create
   - Crie organização `allianza`
   - Migre para `@allianza/qss-js` na próxima versão

---

**✅ Pronto para publicar! Execute: `npm publish`**

