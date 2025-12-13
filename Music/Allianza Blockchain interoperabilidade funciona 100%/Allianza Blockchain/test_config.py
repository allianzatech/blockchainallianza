# test_config.py - CONFIGURAÇÕES PARA TESTES
TEST_PRIVATE_KEYS = {
    "ethereum": {
        "description": "Ethereum Sepolia Testnet - OBTER NO FAUCET",
        "private_key": "0xSuaPrivateKeyEthereumAqui",
        "testnet_faucets": [
            "https://sepoliafaucet.com/",
            "https://www.infura.io/faucet/sepolia"
        ]
    },
    "solana": {
        "description": "Solana Devnet - USAR solana-keygen",
        "private_key": "SuaPrivateKeySolanaAqui", 
        "testnet_faucets": [
            "solana airdrop 1 [ENDERECO]",
            "https://solfaucet.com/"
        ]
    },
    "polygon": {
        "description": "Polygon Mumbai Testnet - OBTER NO FAUCET",
        "private_key": "0xSuaPrivateKeyPolygonAqui",
        "testnet_faucets": [
            "https://faucet.polygon.technology/",
            "https://mumbaifaucet.com/"
        ]
    },
    "bsc": {
        "description": "BSC Testnet - OBTER NO FAUCET", 
        "private_key": "0xSuaPrivateKeyBSCAqui",
        "testnet_faucets": [
            "https://testnet.binance.org/faucet-smart",
            "https://faucet.quicknode.com/bnb/testnet"
        ]
    }
}

# Exemplo de como usar:
def get_test_private_key(chain):
    """Retorna private key de teste para uma chain específica"""
    return TEST_PRIVATE_KEYS.get(chain, {}).get("private_key", "")

def get_faucet_links(chain):
    """Retorna links de faucet para uma chain"""
    return TEST_PRIVATE_KEYS.get(chain, {}).get("testnet_faucets", [])