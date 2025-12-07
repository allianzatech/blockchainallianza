# backend_wallet_integration.py - PRODUÇÃO COM PAGAMENTO DIRETO - CORRIGIDO CORS
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta, timezone
import time
import jwt
import requests
from functools import wraps
import hmac
import hashlib
import secrets
import json
import threading

# Importar serviço de blockchain Allianza
try:
    from allianza_blockchain_service import get_allianza_blockchain_service
    ALLIANZA_BLOCKCHAIN_AVAILABLE = True
except ImportError:
    ALLIANZA_BLOCKCHAIN_AVAILABLE = False
    print("⚠️  Allianza Blockchain Service não disponível")

# ✅ CARREGAR VARIÁVEIS DE AMBIENTE PRIMEIRO
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("🚀 ALLIANZA WALLET BACKEND - PRODUÇÃO COM PAGAMENTO DIRETO")
print("✅ SISTEMA SEMPRE ATIVO - SEM COLD START")
print("🎯 PAGAMENTO DIRETO SEM INTERMEDIÁRIOS")
print("🔒 COFRE SEGURO IMPLEMENTADO")
print("🎯 SISTEMA COMPLETO DE CRYPTO PAGAMENTOS DIRETOS")
print("=" * 60)

# ✅ KEEP-ALIVE AUTOMÁTICO
def keep_alive_service():
    """Serviço para manter o backend sempre ativo"""
    def ping_server():
        while True:
            try:
                # Ping na própria aplicação para evitar hibernação
                response = requests.get(
                    'https://allianza-wallet-backend.onrender.com/health', 
                    timeout=10
                )
                print(f"🔄 Keep-alive executado: {datetime.now().strftime('%H:%M:%S')} - Status: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Keep-alive falhou: {e}")
            time.sleep(240)  # A cada 4 minutos (menos que timeout do Render")
    
    # Iniciar thread em background
    keep_alive_thread = threading.Thread(target=ping_server, daemon=True)
    keep_alive_thread.start()
    print("🚀 Serviço de keep-alive iniciado - Backend sempre ativo!")

# Iniciar keep-alive quando o módulo carregar
keep_alive_service()

# ✅ IMPORTAR SERVIÇO DE PAGAMENTO DIRETO - CORREÇÃO
DIRECT_CRYPTO_AVAILABLE = False
direct_crypto_service = None

try:
    # Tenta importar de várias formas possíveis
    try:
        from direct_crypto_service import direct_crypto_service
        DIRECT_CRYPTO_AVAILABLE = True
        print("✅ Direct Crypto Payment Service importado com sucesso!")
    except ImportError as e:
        print(f"❌ Erro na importação padrão: {e}")
        # Tenta importação alternativa
        import direct_crypto_service
        direct_crypto_service = direct_crypto_service.direct_crypto_service
        DIRECT_CRYPTO_AVAILABLE = True
        print("✅ Direct Crypto Service importado via método alternativo!")
        
except Exception as e:
    print(f"❌ Erro crítico ao importar Direct Crypto Service: {e}")
    DIRECT_CRYPTO_AVAILABLE = False

print(f"🎯 DIRECT_CRYPTO_AVAILABLE: {'✅ SIM' if DIRECT_CRYPTO_AVAILABLE else '❌ NÃO'}")

# ✅ INSTALAÇÃO FORÇADA DO STRIPE
import sys
import subprocess

STRIPE_AVAILABLE = False
stripe = None

# ✅ VERIFICAR VARIÁVEIS PRIMEIRO
stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')

# ✅ ESTRATÉGIA 1: Importação normal
try:
    import stripe
    print("✅ Stripe importado via import padrão")
    STRIPE_AVAILABLE = True
except ImportError as e:
    print(f"❌ Falha importação padrão: {e}")

