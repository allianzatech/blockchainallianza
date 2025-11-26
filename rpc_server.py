#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPC Server para Allianza Blockchain
Implementa JSON-RPC 2.0 para compatibilidade com ferramentas Ethereum
"""

from flask import Flask, request, jsonify
import json
import logging
from typing import Dict, Any, Optional
from functools import wraps

# Importar sistemas
from p2p_network import get_p2p_network, initialize_p2p_network, NodeType
from validators_manager import get_validators_manager, initialize_validators_manager
from dao_system import get_dao_system, initialize_dao_system
from allianza_blockchain import AllianzaBlockchain

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Instância global da blockchain
blockchain: Optional[AllianzaBlockchain] = None

def initialize_blockchain():
    """Inicializa blockchain e sistemas"""
    global blockchain
    
    # Inicializar blockchain
    blockchain = AllianzaBlockchain()
    
    # Inicializar sistemas
    initialize_p2p_network("rpc_node_1", NodeType.RPC_NODE)
    initialize_validators_manager(min_stake=1000.0)
    initialize_dao_system()
    
    logger.info("🚀 RPC Server inicializado")

def json_rpc_error(code: int, message: str, data: Any = None) -> Dict:
    """Cria resposta de erro JSON-RPC"""
    error = {
        "code": code,
        "message": message
    }
    if data is not None:
        error["data"] = data
    
    return {
        "jsonrpc": "2.0",
        "error": error,
        "id": None
    }

def json_rpc_success(result: Any, request_id: Any = None) -> Dict:
    """Cria resposta de sucesso JSON-RPC"""
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }

@app.route('/', methods=['POST'])
def rpc_handler():
    """Handler principal do RPC"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify(json_rpc_error(-32700, "Parse error"))
        
        method = data.get("method")
        params = data.get("params", [])
        request_id = data.get("id")
        
        if not method:
            return jsonify(json_rpc_error(-32600, "Invalid Request"))
        
        # Processar método
        result = process_rpc_method(method, params)
        
        if "error" in result:
            return jsonify(json_rpc_error(
                result["error"]["code"],
                result["error"]["message"],
                result["error"].get("data")
            ))
        
        return jsonify(json_rpc_success(result.get("result"), request_id))
    
    except Exception as e:
        logger.error(f"Erro no RPC handler: {e}")
        return jsonify(json_rpc_error(-32603, "Internal error", str(e)))

