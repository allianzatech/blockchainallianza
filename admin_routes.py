# admin_routes.py - VERSÃO FINAL CORRIGIDA
import os
import json
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
from datetime import datetime, timedelta

# ✅ CARREGAR VARIÁVEIS DE AMBIENTE PRIMEIRO
from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2.extras import RealDictCursor

admin_bp = Blueprint('admin', __name__)
CORS(admin_bp, resources={r"/admin/*": {"origins": "*"}})

# ✅ CONFIGURAÇÃO ÚNICA - Evitar conflitos
def get_db_connection():
    """Conexão única com o banco para evitar conflitos"""
    # ✅ FALLBACK: Usar NEON_DATABASE_URL se DATABASE_URL não existir
    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('NEON_DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL ou NEON_DATABASE_URL não configurada")
    
    print(f"🔗 Conectando ao banco usando: {'DATABASE_URL' if os.getenv('DATABASE_URL') else 'NEON_DATABASE_URL (fallback)'}")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    return conn

# ✅ CONSTANTES GLOBAIS - Evitar recálculos
ALZ_PRICE_BRL = 0.10  # 1 ALZ = R$ 0,10

# ✅ CARREGAR TOKEN DA VARIÁVEL DE AMBIENTE (com debug)
_env_token = os.getenv('VITE_SITE_ADMIN_TOKEN')
if _env_token:
    SITE_ADMIN_TOKEN = _env_token
    print(f"✅ VITE_SITE_ADMIN_TOKEN carregado: {_env_token[:10]}... (comprimento: {len(_env_token)})")
else:
    SITE_ADMIN_TOKEN = 'allianza_super_admin_2024_CdE25$$$'
    print(f"⚠️  VITE_SITE_ADMIN_TOKEN não encontrado, usando valor padrão: {SITE_ADMIN_TOKEN[:10]}...")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({"error": "Token de administrador necessário"}), 401
        
        # ✅ VERIFICAÇÃO DE TOKEN CORRIGIDA
        if token != SITE_ADMIN_TOKEN:
            return jsonify({
                "error": "Token inválido",
                "received": token[:10] + "..." if token else "vazio",
                "expected": SITE_ADMIN_TOKEN[:10] + "..."
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

# ✅ FUNÇÃO DE CÁLCULO GLOBAL
def calculate_alz_from_brl(amount_brl):
    """Calcula ALZ a partir de BRL de forma consistente"""
    return float(amount_brl) / ALZ_PRICE_BRL

# ✅ ROTA DE HEALTH CHECK MELHORADA
@admin_bp.route('/health', methods=['GET'])
def health_check():
    """Verifica saúde do backend e banco"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Testar conexão com banco
        cursor.execute("SELECT 1 as status")
        db_status = cursor.fetchone()
        
        # Testar tabelas
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM payments) as payments_count,
                (SELECT COUNT(*) FROM users) as users_count,
                (SELECT COUNT(*) FROM balances) as balances_count
        """)
        tables_status = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat(),
            "tables": {
                "payments": tables_status['payments_count'],
                "users": tables_status['users_count'],
                "balances": tables_status['balances_count']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

# ✅ DASHBOARD CORRIGIDO
@admin_bp.route('/admin/payments', methods=['GET'])
@admin_required
def get_payments():
    conn = None
    try:
        print("📥 Buscando pagamentos do banco...")
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT id, email, amount, method, status, created_at, 
                   processed_at, tx_hash, metadata, wallet_address
            FROM payments 
            ORDER BY created_at DESC
        ''')
        payments = cursor.fetchall()
        
        print(f"✅ Encontrados {len(payments)} pagamentos")
        
        # ✅ CORREÇÃO GARANTIDA - Cálculo consistente
        corrected_payments = []
        for payment in payments:
            payment_data = dict(payment)
            amount_brl = float(payment_data['amount'])
            
            # SEMPRE calcular ALZ a partir do BRL
            payment_data['alz_amount'] = calculate_alz_from_brl(amount_brl)
            
            # Log para debug
            print(f"💰 Pagamento {payment_data['id']}: R$ {amount_brl} → {payment_data['alz_amount']} ALZ")
            
            corrected_payments.append(payment_data)
        
        return jsonify({
            "success": True,
            "data": corrected_payments,
            "count": len(corrected_payments),
            "calculation_note": "ALZ = BRL / 0.10 (1 ALZ = R$ 0,10)"
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Erro ao carregar pagamentos: {str(e)}")
        print(f"📋 Traceback completo:\n{error_trace}")
        return jsonify({
            "success": False,
            "error": f"Erro no servidor: {str(e)}",
            "type": type(e).__name__
        }), 500
    finally:
        if conn:
            conn.close()

# ✅ ROTA PARA LISTAR TODOS OS STAKES
@admin_bp.route('/admin/stakes', methods=['GET'])
@admin_required
def get_all_stakes():
    conn = None
    try:
        print("📥 Buscando todos os stakes do banco...")
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Buscar todos os stakes (ativos e inativos)
        cursor.execute('''
            SELECT id, user_id, asset, amount, duration, apy, start_date, end_date, 
                   estimated_reward, accrued_reward, status, auto_compound, last_reward_claim, 
                   days_remaining, early_withdrawal_penalty, actual_return, penalty_applied, 
                   withdrawn_at, metadata
            FROM stakes 
            ORDER BY created_at DESC
        ''')
        stakes = cursor.fetchall()
        
        print(f"✅ Encontrados {len(stakes)} stakes")
        
        # Formatar a saída (datas, floats)
        formatted_stakes = []
        for stake in stakes:
            formatted_stake = dict(stake)
            
            # Converter datas para ISO format
            for key in ['start_date', 'end_date', 'last_reward_claim', 'withdrawn_at']:
                if formatted_stake.get(key) and hasattr(formatted_stake[key], 'isoformat'):
                    formatted_stake[key] = formatted_stake[key].isoformat()
                elif formatted_stake.get(key):
                    formatted_stake[key] = formatted_stake[key].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            # Garantir que os numéricos sejam floats
            for key in ['amount', 'apy', 'estimated_reward', 'accrued_reward', 'early_withdrawal_penalty', 'actual_return', 'penalty_applied']:
                if formatted_stake.get(key) is not None:
                    formatted_stake[key] = float(formatted_stake[key])

            formatted_stakes.append(formatted_stake)
        
        return jsonify({
            "success": True,
            "data": formatted_stakes,
            "count": len(formatted_stakes)
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Erro ao carregar stakes: {str(e)}")
        print(f"📋 Traceback completo:\n{error_trace}")
        return jsonify({
            "success": False,
            "error": f"Erro no servidor: {str(e)}",
            "type": type(e).__name__
        }), 500
    finally:
        if conn:
            conn.close()

# ✅ ROTA PARA UNSTAKE FORÇADO PELO ADMIN
@admin_bp.route('/admin/unstake', methods=['POST'])
@admin_required
def admin_unstake():
    # Importações necessárias para a lógica de unstake
    from datetime import datetime, timezone
    from backend_staking_routes import safe_days_remaining, update_stake_rewards
    
    data = request.json
    stake_id = data.get('stake_id')
    user_id = data.get('user_id')
    confirm_early_withdrawal = data.get('confirm_early_withdrawal', False)
    
    if not stake_id or not user_id:
        return jsonify({"error": "stake_id e user_id são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 1. Buscar o stake
        cursor.execute("SELECT * FROM stakes WHERE id = %s AND user_id = %s", (stake_id, user_id))
        stake = cursor.fetchone()
        
        if not stake:
            return jsonify({"error": "Stake não encontrado"}), 404
        
        if stake["status"] != "active":
            return jsonify({"error": "Stake não está ativo"}), 400

        # 2. Atualizar recompensas antes de processar o unstake
        # Nota: update_stake_rewards gerencia sua própria conexão, então é seguro chamar.
        update_stake_rewards(stake_id) 
        
        # Re-buscar o stake após a atualização de recompensas
        cursor.execute("SELECT * FROM stakes WHERE id = %s AND user_id = %s", (stake_id, user_id))
        stake = cursor.fetchone()
        
        # 3. Buscar o saldo de staking para o asset
        cursor.execute("SELECT staking_balance FROM balances WHERE user_id = %s AND asset = %s", (user_id, stake["asset"]))
        balance_result = cursor.fetchone()
        
        if not balance_result or float(balance_result["staking_balance"]) < float(stake["amount"]):
             return jsonify({"error": "Erro de consistência: Saldo de staking insuficiente para retirada"}), 500

        # ✅ USAR FUNÇÃO CORRIGIDA
        days_remaining = safe_days_remaining(stake["end_date"])
        
        is_early_withdrawal = days_remaining > 0
        penalty_rate = float(stake["early_withdrawal_penalty"]) if is_early_withdrawal else 0.0
        penalty_amount = float(stake["amount"]) * penalty_rate if is_early_withdrawal else 0.0
        
        return_amount = float(stake["amount"]) - penalty_amount
        accrued_reward = float(stake["accrued_reward"])

        # 4. Confirmação de retirada antecipada
        if is_early_withdrawal and not confirm_early_withdrawal:
            return jsonify({
                "requires_confirmation": True,
                "warning": "RETIRADA ANTECIPADA DETECTADA",
                "penalty_rate": f"{penalty_rate * 100}%",
                "penalty_amount": penalty_amount,
                "original_amount": float(stake["amount"]),
                "return_amount": return_amount,
                "accrued_rewards": accrued_reward,
                "days_remaining": days_remaining,
                "message": "Confirmação de retirada antecipada necessária."
            }), 400

        cursor.execute("BEGIN")

        # 5. Registrar no ledger (devolução do principal)
        cursor.execute(
            "INSERT INTO ledger_entries (user_id, asset, amount, entry_type, related_id, description) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, stake["asset"], return_amount, "unstake_principal", stake_id, 
             f"Retirada do principal do staking {stake_id} (Penalidade: {penalty_amount:.6f}) - ADMIN")
        )

        # 6. Registrar no ledger (recompensa acumulada)
        if accrued_reward > 0:
            cursor.execute(
                "INSERT INTO ledger_entries (user_id, asset, amount, entry_type, related_id, description) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, stake["asset"], accrued_reward, "unstake_reward", stake_id, 
                 f"Recompensa acumulada do staking {stake_id} - ADMIN")
            )

        # 7. Atualizar saldos (devolver principal + recompensa)
        total_return = return_amount + accrued_reward
        cursor.execute(
            "UPDATE balances SET available = available + %s, staking_balance = staking_balance - %s WHERE user_id = %s AND asset = %s",
            (total_return, stake["amount"], user_id, stake["asset"])
        )

        # 8. Atualizar registro de stake
        new_status = "withdrawn_early" if is_early_withdrawal else "withdrawn_mature"
        now = datetime.now(timezone.utc)
        cursor.execute(
            "UPDATE stakes SET status = %s, actual_return = %s, penalty_applied = %s, withdrawn_at = %s WHERE id = %s",
            (new_status, total_return, penalty_amount, now, stake_id)
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": f"Staking {stake_id} retirado com sucesso pelo ADMIN.",
            "total_received": total_return,
            "returned_amount": return_amount,
            "accrued_rewards": accrued_reward,
            "penalty_applied": penalty_amount,
            "status": new_status
        }), 200

    except Exception as e:
        conn.rollback()
        print(f"[ADMIN UNSTAKE] Erro: {e}")
        return jsonify({"error": f"Erro ao retirar staking: {e}"}), 500
    finally:
        conn.close()

# ✅ PROCESSAMENTO CORRIGIDO
@admin_bp.route('/admin/process-payments', methods=['POST'])
@admin_required
def process_payments():
    data = request.json
    payment_ids = data.get('payment_ids', [])
    admin_user = data.get('admin_user', 'admin')
    
    if not payment_ids:
        return jsonify({"error": "Nenhum pagamento selecionado"}), 400
    
    print(f"🔄 Processando {len(payment_ids)} pagamentos: {payment_ids}")
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("BEGIN")
        processed_count = 0
        errors = []
        
        for payment_id in payment_ids:
            try:
                # ✅ BUSCAR PAGAMENTO COM BLOQUEIO PARA EVITAR CONCORRÊNCIA
                cursor.execute('''
                    SELECT id, email, amount, metadata 
                    FROM payments 
                    WHERE id = %s AND status = 'pending'
                    FOR UPDATE
                ''', (payment_id,))
                
                payment = cursor.fetchone()
                
                if not payment:
                    errors.append(f"Pagamento {payment_id} não encontrado ou já processado")
                    continue
                
                # ✅ CÁLCULO GARANTIDO
                amount_brl = float(payment['amount'])
                alz_amount = calculate_alz_from_brl(amount_brl)
                
                print(f"💰 Processando: R$ {amount_brl} → {alz_amount} ALZ para {payment['email']}")
                
                # ✅ BUSCAR/CRIAR USUÁRIO
                cursor.execute(
                    "SELECT id, wallet_address FROM users WHERE email = %s",
                    (payment['email'],)
                )
                user = cursor.fetchone()
                
                user_id = None
                if user:
                    user_id = user['id']
                    print(f"✅ Usuário encontrado: {user_id}")
                else:
                    # Criar usuário se não existir
                    cursor.execute(
                        "INSERT INTO users (email, created_at) VALUES (%s, NOW()) RETURNING id",
                        (payment['email'],)
                    )
                    user_id = cursor.fetchone()['id']
                    print(f"✅ Novo usuário criado: {user_id}")
                
                # ✅ VERIFICAR/CRIAR BALANCE
                cursor.execute(
                    "SELECT id FROM balances WHERE user_id = %s AND asset = 'ALZ'",
                    (user_id,)
                )
                balance = cursor.fetchone()
                
                if not balance:
                    cursor.execute(
                        "INSERT INTO balances (user_id, asset, available, staking_balance) VALUES (%s, 'ALZ', 0, 0)",
                        (user_id,)
                    )
                    print(f"✅ Balance criado para usuário {user_id}")
                
                # ✅ CREDITAR TOKENS
                cursor.execute(
                    "UPDATE balances SET available = available + %s WHERE user_id = %s AND asset = 'ALZ'",
                    (alz_amount, user_id)
                )
                
                # ✅ REGISTRAR NO LEDGER
                cursor.execute(
                    """INSERT INTO ledger_entries 
                       (user_id, asset, amount, entry_type, description) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (user_id, 'ALZ', alz_amount, 'purchase', 
                     f'Compra de {alz_amount} ALZ via PIX - R$ {amount_brl}')
                )
                
                # ✅ ATUALIZAR PAGAMENTO
                cursor.execute(
                    """UPDATE payments 
                       SET status = 'completed', 
                           processed_at = NOW(),
                           metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('alz_amount_processed', %s)
                       WHERE id = %s""",
                    (alz_amount, payment_id)
                )
                
                processed_count += 1
                print(f"✅ Pagamento {payment_id} processado com sucesso!")
                
            except Exception as e:
                error_msg = f"Erro no pagamento {payment_id}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
                continue
        
        if errors:
            conn.rollback()
            return jsonify({
                "success": False,
                "error": f"Processamento parcialmente falhou",
                "processed_count": processed_count,
                "errors": errors
            }), 400
        
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": f"✅ {processed_count} pagamentos processados com sucesso!",
            "processed_count": processed_count,
            "total_alz_distributed": processed_count * alz_amount if processed_count > 0 else 0
        }), 200
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro geral no processamento: {str(e)}")
        return jsonify({"error": f"Erro no servidor: {str(e)}"}), 500
    finally:
        conn.close()

# ✅ ESTATÍSTICAS CORRIGIDAS
@admin_bp.route('/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Supply Total
        TOTAL_SUPPLY = 1000000000
        
        # Tokens em circulação
        cursor.execute("SELECT SUM(available + staking_balance) as circulating FROM balances WHERE asset = 'ALZ'")
        circulating_result = cursor.fetchone()
        circulating = float(circulating_result['circulating'] or 0)
        
        # ✅ PAGAMENTOS PENDENTES CALCULADOS CORRETAMENTE
        cursor.execute("SELECT SUM(amount) as pending_brl FROM payments WHERE status = 'pending'")
        pending_brl_result = cursor.fetchone()
        pending_brl = float(pending_brl_result['pending_brl'] or 0)
        pending_alz = calculate_alz_from_brl(pending_brl)
        
        # Estatísticas
        cursor.execute('''
            SELECT 
                COUNT(*) as total_users,
                (SELECT COUNT(*) FROM payments) as total_payments,
                (SELECT COUNT(*) FROM payments WHERE status = 'completed') as completed_payments,
                (SELECT COUNT(*) FROM payments WHERE status = 'pending') as pending_payments,
                (SELECT SUM(amount) FROM payments WHERE status = 'completed') as total_processed_brl
        ''')
        stats_result = cursor.fetchone()
        
        total_processed_alz = calculate_alz_from_brl(stats_result['total_processed_brl'] or 0)
        
        return jsonify({
            "success": True,
            "stats": {
                "supply": {
                    "total": TOTAL_SUPPLY,
                    "circulating": circulating,
                    "pending_distribution": pending_alz,
                    "reserve": TOTAL_SUPPLY - circulating - pending_alz
                },
                "users": {
                    "total_users": stats_result['total_users']
                },
                "payments": {
                    "total_payments": stats_result['total_payments'],
                    "completed_payments": stats_result['completed_payments'],
                    "pending_payments": stats_result['pending_payments'],
                    "total_processed_brl": pending_brl,
                    "total_processed_alz": total_processed_alz
                }
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Erro nas estatísticas: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# ✅ ENVIO MANUAL CORRIGIDO
@admin_bp.route('/admin/manual-token-send', methods=['POST'])
@admin_required
def manual_token_send():
    data = request.json
    email = data.get('email')
    amount = data.get('amount')
    description = data.get('description', 'Crédito administrativo manual')
    
    if not email or not amount:
        return jsonify({"error": "Email e quantidade são obrigatórios"}), 400
    
    try:
        amount_alz = float(amount)
    except ValueError:
        return jsonify({"error": "Quantidade deve ser um número válido"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("BEGIN")
        
        # Buscar ou criar usuário
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute(
                "INSERT INTO users (email, created_at) VALUES (%s, NOW()) RETURNING id",
                (email,)
            )
            user_id = cursor.fetchone()['id']
        else:
            user_id = user['id']
        
        # Verificar balance
        cursor.execute(
            "SELECT id FROM balances WHERE user_id = %s AND asset = 'ALZ'",
            (user_id,)
        )
        balance = cursor.fetchone()
        
        if not balance:
            cursor.execute(
                "INSERT INTO balances (user_id, asset, available, staking_balance) VALUES (%s, 'ALZ', 0, 0)",
                (user_id,)
            )
        
        # Creditar
        cursor.execute(
            "UPDATE balances SET available = available + %s WHERE user_id = %s AND asset = 'ALZ'",
            (amount_alz, user_id)
        )
        
        # Registrar
        cursor.execute(
            "INSERT INTO ledger_entries (user_id, asset, amount, entry_type, description) VALUES (%s, %s, %s, %s, %s)",
            (user_id, 'ALZ', amount_alz, 'manual_credit', description)
        )
        
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": f"✅ {amount_alz} ALZ creditados para {email}",
            "amount_alz": amount_alz,
            "email": email
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# ✅ DEBUG CORRIGIDO - Endpoint público para verificar token configurado
@admin_bp.route('/debug-token-info', methods=['GET'])
def debug_token_info():
    """Endpoint público para debug - mostra qual token o backend está esperando"""
    env_token = os.getenv('VITE_SITE_ADMIN_TOKEN', 'NOT_FOUND')
    return jsonify({
        "token_from_env": env_token[:20] + "..." if len(env_token) > 20 else env_token,
        "token_length": len(env_token) if env_token != 'NOT_FOUND' else 0,
        "token_first_10": env_token[:10] if env_token != 'NOT_FOUND' else "NOT_FOUND",
        "token_last_10": env_token[-10:] if env_token != 'NOT_FOUND' and len(env_token) > 10 else "NOT_FOUND",
        "env_var_exists": env_token != 'NOT_FOUND',
        "site_admin_token_used": SITE_ADMIN_TOKEN[:20] + "..." if len(SITE_ADMIN_TOKEN) > 20 else SITE_ADMIN_TOKEN,
        "site_admin_token_length": len(SITE_ADMIN_TOKEN),
        "message": "Debug de token - verifique se VITE_SITE_ADMIN_TOKEN está configurado"
    }), 200

# ✅ DEBUG CORRIGIDO
@admin_bp.route('/admin/debug-token', methods=['GET'])
@admin_required
def debug_token():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    return jsonify({
        "token_received": token,
        "token_expected": SITE_ADMIN_TOKEN,
        "token_length_received": len(token),
        "token_length_expected": len(SITE_ADMIN_TOKEN),
        "match": token == SITE_ADMIN_TOKEN,
        "message": "Debug de token administrativo"
    }), 200