# ✅ ESTRATÉGIA 2: Instalação forçada se necessário
if not STRIPE_AVAILABLE:
    print("🔄 Tentando instalação forçada do Stripe...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "stripe==8.0.0"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            import stripe
            STRIPE_AVAILABLE = True
            print("✅ Stripe instalado via subprocess")
        else:
            print(f"❌ Erro instalação: {result.stderr}")
    except Exception as e:
        print(f"❌ Falha instalação forçada: {e}")

# ✅ CONFIGURAÇÃO FINAL CORRIGIDA - PRODUÇÃO
if STRIPE_AVAILABLE:
    try:
        if stripe_secret_key:
            stripe.api_key = stripe_secret_key
            if stripe_secret_key.startswith('sk_live_'):
                print("🎉 STRIPE EM MODO PRODUÇÃO! Pagamentos reais ativados!")
            else:
                print("🔧 STRIPE EM MODO TESTE")
            print("📦 Versão Stripe: 8.0.0")
        else:
            print("❌ STRIPE_SECRET_KEY não encontrada")
            STRIPE_AVAILABLE = False
    except Exception as e:
        print(f"❌ Erro configuração Stripe: {e}")
        STRIPE_AVAILABLE = False
else:
    print("🔴 STRIPE NÃO DISPONÍVEL - Pagamentos com cartão desativados")

# Importar funções do banco
try:
    from database_neon import get_db_connection, init_db
    print("✅ Usando banco de dados Neon (PostgreSQL)")
except ImportError as e:
    print(f"❌ Erro ao importar database_neon: {e}")
    exit(1)

from generate_wallet import generate_polygon_wallet

print("🚀 Iniciando servidor Flask Allianza Wallet...")

app = Flask(__name__)


# ✅ CONFIGURAÇÃO CORS COMPLETA PARA PRODUÇÃO E DESENVOLVIMENTO - CORRIGIDA
CORS(app, resources={
    r"/*": {
        "origins": [
            "*",
            "https://allianza.tech",
            "https://admin.allianza.tech",
            "https://www.allianza.tech", 
            "https://wallet.allianza.tech",
            "https://www.wallet.allianza.tech",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://localhost:5175",
            "http://127.0.0.1:5175",
            "http://localhost:5176",
            "http://127.0.0.1:5176"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
        "allow_headers": [
            "Content-Type", 
            "Authorization", 
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Methods"
        ],
        "expose_headers": ["Content-Range", "X-Content-Range", "Access-Control-Allow-Origin"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# ✅ MIDDLEWARE CORS GLOBAL - REMOVIDO PARA EVITAR DUPLICAÇÃO COM flask_cors.CORS(app, ...)
# O CORS(app, ...) na linha 147 já configura os headers corretamente.
# A duplicação estava causando o erro 'Access-Control-Allow-Origin' com múltiplos valores.

# ✅ HANDLER GLOBAL PARA OPTIONS - REMOVIDO PARA EVITAR DUPLICAÇÃO COM flask_cors.CORS(app, ...)
# O CORS(app, ...) na linha 147 já configura o handler OPTIONS corretamente.

# ✅ ROTAS OPTIONS ESPECÍFICAS PARA STAKING - REMOVIDAS. Confiando no CORS global e no CORS do Blueprint.

# ✅ ROTAS OPTIONS EXISTENTES
@app.route('/api/site/admin/payments', methods=['OPTIONS'])
@app.route('/api/site/admin/stats', methods=['OPTIONS'])
@app.route('/api/site/admin/process-payments', methods=['OPTIONS']) 
@app.route('/api/site/admin/manual-token-send', methods=['OPTIONS'])
@app.route('/api/site/admin/debug-token', methods=['OPTIONS'])
@app.route('/api/site/admin/debug-token-info', methods=['OPTIONS', 'GET'])
@app.route('/api/site/admin/create-staking-table', methods=['OPTIONS'])
@app.route('/api/site/admin/check-tables', methods=['OPTIONS'])
@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/site/purchase', methods=['OPTIONS'])
@app.route('/create-checkout-session', methods=['OPTIONS'])
@app.route('/create-pagarme-pix', methods=['OPTIONS'])
@app.route('/api/direct-crypto/create-payment', methods=['OPTIONS'])
@app.route('/api/direct-crypto/payment-status/<payment_id>', methods=['OPTIONS'])
@app.route('/api/direct-crypto/verify-payment', methods=['OPTIONS'])
@app.route('/api/direct-crypto/supported-currencies', methods=['OPTIONS'])
@app.route('/api/vault/balance', methods=['OPTIONS'])
@app.route('/api/vault/transfer', methods=['OPTIONS'])
@app.route('/api/vault/initialize', methods=['OPTIONS'])
@app.route('/api/vault/security/settings', methods=['OPTIONS'])
@app.route('/api/vault/stats', methods=['OPTIONS'])
@app.route('/api/vault/security/withdraw-request', methods=['OPTIONS'])
@app.route('/api/vault/security/confirm-withdraw', methods=['OPTIONS'])
@app.route('/api/vault/security/cancel-withdraw', methods=['OPTIONS'])
@app.route('/balances/me', methods=['OPTIONS'])
@app.route('/ledger/history', methods=['OPTIONS'])
@app.route('/login', methods=['OPTIONS'])
@app.route('/register', methods=['OPTIONS'])
def options_handler():
    return '', 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - sempre retorna JSON válido"""
    try:
        # Tentar verificar conexão com banco (opcional)
        try:
            from database_neon import get_db_connection
            conn = get_db_connection()
            conn.close()
            db_status = "connected"
        except:
            db_status = "unknown"
        
        return jsonify({
            "status": "ok",
            "message": "Backend is running",
            "database": db_status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200
    except Exception as e:
        # Mesmo em caso de erro, retornar JSON válido
        return jsonify({
            "status": "error",
            "message": "Backend is running but health check failed",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200

# 🔐 CONFIGURAÇÕES DE SEGURANÇA ADMIN - PRODUÇÃO (CORRIGIDO)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD_1', 'CdE25$$$')
ADMIN_USERS = {
    'admin': ADMIN_PASSWORD,
}

# ✅ TOKEN CORRETO - PRODUÇÃO (CARREGAR DO AMBIENTE)
ADMIN_JWT_SECRET = os.getenv('ADMIN_JWT_SECRET', 'super-secret-jwt-key-2024-allianza-prod')

# ✅ CARREGAR TOKEN DA VARIÁVEL DE AMBIENTE (com debug)
_env_token = os.getenv('VITE_SITE_ADMIN_TOKEN')
if _env_token:
    SITE_ADMIN_TOKEN = _env_token
    print(f"✅ VITE_SITE_ADMIN_TOKEN carregado em backend_wallet_integration: {_env_token[:10]}... (comprimento: {len(_env_token)})")
else:
    SITE_ADMIN_TOKEN = 'allianza_super_admin_2024_CdE25$$$'
    print(f"⚠️  VITE_SITE_ADMIN_TOKEN não encontrado em backend_wallet_integration, usando valor padrão: {SITE_ADMIN_TOKEN[:10]}...")

# Configurações de Pagamento - PRODUÇÃO
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_default_secret_change_in_production')

# ✅ PAGAR.ME CONFIGURAÇÃO
PAGARME_PIX_URL = "https://payment-link-v3.pagar.me/pl_AdQDlEvzg9WJAb7hK3HgOyMN74PGjo1X"

# ✅ DEBUG DAS VARIÁVEIS DE AMBIENTE (CORRIGIDO)
print("🎯 VERIFICAÇÃO DAS VARIÁVEIS:")
print(f"🔑 SITE_ADMIN_TOKEN: '{SITE_ADMIN_TOKEN}'")
print(f"📏 Comprimento: {len(SITE_ADMIN_TOKEN)}")
print(f"🔐 ADMIN_JWT_SECRET: '{ADMIN_JWT_SECRET}'")
print(f"👤 ADMIN_PASSWORD: '{ADMIN_PASSWORD}'")
print(f"🧾 PAGARME_PIX_URL: '{PAGARME_PIX_URL}'")
print("=" * 60)

# Inicializa o banco de dados
# init_db() # Comentado para permitir que o servidor inicie sem a URL do banco de dados

# Registrar blueprints
from admin_routes import admin_bp
from backend_reports_routes import reports_bp
from backend_staking_routes import staking_bp

# Registrar blueprints obrigatórios
app.register_blueprint(admin_bp, url_prefix="/api/site")
app.register_blueprint(reports_bp, url_prefix="/reports")
app.register_blueprint(staking_bp, url_prefix="/api")

# ✅ Importação opcional de balance_ledger_routes
try:
    from balance_ledger_routes import balance_ledger_bp
    app.register_blueprint(balance_ledger_bp)
    print("✅ Balance Ledger routes registradas")
except ImportError as e:
    print(f"⚠️  Balance Ledger routes não disponíveis: {e}")

# 🔒 Middleware de Autenticação Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({"error": "Token de administrador necessário"}), 401
        
        try:
            payload = jwt.decode(token, ADMIN_JWT_SECRET, algorithms=['HS256'])
            if payload.get('role') != 'admin':
                return jsonify({"error": "Acesso não autorizado"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# 🔄 FUNÇÃO PARA PROCESSAR PAGAMENTOS AUTOMATICAMENTE (CORRIGIDA - VALORES ALINHADOS)
def process_automatic_payment(email, amount_alz, method, external_id):
    """Processar pagamento automaticamente e creditar tokens COM VALORES CORRETOS"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        print(f"🔄 Processando pagamento automático: {email} - {amount_alz} ALZ - {method}")
        print(f"💰 Valor a creditar: {amount_alz} ALZ")
        
        # ✅ CORRIGIDO: Calcular USD e BRL a partir do ALZ
        # 1 ALZ = $0,10 USD (valor atualizado)
        amount_usd = float(amount_alz) * 0.10  # 1 ALZ = $0,10 USD
        usd_to_brl_rate = 5.50  # Taxa aproximada USD/BRL
        brl_amount_for_db = amount_usd * usd_to_brl_rate  # Para registro no banco
        
        # Registrar pagamento com metadata correto
        cursor.execute(
            "INSERT INTO payments (email, amount, method, status, tx_hash, metadata) VALUES (%s, %s, %s, 'completed', %s, %s) RETURNING id",
            (email, brl_amount_for_db, method, external_id, json.dumps({'alz_amount': float(amount_alz)}))
        )
        payment_id = cursor.fetchone()['id']
        print(f"✅ Pagamento registrado: ID {payment_id} - {amount_alz} ALZ = R$ {brl_amount_for_db}")
        
        # Buscar ou criar usuário
        cursor.execute("SELECT id, wallet_address FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        user_created = False
        wallet_address = None
        user_id = None
        
        if not user:
            # ✅ NÃO gerar wallet - usuário usará wallet Allianza (saldo bloqueado)
            wallet_address = None
            private_key = None
            temp_password = f"temp_{secrets.token_hex(8)}"
            hashed_password = generate_password_hash(temp_password)
            
            cursor.execute(
                "INSERT INTO users (email, password, wallet_address, private_key, nickname) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (email, hashed_password, wallet_address, private_key, f"User_{email.split('@')[0]}")
            )
            user_id = cursor.fetchone()['id']
            user_created = True
            print(f"👤 Usuário criado: {email} - Wallet Allianza (será gerada no login)")
        else:
            user_id = user['id']
            wallet_address = user['wallet_address']  # Pode ser None se não tiver wallet ainda
            print(f"👤 Usuário existente: {email} - ID: {user_id}")
        
        # Verificar/criar saldo
        cursor.execute("SELECT user_id FROM balances WHERE user_id = %s AND asset = 'ALZ'", (user_id,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO balances (user_id, asset, available, locked, staking_balance) VALUES (%s, 'ALZ', 0, 0, 0)",
                (user_id,)
            )
            print(f"💰 Saldo criado para usuário {user_id}")
        
        # ✅ BLOQUEAR TOKENS (adicionar em locked) - usuário verá ao fazer login
        cursor.execute(
            "UPDATE balances SET locked = locked + %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s AND asset = 'ALZ'",
            (amount_alz, user_id)
        )
        print(f"🔒 Tokens bloqueados: +{amount_alz} ALZ em locked (usuário verá ao fazer login)")
        
        # Registrar entrada no ledger
        cursor.execute(
            "INSERT INTO ledger_entries (user_id, asset, amount, entry_type, related_id, description, idempotency_key) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_id, 'ALZ', amount_alz, 'purchase', payment_id, f'Compra via {method}', f'purchase_{payment_id}')
        )
        print(f"✅ Entrada no ledger registrada para payment {payment_id}")

        # ✅ COMPENSAÇÃO DE TAXAS PARA CRIPTO (usando valor correto)
        if method == 'crypto' or method == 'direct_crypto':
            bonus_amount = float(amount_alz) * 0.02  # 2% do valor em ALZ
            
            cursor.execute(
                "UPDATE balances SET available = available + %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s",
                (bonus_amount, user_id)
            )
            cursor.execute(
                "INSERT INTO ledger_entries (user_id, asset, amount, entry_type, related_id, description, idempotency_key) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user_id, 'ALZ', bonus_amount, 'fee_compensation', payment_id, '🎁 Bônus compensação de taxa crypto', f'fee_comp_{payment_id}')
            )
            print(f"🎁 Bônus aplicado para {email}: +{bonus_amount} ALZ")

        cursor.execute("COMMIT")
        return {"success": True, "user_created": user_created, "wallet_address": wallet_address}

    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"❌ Erro ao processar pagamento automático: {e}")
        return {"success": False, "error": str(e)}
    finally:
        conn.close()

# 🔒 Middleware de Autenticação
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token is missing or invalid"}), 401

        token = auth_header.split(" ")[1]
        user_id = get_user_id_from_token(token)

        if not user_id:
            return jsonify({"error": "Invalid authentication token"}), 401
        
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function

# 🔄 FUNÇÃO authenticate_request - CORRIGIDA PARA ROTAS PÚBLICAS
@app.before_request
def authenticate_request():
    # ✅ LISTA ATUALIZADA DE ROTAS PÚBLICAS
    public_routes = [
        "/health", 
        "/system/info",
        "/webhook/stripe", 
        "/register", 
        "/login", 
        "/first-time-setup", 
        "/check-user",
        "/api/site/purchase",
        "/create-checkout-session",
        "/create-pagarme-pix",
        "/admin/login",
        "/debug/stripe"
    ]
    
    # ✅ ROTAS PÚBLICAS POR PREFIXO
    public_prefixes = [
        "/api/direct-crypto/",
        "/api/vault/"
    ]
    
    # Exclui rotas de admin e OPTIONS
    if request.path.startswith("/api/site/admin") or request.method == "OPTIONS":
        return
        
    # ✅ Verificar se é rota pública por caminho exato
    if request.path in public_routes:
        return
        
    # ✅ Verificar se é rota pública por prefixo
    if any(request.path.startswith(prefix) for prefix in public_prefixes):
        return

    # Rotas protegidas (requerem token)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    user_id = get_user_id_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid authentication token"}), 401
    
    request.user_id = user_id

# 🛒 ROTA DE COMPRA (USADA PELO FRONTEND) - CORREÇÃO CRÍTICA
@app.route('/api/site/purchase', methods=['POST'])
def site_purchase():
    """Registrar uma compra de ALZ - CORREÇÃO URGENTE DOS VALORES"""
    data = request.json
    email = data.get('email')
    amount = data.get('amount') # Este é o valor em ALZ (do frontend Buy.jsx)
    method = data.get('method')
    sourceName = data.get('sourceName')  # Para PIX
    wallet_address_from_user = data.get('wallet_address')  # ✅ NOVO: Wallet address do usuário
    use_own_wallet = data.get('use_own_wallet', False)  # ✅ NOVO: Flag se usa wallet própria
    network = data.get('network')  # ✅ NOVO: Rede selecionada
    currency = data.get('currency', 'usd')  # ✅ NOVO: Moeda
    
    if not email or not amount or not method:
        return jsonify({"error": "Email, amount e method são obrigatórios"}), 400
    
    try:
        amount_alz = float(amount)  # ✅ CORRIGIDO: Buy.jsx envia amount em ALZ
    except ValueError:
        return jsonify({"error": "Valor (amount) inválido"}), 400
    
    if amount_alz <= 0:
        return jsonify({"error": "Valor (amount) deve ser positivo"}), 400
    
    # ✅ CORRIGIDO: Calcular USD e BRL a partir do ALZ
    # 1 ALZ = $0,10 USD (valor atualizado)
    amount_usd = amount_alz * 0.10  # 1 ALZ = $0,10 USD
    # Para compatibilidade, calcular BRL usando cotação (assumindo ~5.50)
    usd_to_brl_rate = 5.50  # Taxa aproximada USD/BRL
    amount_brl = amount_usd * usd_to_brl_rate  # Para registro no banco
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # ✅ VERIFICAR E CRIAR COLUNAS FALTANTES SE NÃO EXISTIREM
        def check_column_exists(column_name):
            """Verifica se uma coluna existe na tabela payments"""
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='payments' AND column_name=%s
                """, (column_name,))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"⚠️  Erro ao verificar coluna {column_name}: {e}")
                return False
        
        def create_column_if_not_exists(column_name, column_type, default_value=None):
            """Cria uma coluna se ela não existir"""
            if not check_column_exists(column_name):
                try:
                    if default_value is not None:
                        cursor.execute(f"""
                            ALTER TABLE payments 
                            ADD COLUMN {column_name} {column_type} DEFAULT %s
                        """, (default_value,))
                    else:
                        cursor.execute(f"""
                            ALTER TABLE payments 
                            ADD COLUMN {column_name} {column_type}
                        """)
                    conn.commit()
                    print(f"✅ Coluna '{column_name}' criada com sucesso")
                    return True
                except Exception as e:
                    print(f"⚠️  Não foi possível criar coluna {column_name}: {e}")
                    conn.rollback()
                    return False
            return True
        
        # Verificar e criar colunas necessárias
        has_expires_at = check_column_exists('expires_at')
        has_currency = check_column_exists('currency')
        has_network = check_column_exists('network')
        
        # Tentar criar colunas faltantes
        if not has_expires_at:
            try:
                from payment_expiration import add_expires_at_column
                add_expires_at_column()
                has_expires_at = check_column_exists('expires_at')
            except Exception as e:
                print(f"⚠️  Não foi possível criar coluna expires_at: {e}")
        
        if not has_currency:
            create_column_if_not_exists('currency', 'VARCHAR(10)', 'usd')
            has_currency = check_column_exists('currency')
        
        if not has_network:
            create_column_if_not_exists('network', 'VARCHAR(50)')
            has_network = check_column_exists('network')
        
        # ✅ CORRIGIDO: Calcular USD e BRL a partir do ALZ
        # 1 ALZ = $0,10 USD (valor atualizado)
        amount_usd = amount_alz * 0.10  # 1 ALZ = $0,10 USD
        # Para compatibilidade, calcular BRL usando cotação (assumindo ~5.50)
        usd_to_brl_rate = 5.50  # Taxa aproximada USD/BRL
        amount_brl = amount_usd * usd_to_brl_rate  # Para registro no banco
        
        # ✅ DEBUG PARA VERIFICAR VALORES
        print(f"🔢 DEBUG VALORES: {amount_alz} ALZ → ${amount_usd} USD → R$ {amount_brl} | Wallet: {wallet_address_from_user or 'Não fornecida'}")
        
        # Preparar metadata
        metadata = {
            'alz_amount': float(amount_alz),
            'amount_usd': float(amount_usd),  # ✅ NOVO: Salvar também em USD
            'network': network,
            'currency': currency,
            'use_own_wallet': use_own_wallet,
            'usd_to_brl_rate': usd_to_brl_rate
        }
        if sourceName:
            metadata['source_name'] = sourceName
        if wallet_address_from_user:
            metadata['user_wallet_address'] = wallet_address_from_user
        
        # ✅ Construir INSERT dinamicamente baseado nas colunas disponíveis
        expires_at = datetime.now(timezone.utc) + timedelta(days=10)
        
        # Construir lista de colunas e valores dinamicamente
        columns = ['email', 'amount', 'method', 'status', 'metadata', 'wallet_address']
        values = [email, amount_brl, method, 'pending', json.dumps(metadata), wallet_address_from_user]
        
        if has_expires_at:
            columns.append('expires_at')
            values.append(expires_at)
        
        if has_currency:
            columns.append('currency')
            values.append(currency)
        
        if has_network:
            columns.append('network')
            values.append(network)
        
        # Construir query SQL dinamicamente
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        insert_query = f"INSERT INTO payments ({columns_str}) VALUES ({placeholders}) RETURNING id"
        
        print(f"✅ INSERT será executado com colunas: {columns_str}")
        
        # ✅ INSERT com tratamento de erro detalhado
        try:
            cursor.execute(insert_query, tuple(values))
            print(f"✅ INSERT executado com sucesso")
            
            result = cursor.fetchone()
            if not result:
                raise Exception("INSERT não retornou ID do pagamento")
            
            payment_id = result['id']
            print(f"✅ Compra registrada: ID {payment_id} | {amount_alz} ALZ = ${amount_usd} USD = R$ {amount_brl} | Método: {method} | Wallet: {wallet_address_from_user or 'Gerada automaticamente'}")
        except Exception as insert_error:
            print(f"❌ ERRO NO INSERT: {insert_error}")
            print(f"❌ Query: {insert_query}")
            print(f"❌ Valores: {values}")
            print(f"❌ Dados do INSERT: email={email}, amount_brl={amount_brl}, method={method}, wallet={wallet_address_from_user}")
            raise  # Re-raise para ser capturado pelo except externo
        
        # Buscar usuário existente
        cursor.execute("SELECT id, wallet_address, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        user_created = False
        wallet_address = None
        user_id = None
        
        if not user:
            # ✅ Se usuário forneceu wallet, usar ela. Senão, NÃO gerar (usará wallet Allianza)
            if wallet_address_from_user and use_own_wallet:
                wallet_address = wallet_address_from_user
                private_key = None  # Não temos a private key se o usuário forneceu a wallet
                print(f"💼 Usando wallet fornecida pelo usuário: {wallet_address}")
            else:
                # ✅ NÃO gerar wallet - usuário usará wallet Allianza (saldo bloqueado)
                wallet_address = None
                private_key = None
                print(f"💼 Wallet não fornecida - tokens serão bloqueados na wallet Allianza")
            
            temp_password = f"temp_{secrets.token_hex(8)}"
            hashed_password = generate_password_hash(temp_password)
            nickname = f"User_{email.split('@')[0]}"
            
            cursor.execute(
                "INSERT INTO users (email, password, nickname, wallet_address, private_key) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (email, hashed_password, nickname, wallet_address, private_key)
            )
            user_id = cursor.fetchone()['id']
            user_created = True
            print(f"👤 Usuário criado com senha temporária: {email}")
        else:
            user_id = user['id']
            # ✅ Se usuário forneceu wallet e quer usar própria, atualizar
            if wallet_address_from_user and use_own_wallet:
                cursor.execute(
                    "UPDATE users SET wallet_address = %s WHERE id = %s",
                    (wallet_address_from_user, user_id)
                )
                wallet_address = wallet_address_from_user
                print(f"💼 Wallet do usuário atualizada: {wallet_address}")
            else:
                # ✅ Se usuário não forneceu wallet, usar None (não usar wallet existente do usuário)
                wallet_address = wallet_address_from_user if wallet_address_from_user and use_own_wallet else None
            print(f"👤 Usuário existente: {email} - ID: {user_id}")
        
        # Verificar/criar saldo
        cursor.execute("SELECT user_id FROM balances WHERE user_id = %s AND asset = 'ALZ'", (user_id,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO balances (user_id, asset, available, locked, staking_balance) VALUES (%s, 'ALZ', 0, 0, 0)",
                (user_id,)
            )
            print(f"💰 Saldo criado para usuário {user_id}")
        
        # ✅ SE NÃO TEM WALLET_ADDRESS, BLOQUEAR TOKENS (adicionar em locked)
        # O usuário verá o saldo bloqueado quando fizer login na wallet Allianza
        if not wallet_address_from_user or not use_own_wallet:
            cursor.execute(
                "UPDATE balances SET locked = locked + %s WHERE user_id = %s AND asset = 'ALZ'",
                (amount_alz, user_id)
            )
            print(f"🔒 Tokens bloqueados: {amount_alz} ALZ adicionados em locked (usuário verá ao fazer login)")
        else:
            # Se tem wallet externa, adicionar em available (será enviado depois)
            cursor.execute(
                "UPDATE balances SET available = available + %s WHERE user_id = %s AND asset = 'ALZ'",
                (amount_alz, user_id)
            )
            print(f"✅ Tokens disponíveis: {amount_alz} ALZ adicionados em available (para envio externo)")
        
        # ✅ Atualizar o registro de pagamento com o user_id e wallet_address final
        # ✅ IMPORTANTE: Só salvar wallet_address se foi fornecida pelo usuário
        final_wallet_address = wallet_address_from_user if (wallet_address_from_user and use_own_wallet) else None
        cursor.execute(
            "UPDATE payments SET user_id = %s, wallet_address = %s WHERE id = %s",
            (user_id, final_wallet_address, payment_id)
        )
        print(f"💾 Payment atualizado: user_id={user_id}, wallet_address={final_wallet_address or 'None (wallet Allianza)'}")
        
        conn.commit()
        
        # Registrar transação na blockchain Allianza
        if ALLIANZA_BLOCKCHAIN_AVAILABLE:
            try:
                blockchain_service = get_allianza_blockchain_service()
                blockchain_result = blockchain_service.register_purchase_transaction(
                    user_id=user_id,
                    amount=amount_alz,
                    payment_method=method,
                    metadata={
                        "payment_id": payment_id,
                        "amount_brl": amount_brl,
                        "email": email
                    }
                )
                if blockchain_result.get('success'):
                    print(f"✅ Transação registrada na blockchain: {blockchain_result.get('tx_hash')}")
            except Exception as e:
                print(f"⚠️  Erro ao registrar na blockchain: {e}")
        
        return jsonify({
            "success": True,
            "message": "Compra processada com sucesso! Aguarde a confirmação do pagamento.",
            "payment_id": payment_id,
            "user_created": user_created,
            "wallet_address": wallet_address,
            "user_id": user_id,
            "calculated_alz": amount_alz,  # ✅ Para debug
            "received_brl": amount_brl    # ✅ Para debug
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro no processamento da compra: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 💰 ROTA PARA CRIAR SESSÃO STRIPE - PRODUÇÃO (CORRIGIDA)
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Criar sessão de checkout Stripe - PRODUÇÃO COM VALORES CORRETOS"""
    
    if not STRIPE_AVAILABLE:
        return jsonify({
            'error': 'Stripe não disponível no servidor',
            'stripe_available': False
        }), 503
        
    try:
        data = request.json
        amount_brl_cents = data.get('amount')  # Valor em centavos de BRL (ex: R$ 0,10 = 10 centavos)
        email = data.get('email')
        currency = data.get('currency', 'brl')
        
        if not amount_brl_cents or not email:
            return jsonify({"error": "Valor e email são obrigatórios"}), 400
            
        # ✅ CORRIGIDO: Calcular valor em ALZ corretamente
        # amount_brl_cents é o valor em centavos de BRL (ex: 10 centavos = R$ 0,10)
        amount_brl = amount_brl_cents / 100  # Converter para BRL
        # ✅ ATUALIZADO: Converter BRL → USD → ALZ (1 ALZ = $0,10 USD)
        usd_to_brl_rate = 5.50
        amount_usd = amount_brl / usd_to_brl_rate  # BRL → USD
        amount_alz = amount_usd / 0.10  # USD → ALZ (1 ALZ = $0,10 USD)
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Tokens Allianza (ALZ)',
                    },
                    'unit_amount': amount_brl_cents,  # Valor em centavos
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=email,
            success_url=request.url_root + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.url_root + 'cancel',
            metadata={
                'email': email,
                'amount_brl': amount_brl,
                'amount_alz': amount_alz,
                'method': 'stripe'
            }
        )
        
        return jsonify({'url': session.url})
        
    except Exception as e:
        print(f"❌ Erro ao criar sessão Stripe: {e}")
        return jsonify({'error': str(e)}), 500

# 🧾 ROTA PARA PAGAR.ME PIX - CORRIGIDA SEM VALOR FIXO
@app.route('/create-pagarme-pix', methods=['POST'])
def create_pagarme_pix():
    """Criar pagamento PIX via Pagar.me - USUÁRIO DIGITA O VALOR"""
    
    try:
        data = request.json
        amount_brl = data.get('amount')  # Valor em BRL (apenas para referência/registro)
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "Email é obrigatório"}), 400
            
        # ✅ CORREÇÃO: NÃO enviar amount na URL do Pagar.me
        # O usuário digitará o valor diretamente no checkout do Pagar.me
        pagarme_url = f"{PAGARME_PIX_URL}?checkout[customer][email]={email}"
        
        print(f"🧾 Criando PIX Pagar.me para: {email}")
        print(f"🔗 URL: {pagarme_url}")
        print(f"💡 Valor será definido pelo usuário no checkout Pagar.me")
        
        # ✅ CORREÇÃO: Registrar o pagamento SEM amount fixo
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            
            # ✅ CORRIGIDO: Se tiver amount, usar para cálculo interno
            amount_alz = 0
            if amount_brl:
                # ✅ ATUALIZADO: Converter BRL → USD → ALZ (1 ALZ = $0,10 USD)
                usd_to_brl_rate = 5.50
                amount_usd = float(amount_brl) / usd_to_brl_rate  # BRL → USD
                amount_alz = amount_usd / 0.10  # USD → ALZ
                print(f"💰 Valor de referência: R$ {amount_brl} = ${amount_usd} USD = {amount_alz} ALZ")
            else:
                print("💰 Valor será definido pelo usuário no Pagar.me")
            
            # ✅ Registrar com método CORRETO 'pix' e amount 0 (será atualizado depois)
            # ✅ Definir expires_at = created_at + 10 dias
            expires_at = datetime.now(timezone.utc) + timedelta(days=10)
            cursor.execute(
                "INSERT INTO payments (email, amount, method, status, metadata, expires_at) VALUES (%s, %s, %s, 'pending', %s, %s) RETURNING id",
                (email, float(amount_brl) if amount_brl else 0, 'pix', json.dumps({
                    'alz_amount': amount_alz,
                    'user_defined_amount': True,  # ✅ Flag indicando que o valor será definido pelo usuário
                    'pagarme_checkout': True,
                    'note': 'Usuário definirá o valor no Pagar.me'
                }), expires_at)
            )
            payment_id = cursor.fetchone()['id']
            
            conn.commit()
            print(f"✅ Pagamento PIX registrado: ID {payment_id} | Email: {email} | Método: pix")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Erro ao registrar pagamento PIX: {e}")
            return jsonify({"error": "Erro ao registrar pagamento"}), 500
        finally:
            conn.close()
        
        return jsonify({
            "success": True,
            "url": pagarme_url,
            "email": email,
            "method": "pix",
            "payment_id": payment_id,
            "user_defined_amount": True,  # ✅ Informar ao frontend que o valor será definido pelo usuário
            "note": "O valor será definido pelo usuário no checkout do Pagar.me"
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao criar PIX Pagar.me: {e}")
        return jsonify({"error": str(e)}), 500

# 🎣 WEBHOOK STRIPE (CORRIGIDO)
@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Receber eventos do Stripe - COM VALORES CORRETOS"""
    if not STRIPE_AVAILABLE:
        return jsonify({'error': 'Stripe not available'}), 503
        
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        email = session.get('customer_email')
        metadata = session.get('metadata', {})
        amount_alz = metadata.get('amount_alz')
        
        if email and amount_alz:
            try:
                amount_alz = float(amount_alz)
                result = process_automatic_payment(email, amount_alz, 'stripe', session.id)
                if result['success']:
                    print(f"✅ Pagamento Stripe processado com sucesso para {email}. {amount_alz} ALZ creditados.")
                else:
                    print(f"❌ Falha ao creditar tokens para {email}: {result['error']}")
            except Exception as e:
                print(f"❌ Erro ao processar pagamento Stripe: {e}")

    return 'OK', 200

# ==================== ROTAS PARA PAGAMENTO DIRETO COM CRIPTO ====================

@app.route('/api/direct-crypto/create-payment', methods=['POST', 'OPTIONS'])
def create_direct_crypto_payment():
    """Criar pagamento direto com criptomoedas - SEM INTERMEDIÁRIOS"""
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        if not DIRECT_CRYPTO_AVAILABLE:
            return jsonify({
                "success": False, 
                "error": "Sistema de pagamento direto temporariamente indisponível"
            }), 503
            
        data = request.json
        email = data.get('email')
        amount_brl = data.get('amount_brl')
        currency = data.get('currency', 'USDT')
        
        if not email or not amount_brl:
            return jsonify({"error": "Email e valor são obrigatórios"}), 400
            
        # Validar valor mínimo
        try:
            amount_brl = float(amount_brl)
            if amount_brl < 5.50:
                return jsonify({"error": "Valor mínimo: R$ 5,50"}), 400
        except ValueError:
            return jsonify({"error": "Valor inválido"}), 400
        
        print(f"🔄 Criando pagamento direto para {email} - R$ {amount_brl} - {currency}")
        
        # 1. Registrar pagamento pendente no DB primeiro
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            
            # Buscar ou criar usuário
            cursor.execute("SELECT id, wallet_address, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            user_id = None
            wallet_address = None
            
            if not user:
                # ✅ NÃO gerar wallet - usuário usará wallet Allianza (saldo bloqueado)
                wallet_address = None
                private_key = None
                temp_password = f"temp_{secrets.token_hex(8)}"
                hashed_password = generate_password_hash(temp_password)
                nickname = f"User_{email.split('@')[0]}"
                
                cursor.execute(
                    "INSERT INTO users (email, password, nickname, wallet_address, private_key) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (email, hashed_password, nickname, wallet_address, private_key)
                )
                user_id = cursor.fetchone()['id']
                print(f"👤 Usuário criado: {email} - Wallet Allianza (será gerada no login)")
            else:
                user_id = user['id']
                wallet_address = user['wallet_address']  # Pode ser None se não tiver wallet ainda
                print(f"👤 Usuário existente: {email}")

            # Verificar/criar saldo
            cursor.execute("SELECT user_id FROM balances WHERE user_id = %s AND asset = 'ALZ'", (user_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO balances (user_id, asset, available, locked, staking_balance) VALUES (%s, 'ALZ', 0, 0, 0)",
                    (user_id,)
                )
                print(f"💰 Saldo criado para user {user_id}")

            # ✅ CORRIGIDO: Calcular ALZ (com bônus de 2% para crypto)
            # ✅ ATUALIZADO: Converter BRL → USD → ALZ (1 ALZ = $0,10 USD)
            usd_to_brl_rate = 5.50
            amount_usd = amount_brl / usd_to_brl_rate  # BRL → USD
            base_alz = amount_usd / 0.10  # USD → ALZ (1 ALZ = $0,10 USD)
            bonus_alz = base_alz * 0.02
            total_alz = base_alz + bonus_alz
            
            # Registrar pagamento pendente
            # ✅ Definir expires_at = created_at + 10 dias
            expires_at = datetime.now(timezone.utc) + timedelta(days=10)
            cursor.execute(
                "INSERT INTO payments (email, amount, method, status, user_id, metadata, expires_at) VALUES (%s, %s, %s, 'pending', %s, %s, %s) RETURNING id",
                (email, amount_brl, 'direct_crypto', user_id, json.dumps({
                    'alz_amount': total_alz,
                    'base_alz': base_alz,
                    'bonus_alz': bonus_alz,
                    'currency': currency,
                    'direct_crypto_pending': True,
                    'user_created': user_id is not None
                }), expires_at)
            )
            db_payment_id = cursor.fetchone()['id']
            
            conn.commit()
            print(f"✅ Pagamento direto registrado no DB: ID {db_payment_id}")

        except Exception as e:
            conn.rollback()
            print(f"❌ Erro ao registrar pagamento direto no DB: {e}")
            return jsonify({"error": "Erro interno ao registrar pagamento"}), 500
        finally:
            conn.close()

        # 2. Criar pagamento direto
        result = direct_crypto_service.create_direct_payment(email, amount_brl, currency)
        
        if result['success']:
            # 3. Atualizar pagamento com ID do pagamento direto
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE payments SET tx_hash = %s, metadata = metadata || %s WHERE id = %s",
                    (result['payment_id'], json.dumps({
                        'direct_payment_id': result['payment_id'],
                        'master_wallet': result['payment_data']['master_wallet'],
                        'network': result['payment_data']['network'],
                        'required_amount': result['payment_data']['required_amount']
                    }), db_payment_id)
                )
                conn.commit()
                print(f"✅ Pagamento atualizado com Direct Payment ID: {result['payment_id']}")
            except Exception as e:
                print(f"⚠️ Aviso: Não foi possível atualizar Direct Payment ID: {e}")
            finally:
                conn.close()
                
            return jsonify({
                "success": True,
                "payment_id": result['payment_id'],
                "db_payment_id": db_payment_id,
                "payment_data": result['payment_data'],
                "alz_info": {
                    "base_alz": base_alz,
                    "bonus_alz": bonus_alz,
                    "total_alz": total_alz
                },
                "email": email
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result['error']
            }, 500)

    except Exception as e:
        print(f"❌ Erro ao criar pagamento direto: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/direct-crypto/payment-status/<payment_id>', methods=['GET'])
def get_direct_crypto_payment_status(payment_id):
    """Obter status de um pagamento direto"""
    try:
        if not DIRECT_CRYPTO_AVAILABLE:
            return jsonify({
                "success": False, 
                "error": "Sistema de pagamento direto temporariamente indisponível"
            }), 503
            
        # Buscar no banco
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.status, p.metadata, p.email, p.amount, p.tx_hash,
                   p.created_at, p.processed_at, p.method,
                   u.wallet_address, u.nickname
            FROM payments p 
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.id = %s OR p.tx_hash = %s
        ''', (payment_id, payment_id))
        
        payment = cursor.fetchone()
        
        if not payment:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        
        payment_data = dict(payment)
        
        # Buscar status do serviço direto
        direct_status = direct_crypto_service.get_payment_status(payment_id)
        
        # Calcular ALZ
        amount_brl = float(payment_data['amount'])
        metadata = payment_data['metadata'] or {}
        
        if metadata.get('alz_amount'):
            total_alz = float(metadata['alz_amount'])
            base_alz = float(metadata.get('base_alz', total_alz))
            bonus_alz = float(metadata.get('bonus_alz', 0))
        else:
            # ✅ CORRIGIDO: Converter BRL → USD → ALZ (1 ALZ = $0,10 USD)
            usd_to_brl_rate = 5.50
            amount_usd = amount_brl / usd_to_brl_rate  # BRL → USD
            base_alz = amount_usd / 0.10  # USD → ALZ (1 ALZ = $0,10 USD)
            bonus_alz = base_alz * 0.02
            total_alz = base_alz + bonus_alz
        
        response_data = {
            "success": True,
            "payment_id": payment_data['id'],
            "status": payment_data['status'],
            "direct_status": direct_status,
            "email": payment_data['email'],
            "amount_brl": amount_brl,
            "alz_info": {
                "base_alz": base_alz,
                "bonus_alz": bonus_alz,
                "total_alz": total_alz
            },
            "method": payment_data['method'],
            "direct_payment_id": payment_data['tx_hash'],
            "created_at": payment_data['created_at'].isoformat() if hasattr(payment_data['created_at'], 'isoformat') else str(payment_data['created_at']),
            "user": {
                "wallet_address": payment_data['wallet_address'],
                "nickname": payment_data['nickname']
            } if payment_data['wallet_address'] else None
        }
        
        # Adicionar processed_at se existir
        if payment_data['processed_at']:
            response_data["processed_at"] = payment_data['processed_at'].isoformat() if hasattr(payment_data['processed_at'], 'isoformat') else str(payment_data['processed_at'])
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f'❌ Erro ao buscar status direto: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/direct-crypto/verify-payment', methods=['POST'])
@admin_required
def verify_direct_payment():
    """Verificar manualmente um pagamento direto (apenas admin)"""
    try:
        data = request.json
        payment_id = data.get('payment_id')
        tx_hash = data.get('tx_hash')
        
        if not payment_id or not tx_hash:
            return jsonify({"error": "payment_id e tx_hash são obrigatórios"}), 400
            
        # Verificar no serviço direto
        result = direct_crypto_service.verify_payment_manual(payment_id, tx_hash)
        
        if result['success']:
            # Atualizar no banco
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("BEGIN")
                
                # Buscar pagamento
                cursor.execute("SELECT id, user_id, email, amount, metadata FROM payments WHERE tx_hash = %s", (payment_id,))
                payment = cursor.fetchone()
                
                if not payment:
                    return jsonify({"error": "Pagamento não encontrado no banco"}), 404
                
                # ✅ CORRIGIDO: Processar pagamento automaticamente
                metadata = payment['metadata'] or {}
                if metadata.get('alz_amount'):
                    alz_amount = float(metadata['alz_amount'])
                else:
                    # ✅ ATUALIZADO: Converter BRL → USD → ALZ (1 ALZ = $0,10 USD)
                    usd_to_brl_rate = 5.50
                    amount_usd = float(payment['amount']) / usd_to_brl_rate  # BRL → USD
                    alz_amount = amount_usd / 0.10  # USD → ALZ
                
                payment_result = process_automatic_payment(
                    payment['email'], 
                    alz_amount, 
                    'direct_crypto', 
                    tx_hash
                )
                
                if payment_result['success']:
                    cursor.execute(
                        "UPDATE payments SET status = 'completed', processed_at = %s WHERE id = %s",
                        (datetime.utcnow(), payment['id'])
                    )
                    conn.commit()
                    
                    return jsonify({
                        "success": True,
                        "message": f"Pagamento verificado e {alz_amount} ALZ creditados para {payment['email']}",
                        "payment": result['payment']
                    }), 200
                else:
                    conn.rollback()
                    return jsonify({
                        "success": False,
                        "error": f"Erro ao creditar tokens: {payment_result['error']}"
                    }), 500
                    
            except Exception as e:
                conn.rollback()
                print(f"❌ Erro ao verificar pagamento no banco: {e}")
                return jsonify({"error": str(e)}), 500
            finally:
                conn.close()
        else:
            return jsonify(result), 400
            
    except Exception as e:
        print(f"❌ Erro na verificação manual: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/direct-crypto/supported-currencies', methods=['GET'])
def get_supported_currencies():
    """Obter moedas suportadas para pagamento direto"""
    try:
        if not DIRECT_CRYPTO_AVAILABLE:
            return jsonify({
                "success": False, 
                "error": "Sistema de pagamento direto temporariamente indisponível"
            }), 503
            
        result = direct_crypto_service.get_supported_currencies()
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Erro ao buscar moedas suportadas: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== ROTAS DO COFRE SEGURO ====================

def calculate_security_level(cold_percentage):
    """Calcular nível de segurança baseado na porcentagem no cold wallet"""
    if cold_percentage >= 80:
        return 'maximum'
    elif cold_percentage >= 60:
        return 'high'
    elif cold_percentage >= 40:
        return 'medium'
    else:
        return 'low'

@app.route('/api/vault/balance', methods=['GET'])
def get_vault_balance():
    """Obter saldo do cofre do usuário"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id é obrigatório"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Buscar ou criar registro do cofre
        cursor.execute('''
            INSERT INTO vault_balances (user_id, hot_wallet, cold_wallet) 
            VALUES (%s, 0.0, 0.0)
            ON CONFLICT (user_id) DO UPDATE SET updated_at = CURRENT_TIMESTAMP
            RETURNING hot_wallet, cold_wallet, security_level, auto_transfer_threshold, transfer_count, last_transfer_at
        ''', (user_id,))
        
        result = cursor.fetchone()
        
        total_balance = float(result['hot_wallet'] + result['cold_wallet'])
        cold_percentage = (float(result['cold_wallet']) / total_balance * 100) if total_balance > 0 else 0
        
        vault_data = {
            "hot_wallet": float(result['hot_wallet']),
            "cold_wallet": float(result['cold_wallet']),
            "security_level": result['security_level'],
            "auto_transfer_threshold": float(result['auto_transfer_threshold']),
            "transfer_count": result['transfer_count'],
            "total_balance": total_balance,
            "cold_percentage": cold_percentage,
            "last_transfer_at": result['last_transfer_at'].isoformat() if result['last_transfer_at'] else None
        }
        
        conn.commit()
        
        return jsonify({
            "success": True,
            "vault": vault_data
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao buscar saldo do cofre: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/vault/transfer', methods=['POST'])
def transfer_between_wallets():
    """Transferir entre hot e cold wallet"""
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    direction = data.get('direction')  # 'to_cold' ou 'to_hot'
    description = data.get('description', 'Transferência entre carteiras')
    
    if not all([user_id, amount, direction]):
        return jsonify({"error": "user_id, amount e direction são obrigatórios"}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount deve ser positivo"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Amount deve ser um número válido"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Buscar saldo atual do cofre com bloqueio para evitar condições de corrida
        cursor.execute('''
            SELECT hot_wallet, cold_wallet 
            FROM vault_balances 
            WHERE user_id = %s 
            FOR UPDATE
        ''', (user_id,))
        
        vault_balance = cursor.fetchone()
        
        if not vault_balance:
            # Criar registro se não existir
            cursor.execute('''
                INSERT INTO vault_balances (user_id, hot_wallet, cold_wallet) 
                VALUES (%s, 0.0, 0.0)
                RETURNING hot_wallet, cold_wallet
            ''', (user_id,))
            vault_balance = cursor.fetchone()
        
        # Verificar saldo suficiente
        if direction == 'to_cold':
            if amount > float(vault_balance['hot_wallet']):
                return jsonify({"error": "Saldo insuficiente na hot wallet"}), 400
            
            new_hot = float(vault_balance['hot_wallet']) - amount
            new_cold = float(vault_balance['cold_wallet']) + amount
            
        elif direction == 'to_hot':
            if amount > float(vault_balance['cold_wallet']):
                return jsonify({"error": "Saldo insuficiente na cold wallet"}), 400
            
            new_hot = float(vault_balance['hot_wallet']) + amount
            new_cold = float(vault_balance['cold_wallet']) - amount
        
        else:
            return jsonify({"error": "Direction deve ser 'to_cold' ou 'to_hot'"}), 400
        
        # Atualizar saldos
        cursor.execute('''
            UPDATE vault_balances 
            SET hot_wallet = %s, 
                cold_wallet = %s,
                last_transfer_at = CURRENT_TIMESTAMP,
                transfer_count = transfer_count + 1,
                security_level = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        ''', (new_hot, new_cold, 
              calculate_security_level((new_cold / (new_hot + new_cold)) * 100 if (new_hot + new_cold) > 0 else 0),
              user_id))
        
        # Registrar no ledger
        entry_type = 'transfer_to_cold' if direction == 'to_cold' else 'transfer_to_hot'
        ledger_description = f"{description} - {amount} ALZ"
        
        cursor.execute('''
            INSERT INTO ledger_entries 
            (user_id, asset, amount, entry_type, description, idempotency_key)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user_id, 'ALZ', amount, entry_type, ledger_description, 
              f"vault_transfer_{user_id}_{datetime.now(timezone.utc).timestamp()}"))
        
        conn.commit()
        
        # Retornar dados atualizados
        cursor.execute('''
            SELECT hot_wallet, cold_wallet, security_level, transfer_count, last_transfer_at
            FROM vault_balances WHERE user_id = %s
        ''', (user_id,))
        
        updated_balance = cursor.fetchone()
        total = float(updated_balance['hot_wallet'] + updated_balance['cold_wallet'])
        cold_percentage = (float(updated_balance['cold_wallet']) / total * 100) if total > 0 else 0
        
        return jsonify({
            "success": True,
            "message": f"Transferência de {amount} ALZ realizada com sucesso",
            "vault": {
                "hot_wallet": float(updated_balance['hot_wallet']),
                "cold_wallet": float(updated_balance['cold_wallet']),
                "total_balance": total,
                "cold_percentage": cold_percentage,
                "security_level": updated_balance['security_level'],
                "transfer_count": updated_balance['transfer_count'],
                "last_transfer_at": updated_balance['last_transfer_at'].isoformat() if updated_balance['last_transfer_at'] else None
            }
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro na transferência do cofre: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/vault/initialize', methods=['POST'])
def initialize_vault():
    """Inicializar cofre com saldo inicial"""
    data = request.json
    user_id = data.get('user_id')
    initial_balance = data.get('initial_balance', 0)
    
    if not user_id:
        return jsonify({"error": "user_id é obrigatório"}), 400
    
    try:
        initial_balance = float(initial_balance)
        if initial_balance < 0:
            return jsonify({"error": "Saldo inicial não pode ser negativo"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Saldo inicial deve ser um número válido"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Verificar se já existe
        cursor.execute('SELECT user_id FROM vault_balances WHERE user_id = %s', (user_id,))
        existing_vault = cursor.fetchone()
        
        if existing_vault:
            return jsonify({"error": "Cofre já inicializado para este usuário"}), 400
        
        # Distribuir saldo inicial (80% cold, 20% hot por padrão)
        cold_amount = initial_balance * 0.8
        hot_amount = initial_balance * 0.2
        
        cursor.execute('''
            INSERT INTO vault_balances 
            (user_id, hot_wallet, cold_wallet, security_level) 
            VALUES (%s, %s, %s, %s)
        ''', (user_id, hot_amount, cold_amount, 'maximum'))
        
        # Registrar no ledger se houver saldo inicial
        if initial_balance > 0:
            cursor.execute('''
                INSERT INTO ledger_entries 
                (user_id, asset, amount, entry_type, description, idempotency_key)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (user_id, 'ALZ', initial_balance, 'vault_initialization', 
                  f"Inicialização do cofre com {initial_balance} ALZ",
                  f"vault_init_{user_id}_{datetime.now(timezone.utc).timestamp()}"))
        
        conn.commit();
        
        return jsonify({
            "success": True,
            "message": f"Cofre inicializado com {initial_balance} ALZ",
            "vault": {
                "hot_wallet": float(hot_amount),
                "cold_wallet": float(cold_amount),
                "total_balance": float(initial_balance),
                "cold_percentage": 80.0,
                "security_level": 'maximum',
                "transfer_count": 0
            }
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao inicializar cofre: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/vault/security/settings', methods=['POST'])
def update_security_settings():
    """Atualizar configurações de segurança do cofre"""
    data = request.json
    user_id = data.get('user_id')
    auto_transfer_threshold = data.get('auto_transfer_threshold')
    security_level = data.get('security_level')
    
    if not user_id:
        return jsonify({"error": "user_id é obrigatório"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Verificar se cofre existe
        cursor.execute('SELECT user_id FROM vault_balances WHERE user_id = %s', (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Cofre não encontrado para este usuário"}), 404
        
        update_fields = []
        params = []
        
        if auto_transfer_threshold is not None:
            try:
                threshold = float(auto_transfer_threshold)
                if threshold < 0:
                    return jsonify({"error": "Threshold não pode ser negativo"}), 400
                update_fields.append("auto_transfer_threshold = %s")
                params.append(threshold)
            except (ValueError, TypeError):
                return jsonify({"error": "Auto transfer threshold deve ser um número válido"}), 400
        
        if security_level and security_level in ['low', 'medium', 'high', 'maximum']:
            update_fields.append("security_level = %s")
            params.append(security_level)
        
        if not update_fields:
            return jsonify({"error": "Nenhum campo para atualizar"}), 400
        
        params.append(user_id)
        
        cursor.execute(f'''
            UPDATE vault_balances 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        ''', params)
        
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": "Configurações de segurança atualizadas com sucesso"
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao atualizar configurações de segurança: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/vault/stats', methods=['GET'])
def get_vault_stats():
    """Obter estatísticas do cofre"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id é obrigatório"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Estatísticas do cofre
        cursor.execute('''
            SELECT 
                hot_wallet,
                cold_wallet,
                security_level,
                transfer_count,
                last_transfer_at,
                auto_transfer_threshold
            FROM vault_balances 
            WHERE user_id = %s
        ''', (user_id,))
        
        vault_data = cursor.fetchone()
        
        if not vault_data:
            return jsonify({"error": "Cofre não encontrado"}), 404
        
        total = float(vault_data['hot_wallet'] + vault_data['cold_wallet'])
        cold_percentage = (float(vault_data['cold_wallet']) / total * 100) if total > 0 else 0
        
        # Estatísticas de transferências recentes
        cursor.execute('''
            SELECT COUNT(*) as recent_transfers
            FROM ledger_entries 
            WHERE user_id = %s 
            AND entry_type IN ('transfer_to_cold', 'transfer_to_hot')
            AND created_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
        ''', (user_id,))
        
        recent_stats = cursor.fetchone()
        
        stats = {
            "total_balance": total,
            "hot_wallet": float(vault_data['hot_wallet']),
            "cold_wallet": float(vault_data['cold_wallet']),
            "cold_percentage": cold_percentage,
            "security_level": vault_data['security_level'],
            "total_transfers": vault_data['transfer_count'],
            "recent_transfers_7d": recent_stats['recent_transfers'],
            "auto_transfer_threshold": float(vault_data['auto_transfer_threshold']),
            "last_transfer": vault_data['last_transfer_at'].isoformat() if vault_data['last_transfer_at'] else None
        }
        
        return jsonify({
            "success": True,
            "stats": stats
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas do cofre: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# ==================== ROTAS DE SEGURANÇA DO COFRE ====================

@app.route('/api/vault/security/withdraw-request', methods=['POST'])
def request_withdraw_from_vault():
    """Solicitar retirada do cofre - requer autorização adicional"""
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    description = data.get('description', 'Retirada do cofre seguro')
    
    if not all([user_id, amount]):
        return jsonify({"error": "user_id e amount são obrigatórios"}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount deve ser positivo"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Amount deve ser um número válido"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Verificar saldo no cold wallet
        cursor.execute('''
            SELECT cold_wallet, security_level 
            FROM vault_balances 
            WHERE user_id = %s 
            FOR UPDATE
        ''', (user_id,))
        
        vault_balance = cursor.fetchone()
        
        if not vault_balance:
            return jsonify({"error": "Cofre não encontrado"}), 404
        
        if amount > float(vault_balance['cold_wallet']):
            return jsonify({"error": "Saldo insuficiente no cofre seguro"}), 400
        
        # Gerar código de autorização único
        auth_code = secrets.token_hex(6).upper()  # Código de 12 caracteres
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)  # Válido por 10 minutos
        
        # Registrar solicitação de retirada
        cursor.execute('''
            INSERT INTO vault_withdraw_requests 
            (user_id, amount, auth_code, expires_at, description, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
            RETURNING id, created_at
        ''', (user_id, amount, auth_code, expires_at, description))
        
        request_data = cursor.fetchone()
        
        conn.commit()
        
        # Em um sistema real, enviar o código por email/SMS
        print(f"🔐 Código de autorização para {user_id}: {auth_code} (Expira: {expires_at})")
        
        return jsonify({
            "success": True,
            "message": "Solicitação de retirada criada. Código de autorização necessário.",
            "withdraw_request_id": request_data['id'],
            "auth_code_required": True,
            "expires_at": expires_at.isoformat(),
            "note": "Em produção, este código seria enviado por email/SMS"
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao solicitar retirada: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/vault/security/confirm-withdraw', methods=['POST'])
def confirm_withdraw_from_vault():
    """Confirmar retirada do cofre com código de autorização"""
    data = request.json
    user_id = data.get('user_id')
    withdraw_request_id = data.get('withdraw_request_id')
    auth_code = data.get('auth_code')
    
    if not all([user_id, withdraw_request_id, auth_code]):
        return jsonify({"error": "user_id, withdraw_request_id e auth_code são obrigatórios"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Buscar solicitação de retirada
        cursor.execute('''
            SELECT id, user_id, amount, auth_code, expires_at, status, description
            FROM vault_withdraw_requests 
            WHERE id = %s AND user_id = %s AND status = 'pending'
            FOR UPDATE
        ''', (withdraw_request_id, user_id))
        
        withdraw_request = cursor.fetchone()
        
        if not withdraw_request:
            return jsonify({"error": "Solicitação de retirada não encontrada ou já processada"}), 404
        
        # Verificar se o código expirou
        if datetime.now(timezone.utc) > withdraw_request['expires_at']:
            cursor.execute('''
                UPDATE vault_withdraw_requests SET status = 'expired' WHERE id = %s
            ''', (withdraw_request_id,))
            conn.commit()
            return jsonify({"error": "Código de autorização expirado"}), 400
        
        # Verificar código de autorização
        if withdraw_request['auth_code'] != auth_code.upper().strip():
            return jsonify({"error": "Código de autorização inválido"}), 400
        
        # Verificar saldo novamente
        cursor.execute('''
            SELECT cold_wallet, hot_wallet 
            FROM vault_balances 
            WHERE user_id = %s 
            FOR UPDATE
        ''', (user_id,))
        
        vault_balance = cursor.fetchone()
        
        if not vault_balance:
            return jsonify({"error": "Cofre não encontrado"}), 404
        
        amount = float(withdraw_request['amount'])
        
        if amount > float(vault_balance['cold_wallet']):
            return jsonify({"error": "Saldo insuficiente no cofre seguro"}), 400
        
        # Realizar transferência
        new_cold = float(vault_balance['cold_wallet']) - amount
        new_hot = float(vault_balance['hot_wallet']) + amount
        
        cursor.execute('''
            UPDATE vault_balances 
            SET cold_wallet = %s, 
                hot_wallet = %s,
                last_transfer_at = CURRENT_TIMESTAMP,
                transfer_count = transfer_count + 1,
                security_level = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        ''', (new_cold, new_hot, 
              calculate_security_level((new_cold / (new_hot + new_cold)) * 100 if (new_hot + new_cold) > 0 else 0),
              user_id))
        
        # Registrar no ledger
        cursor.execute('''
            INSERT INTO ledger_entries 
            (user_id, asset, amount, entry_type, description, idempotency_key)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user_id, 'ALZ', amount, 'withdraw_from_vault', 
              f"Retirada do cofre seguro - {withdraw_request['description']}",
              f"vault_withdraw_{withdraw_request_id}"))
        
        # Marcar solicitação como concluída
        cursor.execute('''
            UPDATE vault_withdraw_requests 
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        ''', (withdraw_request_id,))
        
        conn.commit()
        
        # Retornar dados atualizados
        cursor.execute('''
            SELECT hot_wallet, cold_wallet, security_level, transfer_count, last_transfer_at
            FROM vault_balances WHERE user_id = %s
        ''', (user_id,))
        
        updated_balance = cursor.fetchone()
        total = float(updated_balance['hot_wallet'] + updated_balance['cold_wallet'])
        cold_percentage = (float(updated_balance['cold_wallet']) / total * 100) if total > 0 else 0
        
        return jsonify({
            "success": True,
            "message": f"Retirada de {amount} ALZ do cofre realizada com sucesso",
            "vault": {
                "hot_wallet": float(updated_balance['hot_wallet']),
                "cold_wallet": float(updated_balance['cold_wallet']),
                "total_balance": total,
                "cold_percentage": cold_percentage,
                "security_level": updated_balance['security_level'],
                "transfer_count": updated_balance['transfer_count'],
                "last_transfer_at": updated_balance['last_transfer_at'].isoformat() if updated_balance['last_transfer_at'] else None
            }
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao confirmar retirada: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/vault/security/cancel-withdraw', methods=['POST'])
def cancel_withdraw_request():
    """Cancelar solicitação de retirada pendente"""
    data = request.json
    user_id = data.get('user_id')
    withdraw_request_id = data.get('withdraw_request_id')
    
    if not all([user_id, withdraw_request_id]):
        return jsonify({"error": "user_id e withdraw_request_id são obrigatórios"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE vault_withdraw_requests 
            SET status = 'cancelled', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s AND status = 'pending'
        ''', (withdraw_request_id, user_id))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Solicitação não encontrada ou já processada"}), 404
        
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": "Solicitação de retirada cancelada"
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao cancelar solicitação: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Ajustar redirecionamento para garantir compatibilidade
@app.route('/health', methods=['GET', 'OPTIONS'])
def root_health_check():
    """Health check endpoint - sempre retorna JSON válido"""
    try:
        # Tentar verificar conexão com banco (opcional)
        try:
            from database_neon import get_db_connection
            conn = get_db_connection()
            conn.close()
            db_status = "connected"
        except:
            db_status = "unknown"
        
        return jsonify({
            "status": "ok",
            "message": "Backend is running",
            "database": db_status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200
    except Exception as e:
        # Mesmo em caso de erro, retornar JSON válido
        return jsonify({
            "status": "error",
            "message": "Backend is running but health check failed",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200

# 🚀 INICIALIZAÇÃO DO FLASK
if __name__ == '__main__':
    print("=" * 60)
    print("🔗 Rotas disponíveis:")
    print("🔗 Rotas públicas:")
    print("   - GET  /health")
    print("   - GET  /system/info")
    print("   - POST /register")
    print("   - POST /login")
    print("   - POST /first-time-setup")
    print("   - POST /check-user")
    print("   - POST /api/site/purchase")
    print("   - POST /create-checkout-session")
    print("   - POST /create-pagarme-pix")
    print("   - GET  /debug/stripe")
    print("🔗 Pagamento Direto Crypto (PÚBLICAS):")
    print("   - POST /api/direct-crypto/create-payment")
    print("   - GET  /api/direct-crypto/payment-status/<payment_id>")
    print("   - POST /api/direct-crypto/verify-payment (ADMIN)")
    print("   - GET  /api/direct-crypto/supported-currencies")
    print("🔗 Cofre Seguro (PÚBLICAS):")
    print("   - GET  /api/vault/balance")
    print("   - POST /api/vault/transfer")
    print("   - POST /api/vault/initialize")
    print("   - POST /api/vault/security/settings")
    print("   - GET  /api/vault/stats")
    print("🔗 Segurança do Cofre (PÚBLICAS):")
    print("   - POST /api/vault/security/withdraw-request")
    print("   - POST /api/vault/security/confirm-withdraw")
    print("   - POST /api/vault/security/cancel-withdraw")
    print("🔐 Rotas admin (requer token):")
    print("   - GET  /api/site/admin/payments")
    print("   - GET  /api/site/admin/stats")
    print("   - POST /api/site/admin/process-payments")
    print("   - POST /api/site/admin/manual-token-send")
    print("   - POST /api/site/admin/create-staking-table")
    print("   - GET  /api/site/admin/check-tables")
    print("📞 Webhooks:")
    print("   - POST /webhook/stripe")
    print("💰 Rotas protegidas:")
    print("   - GET  /balances/me")
    print("   - GET  /ledger/history")
    print("🎯 Staking Routes:")
    print("   - POST /staking/stake")
    print("   - POST /staking/unstake")
    print("   - POST /staking/claim-rewards")
    print("   - GET  /staking/me")
    print("   - GET  /staking/options")
    print("   - GET  /staking/stats")
    print("   - PUT  /staking/auto-compound/<stake_id>")
    print("=" * 60)
    
    try:
        app.run(debug=False, port=5000, host='0.0.0.0')
    except Exception as e:
        print(f"❌ Erro ao iniciar o servidor Flask: {e}")