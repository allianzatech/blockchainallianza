# 🔄 Guia de Sincronização Automática

## 🎯 Objetivo

Manter o repositório público sincronizado automaticamente com o privado, excluindo arquivos sensíveis.

---

## 🚀 Como Usar

### **Método 1: Script Manual (Recomendado)**

```bash
# No repositório privado
python sincronizar_repositorio_publico.py
```

**O script:**
1. ✅ Copia arquivos seguros
2. ✅ Exclui arquivos sensíveis automaticamente
3. ✅ Pergunta se deseja fazer commit e push
4. ✅ Mostra resumo do que foi copiado

### **Método 2: GitHub Actions (Automático)**

O workflow `.github/workflows/sync-from-private.yml` pode ser configurado para executar automaticamente.

**Configuração:**
1. Acesse: Settings → Secrets → Actions
2. Adicione secrets se necessário
3. O workflow executará automaticamente

---

## 📋 Checklist Antes de Sincronizar

- [ ] Verificar que não há chaves privadas
- [ ] Verificar que não há senhas
- [ ] Verificar que não há API keys
- [ ] Executar script de verificação
- [ ] Revisar mudanças antes de commitar

---

## 🔐 Segurança

O script **automaticamente exclui:**
- Arquivos com `PRIVATE_KEY` no nome
- Arquivos `.env`
- Arquivos com `secret` ou `password`
- Core da blockchain (ALZ-NIEV, QRS-3)
- Bancos de dados
- Cache e node_modules

---

## 📅 Quando Sincronizar

### **Sempre Sincronizar:**
- ✅ Adicionar novo demo
- ✅ Atualizar documentação
- ✅ Adicionar novos testes
- ✅ Atualizar SDK
- ✅ Criar nova release

### **Frequência Recomendada:**
- **Diária:** Para mudanças frequentes
- **Semanal:** Para mudanças esporádicas
- **Antes de releases:** Sempre

---

## 🛠️ Troubleshooting

### **Erro: "Repositório público não encontrado"**
```bash
# Criar repositório público primeiro
python preparar_repositorio_publico.py
```

### **Erro: "Permission denied"**
```bash
# Verificar permissões do Git
cd ../allianzablockchain-public
git remote -v
```

### **Erro: "Nothing to commit"**
- Isso é normal se não houver mudanças
- Verifique se os arquivos foram realmente modificados

---

## 📊 Monitoramento

### **Verificar Última Sincronização:**
```bash
cd ../allianzablockchain-public
git log --oneline -5
```

### **Ver Diferenças:**
```bash
git diff HEAD~1
```

---

## 💡 Dicas

1. **Sempre teste localmente** antes de fazer push
2. **Revise as mudanças** antes de commitar
3. **Use commits descritivos** (Conventional Commits)
4. **Mantenha CHANGELOG.md atualizado**

---

## 🔗 Links Úteis

- **Script de Sync:** `sincronizar_repositorio_publico.py`
- **Estratégia:** `ESTRATEGIA_DOIS_REPOSITORIOS.md`
- **Repositório Público:** https://github.com/allianzatoken-png/allianzablockchain

---

**Última atualização:** 2025-12-05

