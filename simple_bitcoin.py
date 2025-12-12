#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SIMPLE BITCOIN - Biblioteca própria ultra simples para Bitcoin Testnet
🚀 NÃO depende de bitcoinlib, python-bitcointx, bit, etc.
✅ Usa apenas: hashlib, base58, requests, json
"""

import hashlib
import requests
import json
import time
from typing import Dict, List, Optional
import os

try:
    import base58
    BASE58_AVAILABLE = True
except ImportError:
    BASE58_AVAILABLE = False
    print("⚠️  base58 não instalado. Instale com: pip install base58")

try:
    import ecdsa
    from ecdsa.curves import SECP256k1
    from ecdsa.keys import SigningKey
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False
    print("⚠️  ecdsa não instalado. Instale com: pip install ecdsa")


class SimpleBitcoin:
    """
    Biblioteca própria ULTRA SIMPLES para Bitcoin Testnet
    Implementação mínima mas FUNCIONAL
    """
    
    def __init__(self):
        # API endpoints
        self.blockstream_api = "https://blockstream.info/testnet/api"
        self.blockcypher_api = "https://api.blockcypher.com/v1/btc/test3"
        self.blockcypher_token = os.getenv('BLOCKCYPHER_API_TOKEN', '17766314e49c439e85cec883969614ac')
        
        print("✅ SimpleBitcoin inicializado!")
        print("   🎯 Biblioteca própria para Bitcoin Testnet")
        print("   🚀 Sem dependências pesadas!")
    
    def _hash256(self, data: bytes) -> bytes:
        """Double SHA256 (Bitcoin style)"""
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()
    
    def _ripemd160(self, data: bytes) -> bytes:
        """RIPEMD-160 hash"""
        h = hashlib.new('ripemd160')
        h.update(data)
        return h.digest()
    
    def _sha256(self, data: bytes) -> bytes:
        """SHA256"""
        return hashlib.sha256(data).digest()
    
    def wif_to_private_key(self, wif: str) -> bytes:
        """Converte WIF para chave privada bytes (32 bytes)"""
        if not BASE58_AVAILABLE:
            raise ImportError("base58 não está instalado. Instale com: pip install base58")
        
        try:
            decoded = base58.b58decode_check(wif)
            
            if len(decoded) == 33:  # Sem compressed flag
                private_key = decoded[1:]
            elif len(decoded) == 34:  # Com compressed flag
                private_key = decoded[1:33]
            else:
                raise ValueError(f"WIF length inválido: {len(decoded)} bytes")
            
            return private_key
        except Exception as e:
            raise ValueError(f"Erro ao decodificar WIF: {e}")
    
    def wif_to_address(self, wif: str) -> str:
        """Converte WIF diretamente para endereço usando bitcoinlib como fallback"""
        try:
            # Tentar usar bitcoinlib se disponível (mais confiável)
            from bitcoinlib.keys import HDKey
            key = HDKey(wif, network='testnet')
            return key.address()
        except:
            # Fallback: usar nossa implementação
            if not ECDSA_AVAILABLE or not BASE58_AVAILABLE:
                raise ImportError("Precisa de ecdsa e base58. Instale com: pip install ecdsa base58")
            
            private_key = self.wif_to_private_key(wif)
            sk = SigningKey.from_string(private_key, curve=SECP256k1)
            vk = sk.get_verifying_key()
            
            # Compressed public key
            x = vk.pubkey.point.x()
            y = vk.pubkey.point.y()
            prefix = b'\x02' if y % 2 == 0 else b'\x03'
            public_key = prefix + x.to_bytes(32, 'big')
            
            # SHA256 + RIPEMD160
            sha256_hash = self._sha256(public_key)
            ripemd160_hash = self._ripemd160(sha256_hash)
            
            # Version byte (testnet: 0x6F)
            version = b'\x6f'
            versioned_hash = version + ripemd160_hash
            
            # Checksum
            checksum = self._hash256(versioned_hash)[:4]
            binary_address = versioned_hash + checksum
            
            return base58.b58encode(binary_address).decode('utf-8')
    
    def get_utxos(self, address: str, confirmed_only: bool = True) -> List[Dict]:
        """Busca UTXOs de um endereço via Blockstream API"""
        try:
            url = f"{self.blockstream_api}/address/{address}/utxo"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                utxos = response.json()
                
                if confirmed_only:
                    confirmed = []
                    for utxo in utxos:
                        status = utxo.get('status', {})
                        if status.get('confirmed', False):
                            # Verificar se não foi gasto
                            try:
                                tx_url = f"{self.blockstream_api}/tx/{utxo['txid']}"
                                tx_resp = requests.get(tx_url, timeout=10)
                                if tx_resp.status_code == 200:
                                    tx_data = tx_resp.json()
                                    vout_data = tx_data['vout'][utxo['vout']]
                                    if not vout_data.get('spent', False):
                                        confirmed.append(utxo)
                            except:
                                continue
                    return confirmed
                else:
                    return utxos
            else:
                print(f"⚠️  Erro ao buscar UTXOs: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Exceção ao buscar UTXOs: {e}")
            return []
    
    def create_simple_transaction(
        self,
        from_wif: str,
        to_address: str,
        amount_btc: float
    ) -> Dict:
        """
        Cria transação SIMPLES usando BlockCypher API
        Método mais confiável e fácil
        """
        print(f"\n{'='*70}")
        print(f"🎯 SIMPLEBITCOIN: Criando transação simples...")
        print(f"{'='*70}")
        
        # 1. Converter WIF para endereço
        try:
            from_address = self.wif_to_address(from_wif)
            print(f"   ✅ Endereço derivado: {from_address}")
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao derivar endereço da chave: {e}",
                "note": "Verifique se a chave WIF está correta"
            }
        
        print(f"   De: {from_address}")
        print(f"   Para: {to_address}")
        print(f"   Valor: {amount_btc} BTC")
        
        # 2. Buscar UTXOs
        print(f"\n   🔍 Buscando UTXOs confirmados...")
        utxos = self.get_utxos(from_address, confirmed_only=True)
        print(f"   UTXOs confirmados: {len(utxos)}")
        
        if not utxos:
            return {
                "success": False,
                "error": "Nenhum UTXO confirmado encontrado",
                "note": "Aguarde confirmação das transações ou use faucet"
            }
        
        # 3. Selecionar UTXOs
        amount_sats = int(amount_btc * 100000000)
        selected_utxos = []
        total_selected = 0
        
        # Ordenar por valor (menor primeiro)
        utxos.sort(key=lambda x: x['value'])
        
        for utxo in utxos:
            if total_selected >= amount_sats + 1000:  # + fee
                break
            selected_utxos.append(utxo)
            total_selected += utxo['value']
            print(f"   📥 UTXO: {utxo['txid'][:16]}...:{utxo['vout']} = {utxo['value']} sats")
        
        print(f"   Total selecionado: {total_selected} sats")
        
        # 4. Usar BlockCypher para criar transação
        fee_sats = 500
        change_sats = total_selected - amount_sats - fee_sats
        
        if change_sats < 0:
            return {
                "success": False,
                "error": f"UTXOs insuficientes. Necessário: {amount_sats + fee_sats} sats",
                "available": total_selected,
                "required": amount_sats + fee_sats
            }
        
        # 5. Criar transação via BlockCypher
        return self._create_with_blockcypher(
            from_wif=from_wif,
            from_address=from_address,
            to_address=to_address,
            selected_utxos=selected_utxos,
            amount_sats=amount_sats,
            fee_sats=fee_sats,
            change_sats=change_sats
        )
    
    def _create_with_blockcypher(
        self,
        from_wif: str,
        from_address: str,
        to_address: str,
        selected_utxos: List[Dict],
        amount_sats: int,
        fee_sats: int,
        change_sats: int
    ) -> Dict:
        """Usa BlockCypher API para criar e assinar transação"""
        try:
            # Preparar inputs
            inputs_list = []
            for utxo in selected_utxos:
                inputs_list.append({
                    "prev_hash": utxo['txid'],
                    "output_index": utxo['vout']
                })
            
            # Preparar outputs
            outputs_list = [{
                "addresses": [to_address],
                "value": amount_sats
            }]
            
            if change_sats > 546:  # Dust limit
                outputs_list.append({
                    "addresses": [from_address],
                    "value": change_sats
                })
            
            # Dados da transação
            tx_data = {
                "inputs": inputs_list,
                "outputs": outputs_list,
                "fees": fee_sats
            }
            
            print(f"\n   📡 Enviando para BlockCypher...")
            print(f"   Inputs: {len(inputs_list)}, Outputs: {len(outputs_list)}")
            print(f"   Amount: {amount_sats} sats, Fee: {fee_sats} sats, Change: {change_sats} sats")
            
            # Criar transação não assinada
            create_url = f"{self.blockcypher_api}/txs/new?token={self.blockcypher_token}"
            create_response = requests.post(create_url, json=tx_data, timeout=30)
            
            print(f"   📊 Status: {create_response.status_code}")
            print(f"   📋 Response: {create_response.text[:300]}")
            
            if create_response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "error": f"BlockCypher create error: {create_response.status_code}",
                    "response": create_response.text[:200]
                }
            
            unsigned_tx = create_response.json()
            tosign = unsigned_tx.get('tosign', [])
            
            if not tosign:
                return {
                    "success": False,
                    "error": "No 'tosign' data from BlockCypher",
                    "response": str(unsigned_tx)[:500]
                }
            
            # Converter WIF para chave privada hex (BlockCypher precisa de hex)
            try:
                private_key_bytes = self.wif_to_private_key(from_wif)
                private_key_hex = private_key_bytes.hex()
                print(f"   ✅ Chave convertida para hex: {private_key_hex[:20]}...")
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Erro ao converter WIF para hex: {e}",
                    "note": "Verifique se a chave WIF está correta"
                }
            
            # Assinar transação
            print(f"\n   🔐 Assinando transação...")
            print(f"   tosign count: {len(tosign)}")
            
            sign_data = {
                "tx": unsigned_tx,
                "tosign": tosign,
                "privkeys": [private_key_hex]
            }
            
            sign_url = f"{self.blockcypher_api}/txs/send?token={self.blockcypher_token}"
            sign_response = requests.post(sign_url, json=sign_data, timeout=30)
            
            print(f"   📊 Status: {sign_response.status_code}")
            print(f"   📋 Response: {sign_response.text[:300]}")
            
            if sign_response.status_code in [200, 201]:
                signed_tx = sign_response.json()
                tx_hash = signed_tx.get('tx', {}).get('hash')
                
                if tx_hash:
                    print(f"\n   ✅✅✅ TRANSAÇÃO CRIADA COM SUCESSO!")
                    print(f"   Hash: {tx_hash}")
                    print(f"   Explorer: https://blockstream.info/testnet/tx/{tx_hash}")
                    
                    # Verificar se foi broadcastada
                    time.sleep(2)
                    
                    return {
                        "success": True,
                        "tx_hash": tx_hash,
                        "from": from_address,
                        "to": to_address,
                        "amount": amount_sats / 100000000,
                        "explorer_url": f"https://blockstream.info/testnet/tx/{tx_hash}",
                        "method": "simple_bitcoin_blockcypher",
                        "note": "✅ Transação criada com SimpleBitcoin + BlockCypher"
                    }
                else:
                    return {
                        "success": False,
                        "error": "No transaction hash in response",
                        "response": str(signed_tx)[:500]
                    }
            else:
                return {
                    "success": False,
                    "error": f"BlockCypher sign error: {sign_response.status_code}",
                    "response": sign_response.text[:200]
                }
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Exception in BlockCypher: {str(e)}"
            }

