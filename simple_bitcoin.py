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
        """Busca UTXOs de um endereço via Blockstream API com validação completa"""
        try:
            url = f"{self.blockstream_api}/address/{address}/utxo"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                utxos = response.json()
                print(f"   📦 Total UTXOs encontrados: {len(utxos)}")
                
                if confirmed_only:
                    confirmed = []
                    for i, utxo in enumerate(utxos):
                        txid = utxo.get('txid')
                        vout = utxo.get('vout')
                        value = utxo.get('value', 0)
                        status = utxo.get('status', {})
                        
                        # ✅ VALIDAÇÃO 1: Verificar se está confirmado
                        if not status.get('confirmed', False):
                            print(f"   ⚠️  UTXO {i+1}: {txid[:16]}...:{vout} - NÃO CONFIRMADO")
                            continue
                        
                        # ✅ VALIDAÇÃO 2: Verificar se o UTXO existe na rede e não foi gasto
                        try:
                            tx_url = f"{self.blockstream_api}/tx/{txid}"
                            tx_resp = requests.get(tx_url, timeout=10)
                            
                            if tx_resp.status_code != 200:
                                print(f"   ⚠️  UTXO {i+1}: {txid[:16]}...:{vout} - Transação não encontrada (status {tx_resp.status_code})")
                                continue
                            
                            tx_data = tx_resp.json()
                            
                            # ✅ VALIDAÇÃO 3: Verificar se o vout existe
                            if vout >= len(tx_data.get('vout', [])):
                                print(f"   ⚠️  UTXO {i+1}: {txid[:16]}...:{vout} - vout não existe na transação")
                                continue
                            
                            vout_data = tx_data['vout'][vout]
                            
                            # ✅ VALIDAÇÃO 4: Verificar se foi gasto
                            if vout_data.get('spent', False):
                                print(f"   ⚠️  UTXO {i+1}: {txid[:16]}...:{vout} - JÁ FOI GASTO!")
                                continue
                            
                            # ✅ VALIDAÇÃO 5: Verificar se o valor corresponde
                            vout_value = vout_data.get('value', 0)
                            if vout_value != value:
                                print(f"   ⚠️  UTXO {i+1}: {txid[:16]}...:{vout} - Valor não corresponde (esperado {value}, encontrado {vout_value})")
                                # Usar o valor real da transação
                                utxo['value'] = vout_value
                            
                            # ✅ UTXO VÁLIDO!
                            confirmed.append(utxo)
                            print(f"   ✅ UTXO {i+1} VÁLIDO: {txid[:16]}...:{vout} = {utxo['value']} sats")
                            
                        except Exception as val_err:
                            print(f"   ⚠️  UTXO {i+1}: {txid[:16]}...:{vout} - Erro na validação: {val_err}")
                            continue
                    
                    print(f"   ✅ Total UTXOs válidos após validação: {len(confirmed)}")
                    return confirmed
                else:
                    return utxos
            else:
                print(f"   ❌ Erro ao buscar UTXOs: status {response.status_code}")
            return []
                
        except Exception as e:
            print(f"❌ Exceção ao buscar UTXOs: {e}")
            import traceback
            traceback.print_exc()
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
                # ✅ NORMALIZAÇÃO CRÍTICA: BlockCypher precisa de txid em lowercase
                txid = utxo['txid']
                if isinstance(txid, str):
                    txid = txid.strip().lower()
                
                # ✅ CORREÇÃO CRÍTICA: BlockCypher precisa do campo 'value' no input para validação
                inputs_list.append({
                    "prev_hash": txid,  # Normalizado para lowercase
                    "output_index": utxo['vout'],
                    "value": int(utxo['value'])  # ✅ ADICIONAR VALUE - CRÍTICO PARA BLOCKCYPHER
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
            print(f"\n   🔐 Convertendo chave privada WIF para hex...")
            print(f"   WIF recebido: {from_wif[:20]}... (tamanho: {len(from_wif)})")
            print(f"   WIF completo (primeiros 30): {from_wif[:30]}")
            print(f"   WIF completo (últimos 10): ...{from_wif[-10:]}")
            
            private_key_hex = None
            conversion_method = None
            
            # ✅ MÉTODO 1: Tentar usar bitcoinlib (mais confiável)
            try:
                from bitcoinlib.keys import HDKey
                print(f"   🔄 Tentando bitcoinlib...")
                key_obj = HDKey(from_wif, network='testnet')
                private_key_hex = key_obj.private_hex
                conversion_method = "bitcoinlib"
                print(f"   ✅ Chave convertida via bitcoinlib: {private_key_hex[:20]}... (tamanho: {len(private_key_hex)})")
                
                # ✅ VALIDAÇÃO ADICIONAL: Verificar se o endereço derivado corresponde
                derived_address = key_obj.address()
                print(f"   🔍 Endereço derivado da chave: {derived_address}")
                print(f"   🔍 Endereço esperado (from_address): {from_address}")
                print(f"   🔍 Endereços coincidem: {derived_address == from_address}")
                
                if derived_address != from_address:
                    print(f"   ⚠️  AVISO: Endereço derivado não corresponde ao from_address!")
                    print(f"      Isso pode indicar que a chave WIF está incorreta")
                
            except Exception as lib_err:
                print(f"   ❌ bitcoinlib falhou: {lib_err}")
                import traceback
                traceback.print_exc()
                
                # ✅ MÉTODO 2: Tentar nossa implementação própria
                try:
                    print(f"   🔄 Tentando método próprio...")
                    private_key_bytes = self.wif_to_private_key(from_wif)
                    private_key_hex = private_key_bytes.hex()
                    conversion_method = "método próprio"
                    print(f"   ✅ Chave convertida via método próprio: {private_key_hex[:20]}... (tamanho: {len(private_key_hex)})")
                except Exception as own_err:
                    print(f"   ❌ Método próprio também falhou: {own_err}")
                    import traceback
                    traceback.print_exc()
                    return {
                        "success": False,
                        "error": f"Erro ao converter WIF para hex: {own_err}",
                        "note": "Verifique se a chave WIF está correta",
                        "bitcoinlib_error": str(lib_err),
                        "own_method_error": str(own_err),
                        "wif_preview": from_wif[:30] + "..."
                    }
            
            # ✅ VALIDAÇÃO CRÍTICA: Verificar se a chave hex é válida
            if not private_key_hex:
                return {
                    "success": False,
                    "error": "Chave privada hex está vazia após conversão",
                    "note": "A conversão WIF -> hex falhou"
                }
            
            if len(private_key_hex) != 64:
                return {
                    "success": False,
                    "error": f"Chave privada hex tem tamanho inválido: {len(private_key_hex)} (esperado 64)",
                    "note": "A chave privada deve ter 32 bytes (64 caracteres hex)"
                }
            
            # ✅ VALIDAÇÃO: Verificar se é hex válido
            try:
                bytes.fromhex(private_key_hex)
            except ValueError:
                return {
                    "success": False,
                    "error": "Chave privada hex contém caracteres inválidos",
                    "note": "A chave deve ser hexadecimal válida (0-9, a-f)"
                }
            
            print(f"   ✅ Chave privada validada: {len(private_key_hex)} caracteres hex")
            print(f"   ✅ Método de conversão usado: {conversion_method}")
            
            # ✅ VALIDAÇÃO EXTRA: Verificar se a chave hex corresponde ao endereço
            try:
                from bitcoinlib.keys import HDKey
                test_key = HDKey(private_key_hex, network='testnet', key_type='private')
                test_address = test_key.address()
                print(f"   🔍 Validação: Endereço derivado da chave hex: {test_address}")
                print(f"   🔍 Validação: Endereço esperado: {from_address}")
                if test_address != from_address:
                    print(f"   ⚠️  AVISO: Chave hex não corresponde ao endereço esperado!")
                    print(f"      Isso pode causar erro no BlockCypher")
            except Exception as val_err:
                print(f"   ⚠️  Não foi possível validar chave hex: {val_err}")
            
            # Assinar transação
            print(f"\n   🔐 Preparando dados para assinar transação...")
            print(f"   tosign count: {len(tosign)}")
            print(f"   private_key_hex length: {len(private_key_hex)}")
            print(f"   private_key_hex completo (primeiros 30): {private_key_hex[:30]}")
            print(f"   private_key_hex completo (últimos 10): ...{private_key_hex[-10:]}")
            
            # ✅ GARANTIR que privkeys é uma lista com a chave hex
            privkeys_list = [private_key_hex]
            print(f"   📋 privkeys_list preparado: {len(privkeys_list)} chave(s)")
            print(f"   📋 privkeys_list[0] tamanho: {len(privkeys_list[0]) if privkeys_list else 0}")
            
            sign_data = {
                "tx": unsigned_tx,
                "tosign": tosign,
                "privkeys": privkeys_list
            }
            
            print(f"   📋 sign_data preparado:")
            print(f"      - tx: presente ({'tx' in unsigned_tx})")
            print(f"      - tosign: {len(tosign)} hashes")
            print(f"      - privkeys: {len(sign_data['privkeys'])} chave(s)")
            
            # ✅ VALIDAÇÃO FINAL ANTES DE ENVIAR
            print(f"\n   🔍 VALIDAÇÃO FINAL ANTES DE ENVIAR PARA BLOCKCYPHER:")
            print(f"      - private_key_hex existe: {private_key_hex is not None}")
            print(f"      - private_key_hex tamanho: {len(private_key_hex) if private_key_hex else 0}")
            print(f"      - private_key_hex preview: {private_key_hex[:30] if private_key_hex else 'None'}...")
            print(f"      - privkeys no sign_data: {len(sign_data.get('privkeys', []))}")
            print(f"      - tosign count: {len(sign_data.get('tosign', []))}")
            print(f"      - tx existe: {'tx' in sign_data}")
            
            # ✅ VALIDAÇÃO CRÍTICA: Verificar se privkeys não está vazio
            if not sign_data.get('privkeys') or len(sign_data.get('privkeys', [])) == 0:
                return {
                    "success": False,
                    "error": "Chave privada está vazia no sign_data",
                    "note": "A chave privada não foi adicionada corretamente ao sign_data"
                }
            
            if not sign_data['privkeys'][0] or len(sign_data['privkeys'][0]) != 64:
                return {
                    "success": False,
                    "error": f"Chave privada inválida no sign_data: tamanho {len(sign_data['privkeys'][0]) if sign_data['privkeys'][0] else 0}",
                    "note": "A chave privada deve ter exatamente 64 caracteres hex"
                }
            
            sign_url = f"{self.blockcypher_api}/txs/send?token={self.blockcypher_token}"
            print(f"\n   📡 Enviando para BlockCypher: {sign_url}")
            print(f"   📦 Payload (parcial):")
            print(f"      - tx: presente")
            print(f"      - tosign: {len(sign_data['tosign'])} hashes")
            print(f"      - privkeys: {len(sign_data['privkeys'])} chave(s) (tamanho: {len(sign_data['privkeys'][0]) if sign_data['privkeys'] else 0})")
            
            sign_response = requests.post(sign_url, json=sign_data, timeout=30)
            
            print(f"   📊 Status: {sign_response.status_code}")
            print(f"   📋 Response: {sign_response.text[:500]}")
            
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

