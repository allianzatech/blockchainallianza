import sqlite3
import json
import logging

logger = logging.getLogger(__name__)

class DBManager:
    """Gerencia a conexão e as operações de persistência com o SQLite."""
    
    def __init__(self, db_path='allianza_blockchain.db', check_same_thread=False):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=check_same_thread)
        self.cursor = self.conn.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        """Cria as tabelas do banco de dados se não existirem."""
        try:
            self.cursor.executescript('''
                CREATE TABLE IF NOT EXISTS shards (
                    shard_id INTEGER, block_index INTEGER, previous_hash TEXT, 
                    transactions TEXT, timestamp REAL, hash TEXT, validator TEXT
                );
                CREATE TABLE IF NOT EXISTS wallets (
                    address TEXT PRIMARY KEY, vtx REAL, staked_vtx REAL, 
                    public_key TEXT, private_key TEXT, blockchain_source TEXT, external_address TEXT
                );
                CREATE TABLE IF NOT EXISTS transactions_history (
                    id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL,
                    type TEXT, timestamp REAL, network TEXT, is_public BOOLEAN
                );
                CREATE TABLE IF NOT EXISTS contracts (
                    id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL,
                    condition_timestamp INTEGER, executed BOOLEAN, created_at REAL
                );
                CREATE TABLE IF NOT EXISTS cross_chain_uchainids (
                    uchain_id TEXT PRIMARY KEY, source_chain TEXT, target_chain TEXT,
                    recipient TEXT, amount REAL, timestamp REAL, memo TEXT,
                    commitment_id TEXT, proof_id TEXT, state_id TEXT,
                    tx_hash TEXT, explorer_url TEXT
                );
                CREATE TABLE IF NOT EXISTS cross_chain_zk_proofs (
                    proof_id TEXT PRIMARY KEY, source_chain TEXT, target_chain TEXT,
                    source_commitment_id TEXT, state_transition_hash TEXT,
                    proof TEXT, verification_key TEXT, created_at REAL, valid INTEGER
                );
                CREATE TABLE IF NOT EXISTS cross_chain_state_commitments (
                    commitment_id TEXT PRIMARY KEY, chain TEXT, state_data TEXT,
                    contract_address TEXT, timestamp REAL
                );
            ''')
            self.conn.commit()
            logger.info("Tabelas do banco de dados inicializadas com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inicializar tabelas: {e}")

    def execute_query(self, query, params=()):
        """Executa uma query e retorna o resultado (para SELECT)."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao executar query: {query} com params: {params}. Erro: {e}")
            return []

    def execute_commit(self, query, params=()):
        """Executa uma query e faz commit (para INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao executar commit: {query} com params: {params}. Erro: {e}")
            return False

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
        logger.info("Conexão com o banco de dados fechada.")

# Exemplo de uso (será removido após a integração)
# if __name__ == '__main__':
#     db = DBManager()
#     # db.execute_commit("INSERT INTO wallets VALUES (?, ?, ?, ?, ?, ?, ?)", ('test_addr', 100.0, 0.0, 'pub_key', 'priv_key', 'allianza', 'ext_addr'))
#     # print(db.execute_query("SELECT * FROM wallets"))
#     db.close()
