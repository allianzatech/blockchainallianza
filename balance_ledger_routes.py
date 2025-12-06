"""
Rotas de Balances e Ledger para Allianza Wallet
"""
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from functools import wraps
from database_neon import get_db_connection

balance_ledger_bp = Blueprint('balance_ledger', __name__)

# Configurar CORS para o blueprint
CORS(balance_ledger_bp, resources={
    r"/*": {
        "origins": [
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
        "supports_credentials": True,
        "allow_headers": [
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})

# Middleware de autenticação
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

def get_user_id_from_token(token):
    """Extrair user_id do token mock"""
    try:
        parts = token.split("_")
        if len(parts) >= 3 and parts[0] == "mock" and parts[1] == "token":
            return int(parts[2])
    except (ValueError, IndexError):
        pass
    return None


@balance_ledger_bp.route('/balances/me', methods=['GET'])
@token_required
def get_my_balance():
    """Obter saldo do usuário autenticado"""
    try:
        user_id = request.user_id
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar saldo do usuário
        cursor.execute("""
            SELECT 
                user_id,
                asset,
                available,
                locked,
                staking_balance,
                updated_at
            FROM balances
            WHERE user_id = %s
        """, (user_id,))
        
        balance_row = cursor.fetchone()
        
        if not balance_row:
            # Criar saldo inicial se não existir
            cursor.execute("""
                INSERT INTO balances (user_id, asset, available, locked, staking_balance)
                VALUES (%s, 'ALZ', 0.0, 0.0, 0.0)
                RETURNING user_id, asset, available, locked, staking_balance, updated_at
            """, (user_id,))
            balance_row = cursor.fetchone()
            conn.commit()
        
        cursor.close()
        conn.close()
        
        # Formatar resposta
        balance_data = {
            "user_id": balance_row['user_id'],
            "asset": balance_row['asset'],
            "available": float(balance_row['available']),
            "locked": float(balance_row['locked']),
            "staking_balance": float(balance_row['staking_balance']),
            "total": float(balance_row['available']) + float(balance_row['locked']) + float(balance_row['staking_balance']),
            "updated_at": balance_row['updated_at'].isoformat() if balance_row['updated_at'] else None
        }
        
        return jsonify({
            "success": True,
            "balance": balance_data
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao buscar saldo: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@balance_ledger_bp.route('/ledger/history', methods=['GET'])
@token_required
def get_ledger_history():
    """Obter histórico de transações do ledger"""
    try:
        user_id = request.user_id
        
        # Parâmetros de paginação
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar histórico do ledger
        cursor.execute("""
            SELECT 
                id,
                user_id,
                asset,
                amount,
                entry_type,
                related_id,
                description,
                created_at,
                idempotency_key
            FROM ledger_entries
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (user_id, limit, offset))
        
        entries = cursor.fetchall()
        
        # Contar total de entradas
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM ledger_entries
            WHERE user_id = %s
        """, (user_id,))
        
        total_count = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        # Formatar resposta
        history = []
        for entry in entries:
            history.append({
                "id": entry['id'],
                "user_id": entry['user_id'],
                "asset": entry['asset'],
                "amount": float(entry['amount']),
                "entry_type": entry['entry_type'],
                "related_id": entry['related_id'],
                "description": entry['description'],
                "created_at": entry['created_at'].isoformat() if entry['created_at'] else None,
                "idempotency_key": entry['idempotency_key']
            })
        
        return jsonify({
            "success": True,
            "history": history,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total_count
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao buscar histórico: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@balance_ledger_bp.route('/login', methods=['POST'])
def login():
    """Autenticar usuário e retornar token"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar usuário por email
        cursor.execute("""
            SELECT id, email, password, nickname, wallet_address
            FROM users
            WHERE email = %s
        """, (email,))
        
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        # Verificar senha (simplificado - em produção use check_password_hash)
        from werkzeug.security import check_password_hash
        
        if not check_password_hash(user['password'], password):
            cursor.close()
            conn.close()
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        # ✅ GERAR WALLET AUTOMATICAMENTE SE NÃO TIVER (primeiro login)
        wallet_address = user['wallet_address']
        if not wallet_address:
            from generate_wallet import generate_polygon_wallet
            private_key, wallet_address = generate_polygon_wallet()
            
            # Atualizar usuário com wallet gerada
            cursor.execute("""
                UPDATE users 
                SET wallet_address = %s, private_key = %s 
                WHERE id = %s
            """, (wallet_address, private_key, user['id']))
            
            conn.commit()
            print(f"👛 Wallet gerada automaticamente no login: {wallet_address} para usuário {user['id']}")
        
        cursor.close()
        conn.close()
        
        # Gerar token mock (em produção use JWT)
        token = f"mock_token_{user['id']}"
        
        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "nickname": user['nickname'],
                "wallet_address": wallet_address  # ✅ Retornar wallet_address atualizado (pode ter sido gerado)
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@balance_ledger_bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        nickname = data.get('nickname', email.split('@')[0])
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se usuário já existe
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Email já cadastrado"}), 400
        
        # Gerar carteira
        from generate_wallet import generate_polygon_wallet
        private_key, wallet_address = generate_polygon_wallet()
        
        # Hash da senha
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        
        # Criar usuário
        cursor.execute("""
            INSERT INTO users (email, password, nickname, wallet_address, private_key)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (email, hashed_password, nickname, wallet_address, private_key))
        
        user_id = cursor.fetchone()['id']
        
        # Criar saldo inicial
        cursor.execute("""
            INSERT INTO balances (user_id, asset, available, locked, staking_balance)
            VALUES (%s, 'ALZ', 0.0, 0.0, 0.0)
        """, (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Gerar token
        token = f"mock_token_{user_id}"
        
        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "id": user_id,
                "email": email,
                "nickname": nickname,
                "wallet_address": wallet_address
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Erro no registro: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
