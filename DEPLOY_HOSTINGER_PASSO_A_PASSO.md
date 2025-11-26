# 📦 PASSO A PASSO PARA IMPLANTAR NA HOSTINGER

**Versão:** 1.0  
**Data:** 2025-11-26

---

## ✅ PASSO 1: COMPACTAR A PASTA DEPLOY

No seu computador Windows, execute:

```powershell
powershell Compress-Archive -Path deploy -DestinationPath allianza_deploy.zip
```

Isso criará o arquivo `allianza_deploy.zip` pronto para upload.

---

## ✅ PASSO 2: ACESSAR O PAINEL DA HOSTINGER

1. Entre no painel da Hostinger (hPanel)
2. Vá em **"Arquivos"** ou **"Gerenciador de Arquivos"**

---

## ✅ PASSO 3: FAZER UPLOAD DO ARQUIVO ZIP

1. No Gerenciador de Arquivos, navegue até a pasta raiz do seu domínio
   - Geralmente: `public_html` ou `domains/seu-dominio.com/public_html`

2. Clique em **"Upload"** no menu superior

3. Selecione o arquivo `allianza_deploy.zip` que você criou

4. Aguarde o upload completar (pode levar alguns minutos dependendo do tamanho)

---

## ✅ PASSO 4: EXTRAIR OS ARQUIVOS

1. No Gerenciador de Arquivos, clique com o botão direito no arquivo `allianza_deploy.zip`

2. Selecione **"Extrair"** ou **"Extract"**

3. Isso criará uma pasta `deploy` no seu servidor

---

## ✅ PASSO 5: MOVER OS ARQUIVOS PARA A RAIZ (IMPORTANTE!)

1. Entre na pasta `deploy` que foi extraída

2. Selecione **TODOS os arquivos e pastas** (Ctrl+A ou Cmd+A)

3. Clique em **"Mover"** ou **"Move"**

4. Digite o caminho: `/public_html` (ou apenas `/` dependendo da configuração)

5. Confirme a movimentação

**⚠️ IMPORTANTE:** Todos os arquivos devem estar diretamente em `public_html`, não dentro de uma subpasta.

**Estrutura correta após mover:**
```
public_html/
├── wsgi.py                    ← Arquivo principal
├── allianza_blockchain.py     ← App Flask
├── requirements.txt           ← Dependências
├── .env                       ← Variáveis de ambiente
├── .htaccess                  ← Configuração Apache
├── templates/                 ← Templates HTML
├── contracts/                 ← Contratos
├── proofs/                    ← Provas
└── ... (outros arquivos .py)
```

---

## ✅ PASSO 6: CONFIGURAR A APLICAÇÃO PYTHON

1. Volte ao painel principal da Hostinger

2. Vá em **"Python Apps"** (geralmente na seção **"Avançado"** ou **"Desenvolvimento"**)

3. Clique em **"Criar aplicação Python"** ou **"Add Python App"**

---

## ✅ PASSO 7: CONFIGURAR OS PARÂMETROS

Configure os seguintes parâmetros:

- **Versão do Python:** `3.8` ou superior (recomendo `3.9` ou `3.10`)
- **Arquivo de inicialização:** `wsgi.py` ⚠️ **IMPORTANTE: Use `wsgi.py`, NÃO `app.py`!**
- **Pasta da aplicação:** `/public_html` (deve apontar para onde você moveu os arquivos)
- **URL da aplicação:** Seu domínio principal (ex: `https://seu-dominio.com`)
- **Porta:** Deixe o padrão ou configure conforme necessário

**⚠️ ATENÇÃO:** 
- O arquivo de inicialização deve ser **`wsgi.py`**, não `app.py`!
- A pasta deve ser `/public_html` (caminho absoluto)

---

## ✅ PASSO 8: AGUARDAR A IMPLANTAÇÃO

1. A Hostinger irá instalar as dependências automaticamente do `requirements.txt`

2. Isso pode levar alguns minutos (5-15 minutos dependendo do número de dependências)

3. Você verá o progresso na tela de "Python Apps"

4. Aguarde até ver a mensagem de sucesso

---

## ✅ PASSO 9: VERIFICAR SE ESTÁ FUNCIONANDO

1. Acesse seu domínio no navegador:
   - `https://seu-dominio.com` - Página principal
   - `https://seu-dominio.com/health` - Health check
   - `https://seu-dominio.com/testnet/professional-tests/` - Dashboard de testes

2. Você deve ver a interface da Allianza Blockchain

---

## 🔧 SOLUÇÃO DE PROBLEMAS COMUNS

