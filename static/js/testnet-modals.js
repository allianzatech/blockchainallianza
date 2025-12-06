/**
 * 🎨 Sistema de Modais Moderno - Allianza Testnet
 * Funções compartilhadas para criar modais modernos e responsivos
 */

/**
 * Cria um modal moderno com resultado de teste
 * @param {string} title - Título do modal
 * @param {Object} data - Dados para exibir
 * @param {string} type - Tipo: 'success', 'warning', 'error'
 * @param {Object} options - Opções adicionais
 */
function createModernModal(title, data, type = 'success', options = {}) {
    // Remover modal existente se houver
    const existingModal = document.querySelector('.modern-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Determinar cores baseado no tipo
    const typeConfig = {
        success: {
            icon: 'check-circle',
            color: 'text-green-400',
            bgColor: 'bg-green-500/20',
            borderColor: 'border-green-500',
            badgeClass: 'status-success'
        },
        warning: {
            icon: 'exclamation-circle',
            color: 'text-yellow-400',
            bgColor: 'bg-yellow-500/20',
            borderColor: 'border-yellow-500',
            badgeClass: 'status-warning'
        },
        error: {
            icon: 'times-circle',
            color: 'text-red-400',
            bgColor: 'bg-red-500/20',
            borderColor: 'border-red-500',
            badgeClass: 'status-error'
        }
    };
    
    const config = typeConfig[type] || typeConfig.success;
    const jsonString = JSON.stringify(data, null, 2);
    const escapedJson = jsonString.replace(/`/g, '\\`').replace(/\$/g, '\\$');
    
    // Função helper para codificar Unicode em base64 de forma segura
    const safeBase64Encode = (str) => {
        try {
            // Converter para UTF-8 primeiro, depois para base64
            return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (match, p1) => {
                return String.fromCharCode(parseInt(p1, 16));
            }));
        } catch (e) {
            // Fallback: usar escape simples se falhar
            return btoa(unescape(encodeURIComponent(str)));
        }
    };
    
    // Armazenar JSON de forma segura usando data attribute
    const modalId = 'modal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    
    // Criar modal
    const modal = document.createElement('div');
    modal.className = 'modern-modal';
    modal.setAttribute('data-json', jsonString);
    modal.setAttribute('data-modal-id', modalId);
    modal.onclick = function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    };
    
    // Verificar se há verification_details
    const hasVerificationDetails = data.verification_details && typeof data.verification_details === 'object';
    const verificationDetailsHTML = hasVerificationDetails ? generateVerificationDetails(data.verification_details) : '';
    
    modal.innerHTML = `
        <div class="modern-modal-content border-2 ${config.borderColor}">
            <div class="modern-modal-header">
                <div class="flex-1">
                    <h2 class="text-2xl font-bold ${config.color} flex items-center gap-3 mb-3">
                        <i class="fas fa-${config.icon} text-3xl"></i>
                        <span>${title}</span>
                    </h2>
                    ${options.description ? `
                        <div class="${config.bgColor} border ${config.borderColor} rounded-lg p-3">
                            <p class="font-semibold ${config.color} mb-1">${options.statusTitle || title}</p>
                            <p class="text-sm text-gray-300">${options.description}</p>
                        </div>
                    ` : ''}
                </div>
                <button class="btn-close-modern" onclick="this.closest('.modern-modal').remove()" title="Fechar">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div class="modern-modal-body">
                ${verificationDetailsHTML}
                
                <div class="mt-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-sm font-semibold text-gray-400">Resposta JSON Completa</h3>
                        <button class="btn-copy-modern" onclick="copyJsonFromModal(this, '${modalId}')">
                            <i class="fas fa-copy"></i>
                            <span>Copiar JSON</span>
                        </button>
                    </div>
                    <div class="code-block-modern">
                        <pre><code>${escapedJson}</code></pre>
                    </div>
                </div>
            </div>
            
            <div class="modern-modal-footer">
                <button class="btn-copy-modern" onclick="copyJsonFromModal(this, '${modalId}')">
                    <i class="fas fa-copy"></i>
                    <span>Copiar JSON</span>
                </button>
                <button class="btn-copy-modern" style="background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);" onclick="this.closest('.modern-modal').remove()">
                    <i class="fas fa-times"></i>
                    <span>Fechar</span>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Fechar com ESC
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            modal.remove();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
    
    return modal;
}

/**
 * Gera HTML para detalhes de verificação
 */
function generateVerificationDetails(details) {
    if (!details || typeof details !== 'object') return '';
    
    const items = Object.entries(details).map(([key, value]) => {
        const isValid = value === true;
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        return `
            <div class="verification-item">
                <span class="verification-item-label">${label}:</span>
                <span class="verification-item-value ${isValid ? 'valid' : 'invalid'}">
                    ${isValid ? '✓ Válido' : '✗ Inválido'}
                </span>
            </div>
        `;
    }).join('');
    
    return `
        <div class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-4">
            <h3 class="font-bold text-yellow-400 mb-3 flex items-center gap-2">
                <i class="fas fa-clipboard-check"></i>
                Detalhes da Verificação
            </h3>
            <div class="verification-grid">
                ${items}
            </div>
        </div>
    `;
}

/**
 * Copia JSON do modal
 * @param {HTMLElement} button - Botão que foi clicado
 * @param {string} modalId - ID do modal ou base64 (para compatibilidade)
 */
function copyJsonFromModal(button, modalId) {
    try {
        let jsonString = '';
        
        // Tentar encontrar o modal pelo ID
        const modal = document.querySelector(`[data-modal-id="${modalId}"]`);
        if (modal && modal.getAttribute('data-json')) {
            // Usar data attribute (método seguro para Unicode)
            jsonString = modal.getAttribute('data-json');
        } else {
            // Fallback: tentar decodificar como base64 (compatibilidade)
            try {
                jsonString = atob(modalId);
            } catch (e) {
                // Se falhar, tentar encontrar o modal mais próximo
                const closestModal = button.closest('.modern-modal');
                if (closestModal && closestModal.getAttribute('data-json')) {
                    jsonString = closestModal.getAttribute('data-json');
                } else {
                    throw new Error('Não foi possível encontrar o JSON para copiar');
                }
            }
        }
        
        navigator.clipboard.writeText(jsonString).then(() => {
            const originalHTML = button.innerHTML;
            button.classList.add('copied');
            button.innerHTML = '<i class="fas fa-check"></i><span>Copiado!</span>';
            
            setTimeout(() => {
                button.classList.remove('copied');
                button.innerHTML = originalHTML;
            }, 2000);
        }).catch(err => {
            console.error('Erro ao copiar:', err);
            alert('❌ Erro ao copiar. Tente selecionar e copiar manualmente.');
        });
    } catch (err) {
        console.error('Erro ao processar JSON:', err);
        alert('❌ Erro ao processar JSON: ' + err.message);
    }
}

/**
 * Determina o tipo de resultado baseado nos dados
 */
function determineResultType(data) {
    if (data.success === false || data.error) {
        return 'error';
    } else if (data.success === true && data.valid === false) {
        return 'warning';
    } else if (data.success === true && (data.valid === true || data.valid === undefined)) {
        return 'success';
    }
    return 'success';
}

/**
 * Cria descrição baseada no tipo de resultado
 */
function createResultDescription(data, type) {
    if (type === 'error') {
        return {
            statusTitle: 'Erro do Sistema',
            description: data.error || 'Erro desconhecido ao processar a requisição'
        };
    } else if (type === 'warning') {
        const failedChecks = [];
        if (data.verification_details) {
            if (data.verification_details.signature_valid === false) failedChecks.push('Assinatura inválida');
            if (data.verification_details.merkle_proof_valid === false) failedChecks.push('Merkle proof inválido');
            if (data.verification_details.proof_hash_valid === false) failedChecks.push('Hash da prova inválido');
            if (data.verification_details.timestamp_valid === false) failedChecks.push('Timestamp inválido');
        }
        
        return {
            statusTitle: 'Validação Falhada',
            description: failedChecks.length > 0 
                ? `Prova inválida: ${failedChecks.join(', ')}`
                : 'A requisição foi processada, mas a prova é inválida'
        };
    } else {
        return {
            statusTitle: 'Sucesso',
            description: 'Requisição processada com sucesso'
        };
    }
}

// Exportar para uso global
window.createModernModal = createModernModal;
window.copyJsonFromModal = copyJsonFromModal;
window.determineResultType = determineResultType;
window.createResultDescription = createResultDescription;

