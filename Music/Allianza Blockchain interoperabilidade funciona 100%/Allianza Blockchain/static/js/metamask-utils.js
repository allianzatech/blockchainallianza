/**
 * 🔐 MetaMask Utilities
 * Utilitários para conexão segura com MetaMask
 */

const MetaMaskUtils = {
    /**
     * Verifica se MetaMask está disponível
     */
    isAvailable: function() {
        return typeof window !== 'undefined' && 
               typeof window.ethereum !== 'undefined' && 
               window.ethereum.isMetaMask === true;
    },

    /**
     * Conecta ao MetaMask de forma segura
     */
    connect: async function() {
        if (!this.isAvailable()) {
            throw new Error('MetaMask extension not found. Por favor, instale a extensão MetaMask.');
        }

        try {
            // Solicitar acesso à conta
            const accounts = await window.ethereum.request({
                method: 'eth_requestAccounts'
            });

            if (!accounts || accounts.length === 0) {
                throw new Error('Nenhuma conta MetaMask encontrada');
            }

            return {
                success: true,
                account: accounts[0],
                accounts: accounts
            };
        } catch (error) {
            // Tratar erros específicos do MetaMask
            if (error.code === 4001) {
                throw new Error('Usuário rejeitou a conexão com MetaMask');
            } else if (error.code === -32002) {
                throw new Error('Requisição já pendente. Por favor, verifique a extensão MetaMask.');
            } else {
                throw new Error(`Erro ao conectar MetaMask: ${error.message}`);
            }
        }
    },

    /**
     * Obtém a conta atual conectada
     */
    getCurrentAccount: async function() {
        if (!this.isAvailable()) {
            return null;
        }

        try {
            const accounts = await window.ethereum.request({
                method: 'eth_accounts'
            });
            return accounts.length > 0 ? accounts[0] : null;
        } catch (error) {
            console.error('Erro ao obter conta MetaMask:', error);
            return null;
        }
    },

    /**
     * Obtém a chain ID atual
     */
    getChainId: async function() {
        if (!this.isAvailable()) {
            return null;
        }

        try {
            const chainId = await window.ethereum.request({
                method: 'eth_chainId'
            });
            return chainId;
        } catch (error) {
            console.error('Erro ao obter chain ID:', error);
            return null;
        }
    },

    /**
     * Escuta mudanças de conta
     */
    onAccountsChanged: function(callback) {
        if (!this.isAvailable()) {
            return;
        }

        window.ethereum.on('accountsChanged', (accounts) => {
            callback(accounts);
        });
    },

    /**
     * Escuta mudanças de chain
     */
    onChainChanged: function(callback) {
        if (!this.isAvailable()) {
            return;
        }

        window.ethereum.on('chainChanged', (chainId) => {
            callback(chainId);
        });
    }
};

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.MetaMaskUtils = MetaMaskUtils;
}










