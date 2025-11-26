# 🚀 GUIA COMPLETO - DEPLOY NA HOSTINGER

**Versão:** 1.0  
**Data:** 2025-11-26

---

## 📦 PASSO A PASSO PARA IMPLANTAR NA HOSTINGER

### 1️⃣ COMPACTAR A PASTA DEPLOY

No seu computador, execute:

```powershell
powershell Compress-Archive -Path deploy -DestinationPath allianza_deploy.zip
```

Isso criará o arquivo `allianza_deploy.zip` pronto para upload.

---

### 2️⃣ ACESSAR O PAINEL DA HOSTINGER

1. Entre no painel da Hostinger (hPanel)
2. Vá em **"Arquivos"** ou **"Gerenciador de Arquivos"**

---

### 3️⃣ FAZER UPLOAD DO ARQUIVO ZIP

1. No Gerenciador de Arquivos, navegue até a pasta raiz do seu domínio
   - Geralmente: `public_html` ou `domains/seu-dominio.com/public_html`

2. Clique em **"Upload"** no menu superior

3. Selecione o arquivo `allianza_deploy.zip` que você criou

4. Aguarde o upload completar (pode levar alguns minutos dependendo do tamanho)

---

### 4️⃣ EXTRAIR OS ARQUIVOS

1. No Gerenciador de Arquivos, clique com o botão direito no arquivo `allianza_deploy.zip`

2. Selecione **"Extrair"** ou **"Extract"**

3. Isso criará uma pasta `deploy` no seu servidor

---

### 5️⃣ MOVER OS ARQUIVOS PARA A RAIZ (IMPORTANTE!)

1. Entre na pasta `deploy` que foi extraída

2. Selecione **TODOS os arquivos e pastas** (Ctrl+A ou Cmd+A)

3. Clique em **"Mover"** ou **"Move"**

4. Digite o caminho: `/public_html` (ou apenas `/` dependendo da configuração)

5. Confirme a movimentação

**⚠️ IMPORTANTE:** Todos os arquivos devem estar diretamente em `public_html`, não dentro de uma subpasta.

---

### 6️⃣ CONFIGURAR A APLICAÇÃO PYTHON

1. Volte ao painel principal da Hostinger

2. Vá em **"Python Apps"** (geralmente na seção **"Avançado"** ou **"Desenvolvimento"**)

3. Clique em **"Criar aplicação Python"** ou **"Add Python App"**

---

### 7️⃣ CONFIGURAR OS PARÂMETROS

Configure os seguintes parâmetros:

- **Versão do Python:** `3.8` ou superior (recomendo `3.9` ou `3.10`)
- **Arquivo de inicialização:** `wsgi.py` ⚠️ **NÃO use `app.py`!**
- **Pasta da aplicação:** `/public_html` (deve apontar para onde você moveu os arquivos)
- **URL da aplicação:** Seu domínio principal (ex: `https://seu-dominio.com`)
- **Porta:** Deixe o padrão ou configure conforme necessário

---

### 8️⃣ AGUARDAR A IMPLANTAÇÃO

1. A Hostinger irá instalar as dependências automaticamente do `requirements.txt`

2. Isso pode levar alguns minutos (5-15 minutos dependendo do número de dependências)

3. Você verá o progresso na tela de "Python Apps"

---

### 9️⃣ VERIFICAR SE ESTÁ FUNCIONANDO

1. Acesse seu domínio no navegador:
   - `https://seu-dominio.com`
   - `https://seu-dominio.com/health` (endpoint de health check)
   - `https://seu-dominio.com/testnet/professional-tests/` (dashboard de testes)

2. Você deve ver a interface da Allianza Blockchain

---

## 🔧 SOLUÇÃO DE PROBLEMAS COMUNS

### ❌ Erro 500 (Internal Server Error)

**Soluções:**

1. **Verifique os logs:**
   - No painel Hostinger, vá em **"Python Apps"** → **"Logs"**
   - Procure por erros recentes

2. **Confirme dependências:**
   - Verifique se o `requirements.txt` está completo
   - Algumas dependências podem precisar ser instaladas manualmente

3. **Verifique o arquivo wsgi.py:**
   - Confirme que `wsgi.py` existe em `public_html`
   - Verifique se o arquivo não está corrompido

4. **Verifique variáveis de ambiente:**
   - Crie/edite o arquivo `.env` em `public_html`
   - Configure pelo menos:
     ```env
     FLASK_ENV=production
     FLASK_DEBUG=False
     SECRET_KEY=sua_chave_secreta_aqui
     ```

---

### ❌ Arquivos não encontrados

**Soluções:**

