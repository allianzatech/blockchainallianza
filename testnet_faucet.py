"""
💰 Faucet Profissional da Allianza Testnet
Com rate limiting, PQC signatures e log público
"""

import time
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from pathlib import Path

# =============================================================================
# FUNÇÕES AUXILIARES SEGURAS PARA JSON
# =============================================================================

def load_json_safe(path: str, default: Dict = None) -> Dict:
    """
    Carrega JSON de forma segura, criando arquivo se não existir
    ou retornando default se estiver vazio/corrompido
    """
    if default is None:
        default = {}
    
    # Criar diretório se não existir
    dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    
    # Se arquivo não existe, criar com JSON válido
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
            return default
        except Exception:
            return default
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read().strip()
            # Se arquivo está vazio, retornar default
            if not data or data == "":
                with open(path, "w", encoding="utf-8") as fw:
                    json.dump(default, fw, indent=2)
                return default
            # Tentar fazer parse do JSON
            return json.loads(data)
    except (json.JSONDecodeError, ValueError, IOError) as e:
        # Se falhar, criar arquivo novo com default
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
        except Exception:
            pass
        return default

def save_json_safe(path: str, data: Dict):
    """
    Salva JSON de forma segura, criando diretório se necessário
    """
    try:
        # Criar diretório se não existir
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Erro ao salvar JSON em {path}: {e}")

def parse_json_line_safe(line: str) -> Optional[Dict]:
    """
    Faz parse de uma linha JSON de forma segura
    Retorna None se falhar
    """
    if not line or not line.strip():
        return None
    
    try:
        return json.loads(line.strip())
    except (json.JSONDecodeError, ValueError):
        return None

from testnet_config import (
    FAUCET_AMOUNT,
    FAUCET_MAX_PER_IP_PER_DAY,
    FAUCET_MAX_PER_ADDRESS_PER_DAY,
    FAUCET_COOLDOWN_HOURS,
    FAUCET_ADDRESS,
    is_valid_testnet_address
)

# =============================================================================
# GERENCIADOR DE FAUCET
# =============================================================================

