# ⚡ COMANDOS RÁPIDOS - OTIMIZAR GIT PUSH

O push está demorando porque há arquivos grandes. Execute estes comandos:

---

## 🚀 SOLUÇÃO RÁPIDA (Windows)

### Opção 1: Usar script automatizado
```batch
otimizar_git_push.bat
git commit -m "Otimizar: remover arquivos grandes"
git push -u origin main
```

### Opção 2: Comandos manuais

```powershell
# Remover liboqs (muito grande)
git rm -r --cached liboqs
git rm -r --cached liboqs-python

# Remover databases e logs
git rm --cached *.db
git rm --cached *.log
git rm --cached *.zip

# Atualizar .gitignore
git add .gitignore

# Commit
git commit -m "Otimizar: remover arquivos grandes"

# Push (será muito mais rápido!)
git push -u origin main
```

---

## ⏱️ TEMPO ESTIMADO

**Antes (com liboqs):** 20-60 minutos  
**Depois (otimizado):** 2-5 minutos ✅

---

## 📋 O QUE SERÁ ENVIADO

✅ Código Python (.py)  
✅ requirements.txt  
✅ Procfile  
✅ render.yaml  
✅ wsgi.py  
✅ templates/  
✅ contracts/  

❌ liboqs/ (muito grande)  
❌ *.db (databases)  
❌ *.log (logs)  
❌ *.zip (arquivos compactados)  

---

**Execute `otimizar_git_push.bat` e depois faça push novamente!**