### ❌ Erro 500 (Internal Server Error)

**Soluções:**

1. **Verifique os logs:**
   - No painel Hostinger, vá em **"Python Apps"** → **"Logs"**
   - Procure por erros recentes
   - Os logs mostrarão exatamente qual é o problema

2. **Confirme que todas as dependências estão no requirements.txt:**
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

3. **Verifique o arquivo wsgi.py:**
   - Confirme que `wsgi.py` existe em `public_html`
   - Verifique se o arquivo não está corrompido
   - O arquivo deve ter a variável `application` definida

4. **Verifique variáveis de ambiente:**
   - Crie/edite o arquivo `.env` em `public_html`
   - Configure pelo menos:
     ```env
     FLASK_ENV=production
     FLASK_DEBUG=False
     SECRET_KEY=sua_chave_secreta_aqui_gerada_aleatoriamente
     PORT=5000
     HOST=0.0.0.0
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
   ├── wsgi.py                    ← DEVE ESTAR AQUI
   ├── allianza_blockchain.py     ← DEVE ESTAR AQUI
   ├── requirements.txt           ← DEVE ESTAR AQUI
   ├── .env                       ← DEVE ESTAR AQUI
   ├── .htaccess                  ← DEVE ESTAR AQUI
   ├── templates/                 ← DEVE ESTAR AQUI
   ├── contracts/                 ← DEVE ESTAR AQUI
   ├── proofs/                    ← DEVE ESTAR AQUI
   └── ... (outros arquivos .py)  ← DEVEM ESTAR AQUI
   ```

3. **NÃO deve ter subpastas:**
   ```
   ❌ ERRADO:
   public_html/
   └── deploy/
       └── wsgi.py
   
   ✅ CORRETO:
   public_html/
   └── wsgi.py
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
   - Todos os módulos Python devem estar no mesmo diretório (`public_html`)
   - Pastas como `templates`, `contracts` devem estar acessíveis

3. **Verifique os imports no wsgi.py:**
   - O `wsgi.py` deve importar corretamente de `allianza_blockchain`
   - Se houver erros de import, verifique os logs

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
   - O arquivo deve incluir todas as dependências necessárias
   - Se faltar alguma, adicione manualmente

---

### ❌ Erro: "Application failed to start"

**Soluções:**

1. **Verifique o arquivo wsgi.py:**
   - Confirme que o arquivo existe e está correto
   - O arquivo deve ter a variável `application` definida
   - Verifique se não há erros de sintaxe

2. **Verifique os logs de erro:**
   - Acesse os logs em **"Python Apps"** → **"Logs"**
   - Procure por mensagens de erro específicas
   - Os logs mostrarão exatamente qual linha está causando o problema

3. **Teste localmente primeiro:**
   - Se possível, teste o `wsgi.py` localmente antes de fazer deploy
   - Execute: `python wsgi.py` no seu computador

---

## 📋 CHECKLIST FINAL

Antes de considerar o deploy completo, verifique:

- [ ] Arquivo `allianza_deploy.zip` criado
- [ ] Upload para Hostinger concluído
- [ ] Arquivos extraídos da pasta `deploy`
- [ ] **TODOS os arquivos movidos para `public_html` (não dentro de subpasta)**
- [ ] Aplicação Python criada no painel
- [ ] **Arquivo de inicialização configurado como `wsgi.py` (NÃO `app.py`)**
- [ ] Pasta da aplicação apontando para `/public_html`
- [ ] Dependências instaladas (verificar logs)
- [ ] Arquivo `.env` configurado em `public_html`
- [ ] Arquivo `.htaccess` presente em `public_html`
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

## ✅ PRONTO!

Após seguir todos os passos, sua Allianza Blockchain Testnet estará online e acessível!

**URLs esperadas:**
- `https://seu-dominio.com/` - Página principal
- `https://seu-dominio.com/health` - Health check
- `https://seu-dominio.com/testnet/professional-tests/` - Dashboard de testes
- `https://seu-dominio.com/dashboard` - Dashboard principal

---

## ⚠️ LEMBRETES IMPORTANTES

1. **Arquivo de inicialização:** Use `wsgi.py`, NÃO `app.py`!
2. **Estrutura de pastas:** Todos os arquivos devem estar diretamente em `public_html`, não em subpastas
3. **Dependências:** O `requirements.txt` já foi atualizado com `gunicorn` e `gevent`
4. **Variáveis de ambiente:** Crie o arquivo `.env` em `public_html` com as configurações necessárias

---

**Última Atualização:** 2025-11-26

