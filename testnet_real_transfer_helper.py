"""
🔧 Helper para executar transferências cross-chain REAIS na testnet
Permite que desenvolvedores configurem chaves privadas e executem transferências reais
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class RealTransferHelper:
    """Helper para executar transferências reais"""
    
    @staticmethod
    def check_real_transfer_available(source_chain: str, target_chain: str) -> Dict:
        """
        Verifica se é possível executar transferência real
        
        Returns:
            Dict com status e instruções
        """
        # Verificar chaves privadas disponíveis
        source_key = None
        target_key = None
        
        key_env_vars = {
            "polygon": "POLYGON_PRIVATE_KEY",
            "ethereum": "ETH_PRIVATE_KEY",
            "bitcoin": "BITCOIN_PRIVATE_KEY",  # Priorizar WIF
            "solana": "SOLANA_PRIVATE_KEY",
            "bsc": "BSC_PRIVATE_KEY",
            "base": "BASE_PRIVATE_KEY"
        }
        
        source_key_env = key_env_vars.get(source_chain.lower())
        target_key_env = key_env_vars.get(target_chain.lower())
        
        if source_key_env:
            source_key = os.getenv(source_key_env)
            # Para Bitcoin, verificar se é WIF válido (não xprv/vprv/vpub/xpub)
            if source_chain.lower() == "bitcoin" and source_key:
                # Verificar se é extended key (não serve para transações)
                if source_key.startswith(('xprv', 'vprv', 'tprv', 'xpub', 'vpub', 'tpub', 'ypub', 'zpub')):
                    # É extended key, não WIF - não serve para transações
                    print(f"⚠️  Chave Bitcoin inválida: é extended key ({source_key[:10]}...), não WIF")
                    source_key = None
                # Verificar formato WIF válido (deve começar com c, 9, K, L para testnet/mainnet)
                elif not source_key.startswith(('c', '9', 'K', 'L', '5')):
                    print(f"⚠️  Chave Bitcoin inválida: formato WIF inválido (deve começar com c, 9, K, L ou 5)")
                    source_key = None
                elif len(source_key) < 51 or len(source_key) > 52:
                    print(f"⚠️  Chave Bitcoin inválida: tamanho incorreto (WIF deve ter 51-52 caracteres, encontrado: {len(source_key)})")
                    source_key = None
        
        if target_key_env:
            target_key = os.getenv(target_key_env)
            # Para Bitcoin, verificar se é WIF válido (não xprv/vprv/vpub/xpub)
            if target_chain.lower() == "bitcoin" and target_key:
                # Verificar se é extended key (não serve para transações)
                if target_key.startswith(('xprv', 'vprv', 'tprv', 'xpub', 'vpub', 'tpub', 'ypub', 'zpub')):
                    # É extended key, não WIF - não serve para transações
                    print(f"⚠️  Chave Bitcoin inválida: é extended key ({target_key[:10]}...), não WIF")
                    target_key = None
                # Verificar formato WIF válido
                elif not target_key.startswith(('c', '9', 'K', 'L', '5')):
                    print(f"⚠️  Chave Bitcoin inválida: formato WIF inválido")
                    target_key = None
                elif len(target_key) < 51 or len(target_key) > 52:
                    print(f"⚠️  Chave Bitcoin inválida: tamanho incorreto")
                    target_key = None
        
        # Verificar se bridge está disponível
        bridge_available = False
        try:
            from real_cross_chain_bridge import RealCrossChainBridge
            bridge_available = True
        except:
            pass
        
        can_execute_real = (
            bridge_available and
            source_key is not None and
            len(source_key) > 0
        )
        
        return {
            "can_execute_real": can_execute_real,
            "bridge_available": bridge_available,
            "source_key_configured": source_key is not None and len(source_key) > 0,
            "target_key_configured": target_key is not None and len(target_key) > 0,
            "instructions": RealTransferHelper._get_instructions(source_chain, target_chain, can_execute_real),
            "env_vars_needed": {
                "source": source_key_env,
                "target": target_key_env
            }
        }
    
    @staticmethod
    def _get_instructions(source_chain: str, target_chain: str, can_execute: bool) -> str:
        """Gera instruções para configurar transferência real"""
        if can_execute:
            return "✅ Transferência real disponível! Configure as chaves privadas no arquivo .env"
        
        instructions = []
        instructions.append("Para executar transferência REAL:")
        instructions.append("")
        instructions.append("1. Configure as chaves privadas no arquivo .env:")
        
        key_vars = {
            "polygon": "POLYGON_PRIVATE_KEY",
            "ethereum": "ETH_PRIVATE_KEY",
            "bitcoin": "BITCOIN_PRIVATE_KEY",
            "solana": "SOLANA_PRIVATE_KEY",
            "bsc": "BSC_PRIVATE_KEY",
            "base": "BASE_PRIVATE_KEY"
        }
        
        source_var = key_vars.get(source_chain.lower())
        target_var = key_vars.get(target_chain.lower())
        
        if source_var:
            instructions.append(f"   {source_var}=sua_chave_privada_source")
        if target_var:
            instructions.append(f"   {target_var}=sua_chave_privada_target")
        
        instructions.append("")
        instructions.append("2. Certifique-se de ter saldo na testnet:")
        instructions.append(f"   - {source_chain}: Obtenha tokens de teste")
        instructions.append(f"   - {target_chain}: Configure reservas de liquidez")
        instructions.append("")
        instructions.append("3. Reinicie o servidor após configurar")
        instructions.append("")
        instructions.append("⚠️ IMPORTANTE: Use apenas chaves de TESTNET, nunca mainnet!")
        
        return "\n".join(instructions)

