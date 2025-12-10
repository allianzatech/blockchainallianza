# 🆕 Guia: Configurar Nova Conta GitHub

## Passo 1: Criar Nova Conta GitHub
1. Acesse: https://github.com/signup
2. Crie uma nova conta
3. Verifique o email

## Passo 2: Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. Nome do repositório: `blockchainallianza` (ou o nome que preferir)
3. Deixe **público**
4. **NÃO** marque "Initialize with README"
5. Clique em **"Create repository"**

## Passo 3: Configurar GitHub Desktop
1. Abra o GitHub Desktop
2. File → Options → Accounts
3. Se já tiver outra conta, faça **Sign out**
4. Clique em **"Sign in"**
5. Escolha **"Sign in with your browser"**
6. Faça login com a **nova conta**
7. Autorize o GitHub Desktop

## Passo 4: Adicionar Repositório Local
1. No GitHub Desktop: **File → Add Local Repository**
2. Clique em **"Choose..."**
3. Selecione: `C:\Users\notebook\Downloads\Allianza Blockchain`
4. Clique em **"Add repository"**

## Passo 5: Configurar Remote
1. No GitHub Desktop: **Repository → Repository Settings → Remote**
2. Altere a URL para: `https://github.com/SUA_NOVA_CONTA/blockchainallianza.git`
3. Clique em **"Save"**

## Passo 6: Fazer Push
1. No GitHub Desktop, clique em **"Publish branch"**
2. Deve funcionar agora!

## Passo 7: Configurar Render
1. Acesse: https://dashboard.render.com
2. Crie um novo Web Service
3. Conecte ao repositório: `SUA_NOVA_CONTA/blockchainallianza`
4. Configure:
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 2 -b 0.0.0.0:$PORT --timeout 300 --keep-alive 5 --preload wsgi_optimized:application`
5. Salve e faça deploy

## ✅ Pronto!
Agora tudo deve funcionar perfeitamente!