class TestnetFaucet:
    def __init__(self, blockchain_instance, quantum_security_instance):
        self.blockchain = blockchain_instance
        self.quantum_security = quantum_security_instance
        
        # Rate limiting por IP
        self.ip_requests = defaultdict(list)  # {ip: [timestamps]}
        self.address_requests = defaultdict(list)  # {address: [timestamps]}
        
        # Log público de transações
        self.logs_dir = Path("proofs/testnet/faucet_logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Estatísticas
        self.stats = {
            "total_requests": 0,
            "total_sent": 0,
            "total_rejected": 0,
            "reasons": defaultdict(int)
        }
        
        # NÃO inicializar carteira aqui - será criada quando necessário
        # A inicialização no __init__ pode falhar se o blockchain ainda não estiver pronto
        self._faucet_wallet_initialized = False
    
    def _ensure_faucet_wallet(self):
        """Garante que o endereço do faucet tenha uma carteira criada com saldo suficiente"""
        try:
            from db_manager import DBManager
            db_manager = DBManager()
            from allianza_blockchain import AdvancedCrypto, cipher, TOTAL_SUPPLY
            from cryptography.hazmat.primitives import serialization
            
            # Calcular saldo inicial do faucet (10% do supply total = 100 milhões)
            FAUCET_INITIAL_BALANCE = int(TOTAL_SUPPLY * 0.10)  # 10% do supply total
            
            # Verificar se a carteira existe no banco de dados
            existing_wallet = db_manager.execute_query(
                "SELECT address, private_key FROM wallets WHERE address = ?",
                (FAUCET_ADDRESS,)
            )
            
            # Verificar se a carteira do faucet existe na memória
            if FAUCET_ADDRESS not in self.blockchain.wallets:
                print(f"🔧 Criando carteira para o faucet: {FAUCET_ADDRESS}")
                
                # Gerar chave privada e pública
                private_key, public_key = AdvancedCrypto.generate_keypair()
                
                # Criar carteira no blockchain
                self.blockchain.wallets[FAUCET_ADDRESS] = {
                    "ALZ": FAUCET_INITIAL_BALANCE,  # 10% do supply total (100 milhões)
                    "staked": 0,
                    "blockchain_source": "allianza",
                    "external_address": None
                }
                self.blockchain.staking_pool[FAUCET_ADDRESS] = 0
                
                # Criptografar e armazenar chave privada
                encrypted_private_key = cipher.encrypt(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                ).decode()
                
                # Salvar no banco de dados
                public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode()
                
                db_manager.execute_commit(
                    "INSERT OR REPLACE INTO wallets (address, vtx, staked_vtx, public_key, private_key, blockchain_source, external_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (FAUCET_ADDRESS, FAUCET_INITIAL_BALANCE, 0, public_key_pem, encrypted_private_key, "allianza", None)
                )
                
                print(f"✅ Carteira do faucet criada com sucesso! Saldo: {FAUCET_INITIAL_BALANCE:,} ALZ ({FAUCET_INITIAL_BALANCE/TOTAL_SUPPLY*100:.1f}% do supply)")
            elif not existing_wallet or not existing_wallet[0] or not existing_wallet[0][1]:
                # Carteira existe na memória mas não no banco ou sem chave privada
                print(f"⚠️  Carteira do faucet existe na memória mas não no banco ou sem chave privada. Recriando...")
                # Recriar carteira
                private_key, public_key = AdvancedCrypto.generate_keypair()
                encrypted_private_key = cipher.encrypt(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                ).decode()
                public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode()
                db_manager.execute_commit(
                    "INSERT OR REPLACE INTO wallets (address, vtx, staked_vtx, public_key, private_key, blockchain_source, external_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (FAUCET_ADDRESS, FAUCET_INITIAL_BALANCE, 0, public_key_pem, encrypted_private_key, "allianza", None)
                )
                print(f"✅ Chave privada do faucet recriada e salva no banco!")
            else:
                # Verificar se tem saldo suficiente
                balance = self.blockchain.wallets[FAUCET_ADDRESS].get("ALZ", 0)
                if balance < FAUCET_AMOUNT * 100:  # Garantir saldo para pelo menos 100 requisições
                    print(f"⚠️  Saldo do faucet baixo: {balance:,} ALZ")
                    # Recarregar saldo do faucet para 10% do supply
                    from db_manager import DBManager
                    db_manager = DBManager()
                    self.blockchain.wallets[FAUCET_ADDRESS]["ALZ"] = FAUCET_INITIAL_BALANCE
                    db_manager.execute_commit(
                        "UPDATE wallets SET vtx = ? WHERE address = ?",
                        (FAUCET_INITIAL_BALANCE, FAUCET_ADDRESS)
                    )
                    print(f"✅ Saldo do faucet recarregado para {FAUCET_INITIAL_BALANCE:,} ALZ ({FAUCET_INITIAL_BALANCE/TOTAL_SUPPLY*100:.1f}% do supply)")
        except Exception as e:
            print(f"⚠️  Erro ao garantir carteira do faucet: {e}")
            import traceback
            traceback.print_exc()
    
    def _get_faucet_private_key(self):
        """Obtém a chave privada do faucet do banco de dados"""
        try:
            print(f"🔍 Iniciando busca da chave privada do faucet...")
            from db_manager import DBManager
            db_manager = DBManager()
            from cryptography.hazmat.primitives import serialization
            from cryptography.fernet import Fernet
            
            # Importar cipher de forma segura
            try:
                from allianza_blockchain import cipher, ENCRYPTION_KEY
                current_cipher = cipher
            except (ImportError, AttributeError) as import_err:
                print(f"⚠️  Erro ao importar cipher: {import_err}. Tentando criar novo...")
                try:
                    # Tentar carregar ENCRYPTION_KEY de variável de ambiente ou arquivo
                    import os
                    encryption_key_file = "secrets/encryption_key.key"
                    if os.getenv("ENCRYPTION_KEY"):
                        ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()
                    elif os.path.exists(encryption_key_file):
                        with open(encryption_key_file, "rb") as f:
                            ENCRYPTION_KEY = f.read()
                    else:
                        print(f"❌ ENCRYPTION_KEY não encontrada em variável de ambiente nem em arquivo")
                        return None
                    current_cipher = Fernet(ENCRYPTION_KEY)
                except Exception as cipher_err:
                    print(f"❌ Erro ao criar cipher: {cipher_err}")
                    return None
            
            # Verificar se o cipher está disponível
            if current_cipher is None:
                print(f"❌ Cipher é None após tentativas de criação")
                return None
            
            # Garantir que a carteira existe antes de buscar a chave (lazy initialization)
            if not self._faucet_wallet_initialized:
                print(f"🔧 Garantindo que a carteira do faucet existe (inicialização tardia)...")
                self._ensure_faucet_wallet()
                self._faucet_wallet_initialized = True
            
            # Buscar chave privada criptografada do banco
            print(f"🔍 Buscando chave privada no banco de dados...")
            rows = db_manager.execute_query(
                "SELECT private_key FROM wallets WHERE address = ?",
                (FAUCET_ADDRESS,)
            )
            
            print(f"📊 Resultado da busca: {len(rows) if rows else 0} linhas encontradas")
            
            if not rows or not rows[0] or not rows[0][0]:
                print(f"⚠️  Chave privada do faucet não encontrada no banco de dados. Tentando criar carteira...")
                # Tentar criar a carteira novamente
                self._ensure_faucet_wallet()
                # Tentar buscar novamente
                rows = db_manager.execute_query(
                    "SELECT private_key FROM wallets WHERE address = ?",
                    (FAUCET_ADDRESS,)
                )
                if not rows or not rows[0] or not rows[0][0]:
                    print(f"❌ Não foi possível criar/obter chave privada do faucet após tentativa de recriação")
                    return None
                print(f"✅ Chave privada encontrada após recriação da carteira")
            
            encrypted_private_key = rows[0][0]
            
            if not encrypted_private_key:
                print(f"❌ Chave privada criptografada está vazia")
                return None
            
            print(f"🔓 Tentando descriptografar chave privada (tamanho: {len(str(encrypted_private_key))} caracteres)...")
            
            # Descriptografar chave privada
            try:
                # Verificar se já é bytes ou string
                if isinstance(encrypted_private_key, bytes):
                    private_key_pem = current_cipher.decrypt(encrypted_private_key)
                else:
                    private_key_pem = current_cipher.decrypt(encrypted_private_key.encode())
                
                print(f"✅ Chave descriptografada com sucesso. Carregando chave privada...")
                
                private_key = serialization.load_pem_private_key(
                    private_key_pem,
                    password=None,
                    backend=None
                )
                
                print(f"✅ Chave privada do faucet obtida e carregada com sucesso!")
                return private_key
            except Exception as decrypt_error:
                print(f"❌ Erro ao descriptografar chave privada: {type(decrypt_error).__name__}: {decrypt_error}")
                import traceback
                traceback.print_exc()
                return None
            
        except ImportError as import_error:
            print(f"❌ Erro de importação ao obter chave privada: {import_error}")
            import traceback
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"❌ Erro ao obter chave privada do faucet: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            # Tentar criar a carteira novamente em caso de erro
            try:
                print(f"🔄 Tentando recriar carteira do faucet...")
                self._ensure_faucet_wallet()
            except Exception as recreate_error:
                print(f"❌ Erro ao recriar carteira: {recreate_error}")
            return None
    
    def _get_client_ip(self, request) -> str:
        """Obtém o IP do cliente"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr or 'unknown'
    
    def _check_rate_limit(self, ip: str, address: str) -> tuple[bool, str]:
        """Verifica rate limiting"""
        now = time.time()
        cooldown_seconds = FAUCET_COOLDOWN_HOURS * 3600
        
        # Verificar limite por IP
        ip_timestamps = self.ip_requests[ip]
        recent_ip_requests = [ts for ts in ip_timestamps if now - ts < 86400]  # 24 horas
        
        if len(recent_ip_requests) >= FAUCET_MAX_PER_IP_PER_DAY:
            return False, f"Limite de {FAUCET_MAX_PER_IP_PER_DAY} requisições por IP por dia atingido"
        
        # Verificar cooldown por IP
        if ip_timestamps and (now - ip_timestamps[-1]) < cooldown_seconds:
            remaining = cooldown_seconds - (now - ip_timestamps[-1])
            return False, f"Aguarde {int(remaining/60)} minutos antes de fazer outra requisição"
        
        # Verificar limite por endereço
        address_timestamps = self.address_requests[address]
        recent_address_requests = [ts for ts in address_timestamps if now - ts < 86400]
        
        if len(recent_address_requests) >= FAUCET_MAX_PER_ADDRESS_PER_DAY:
            return False, f"Limite de {FAUCET_MAX_PER_ADDRESS_PER_DAY} requisições por endereço por dia atingido"
        
        # Verificar cooldown por endereço
        if address_timestamps and (now - address_timestamps[-1]) < cooldown_seconds:
            remaining = cooldown_seconds - (now - address_timestamps[-1])
            return False, f"Este endereço já recebeu tokens recentemente. Aguarde {int(remaining/60)} minutos"
        
        return True, "OK"
    
    def _generate_pow_proof(self, address: str, ip: str) -> str:
        """Gera prova de trabalho leve (anti-abuso)"""
        timestamp = str(int(time.time()))
        challenge = f"{address}:{ip}:{timestamp}"
        
        # PoW simples: encontrar hash que comece com 0000
        nonce = 0
        while True:
            data = f"{challenge}:{nonce}"
            hash_result = hashlib.sha256(data.encode()).hexdigest()
            if hash_result.startswith("0000"):
                return f"{nonce}:{hash_result}"
            nonce += 1
            if nonce > 100000:  # Limite de segurança
                break
        
        # Fallback: hash simples
        return hashlib.sha256(challenge.encode()).hexdigest()
    
    def request_tokens(self, address: str, request) -> Dict:
        """
        Processa requisição de tokens do faucet
        
        Returns:
            Dict com status, mensagem, tx_hash (se sucesso), etc.
        """
        self.stats["total_requests"] += 1
        ip = self._get_client_ip(request)
        
        # Validar endereço
        if not is_valid_testnet_address(address):
            self.stats["total_rejected"] += 1
            self.stats["reasons"]["invalid_address"] += 1
            return {
                "success": False,
                "error": "Endereço inválido. Use um endereço Allianza válido gerado pelo sistema.",
                "address": address
            }
        
        # Verificar rate limiting
        allowed, message = self._check_rate_limit(ip, address)
        if not allowed:
            self.stats["total_rejected"] += 1
            self.stats["reasons"]["rate_limit"] += 1
            return {
                "success": False,
                "error": message,
                "address": address,
                "ip": ip
            }
        
        try:
            # Gerar prova anti-abuso (PoW)
            pow_proof = self._generate_pow_proof(address, ip)
            
            # Obter chave privada do faucet
            faucet_private_key = self._get_faucet_private_key()
            if not faucet_private_key:
                self.stats["total_rejected"] += 1
                self.stats["reasons"]["no_private_key"] += 1
                return {
                    "success": False,
                    "error": "Erro ao acessar chave privada do faucet. Por favor, tente novamente mais tarde.",
                    "address": address
                }
            
            # Verificar saldo do faucet
            if FAUCET_ADDRESS not in self.blockchain.wallets:
                self._ensure_faucet_wallet()
            
            faucet_balance = self.blockchain.wallets.get(FAUCET_ADDRESS, {}).get("ALZ", 0)
            if faucet_balance < FAUCET_AMOUNT:
                self.stats["total_rejected"] += 1
                self.stats["reasons"]["insufficient_balance"] += 1
                return {
                    "success": False,
                    "error": f"Saldo insuficiente no faucet. Saldo atual: {faucet_balance} ALZ",
                    "address": address
                }
            
            # Criar transação usando o método correto do blockchain
            try:
                transaction = self.blockchain.create_transaction(
                    sender=FAUCET_ADDRESS,
                    receiver=address,
                    amount=FAUCET_AMOUNT,
                    private_key=faucet_private_key,
                    is_public=True,
                    network="allianza"
                )
                
                tx_hash = transaction.get("id", "")
                success = True
                
            except ValueError as e:
                # Erro de validação (ex: saldo insuficiente)
                self.stats["total_rejected"] += 1
                self.stats["reasons"]["validation_error"] += 1
                return {
                    "success": False,
                    "error": str(e),
                    "address": address
                }
            except Exception as e:
                # Outro erro
                print(f"❌ Erro ao criar transação do faucet: {e}")
                import traceback
                traceback.print_exc()
                self.stats["total_rejected"] += 1
                self.stats["reasons"]["transaction_error"] += 1
                return {
                    "success": False,
                    "error": f"Erro ao processar transação: {str(e)}",
                    "address": address
                }
            
            if success:
                
                # Registrar requisição
                now = time.time()
                self.ip_requests[ip].append(now)
                self.address_requests[address].append(now)
                
                # Log público
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "address": address,
                    "ip": ip,
                    "amount": FAUCET_AMOUNT,
                    "tx_hash": tx_hash,
                    "pow_proof": pow_proof,
                    "status": "success"
                }
                self._save_log(log_entry)
                
                self.stats["total_sent"] += 1
                
                return {
                    "success": True,
                    "message": f"✅ {FAUCET_AMOUNT} tokens enviados com sucesso!",
                    "address": address,
                    "amount": FAUCET_AMOUNT,
                    "tx_hash": tx_hash,
                    "pow_proof": pow_proof,
                    "timestamp": log_entry["timestamp"]
                }
        
        except Exception as e:
            self.stats["total_rejected"] += 1
            self.stats["reasons"]["exception"] += 1
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "address": address
            }
    
    def _save_log(self, log_entry: Dict):
        """Salva log público da transação"""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.logs_dir / f"faucet_{date_str}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Retorna logs públicos recentes"""
        logs = []
        log_files = sorted(self.logs_dir.glob("faucet_*.jsonl"), reverse=True)
        
        for log_file in log_files:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        parsed = parse_json_line_safe(line)
                        if parsed:
                            logs.append(parsed)
                        if len(logs) >= limit:
                            break
                if len(logs) >= limit:
                    break
            except (IOError, OSError, Exception) as e:
                # Continuar mesmo se houver erro em um arquivo
                print(f"⚠️  Erro ao ler log {log_file}: {e}")
                continue
        
        return logs[:limit]
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do faucet"""
        return {
            **self.stats,
            "faucet_address": FAUCET_ADDRESS,
            "amount_per_request": FAUCET_AMOUNT,
            "limits": {
                "max_per_ip_per_day": FAUCET_MAX_PER_IP_PER_DAY,
                "max_per_address_per_day": FAUCET_MAX_PER_ADDRESS_PER_DAY,
                "cooldown_hours": FAUCET_COOLDOWN_HOURS
            }
        }