1. **Certifique-se de que moveu TODOS os arquivos:**
   - Verifique se `wsgi.py` está em `public_html`
   - Verifique se `allianza_blockchain.py` está em `public_html`
   - Verifique se as pastas `templates`, `contracts`, `proofs` foram movidas

2. **Estrutura correta deve ser:**
   ```
   public_html/
   ├── wsgi.py
   ├── allianza_blockchain.py
   ├── requirements.txt
   ├── .env
   ├── .htaccess
   ├── templates/
   ├── contracts/
   ├── proofs/
   └── ... (outros arquivos .py)
   ```

---

### ❌ Problemas de importação

**Soluções:**

1. **Verifique o .htaccess:**
   - Confirme que o arquivo `.htaccess` foi copiado para `public_html`
   - O conteúdo deve ser:
     ```apache
     RewriteEngine On
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteCond %{REQUEST_FILENAME} !-d
     RewriteRule ^(.*)$ wsgi.py/$1 [QSA,L]
     ```

2. **Confirme a estrutura de pastas:**
   - Todos os módulos Python devem estar no mesmo diretório
   - Pastas como `templates`, `contracts` devem estar acessíveis

3. **Verifique os imports no wsgi.py:**
   - O `wsgi.py` deve importar corretamente de `allianza_blockchain`

---

### ❌ Erro: "Module not found"

**Soluções:**

1. **Instale dependências manualmente:**
   - No painel Hostinger, vá em **"Python Apps"** → **"Terminal"** ou **"SSH"**
   - Execute:
     ```bash
     cd public_html
     pip install -r requirements.txt
     ```

2. **Verifique se todas as dependências estão no requirements.txt:**
   - O arquivo deve incluir pelo menos:
     ```
     flask==2.3.3
     flask-socketio==5.3.6
     flask-limiter==3.5.0
     python-socketio==5.8.0
     cryptography==41.0.7
     web3==6.11.0
     python-dotenv==1.0.0
     gunicorn==21.2.0
     gevent==23.9.1
     ```

---

### ❌ Erro: "Application failed to start"

**Soluções:**

1. **Verifique o arquivo wsgi.py:**
   - Confirme que o arquivo existe e está correto
   - O arquivo deve ter a variável `application` definida

2. **Verifique os logs de erro:**
   - Acesse os logs em **"Python Apps"** → **"Logs"**
   - Procure por mensagens de erro específicas

3. **Teste localmente primeiro:**
   - Se possível, teste o `wsgi.py` localmente antes de fazer deploy

---

## 📋 CHECKLIST FINAL

Antes de considerar o deploy completo, verifique:

- [ ] Arquivo `allianza_deploy.zip` criado
- [ ] Upload para Hostinger concluído
- [ ] Arquivos extraídos
- [ ] Todos os arquivos movidos para `public_html`
- [ ] Aplicação Python criada no painel
- [ ] Arquivo de inicialização configurado como `wsgi.py`
- [ ] Pasta da aplicação apontando para `/public_html`
- [ ] Dependências instaladas (verificar logs)
- [ ] Arquivo `.env` configurado
- [ ] Site acessível no navegador
- [ ] Endpoint `/health` funcionando
- [ ] Dashboard `/testnet/professional-tests/` acessível

---

## 🎯 CONFIGURAÇÕES ADICIONAIS (OPCIONAL)

### Configurar Domínio Personalizado

1. No painel Hostinger, vá em **"Domains"**
2. Configure o DNS para apontar para o servidor
3. Aguarde a propagação (pode levar até 24 horas)

### Configurar SSL/HTTPS

1. No painel Hostinger, vá em **"SSL"**
2. Ative o certificado SSL gratuito (Let's Encrypt)
3. Configure redirecionamento HTTP → HTTPS

### Configurar Backup Automático

1. No painel Hostinger, vá em **"Backups"**
2. Configure backups automáticos
3. Recomendado: backups diários

---

## 📞 SUPORTE

Se encontrar problemas que não consegue resolver:

1. **Verifique os logs:**
   - Python Apps → Logs
   - Gerenciador de Arquivos → Ver logs do servidor

2. **Contate o suporte da Hostinger:**
   - Eles podem ajudar com configurações específicas do servidor

3. **Documentação:**
   - Consulte `DEPLOY_HOSTINGER.md` para mais detalhes técnicos

---

## ✅ PRONTO!

Após seguir todos os passos, sua Allianza Blockchain Testnet estará online e acessível!

**URLs esperadas:**
- `https://seu-dominio.com/` - Página principal
- `https://seu-dominio.com/health` - Health check
- `https://seu-dominio.com/testnet/professional-tests/` - Dashboard de testes
- `https://seu-dominio.com/dashboard` - Dashboard principal

---

**Última Atualização:** 2025-11-26

