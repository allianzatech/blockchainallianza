# 🖥️ DEPLOY NO VPS HOSTINGER - ALLIANZA BLOCKCHAIN

Se você optar por migrar para VPS da Hostinger, aqui está o guia completo.

---

## ✅ VANTAGENS DO VPS

- ✅ **Root access completo**
- ✅ **Controle total do ambiente**
- ✅ **Instalar qualquer software**
- ✅ **Melhor performance**
- ✅ **Mais recursos**

---

## 📦 PASSO 1: CONTRATAR VPS

1. Acesse o painel Hostinger
2. Vá em **"VPS"** → **"Order VPS"**
3. Escolha o plano (recomendo pelo menos 2GB RAM)
4. Configure o sistema operacional (Ubuntu 22.04 recomendado)

---

## 🔧 PASSO 2: CONFIGURAR SERVIDOR

### 2.1. Conectar via SSH

```bash
ssh root@seu-ip-vps
```

### 2.2. Atualizar Sistema

```bash
apt update && apt upgrade -y
```

### 2.3. Instalar Dependências

```bash
# Python e pip
apt install python3 python3-pip python3-venv -y

# Git
apt install git -y

# Nginx (opcional, para reverse proxy)
apt install nginx -y

# Firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

---

## 📤 PASSO 3: ENVIAR CÓDIGO PARA O SERVIDOR

### Opção A: Via Git (Recomendado)

```bash
# No servidor
cd /var/www
git clone https://github.com/seu-usuario/allianza-blockchain.git
cd allianza-blockchain
```

### Opção B: Via SCP

```bash
# No seu computador
scp -r deploy/* root@seu-ip-vps:/var/www/allianza/
```

---

## 🚀 PASSO 4: CONFIGURAR APLICAÇÃO

### 4.1. Criar Ambiente Virtual

```bash
cd /var/www/allianza
python3 -m venv venv
source venv/bin/activate
```

### 4.2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.3. Configurar Variáveis de Ambiente

```bash
nano .env
```

Adicione:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
PORT=5000
HOST=0.0.0.0
```

---

## 🔧 PASSO 5: CONFIGURAR SYSTEMD (SERVIÇO)

### 5.1. Criar Serviço

```bash
nano /etc/systemd/system/allianza.service
```

Conteúdo:
```ini
[Unit]
Description=Allianza Blockchain Testnet
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/allianza
Environment="PATH=/var/www/allianza/venv/bin"
ExecStart=/var/www/allianza/venv/bin/gunicorn -c gunicorn_config.py wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5.2. Ativar e Iniciar

```bash
systemctl daemon-reload
systemctl enable allianza
systemctl start allianza
systemctl status allianza
```

---

## 🌐 PASSO 6: CONFIGURAR NGINX (REVERSE PROXY)

### 6.1. Criar Configuração Nginx

```bash
nano /etc/nginx/sites-available/allianza
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6.2. Ativar Site

```bash
ln -s /etc/nginx/sites-available/allianza /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

---

## 🔒 PASSO 7: CONFIGURAR SSL (LET'S ENCRYPT)

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

---

## ✅ PASSO 8: VERIFICAR

```bash
# Ver status do serviço
systemctl status allianza

# Ver logs
journalctl -u allianza -f

# Testar endpoint
curl http://localhost:5000/health
```

---

## 📋 COMANDOS ÚTEIS

```bash
# Reiniciar serviço
systemctl restart allianza

# Ver logs
journalctl -u allianza -f

# Parar serviço
systemctl stop allianza

# Iniciar serviço
systemctl start allianza

# Ver status
systemctl status allianza
```

---

## 💰 CUSTOS

**VPS Hostinger:**
- Básico: ~R$ 25-30/mês (1GB RAM)
- Recomendado: ~R$ 40-50/mês (2GB RAM)
- Avançado: ~R$ 80-100/mês (4GB RAM)

---

**VPS oferece máximo controle! 🖥️**

