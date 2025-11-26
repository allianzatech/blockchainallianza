# 🎨 ALLIANZA BLOCKCHAIN - DEPLOY NO RENDER

Este projeto está configurado para deploy automático no Render.com.

---

## 🚀 DEPLOY RÁPIDO

1. **Fazer push para GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Render"
   git push
   ```

2. **No Render:**
   - New + → Web Service
   - Conectar repositório GitHub
   - Render detecta automaticamente Python
   - Deploy automático!

---

## 📋 ARQUIVOS DE CONFIGURAÇÃO

- `Procfile` - Comando de inicialização
- `render.yaml` - Configuração do Render
- `wsgi.py` - Entry point WSGI
- `requirements.txt` - Dependências

---

## ⚙️ VARIÁVEIS DE AMBIENTE

Configure no Render:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
PORT=5000
HOST=0.0.0.0
```

---

## 🌐 DOMÍNIO

Render fornece automaticamente:
- `allianza-blockchain.onrender.com`

Ou configure domínio customizado nas Settings.

---

## 📚 DOCUMENTAÇÃO

- Guia completo: `DEPLOY_RENDER_PASSO_A_PASSO.md`
- Comparação de hospedagens: `COMPARACAO_HOSPEDAGENS.md`

---

**Deploy em minutos! 🚀**

