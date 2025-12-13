import hashlib
import base58

def double_sha256(data):
    """Calcula SHA256(SHA256(data))"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def encode_base58_checksum(payload):
    """
    Codifica um payload em Base58 com checksum (Base58Check).
    
    Args:
        payload (bytes): O dado a ser codificado (ex: versão + hash da chave pública).
        
    Returns:
        str: A string codificada em Base58Check.
    """
    # 1. Calcular o checksum (primeiros 4 bytes do double_sha256)
    checksum = double_sha256(payload)[:4]
    
    # 2. Concatenar payload e checksum
    full_payload = payload + checksum
    
    # 3. Codificar em Base58
    return base58.b58encode(full_payload).decode('utf-8')

def decode_base58_checksum(encoded_string):
    """
    Decodifica uma string Base58Check e verifica o checksum.
    
    Args:
        encoded_string (str): A string codificada em Base58Check.
        
    Returns:
        bytes: O payload decodificado se o checksum for válido, ou None.
    """
    try:
        # 1. Decodificar de Base58
        full_payload = base58.b58decode(encoded_string)
        
        # 2. Separar payload e checksum
        checksum = full_payload[-4:]
        payload = full_payload[:-4]
        
        # 3. Recalcular o checksum esperado
        expected_checksum = double_sha256(payload)[:4]
        
        # 4. Verificar o checksum
        if checksum == expected_checksum:
            return payload
        else:
            return None
            
    except ValueError:
        # Erro de decodificação Base58
        return None
    except Exception:
        # Outros erros
        return None

# Constante de versão para endereços Allianza (ex: 0x00 para Bitcoin)
ADDRESS_VERSION = b'\x00'

def generate_allianza_address(public_key_hash):
    """
    Gera um endereço Allianza com Base58Check.
    
    Args:
        public_key_hash (bytes): O hash da chave pública (ex: SHA256).
        
    Returns:
        str: O endereço Allianza.
    """
    # 1. Adicionar byte de versão
    payload = ADDRESS_VERSION + public_key_hash
    
    # 2. Codificar com checksum
    return encode_base58_checksum(payload)

def validate_allianza_address(address):
    """
    Valida um endereço Allianza.
    
    Args:
        address (str): O endereço a ser validado.
        
    Returns:
        bool: True se o endereço for válido, False caso contrário.
    """
    return decode_base58_checksum(address) is not None
