# 🚀 Publish Now (Without Scope)

## ✅ Quick Solution

Changed `package.json` to publish **without scope** temporarily.

### **Publish Now:**

```bash
npm publish
```

**Installation will be:**
```bash
npm install allianza-qss-js
```

### **Later (When Creating Organization):**

1. Create `allianza` organization on npm
2. Change `package.json` back to `@allianza/qss-js`
3. Publish new version
4. Deprecate old version: `npm deprecate allianza-qss-js "Use @allianza/qss-js instead"`

---

## 📝 What Was Changed

**Before:**
```json
"name": "@allianza/qss-js"
```

**Now:**
```json
"name": "allianza-qss-js"
```

**Everything else remains the same!**

---

## 🎯 Next Steps

1. **Publish now:**
   ```bash
   npm publish
   ```

2. **Test installation:**
   ```bash
   npm install allianza-qss-js
   ```

3. **Later create organization:**
   - Visit: https://www.npmjs.com/org/create
   - Create `allianza` organization
   - Migrate to `@allianza/qss-js` in next version

---

**✅ Ready to publish! Run: `npm publish`**
