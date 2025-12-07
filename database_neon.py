# database_neon.py - COMPLETO E CORRIGIDO COM COFRE
import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

class NeonDatabase:
    def __init__(self):
        # ✅ CORRIGIDO: Aceitar ambos os nomes (NEON_DATABASE_URL ou DATABASE_URL)
        self.database_url = os.getenv('NEON_DATABASE_URL') or os.getenv('DATABASE_URL')
        if self.database_url:
            safe_url = self.database_url.split('@')
            if len(safe_url) > 1:
                print(f"🔗 Conectando ao: {safe_url[1].split('?')[0]}")
            else:
                print("🔗 URL do Neon configurada")
        else:
            print("❌ NEON_DATABASE_URL ou DATABASE_URL não encontrada")
        
    def get_connection(self):
        """Obter conexão com o Neon PostgreSQL"""
        if not self.database_url:
            raise ValueError("NEON_DATABASE_URL ou DATABASE_URL não configurada no .env")
        
        try:
            conn = psycopg.connect(
                self.database_url,
                row_factory=dict_row,
                connect_timeout=10
            )
            return conn
        except Exception as e:
            print(f"❌ Erro de conexão com Neon: {e}")
            raise

    def init_db(self):
        """Inicializar tabelas no Neon - CORRIGIDO COM COFRE"""
        conn = None
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            print("🗃️  Criando/verificando tabelas no Neon...")
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password TEXT,
                    nickname VARCHAR(100),
                    wallet_address VARCHAR(255) UNIQUE,
                    private_key TEXT,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            print("✅ Tabela 'users' criada/verificada")
            
            # ✅ MIGRAÇÃO: Alterar coluna password para permitir NULL (se já existir com NOT NULL)
            try:
                cursor.execute("""
                    ALTER TABLE users 
                    ALTER COLUMN password DROP NOT NULL;
                """)
                print("✅ Coluna 'password' alterada para permitir NULL")
            except Exception as e:
                # Se a coluna já permite NULL ou não existe constraint, ignorar erro
                if "does not exist" not in str(e) and "does not have" not in str(e):
                    print(f"ℹ️  Coluna 'password' já permite NULL ou não tem constraint: {e}")
            
            # Tabela de saldos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS balances (
                    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                    asset VARCHAR(10) DEFAULT 'ALZ' NOT NULL,
                    available NUMERIC(20,8) DEFAULT 0.0 NOT NULL,
                    locked NUMERIC(20,8) DEFAULT 0.0 NOT NULL,
                    staking_balance NUMERIC(20,8) DEFAULT 0.0 NOT NULL,
                    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            print("✅ Tabela 'balances' criada/verificada")

            # ✅ TABELA DO COFRE ADICIONADA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vault_balances (
                    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                    hot_wallet NUMERIC(20,8) DEFAULT 0.0 NOT NULL,
                    cold_wallet NUMERIC(20,8) DEFAULT 0.0 NOT NULL,
                    last_transfer_at TIMESTAMPTZ,
                    transfer_count INTEGER DEFAULT 0,
                    security_level VARCHAR(20) DEFAULT 'medium',
                    auto_transfer_threshold NUMERIC(20,8) DEFAULT 1000.0,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            print("✅ Tabela 'vault_balances' criada/verificada")
            
            # ✅ TABELA DE SOLICITAÇÕES DE RETIRADA DO COFRE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vault_withdraw_requests (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    amount NUMERIC(20,8) NOT NULL,
                    auth_code VARCHAR(12) NOT NULL,
                    expires_at TIMESTAMPTZ NOT NULL,
                    description TEXT,
                    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMPTZ,
                    cancelled_at TIMESTAMPTZ
                );
            ''')
            print("✅ Tabela 'vault_withdraw_requests' criada/verificada")
            
            # Tabela de ledger
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ledger_entries (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    asset VARCHAR(10) DEFAULT 'ALZ' NOT NULL,
                    amount NUMERIC(20,8) NOT NULL,
                    entry_type VARCHAR(50) NOT NULL,
                    related_id VARCHAR(100),
                    description TEXT,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    idempotency_key VARCHAR(255) UNIQUE
                );
            ''')
            print("✅ Tabela 'ledger_entries' criada/verificada")
            
            # Tabela de solicitações de saque
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS withdrawal_requests (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    to_address VARCHAR(255) NOT NULL,
                    amount NUMERIC(20,8) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
                    tx_hash VARCHAR(255),
                    gas_used NUMERIC(20,8),
                    gas_cost_matic NUMERIC(20,8),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            print("✅ Tabela 'withdrawal_requests' criada/verificada")
            
            # ✅✅✅ CORREÇÃO: Verificar se a tabela stakes existe de forma correta
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'stakes'
                );
            """)
            result = cursor.fetchone()
            stakes_exists = result['exists'] if result else False
            
            if stakes_exists:
                print("🔄 Tabela 'stakes' já existe, verificando estrutura...")
                # Verificar se a coluna asset existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'stakes' AND column_name = 'asset'
                """)
                asset_column_exists = cursor.fetchone() is not None
                
                # Verificar se a coluna staking_plan existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'stakes' AND column_name = 'staking_plan'
                """)
                staking_plan_column_exists = cursor.fetchone() is not None
                
                if not staking_plan_column_exists:
                    print("🔧 Adicionando coluna 'staking_plan' à tabela stakes...")
                    cursor.execute('ALTER TABLE stakes ADD COLUMN staking_plan VARCHAR(50);')
                    print("✅ Coluna 'staking_plan' adicionada à tabela stakes")
                    
                # Verificar se a coluna total_rewards_claimed existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'stakes' AND column_name = 'total_rewards_claimed'
                """)
                total_rewards_claimed_column_exists = cursor.fetchone() is not None
                
                if not total_rewards_claimed_column_exists:
                    print("🔧 Adicionando coluna 'total_rewards_claimed' à tabela stakes...")
                    cursor.execute('ALTER TABLE stakes ADD COLUMN total_rewards_claimed NUMERIC(20,8) DEFAULT 0.0;')
                    print("✅ Coluna 'total_rewards_claimed' adicionada à tabela stakes")
                
                # Verificar se a coluna asset existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'stakes' AND column_name = 'asset'
                """)
                asset_column_exists = cursor.fetchone() is not None
                
                if not asset_column_exists:
                    print("🔧 Adicionando coluna 'asset' à tabela stakes...")
                    cursor.execute('ALTER TABLE stakes ADD COLUMN asset VARCHAR(10) DEFAULT \'ALZ\' NOT NULL;')
                    print("✅ Coluna 'asset' adicionada à tabela stakes")
            else:
                # Criar tabela do zero
                cursor.execute('''
                    CREATE TABLE stakes (
                        id VARCHAR(100) PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        asset VARCHAR(10) DEFAULT 'ALZ' NOT NULL,
                        amount NUMERIC(20,8) NOT NULL,
                        staking_plan VARCHAR(50) NOT NULL, -- Novo campo para referenciar o plano
                        start_date TIMESTAMPTZ NOT NULL,
                        end_date TIMESTAMPTZ NOT NULL,
                        status VARCHAR(20) DEFAULT 'active' NOT NULL,
                        last_reward_claim TIMESTAMPTZ, -- Pode ser NULL antes do primeiro resgate
                        total_rewards_claimed NUMERIC(20,8) DEFAULT 0.0, -- Novo campo
                        actual_return NUMERIC(20,8),
                        penalty_applied NUMERIC(20,8),
                        withdrawn_at TIMESTAMPTZ,
                        metadata JSONB,
                        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                print("✅ Tabela 'stakes' criada do zero")
            
            print("✅ Tabela 'stakes' criada/verificada")

            # Tabela de pagamentos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    amount NUMERIC(20,8) NOT NULL,
                    method VARCHAR(50) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
                    tx_hash VARCHAR(255),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMPTZ,
                    metadata JSONB,
                    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
                );
            ''')
            print("✅ Tabela 'payments' criada/verificada")

            # Tabela de logs administrativos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_logs (
                    id SERIAL PRIMARY KEY,
                    admin_user VARCHAR(100) NOT NULL,
                    action VARCHAR(100) NOT NULL,
                    description TEXT,
                    target_id INTEGER,
                    ip_address VARCHAR(45),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            print("✅ Tabela 'admin_logs' criada/verificada")
            
            # ✅ CORREÇÃO: Índices apenas após garantir que as colunas existem
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ledger_user_id ON ledger_entries(user_id);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ledger_created_at ON ledger_entries(created_at);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stakes_user_id ON stakes(user_id);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stakes_status ON stakes(status);')
            
            # ✅ Índices para o cofre
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_vault_balances_user_id ON vault_balances(user_id);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_vault_balances_security_level ON vault_balances(security_level);')
            
            # ✅ Índices para solicitações de retirada
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_vault_withdraw_requests_user_id ON vault_withdraw_requests(user_id);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_vault_withdraw_requests_status ON vault_withdraw_requests(status);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_vault_withdraw_requests_expires_at ON vault_withdraw_requests(expires_at);')
            
            # ✅ CORREÇÃO: Verificar se a coluna asset existe antes de criar índice
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'stakes' AND column_name = 'asset'
            """)
            if cursor.fetchone():
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_stakes_asset ON stakes(asset);')
                print("✅ Índice idx_stakes_asset criado/verificado")
            else:
                print("⚠️ Índice idx_stakes_asset ignorado (coluna asset não existe)")
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stakes_end_date ON stakes(end_date);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_email ON payments(email);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_admin_logs_admin_user ON admin_logs(admin_user);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_admin_logs_created_at ON admin_logs(created_at);')
            print("✅ Índices criados/verificados")
            
            conn.commit()
            print("🎉 Todas as tabelas foram criadas/verificadas com sucesso no Neon!")
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao criar tabelas: {e}")
            raise
        finally:
            if conn:
                conn.close()

# Instância global
neon_db = NeonDatabase()

# Funções de conveniência
def get_db_connection():
    return neon_db.get_connection()

def init_db():
    return neon_db.init_db()
