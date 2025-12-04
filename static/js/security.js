/**
 * 🔐 Security Utilities - Frontend
 * Sanitização e proteção contra XSS
 */

const SecurityUtils = {
    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml: function(text) {
        if (typeof text !== 'string') {
            text = String(text);
        }
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    /**
     * Sanitiza string para uso seguro em innerHTML
     */
    sanitizeForHTML: function(text) {
        return this.escapeHtml(text);
    },
    
    /**
     * Sanitiza dados para JSON
     */
    sanitizeForJSON: function(data) {
        if (typeof data === 'string') {
            // Remover caracteres de controle
            return data.replace(/[\x00-\x1f\x7f-\x9f]/g, '').substring(0, 10000);
        } else if (Array.isArray(data)) {
            return data.map(item => this.sanitizeForJSON(item));
        } else if (data && typeof data === 'object') {
            const sanitized = {};
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    sanitized[key] = this.sanitizeForJSON(data[key]);
                }
            }
            return sanitized;
        }
        return data;
    },
    
    /**
     * Define textContent de forma segura (preferido sobre innerHTML)
     */
    setTextContent: function(element, text) {
        if (element) {
            element.textContent = text;
        }
    },
    
    /**
     * Define innerHTML de forma segura (com sanitização)
     */
    setInnerHTML: function(element, html) {
        if (element) {
            element.innerHTML = this.escapeHtml(html);
        }
    },
    
    /**
     * Cria elemento de forma segura
     */
    createElement: function(tag, text, className) {
        const element = document.createElement(tag);
        if (text) {
            element.textContent = text;
        }
        if (className) {
            element.className = className;
        }
        return element;
    },
    
    /**
     * Valida endereço de blockchain
     */
    validateAddress: function(address) {
        if (typeof address !== 'string') {
            return false;
        }
        const clean = address.trim().toLowerCase();
        return /^[0-9a-f]{40,42}$/.test(clean);
    },
    
    /**
     * Valida hash de transação
     */
    validateTxHash: function(hash) {
        if (typeof hash !== 'string') {
            return false;
        }
        const clean = hash.trim().toLowerCase();
        return /^[0-9a-f]{64}$/.test(clean);
    }
};

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.SecurityUtils = SecurityUtils;
}

