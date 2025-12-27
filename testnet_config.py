"""
🌐 Configuração da Allianza Testnet
Network ID, Chain ID, Genesis Block e Identidade da Rede
"""

# =============================================================================
# IDENTIDADE DA REDE
# =============================================================================

# Network ID único da testnet (diferente da mainnet)
TESTNET_NETWORK_ID = 0x414C5A54  # "ALZT" em hex

# Chain ID (compatível com EVM)
TESTNET_CHAIN_ID = 20241120  # Data de lançamento da testnet

# Nome oficial da rede
TESTNET_NAME = "Allianza Testnet"
TESTNET_NAME_SHORT = "ALZ-Testnet"
TESTNET_SYMBOL = "ALZ-T"

# Prefixos
ADDRESS_PREFIX = "ALZ1"  # Prefixo para endereços
PRIVATE_KEY_PREFIX = "ALZ-PRIV-"  # Prefixo para chaves privadas (apenas para identificação)
TX_PREFIX = "ALZ-TX-"  # Prefixo para transações

# =============================================================================
# GENESIS BLOCK
# =============================================================================

GENESIS_BLOCK = {
    "index": 0,
    "timestamp": 1732147200,  # 2024-11-20 00:00:00 UTC
    "previous_hash": "0" * 64,
    "hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
    "transactions": [],
    "shard_id": 0,
    "validator": "genesis",
    "signature": {
        "ecdsa": "",
        "ml_dsa": "",
        "sphincs": ""
    }
}

# =============================================================================
# CONFIGURAÇÕES DA TESTNET
# =============================================================================

# Faucet
FAUCET_AMOUNT = 1000  # Quantidade de tokens por requisição
FAUCET_MAX_PER_IP_PER_DAY = 10  # Máximo de requisições por IP por dia
FAUCET_MAX_PER_ADDRESS_PER_DAY = 5  # Máximo de requisições por endereço por dia
FAUCET_COOLDOWN_HOURS = 1  # Cooldown entre requisições (horas)

# Bootstrap Nodes (IPs públicos - serão configurados em produção)
BOOTSTRAP_NODES = [
    {
        "id": "bootstrap-1",
        "ip": "0.0.0.0",  # Será configurado em produção
        "port": 5009,
        "public_key": "",
        "status": "active"
    },
    {
        "id": "bootstrap-2",
        "ip": "0.0.0.0",  # Será configurado em produção
        "port": 5010,
        "public_key": "",
        "status": "active"
    }
]

# Portas padrão
P2P_PORT = 5009  # Porta P2P padrão
RPC_PORT = 5008  # Porta RPC/API padrão

# Endereços especiais
FAUCET_ADDRESS = "ALZ1Faucet000000000000000000000000000000000000"
TREASURY_ADDRESS = "ALZ1Treasury0000000000000000000000000000000000"

# =============================================================================
# RANGES DE ENDEREÇOS
# =============================================================================

# Endereços válidos devem começar com ALZ1
VALID_ADDRESS_PREFIX = "ALZ1"
ADDRESS_LENGTH = 42  # Comprimento total do endereço

# Endereços reservados (não podem ser usados por usuários)
RESERVED_ADDRESSES = [
    FAUCET_ADDRESS,
    TREASURY_ADDRESS,
    "ALZ1Genesis00000000000000000000000000000000000",
    "ALZ1Validator000000000000000000000000000000000"
]

# =============================================================================
# VERSÃO DA TESTNET
# =============================================================================

TESTNET_VERSION = "1.0.0"
MIN_NODE_VERSION = "1.0.0"  # Versão mínima suportada

# =============================================================================
# FUNÇÕES ÚTEIS
# =============================================================================

def is_valid_testnet_address(address: str) -> bool:
    """Verifica se um endereço é válido para a testnet"""
    if not address or not isinstance(address, str):
        return False
    
    # Aceitar endereços que começam com ALZ1 (formato testnet)
    if address.startswith(VALID_ADDRESS_PREFIX):
        if len(address) != ADDRESS_LENGTH:
            return False
        if address in RESERVED_ADDRESSES:
            return False
        return True
    
    # Aceitar endereços Base58 gerados pelo blockchain (formato real)
    # Endereços Base58 geralmente têm 34-44 caracteres e contêm apenas caracteres Base58
    try:
        from base58_utils import validate_allianza_address
        if validate_allianza_address(address):
            # Verificar se não é um endereço reservado
            if address in RESERVED_ADDRESSES:
                return False
            return True
    except:
        pass
    
    # Se não passou em nenhuma validação, considerar inválido
    return False

def get_network_info():
    """Retorna informações da rede"""
    return {
        "network_id": hex(TESTNET_NETWORK_ID),
        "chain_id": TESTNET_CHAIN_ID,
        "name": TESTNET_NAME,
        "name_short": TESTNET_NAME_SHORT,
        "symbol": TESTNET_SYMBOL,
        "version": TESTNET_VERSION,
        "min_node_version": MIN_NODE_VERSION,
        "genesis_block": {
            "hash": GENESIS_BLOCK["hash"],
            "timestamp": GENESIS_BLOCK["timestamp"]
        },
        "address_prefix": ADDRESS_PREFIX,
        "p2p_port": P2P_PORT,
        "rpc_port": RPC_PORT,
        "bootstrap_nodes": len(BOOTSTRAP_NODES)
    }

