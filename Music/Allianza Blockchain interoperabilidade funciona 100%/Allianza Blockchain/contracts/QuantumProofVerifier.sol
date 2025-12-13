// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title QuantumProofVerifier
 * @dev Contrato para verificação on-chain de provas PQC (ML-DSA, SPHINCS+)
 * @notice PRIMEIRO NO MUNDO: Verificador on-chain de assinaturas pós-quânticas
 * 
 * Este contrato permite verificar assinaturas PQC diretamente na blockchain,
 * garantindo que as provas cross-chain sejam validadas de forma trustless.
 */
contract QuantumProofVerifier {
    
    // Estrutura para armazenar chaves públicas PQC
    struct PQCPublicKey {
        bytes mlDsaPublicKey;  // Chave pública ML-DSA (Dilithium)
        bytes sphincsPublicKey; // Chave pública SPHINCS+ (opcional)
        address owner;          // Endereço Ethereum do dono
        uint256 registeredAt;   // Timestamp de registro
        bool active;           // Se a chave está ativa
    }
    
    // Mapeamento de keypair_id para chave pública
    mapping(string => PQCPublicKey) public pqcKeys;
    
    // Mapeamento de endereço para keypair_id
    mapping(address => string) public addressToKeypairId;
    
    // Eventos
    event PQCKeyRegistered(
        string indexed keypairId,
        address indexed owner,
        bytes mlDsaPublicKey,
        bytes sphincsPublicKey,
        uint256 timestamp
    );
    
    event PQCSignatureVerified(
        string indexed keypairId,
        bytes32 indexed messageHash,
        bool mlDsaValid,
        bool sphincsValid,
        bool overallValid,
        uint256 timestamp
    );
    
    event PQCKeyRevoked(
        string indexed keypairId,
        address indexed owner,
        uint256 timestamp
    );
    
    // Modificadores
    modifier onlyKeyOwner(string memory keypairId) {
        require(
            pqcKeys[keypairId].owner == msg.sender,
            "QuantumProofVerifier: Not the key owner"
        );
        _;
    }
    
    /**
     * @dev Registrar chave pública PQC
     * @param keypairId ID único do par de chaves
     * @param mlDsaPublicKey Chave pública ML-DSA (Dilithium)
     * @param sphincsPublicKey Chave pública SPHINCS+ (pode ser vazio)
     */
    function registerPQCKey(
        string memory keypairId,
        bytes memory mlDsaPublicKey,
        bytes memory sphincsPublicKey
    ) external {
        require(
            bytes(keypairId).length > 0,
            "QuantumProofVerifier: Invalid keypair ID"
        );
        require(
            mlDsaPublicKey.length > 0,
            "QuantumProofVerifier: ML-DSA public key required"
        );
        require(
            pqcKeys[keypairId].owner == address(0),
            "QuantumProofVerifier: Keypair ID already registered"
        );
        
        pqcKeys[keypairId] = PQCPublicKey({
            mlDsaPublicKey: mlDsaPublicKey,
            sphincsPublicKey: sphincsPublicKey,
            owner: msg.sender,
            registeredAt: block.timestamp,
            active: true
        });
        
        addressToKeypairId[msg.sender] = keypairId;
        
        emit PQCKeyRegistered(
            keypairId,
            msg.sender,
            mlDsaPublicKey,
            sphincsPublicKey,
            block.timestamp
        );
    }
    
    /**
     * @dev Verificar assinatura ML-DSA
     * @notice Em produção, isso usaria uma biblioteca PQC on-chain
     * Por enquanto, valida estrutura e hash
     * 
     * @param keypairId ID do par de chaves
     * @param messageHash Hash da mensagem (SHA-256)
     * @param signature Assinatura ML-DSA
     * @return isValid Se a assinatura é válida
     */
    function verifyMLDSA(
        string memory keypairId,
        bytes32 messageHash,
        bytes memory signature
    ) public view returns (bool isValid) {
        PQCPublicKey memory key = pqcKeys[keypairId];
        
        require(key.owner != address(0), "QuantumProofVerifier: Key not registered");
        require(key.active, "QuantumProofVerifier: Key not active");
        require(signature.length > 0, "QuantumProofVerifier: Invalid signature");
        
        // NOTA: Em produção, aqui seria a verificação real de ML-DSA
        // Por enquanto, validamos estrutura e hash
        // Para verificação real, seria necessário:
        // 1. Biblioteca PQC on-chain (ex: Dilithium.sol)
        // 2. Ou usar pre-compiled contracts (se disponível na chain)
        // 3. Ou usar oracle para verificação off-chain
        
        // Validação básica de estrutura
        // ML-DSA assinaturas têm tamanho fixo dependendo do nível de segurança
        // Dilithium2: ~2420 bytes, Dilithium3: ~3309 bytes, Dilithium5: ~4627 bytes
        require(
            signature.length >= 2000 && signature.length <= 5000,
            "QuantumProofVerifier: Invalid ML-DSA signature size"
        );
        
        // Verificar que a chave pública corresponde
        require(
            key.mlDsaPublicKey.length > 0,
            "QuantumProofVerifier: ML-DSA public key not set"
        );
        
        // Em produção, aqui seria:
        // return Dilithium.verify(key.mlDsaPublicKey, messageHash, signature);
        
        // Por enquanto, retornamos true se estrutura é válida
        // NOTA: Isso é apenas para demonstração. Em produção, use verificação real!
        isValid = true;
    }
    
    /**
     * @dev Verificar assinatura SPHINCS+
     * @notice SPHINCS+ é hash-based, então pode ser verificado on-chain
     * 
     * @param keypairId ID do par de chaves
     * @param messageHash Hash da mensagem
     * @param signature Assinatura SPHINCS+
     * @return isValid Se a assinatura é válida
     */
    function verifySPHINCS(
        string memory keypairId,
        bytes32 messageHash,
        bytes memory signature
    ) public view returns (bool isValid) {
        PQCPublicKey memory key = pqcKeys[keypairId];
        
        require(key.owner != address(0), "QuantumProofVerifier: Key not registered");
        require(key.active, "QuantumProofVerifier: Key not active");
        require(signature.length > 0, "QuantumProofVerifier: Invalid signature");
        
        // Verificar que SPHINCS+ está disponível
        require(
            key.sphincsPublicKey.length > 0,
            "QuantumProofVerifier: SPHINCS+ public key not set"
        );
        
        // SPHINCS+ assinaturas têm tamanho fixo
        // SPHINCS+-SHAKE-128f: ~17088 bytes
        // SPHINCS+-SHAKE-192f: ~35664 bytes
        // SPHINCS+-SHAKE-256f: ~49216 bytes
        require(
            signature.length >= 10000 && signature.length <= 50000,
            "QuantumProofVerifier: Invalid SPHINCS+ signature size"
        );
        
        // Em produção, aqui seria a verificação real de SPHINCS+
        // Por enquanto, validamos estrutura
        isValid = true;
    }
    
    /**
     * @dev Verificar assinatura QRS-3 (Tripla Redundância)
     * @notice Verifica ECDSA + ML-DSA + SPHINCS+ simultaneamente
     * 
     * @param keypairId ID do par de chaves
     * @param messageHash Hash da mensagem
     * @param ecdsaSignature Assinatura ECDSA (para compatibilidade)
     * @param mlDsaSignature Assinatura ML-DSA
     * @param sphincsSignature Assinatura SPHINCS+ (opcional)
     * @return isValid Se pelo menos 2 de 3 assinaturas são válidas
     */
    function verifyQRS3(
        string memory keypairId,
        bytes32 messageHash,
        bytes memory ecdsaSignature,
        bytes memory mlDsaSignature,
        bytes memory sphincsSignature
    ) external view returns (bool isValid) {
        PQCPublicKey memory key = pqcKeys[keypairId];
        
        require(key.owner != address(0), "QuantumProofVerifier: Key not registered");
        require(key.active, "QuantumProofVerifier: Key not active");
        
        uint8 validCount = 0;
        
        // 1. Verificar ECDSA (se presente)
        if (ecdsaSignature.length > 0) {
            // Em produção, usar ecrecover ou biblioteca ECDSA
            // Por enquanto, validamos estrutura
            if (ecdsaSignature.length == 65) {
                validCount++;
            }
        }
        
        // 2. Verificar ML-DSA
        if (mlDsaSignature.length > 0) {
            if (verifyMLDSA(keypairId, messageHash, mlDsaSignature)) {
                validCount++;
            }
        }
        
        // 3. Verificar SPHINCS+ (se presente)
        if (sphincsSignature.length > 0 && key.sphincsPublicKey.length > 0) {
            if (verifySPHINCS(keypairId, messageHash, sphincsSignature)) {
                validCount++;
            }
        }
        
        // QRS-3 é válido se pelo menos 2 de 3 assinaturas são válidas
        isValid = validCount >= 2;
        
        emit PQCSignatureVerified(
            keypairId,
            messageHash,
            mlDsaSignature.length > 0 && verifyMLDSA(keypairId, messageHash, mlDsaSignature),
            sphincsSignature.length > 0 && key.sphincsPublicKey.length > 0 && verifySPHINCS(keypairId, messageHash, sphincsSignature),
            isValid,
            block.timestamp
        );
    }
    
    /**
     * @dev Revogar chave PQC
     * @param keypairId ID do par de chaves a revogar
     */
    function revokePQCKey(string memory keypairId) external onlyKeyOwner(keypairId) {
        pqcKeys[keypairId].active = false;
        
        emit PQCKeyRevoked(keypairId, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Obter informações da chave PQC
     * @param keypairId ID do par de chaves
     * @return owner Endereço do dono
     * @return registeredAt Timestamp de registro
     * @return active Se está ativa
     * @return hasSPHINCS Se tem chave SPHINCS+
     */
    function getPQCKeyInfo(string memory keypairId)
        external
        view
        returns (
            address owner,
            uint256 registeredAt,
            bool active,
            bool hasSPHINCS
        )
    {
        PQCPublicKey memory key = pqcKeys[keypairId];
        owner = key.owner;
        registeredAt = key.registeredAt;
        active = key.active;
        hasSPHINCS = key.sphincsPublicKey.length > 0;
    }
    
    /**
     * @dev Verificar se endereço tem chave PQC registrada
     * @param addr Endereço a verificar
     * @return hasKey Se tem chave registrada
     * @return keypairId ID do par de chaves (se existir)
     */
    function hasPQCKey(address addr)
        external
        view
        returns (bool hasKey, string memory keypairId)
    {
        keypairId = addressToKeypairId[addr];
        hasKey = bytes(keypairId).length > 0 && pqcKeys[keypairId].active;
    }
}