def process_rpc_method(method: str, params: list) -> Dict:
    """Processa método RPC"""
    
    # Métodos Ethereum padrão
    if method == "eth_blockNumber":
        return {"result": hex(blockchain.get_latest_block_index() if blockchain else 0)}
    
    elif method == "eth_getBalance":
        address = params[0] if params else None
        if not address:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        # Em produção, obteria saldo real
        return {"result": hex(0)}
    
    elif method == "eth_sendTransaction":
        # Em produção, processaria transação
        return {"result": "0x" + "0" * 64}
    
    elif method == "eth_sendRawTransaction":
        # Recebe transação assinada e processa
        raw_tx = params[0] if params else None
        if not raw_tx:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        
        # Em produção, validaria e processaria a transação
        # Por agora, retorna hash simulado
        import hashlib
        tx_hash = "0x" + hashlib.sha256(raw_tx.encode() if isinstance(raw_tx, str) else raw_tx).hexdigest()[:64]
        
        logger.info(f"📤 Transação recebida: {tx_hash}")
        
        return {"result": tx_hash}
    
    elif method == "eth_getTransactionReceipt":
        tx_hash = params[0] if params else None
        if not tx_hash:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        # Em produção, obteria receipt real
        return {"result": None}
    
    elif method == "eth_gasPrice":
        # Retorna gas price padrão (20 gwei)
        return {"result": hex(20000000000)}
    
    elif method == "eth_getTransactionCount":
        address = params[0] if len(params) > 0 else None
        block = params[1] if len(params) > 1 else "latest"
        if not address:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        # Em produção, obteria nonce real
        return {"result": hex(0)}
    
    elif method == "eth_estimateGas":
        # Retorna estimativa de gas padrão
        return {"result": hex(21000)}
    
    elif method == "eth_getBlockByNumber":
        block_number = params[0] if len(params) > 0 else None
        full_txs = params[1] if len(params) > 1 else False
        if not block_number:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        # Em produção, obteria bloco real
        return {"result": None}
    
    elif method == "eth_getTransactionByHash":
        tx_hash = params[0] if params else None
        if not tx_hash:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        # Em produção, obteria transação real
        return {"result": None}
    
    # Métodos Allianza customizados
    elif method == "allianza_getNetworkInfo":
        p2p = get_p2p_network()
        validators = get_validators_manager()
        
        return {
            "result": {
                "chain_id": 12345,
                "chain_name": "Allianza Blockchain",
                "network_info": p2p.get_network_info() if p2p else {},
                "validators_stats": validators.get_network_stats() if validators else {}
            }
        }
    
    elif method == "allianza_getValidators":
        validators = get_validators_manager()
        if not validators:
            return {"result": []}
        return {"result": validators.get_all_validators()}
    
    elif method == "allianza_getValidatorInfo":
        address = params[0] if params else None
        if not address:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        
        validators = get_validators_manager()
        if not validators:
            return {"result": None}
        
        info = validators.get_validator_info(address)
        return {"result": info}
    
    elif method == "allianza_sendCrossChain":
        target_chain = params[0] if len(params) > 0 else None
        recipient = params[1] if len(params) > 1 else None
        amount = params[2] if len(params) > 2 else None
        
        if not all([target_chain, recipient, amount]):
            return {"error": {"code": -32602, "message": "Invalid params"}}
        
        # Em produção, processaria transferência cross-chain
        return {
            "result": {
                "success": True,
                "tx_hash": "0x" + "0" * 64,
                "message": "Transação cross-chain iniciada"
            }
        }
    
    elif method == "allianza_getCrossChainStatus":
        tx_hash = params[0] if params else None
        if not tx_hash:
            return {"error": {"code": -32602, "message": "Invalid params"}}
        
        # Em produção, verificaria status real
        return {
            "result": {
                "status": "pending",
                "tx_hash": tx_hash
            }
        }
    
    elif method == "allianza_stake":
        address = params[0] if len(params) > 0 else None
        amount = params[1] if len(params) > 1 else None
        
        if not all([address, amount]):
            return {"error": {"code": -32602, "message": "Invalid params"}}
        
        validators = get_validators_manager()
        if not validators:
            return {"error": {"code": -32603, "message": "Validators manager not initialized"}}
        
        result = validators.stake(address, float(amount))
        return {"result": result}
    
    elif method == "allianza_unstake":
        address = params[0] if len(params) > 0 else None
        amount = params[1] if len(params) > 1 else None
        
        if not all([address, amount]):
            return {"error": {"code": -32602, "message": "Invalid params"}}
        
        validators = get_validators_manager()
        if not validators:
            return {"error": {"code": -32603, "message": "Validators manager not initialized"}}
        
        result = validators.unstake(address, float(amount))
        return {"result": result}
    
    else:
        return {"error": {"code": -32601, "message": f"Method not found: {method}"}}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "chain_id": 12345,
        "chain_name": "Allianza Blockchain"
    })

@app.route('/network', methods=['GET'])
def network_info():
    """Endpoint para informações da rede"""
    p2p = get_p2p_network()
    validators = get_validators_manager()
    
    return jsonify({
        "chain_id": 12345,
        "chain_name": "Allianza Blockchain",
        "network": p2p.get_network_info() if p2p else {},
        "validators": validators.get_network_stats() if validators else {}
    })

if __name__ == '__main__':
    initialize_blockchain()
    print("🚀 Allianza RPC Server iniciando...")
    print("📡 Endpoint: http://localhost:8545")
    print("📋 Health: http://localhost:8545/health")
    print("🌐 Network: http://localhost:8545/network")
    app.run(host='0.0.0.0', port=8545, debug=True)

