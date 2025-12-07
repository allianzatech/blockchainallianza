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
    """Extrair user_id do token mock - formato: mock_token_{user_id}"""
    try:
        # ✅ Extrair user_id do formato mock_token_{user_id}
        parts = token.split("_")
        if len(parts) >= 3 and parts[0] == "mock" and parts[1] == "token":
            user_id = int(parts[2])
            # ✅ Verificar se o user_id existe no banco (validação)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return user_id
            else:
                print(f"⚠️ Token contém user_id {user_id} mas usuário não existe no banco")
    except (ValueError, IndexError, Exception) as e:
        print(f"⚠️ Erro ao extrair user_id do token '{token}': {e}")
        import traceback
        traceback.print_exc()
    return None


@balance_ledger_bp.route('/balances/me', methods=['GET'])
@token_required
def get_my_balance():
    """Obter saldo do usuário autenticado - BUSCA REAL DO BANCO"""
    try:
        user_id = request.user_id
        
        if not user_id:
            return jsonify({"error": "User ID não encontrado no token"}), 401
        
        print(f"💰 Buscando saldo para user_id: {user_id}")
        
        conn = get_db_connection()
        # ✅ psycopg (psycopg3) já retorna dict_row por padrão
        cursor = conn.cursor()
        
        # ✅ Buscar email e nickname do usuário para debug
        cursor.execute("SELECT email, nickname FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        user_email = user.get('email', 'unknown') if user else 'unknown'
        user_nickname = user.get('nickname', 'unknown') if user else 'unknown'
        print(f"📧 Usuário: {user_email} ({user_nickname}) - ID: {user_id}")
        
        # ✅ DEBUG: Verificar se há pagamentos pendentes para este email
        cursor.execute("""
            SELECT id, email, amount, status, user_id, wallet_address 
            FROM payments 
            WHERE email = %s AND status = 'pending'
            ORDER BY id DESC
            LIMIT 5
        """, (user_email,))
        pending_payments = cursor.fetchall()
        if pending_payments:
            print(f"📋 Pagamentos pendentes encontrados para {user_email}: {len(pending_payments)}")
            for payment in pending_payments:
                print(f"   - Payment ID {payment.get('id')}: {payment.get('amount')} | user_id={payment.get('user_id')} | wallet={payment.get('wallet_address')}")
        else:
            print(f"⚠️ Nenhum pagamento pendente encontrado para {user_email}")
        
        # ✅ Buscar saldo do usuário (SEMPRE DO BANCO REAL - não mock)
        cursor.execute("""
            SELECT 
                user_id,
                asset,
                available,
                locked,
                staking_balance,
                updated_at
            FROM balances
            WHERE user_id = %s AND asset = 'ALZ'
        """, (user_id,))
        
        balance_row = cursor.fetchone()
        
        if not balance_row:
            # ✅ Criar saldo inicial se não existir (ZERO - não usar mock)
            cursor.execute("""
                INSERT INTO balances (user_id, asset, available, locked, staking_balance)
                VALUES (%s, 'ALZ', 0.0, 0.0, 0.0)
                RETURNING user_id, asset, available, locked, staking_balance, updated_at
            """, (user_id,))
            balance_row = cursor.fetchone()
            conn.commit()
            print(f"✅ Saldo inicial criado para user_id {user_id}: 0 ALZ")
        
        # ✅ Formatar resposta com valores REAIS do banco
        # psycopg3 retorna dict_row, então podemos acessar como dict
        try:
            if balance_row:
                # ✅ Acesso seguro aos campos do dict
                available = float(balance_row.get('available') or 0)
                locked = float(balance_row.get('locked') or 0)
                staking = float(balance_row.get('staking_balance') or 0)
                total = available + locked + staking
                
                print(f"💰 Saldo encontrado para {user_email} ({user_nickname}): available={available}, locked={locked}, staking={staking}, total={total}")
                
                # ✅ Tratamento seguro para updated_at
                updated_at_value = balance_row.get('updated_at')
                updated_at_str = None
                if updated_at_value:
                    try:
                        if hasattr(updated_at_value, 'isoformat'):
                            updated_at_str = updated_at_value.isoformat()
                        else:
                            updated_at_str = str(updated_at_value)
                    except Exception as e:
                        print(f"⚠️ Erro ao formatar updated_at: {e}")
                        updated_at_str = None
                
                balance_data = {
                    "user_id": balance_row.get('user_id', user_id),
                    "asset": balance_row.get('asset', 'ALZ'),
                    "available": available,
                    "locked": locked,
                    "staking_balance": staking,
                    "total": total,
                    "updated_at": updated_at_str
                }
            else:
                # Fallback se balance_row for None (não deveria acontecer)
                print(f"⚠️ balance_row é None para user_id {user_id}")
                balance_data = {
                    "user_id": user_id,
                    "asset": 'ALZ',
                    "available": 0,
                    "locked": 0,
                    "staking_balance": 0,
                    "total": 0,
                    "updated_at": None
                }
        except Exception as e:
            print(f"❌ Erro ao formatar balance_data: {e}")
            import traceback
            traceback.print_exc()
            # Retornar saldo zero em caso de erro
            balance_data = {
                "user_id": user_id,
                "asset": 'ALZ',
                "available": 0,
                "locked": 0,
                "staking_balance": 0,
                "total": 0,
                "updated_at": None
            }
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        return jsonify({
            "success": True,
            "balance": balance_data
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao buscar saldo: {e}")
        import traceback
        traceback.print_exc()
        # ✅ Retornar saldo zero em caso de erro, mas ainda assim retornar JSON válido
        return jsonify({
            "success": True,
            "balance": {
                "user_id": request.user_id if hasattr(request, 'user_id') else None,
                "asset": 'ALZ',
                "available": 0,
                "locked": 0,
                "staking_balance": 0,
                "total": 0,
                "updated_at": None
            },
            "error": str(e)
        }), 200  # Retornar 200 para não quebrar o frontend, mas incluir erro na resposta


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
        
        total_result = cursor.fetchone()
        total_count = total_result.get('total', 0) if total_result else 0
        
        cursor.close()
        conn.close()
        
        # ✅ Formatar resposta com valores REAIS do banco
        history = []
        for entry in entries:
            history.append({
                "id": entry.get('id'),
                "user_id": entry.get('user_id'),
                "asset": entry.get('asset', 'ALZ'),
                "amount": float(entry.get('amount', 0)),
                "entry_type": entry.get('entry_type'),
                "related_id": entry.get('related_id'),
                "description": entry.get('description', ''),
                "created_at": entry.get('created_at').isoformat() if entry.get('created_at') else None,
                "idempotency_key": entry.get('idempotency_key')
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
        
        # ✅ Acesso seguro aos campos do dict
        user_password = user.get('password')
        if not user_password:
            cursor.close()
            conn.close()
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        try:
            if not check_password_hash(user_password, password):
                cursor.close()
                conn.close()
                return jsonify({"error": "Credenciais inválidas"}), 401
        except Exception as e:
            print(f"❌ Erro ao verificar senha: {e}")
            import traceback
            traceback.print_exc()
            cursor.close()
            conn.close()
            return jsonify({"error": "Erro ao verificar credenciais"}), 500
        
        # ✅ GERAR WALLET AUTOMATICAMENTE SE NÃO TIVER (primeiro login)
        wallet_address = user.get('wallet_address')
        if not wallet_address:
            from generate_wallet import generate_polygon_wallet
            private_key, wallet_address = generate_polygon_wallet()
            
            # Atualizar usuário com wallet gerada
            cursor.execute("""
                UPDATE users 
                SET wallet_address = %s, private_key = %s 
                WHERE id = %s
            """, (wallet_address, private_key, user.get('id')))
            
            conn.commit()
            print(f"👛 Wallet gerada automaticamente no login: {wallet_address} para usuário {user.get('id')}")
        
        cursor.close()
        conn.close()
        
        # ✅ Gerar token que identifica o usuário
        # Formato: mock_token_{user_id} - o user_id está no token
        user_id = user.get('id')
        user_email = user.get('email', 'unknown')
        user_nickname = user.get('nickname') or user_email.split('@')[0]  # ✅ Usar email se não tiver nickname
        
        token = f"mock_token_{user_id}"
        
        print(f"🔑 Token gerado para usuário {user_id} ({user_email} - {user_nickname}): {token}")
        
        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "id": user_id,
                "email": user_email,
                "nickname": user_nickname,  # ✅ Garantir que sempre tenha nickname
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
