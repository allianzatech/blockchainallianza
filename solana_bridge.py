#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ SOLANA BRIDGE - INTEGRAÇÃO COMPLETA
Suporte completo para transferências Solana no bridge cross-chain
"""

import os
import time
import json
import base58
import requests
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

# Tentar importar bibliotecas Solana
try:
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.system_program import transfer, TransferParams
    from solders.transaction import Transaction
    from solders.message import Message
    # SendTransaction não existe mais na versão atual do solders - removido
    from solana.rpc.api import Client
    from solana.rpc.commitment import Confirmed
    from solana.rpc.types import TxOpts
    SOLANA_LIBS_AVAILABLE = True
except ImportError as e:
    SOLANA_LIBS_AVAILABLE = False
    print(f"⚠️  Bibliotecas Solana não disponíveis: {e}")
    print("   Instale com: pip install solana solders")

class SolanaBridge:
    """Bridge para Solana - Transferências Reais"""
    
    def __init__(self):
        # RPC endpoints Solana
        # ✅ PRIORIDADE: Usar SOLANA_RPC_URL se configurado, senão usar SOLANA_TESTNET_RPC
        solana_rpc_url = os.getenv('SOLANA_RPC_URL') or os.getenv('SOLANA_TESTNET_RPC')
        
        self.rpc_endpoints = {
            "mainnet": os.getenv('SOLANA_MAINNET_RPC', 'https://api.mainnet-beta.solana.com'),
            "testnet": solana_rpc_url or 'https://api.testnet.solana.com',
            "devnet": os.getenv('SOLANA_DEVNET_RPC', 'https://api.devnet.solana.com')
        }
        
        self.network = os.getenv('SOLANA_NETWORK', 'testnet')
        self.rpc_url = solana_rpc_url or self.rpc_endpoints.get(self.network, self.rpc_endpoints['testnet'])
        
        # ✅ Endereço Solana configurado (se disponível)
        self.solana_address = os.getenv('SOLANA_ADDRESS')
        if self.solana_address:
            print(f"✅ Endereço Solana configurado: {self.solana_address}")
        
        # Cliente RPC
        self.client = None
        if SOLANA_LIBS_AVAILABLE:
            try:
                self.client = Client(self.rpc_url)
                print(f"✅ Solana RPC conectado: {self.network}")
            except Exception as e:
                print(f"⚠️  Erro ao conectar Solana RPC: {e}")
                self.client = None
        
        # Taxa de câmbio
        self.exchange_rates = {
            "SOL": 100.0,  # $100 por SOL (fallback)
            "USDC": 1.0,
            "USDT": 1.0
        }
    
    def validate_address(self, address: str) -> Tuple[bool, Optional[str]]:
        """Validar endereço Solana"""
        try:
            if not address or not isinstance(address, str):
                return False, "Endereço inválido"
            
            # Solana addresses são Base58, 32-44 caracteres
            if len(address) < 32 or len(address) > 44:
                return False, "Comprimento inválido (deve ser 32-44 caracteres)"
            
            # Tentar decodificar Base58
            try:
                decoded = base58.b58decode(address)
                if len(decoded) != 32:
                    return False, "Comprimento de bytes inválido (deve ser 32 bytes)"
                
                # Se bibliotecas Solana disponíveis, validar com Pubkey
                if SOLANA_LIBS_AVAILABLE:
                    try:
                        pubkey = Pubkey.from_string(address)
                        return True, None
                    except:
                        return False, "Endereço Base58 inválido"
                
                return True, None
            except Exception as e:
                return False, f"Erro ao decodificar Base58: {e}"
        except Exception as e:
            return False, f"Erro ao validar endereço: {e}"
    
    def get_balance(self, address: str) -> Dict:
        """Obter saldo SOL de um endereço"""
        is_valid, error = self.validate_address(address)
        if not is_valid:
            return {
                "success": False,
                "error": f"Endereço inválido: {error}"
            }
        
        try:
            if self.client:
                # Usar biblioteca Solana
                pubkey = Pubkey.from_string(address)
                response = self.client.get_balance(pubkey, commitment=Confirmed)
                
                if response.value is not None:
                    balance_lamports = response.value
                    balance_sol = balance_lamports / 1e9  # SOL tem 9 decimais
                    
                    return {
                        "success": True,
                        "address": address,
                        "balance_lamports": balance_lamports,
                        "balance_sol": balance_sol,
                        "network": self.network
                    }
            else:
                # Fallback: usar RPC direto
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getBalance",
                    "params": [address]
                }
                
                response = requests.post(
                    self.rpc_url,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "result" in data and "value" in data["result"]:
                        balance_lamports = data["result"]["value"]
                        balance_sol = balance_lamports / 1e9
                        
                        return {
                            "success": True,
                            "address": address,
                            "balance_lamports": balance_lamports,
                            "balance_sol": balance_sol,
                            "network": self.network
                        }
            
            return {
                "success": False,
                "error": "Não foi possível obter saldo"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao obter saldo: {e}"
            }
    
    def send_transaction(
        self,
        from_private_key: str,
        to_address: str,
        amount_sol: float
    ) -> Dict:
        """
        Enviar transação SOL real
        
        Args:
            from_private_key: Chave privada do remetente (Base58 ou bytes)
            to_address: Endereço do destinatário
            amount_sol: Quantidade em SOL
        """
        # Validar endereço de destino
        is_valid, error = self.validate_address(to_address)
        if not is_valid:
            return {
                "success": False,
                "error": f"Endereço de destino inválido: {error}"
            }
        
        # Validar quantidade
        if amount_sol <= 0:
            return {
                "success": False,
                "error": "Quantidade deve ser maior que zero"
            }
        
        # Converter para lamports
        amount_lamports = int(amount_sol * 1e9)
        
        try:
            if not SOLANA_LIBS_AVAILABLE:
                # ✅ FALLBACK: Tentar usar API RPC direta (sem bibliotecas Python)
                print("⚠️  Bibliotecas Solana não disponíveis, tentando método alternativo via RPC direto...")
                return self._send_transaction_via_rpc_direct(
                    from_private_key=from_private_key,
                    to_address=to_address,
                    amount_sol=amount_sol
                )
            
            # Carregar keypair
            try:
                # Tentar como Base58 string
                if isinstance(from_private_key, str):
                    # Remover espaços e quebras de linha
                    from_private_key = from_private_key.strip()
                    
                    # Validar comprimento (chave privada Solana tem 64 bytes = 88 caracteres Base58)
                    if len(from_private_key) < 80 or len(from_private_key) > 100:
                        return {
                            "success": False,
                            "error": f"Chave privada tem comprimento inválido: {len(from_private_key)} caracteres (esperado ~88)",
                            "note": "Chave privada Solana deve ter 64 bytes codificados em Base58 (~88 caracteres)"
                        }
                    
                    try:
                        keypair_bytes = base58.b58decode(from_private_key)
                        if len(keypair_bytes) != 64:
                            return {
                                "success": False,
                                "error": f"Chave privada decodificada tem tamanho inválido: {len(keypair_bytes)} bytes (esperado 64)",
                                "note": "Chave privada Solana deve ter exatamente 64 bytes"
                            }
                        keypair = Keypair.from_bytes(keypair_bytes)
                    except Exception as decode_err:
                        return {
                            "success": False,
                            "error": f"Erro ao decodificar chave privada Base58: {str(decode_err)}",
                            "note": "Verifique se a chave privada está em formato Base58 válido"
                        }
                else:
                    keypair = Keypair.from_bytes(from_private_key)
            except Exception as keypair_err:
                return {
                    "success": False,
                    "error": f"Erro ao criar keypair: {str(keypair_err)}",
                    "note": "Verifique se a chave privada está no formato correto"
                }
            
            # Obter saldo do remetente
            from_pubkey = keypair.pubkey()
            balance_result = self.get_balance(str(from_pubkey))
            
            if not balance_result.get("success"):
                return {
                    "success": False,
                    "error": f"Não foi possível verificar saldo: {balance_result.get('error')}"
                }
            
            balance_sol = balance_result.get("balance_sol", 0)
            
            # ✅ CORREÇÃO CRÍTICA: Verificar se conta de destino existe e calcular rent
            to_pubkey = Pubkey.from_string(to_address)
            to_balance_result = self.get_balance(to_address)
            to_balance_sol = to_balance_result.get("balance_sol", 0) if to_balance_result.get("success") else 0
            
            # Rent mínimo em Solana é ~0.00089 SOL (890,000 lamports)
            # Se a conta não existe ou tem saldo zero, precisamos adicionar rent
            rent_exempt_minimum = 0.00089  # SOL mínimo para rent exemption
            rent_needed = 0.0
            
            if to_balance_sol == 0:
                # Conta não existe ou está vazia - precisa criar e pagar rent
                # Se o valor enviado for menor que rent mínimo, adicionar rent
                if amount_sol < rent_exempt_minimum:
                    rent_needed = rent_exempt_minimum - amount_sol
                    print(f"   ⚠️  Conta de destino não existe ou está vazia")
                    print(f"   💰 Adicionando rent mínimo: {rent_needed} SOL (total: {amount_sol + rent_needed} SOL)")
            
            # Verificar saldo suficiente (incluindo fee e rent se necessário)
            fee_estimate = 0.000005  # ~5000 lamports (fee típico Solana)
            total_required = amount_sol + rent_needed + fee_estimate
            
            if balance_sol < total_required:
                return {
                    "success": False,
                    "error": f"Saldo insuficiente. Disponível: {balance_sol} SOL, Necessário: {total_required} SOL (amount: {amount_sol}, rent: {rent_needed}, fee: {fee_estimate})",
                    "balance": balance_sol,
                    "required": total_required,
                    "breakdown": {
                        "amount": amount_sol,
                        "rent": rent_needed,
                        "fee": fee_estimate
                    }
                }
            
            # Ajustar amount_lamports se precisar adicionar rent
            if rent_needed > 0:
                amount_sol = amount_sol + rent_needed
                amount_lamports = int(amount_sol * 1e9)
                print(f"   ✅ Valor ajustado para incluir rent: {amount_sol} SOL ({amount_lamports} lamports)")
            
            # Criar transação
            to_pubkey = Pubkey.from_string(to_address)
            
            # Criar instrução de transferência
            instruction = transfer(
                TransferParams(
                    from_pubkey=from_pubkey,
                    to_pubkey=to_pubkey,
                    lamports=amount_lamports
                )
            )
            
            # Obter recent blockhash ANTES de criar a transação
            recent_blockhash_resp = self.client.get_latest_blockhash(commitment=Confirmed)
            recent_blockhash = recent_blockhash_resp.value.blockhash
            
            # ✅ CORREÇÃO: Nova API do solders - usar new_signed_with_payer
            # new_signed_with_payer(instructions, payer, signing_keypairs, recent_blockhash)
            # Este método cria a Message, assina e cria a Transaction automaticamente
            # Não precisamos criar Message separadamente
            transaction = Transaction.new_signed_with_payer(
                [instruction],      # Lista de instruções
                from_pubkey,        # Payer (remetente)
                [keypair],          # Lista de keypairs para assinar
                recent_blockhash    # Blockhash recente
            )
            
            # Enviar transação
            # A transação já está assinada pelo new_signed_with_payer, então só precisamos passar a transação
            # Criar TxOpts corretamente com os parâmetros desejados
            opts = TxOpts(
                skip_preflight=False,
                preflight_commitment=Confirmed,
                skip_confirmation=False
            )
            
            print(f"   📡 Enviando transação Solana...")
            print(f"      De: {str(from_pubkey)}")
            print(f"      Para: {to_address}")
            print(f"      Valor: {amount_sol} SOL ({amount_lamports} lamports)")
            
            response = self.client.send_transaction(
                transaction,
                opts=opts
            )
            
            print(f"   📊 Resposta do RPC: {response}")
            
            if response.value:
                tx_signature = str(response.value)
                print(f"   ✅ Transação enviada! Signature: {tx_signature}")
                
                # Aguardar confirmação
                print(f"   ⏳ Aguardando confirmação...")
                confirmation = self.client.confirm_transaction(
                    tx_signature,
                    commitment=Confirmed,
                    timeout=30
                )
                
                confirmation_status = None
                if confirmation.value:
                    confirmation_status = confirmation.value[0].confirmation_status if hasattr(confirmation.value[0], 'confirmation_status') else "confirmed"
                    print(f"   ✅ Transação confirmada! Status: {confirmation_status}")
                
                return {
                    "success": True,
                    "tx_signature": tx_signature,
                    "from": str(from_pubkey),
                    "to": to_address,
                    "amount_sol": amount_sol,
                    "amount_lamports": amount_lamports,
                    "network": self.network,
                    "confirmed": confirmation_status,
                    "explorer_url": f"https://explorer.solana.com/tx/{tx_signature}?cluster={self.network}"
                }
            else:
                error_msg = "Transação não foi enviada"
                if hasattr(response, 'error'):
                    error_msg = f"Erro do RPC: {response.error}"
                print(f"   ❌ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "response": str(response)
                }
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"   ❌ Exceção ao enviar transação Solana: {e}")
            print(f"   📋 Traceback completo:")
            print(error_trace)
            return {
                "success": False,
                "error": f"Erro ao enviar transação Solana: {e}",
                "traceback": error_trace
            }
    
    def get_transaction_status(self, tx_signature: str) -> Dict:
        """Obter status de uma transação"""
        try:
            if self.client:
                signature = Pubkey.from_string(tx_signature) if isinstance(tx_signature, str) else tx_signature
                response = self.client.get_transaction(
                    signature,
                    commitment=Confirmed
                )
                
                if response.value:
                    tx_data = response.value
                    return {
                        "success": True,
                        "tx_signature": tx_signature,
                        "slot": tx_data.slot,
                        "block_time": tx_data.block_time,
                        "status": "confirmed" if tx_data.meta and tx_data.meta.err is None else "failed"
                    }
            
            return {
                "success": False,
                "error": "Transação não encontrada"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao obter status: {e}"
            }
    
    def _send_transaction_via_rpc_direct(
        self,
        from_private_key: str,
        to_address: str,
        amount_sol: float
    ) -> Dict:
        """
        Método alternativo: Enviar transação Solana via RPC HTTP direto
        (sem precisar das bibliotecas solders/solana)
        
        NOTA: Este método requer construção manual da transação Solana,
        o que é complexo. Por enquanto, retorna erro informativo.
        """
        try:
            # Validar endereço
            is_valid, error = self.validate_address(to_address)
            if not is_valid:
                return {
                    "success": False,
                    "error": f"Endereço de destino inválido: {error}"
                }
            
            # Converter para lamports
            amount_lamports = int(amount_sol * 1e9)
            
            # Verificar saldo primeiro (isso funciona sem bibliotecas)
            from_address = os.getenv('SOLANA_ADDRESS')
            if not from_address:
                # Tentar derivar endereço da chave privada (simplificado)
                try:
                    keypair_bytes = base58.b58decode(from_private_key.strip())
                    # Em Solana, a chave privada é 64 bytes: [32 bytes privados][32 bytes públicos]
                    # A chave pública está nos últimos 32 bytes
                    public_key_bytes = keypair_bytes[32:64] if len(keypair_bytes) == 64 else keypair_bytes[:32]
                    from_address = base58.b58encode(public_key_bytes).decode('utf-8')
                except:
                    return {
                        "success": False,
                        "error": "Não foi possível derivar endereço da chave privada. Configure SOLANA_ADDRESS no .env"
                    }
            
            balance_result = self.get_balance(from_address)
            if not balance_result.get("success"):
                return {
                    "success": False,
                    "error": f"Não foi possível verificar saldo: {balance_result.get('error')}"
                }
            
            balance_sol = balance_result.get("balance_sol", 0)
            fee_estimate = 0.000005
            required = amount_sol + fee_estimate
            
            if balance_sol < required:
                return {
                    "success": False,
                    "error": f"Saldo insuficiente. Disponível: {balance_sol} SOL, Necessário: {required} SOL",
                    "balance": balance_sol,
                    "required": required
                }
            
            # ❌ CONSTRUÇÃO MANUAL DE TRANSAÇÃO SOLANA É MUITO COMPLEXA
            # Requer: serialização de instruções, assinatura Ed25519, construção de transação versionada
            # Por enquanto, retornar erro informativo sugerindo instalação das bibliotecas
            
            return {
                "success": False,
                "error": "Bibliotecas Solana não instaladas no servidor Render",
                "note": "As bibliotecas 'solana' e 'solders' são necessárias para enviar transações Solana. A biblioteca 'solders' precisa ser compilada (Rust), o que pode estar falhando no build do Render.",
                "solution": "1) Verifique os logs de build do Render para erros de compilação do 'solders', 2) Considere usar uma versão pré-compilada (wheel) se disponível, 3) Ou configure um ambiente de build com Rust compiler",
                "requirements_check": "requirements.txt contém: solana>=0.30.2 e solders>=0.18.0",
                "debug": "SOLANA_LIBS_AVAILABLE = False - tentativa de fallback via RPC direto não implementada (muito complexo)",
                "alternative": "Para testar localmente, instale: pip install solana solders"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro no método alternativo: {str(e)}"
            }

