/**
 * Allianza Blockchain SDK - JavaScript
 * Baseado em ethers.js para compatibilidade máxima
 * 
 * @module allianza-sdk
 */

const { ethers } = require('ethers');

/**
 * Provider customizado para Allianza Blockchain
 */
class AllianzaProvider extends ethers.providers.JsonRpcProvider {
    constructor(url = 'http://localhost:8545') {
        super(url);
        this.chainId = 12345; // Allianza Chain ID
        this.chainName = 'Allianza Blockchain';
        this.nativeCurrency = {
            name: 'Allianza',
            symbol: 'ALZ',
            decimals: 18
        };
    }

    /**
     * Envia transação cross-chain
     * @param {string} targetChain - Chain de destino (bitcoin, ethereum, polygon, etc.)
     * @param {string} recipient - Endereço de destino
     * @param {string} amount - Quantidade (em wei ou unidades nativas)
     * @returns {Promise<Object>} Resultado da transação
     */
    async sendCrossChainTransaction(targetChain, recipient, amount) {
        const method = 'allianza_sendCrossChain';
        const params = [targetChain, recipient, amount];
        
        return this.send(method, params);
    }

    /**
     * Verifica status de transferência cross-chain
     * @param {string} txHash - Hash da transação
     * @returns {Promise<Object>} Status da transferência
     */
    async getCrossChainStatus(txHash) {
        const method = 'allianza_getCrossChainStatus';
        const params = [txHash];
        
        return this.send(method, params);
    }

    /**
     * Obtém saldo cross-chain
     * @param {string} address - Endereço
     * @param {string} chain - Chain (bitcoin, ethereum, etc.)
     * @returns {Promise<string>} Saldo
     */
    async getCrossChainBalance(address, chain) {
        const method = 'allianza_getCrossChainBalance';
        const params = [address, chain];
        
        return this.send(method, params);
    }
}

/**
 * Wallet customizada para Allianza Blockchain
 */
class AllianzaWallet extends ethers.Wallet {
    constructor(privateKey, provider) {
        super(privateKey, provider);
    }

    /**
     * Envia transação cross-chain
     * @param {string} targetChain - Chain de destino
     * @param {string} recipient - Endereço de destino
     * @param {string} amount - Quantidade
     * @param {Object} options - Opções adicionais
     * @returns {Promise<Object>} Resultado da transação
     */
    async sendCrossChainTransaction(targetChain, recipient, amount, options = {}) {
        if (!this.provider || !(this.provider instanceof AllianzaProvider)) {
            throw new Error('Provider deve ser AllianzaProvider');
        }

        const tx = {
            to: recipient,
            value: ethers.utils.parseEther(amount.toString()),
            chain: targetChain,
            ...options
        };

        const signedTx = await this.signTransaction(tx);
        
        return this.provider.sendCrossChainTransaction(
            targetChain,
            recipient,
            amount
        );
    }

    /**
     * Stake tokens para validação
     * @param {string} amount - Quantidade para stake
     * @returns {Promise<Object>} Resultado do stake
     */
    async stake(amount) {
        const method = 'allianza_stake';
        const params = [this.address, ethers.utils.parseEther(amount.toString())];
        
        return this.provider.send(method, params);
    }

    /**
     * Unstake tokens
     * @param {string} amount - Quantidade para unstake
     * @returns {Promise<Object>} Resultado do unstake
     */
    async unstake(amount) {
        const method = 'allianza_unstake';
        const params = [this.address, ethers.utils.parseEther(amount.toString())];
        
        return this.provider.send(method, params);
    }
}

/**
 * Cliente principal do SDK
 */
class AllianzaSDK {
    constructor(rpcUrl = 'http://localhost:8545') {
        this.provider = new AllianzaProvider(rpcUrl);
    }

    /**
     * Cria nova wallet
     * @returns {AllianzaWallet} Nova wallet
     */
    createWallet() {
        const wallet = ethers.Wallet.createRandom();
        return new AllianzaWallet(wallet.privateKey, this.provider);
    }

    /**
     * Conecta wallet existente
     * @param {string} privateKey - Chave privada
     * @returns {AllianzaWallet} Wallet conectada
     */
    connectWallet(privateKey) {
        return new AllianzaWallet(privateKey, this.provider);
    }

    /**
     * Obtém informações da rede
     * @returns {Promise<Object>} Informações da rede
     */
    async getNetworkInfo() {
        const method = 'allianza_getNetworkInfo';
        return this.provider.send(method, []);
    }

    /**
     * Obtém lista de validadores
     * @returns {Promise<Array>} Lista de validadores
     */
    async getValidators() {
        const method = 'allianza_getValidators';
        return this.provider.send(method, []);
    }

    /**
     * Obtém informações de um validador
     * @param {string} address - Endereço do validador
     * @returns {Promise<Object>} Informações do validador
     */
    async getValidatorInfo(address) {
        const method = 'allianza_getValidatorInfo';
        return this.provider.send(method, [address]);
    }
}

module.exports = {
    AllianzaSDK,
    AllianzaProvider,
    AllianzaWallet
};






