#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Sistema de Internacionalização (i18n) - Allianza Blockchain
Detecção automática de idioma por IP/país
"""

import json
import requests
from typing import Dict, Optional
from flask import request, g, session
import logging

logger = logging.getLogger(__name__)

# Dicionários de tradução
TRANSLATIONS = {
    'pt': {
        # Dashboard
        'dashboard_title': 'Allianza Testnet',
        'dashboard_subtitle': 'Primeira testnet do mundo com proteção quântica nativa',
        'total_blocks': 'Total de Blocos',
        'total_transactions': 'Total de Transações',
        'tps_24h': 'TPS (24h)',
        'avg_latency': 'Latência Média',
        'network_status': 'Status da Rede',
        'developer_hub': 'Developer Hub',
        'leaderboard': 'Leaderboard',
        'faucet': 'Faucet',
        'explorer': 'Explorer',
        'qrs3_verifier': 'Verificador QRS-3',
        'quantum_attack_simulator': 'Simulador de Ataque Quântico',
        'quantum_security_service': 'Quantum Security Service',
        'professional_features': 'Funcionalidades Profissionais',
        'status_page': 'Status Page',
        'quantum_security': 'Segurança Quântica',
        'interoperability': 'Interoperabilidade',
        'alz_niev': 'ALZ-NIEV',
        'public_tests': 'Testes Públicos',
        'professional_tests': 'Testes Profissionais',
        'complete_validations': '41 Validações Completas',
        'recent_activity': 'Atividade Recente',
        'obtain_tokens': 'Obter tokens de teste',
        'explore_blocks': 'Explorar blocos e transações',
        'verify_signatures': 'Verificar assinaturas quânticas',
        'test_security': 'Testar segurança quântica',
        'quantum_security_other': 'Segurança quântica para outras blockchains',
        'monitoring': 'Monitoramento em tempo real',
        'dashboard_qrs3': 'Dashboard QRS-3 e PQC',
        'test_crosschain': 'Teste cross-chain real',
        'unique_interop': 'Interoperabilidade Única',
        'execute_tests': 'Execute testes reais',
        'complete_suite': 'Suite completa de testes',
        'execute_all': 'Execute todos os testes documentados',
    },
    'en': {
        # Dashboard
        'dashboard_title': 'Allianza Testnet',
        'dashboard_subtitle': 'World\'s first testnet with native quantum protection',
        'total_blocks': 'Total Blocks',
        'total_transactions': 'Total Transactions',
        'tps_24h': 'TPS (24h)',
        'avg_latency': 'Average Latency',
        'network_status': 'Network Status',
        'developer_hub': 'Developer Hub',
        'leaderboard': 'Leaderboard',
        'faucet': 'Faucet',
        'explorer': 'Explorer',
        'qrs3_verifier': 'QRS-3 Verifier',
        'quantum_attack_simulator': 'Quantum Attack Simulator',
        'quantum_security_service': 'Quantum Security Service',
        'professional_features': 'Professional Features',
        'status_page': 'Status Page',
        'quantum_security': 'Quantum Security',
        'interoperability': 'Interoperability',
        'alz_niev': 'ALZ-NIEV',
        'public_tests': 'Public Tests',
        'professional_tests': 'Professional Tests',
        'complete_validations': '41 Complete Validations',
        'recent_activity': 'Recent Activity',
        'obtain_tokens': 'Obtain test tokens',
        'explore_blocks': 'Explore blocks and transactions',
        'verify_signatures': 'Verify quantum signatures',
        'test_security': 'Test quantum security',
        'quantum_security_other': 'Quantum security for other blockchains',
        'monitoring': 'Real-time monitoring',
        'dashboard_qrs3': 'QRS-3 and PQC Dashboard',
        'test_crosschain': 'Real cross-chain test',
        'unique_interop': 'Unique Interoperability',
        'execute_tests': 'Execute real tests',
        'complete_suite': 'Complete test suite',
        'execute_all': 'Execute all documented tests',
    }
}

# Mapeamento de países para idiomas
COUNTRY_LANGUAGE_MAP = {
    'US': 'en', 'GB': 'en', 'CA': 'en', 'AU': 'en', 'NZ': 'en', 'IE': 'en',
    'BR': 'pt', 'PT': 'pt', 'AO': 'pt', 'MZ': 'pt',
    # Adicionar mais países conforme necessário
}

def detect_language_by_ip(ip_address: str) -> str:
    """
    Detecta idioma baseado no IP usando serviço de geolocalização
    Retorna 'en' ou 'pt' baseado no país
    """
    try:
        # Usar serviço gratuito de geolocalização
        # ipapi.co é gratuito e não requer API key
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=2)
        if response.status_code == 200:
            data = response.json()
            country_code = data.get('country_code', '').upper()
            
            # Mapear país para idioma
            language = COUNTRY_LANGUAGE_MAP.get(country_code, 'en')
            logger.debug(f"🌍 Idioma detectado: {language} (país: {country_code}, IP: {ip_address})")
            return language
    except Exception as e:
        logger.debug(f"⚠️  Erro ao detectar idioma por IP: {e}")
    
    # Fallback: verificar Accept-Language header
    try:
        accept_language = request.headers.get('Accept-Language', '')
        if 'pt' in accept_language.lower():
            return 'pt'
    except:
        pass
    
    # Default: inglês
    return 'en'

def get_language() -> str:
    """
    Obtém idioma atual (da sessão, IP ou padrão)
    """
    # 1. Verificar se há idioma na sessão (usuário escolheu manualmente)
    if session.get('language'):
        return session['language']
    
    # 2. Verificar se já foi detectado nesta requisição
    if hasattr(g, 'language'):
        return g.language
    
    # 3. Detectar por IP
    try:
        ip = request.remote_addr or request.environ.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
        if ip:
            language = detect_language_by_ip(ip)
            g.language = language
            return language
    except:
        pass
    
    # 4. Default: inglês
    g.language = 'en'
    return 'en'

def t(key: str, default: Optional[str] = None) -> str:
    """
    Função de tradução
    Uso: t('dashboard_title') -> 'Allianza Testnet' ou 'Allianza Testnet'
    """
    language = get_language()
    translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
    return translations.get(key, default or key)

def setup_i18n(app):
    """
    Configura sistema de i18n no Flask app
    """
    @app.before_request
    def detect_language():
        """Detecta idioma antes de cada requisição"""
        language = get_language()
        g.language = language
        g.translate = lambda key, default=None: t(key, default)
    
    @app.context_processor
    def inject_translations():
        """Injeta função de tradução nos templates"""
        return {
            't': t,
            'current_language': get_language(),
            'lang': get_language()
        }
    
    # Rota para mudar idioma manualmente
    @app.route('/set-language/<language>', methods=['POST', 'GET'])
    def set_language(language):
        """Permite usuário escolher idioma manualmente"""
        if language in ['en', 'pt']:
            session['language'] = language
            return jsonify({'success': True, 'language': language})
        return jsonify({'success': False, 'error': 'Invalid language'}), 400
    
    logger.info("🌍 Sistema de i18n configurado!")
    print("🌍 Sistema de i18n configurado!")
    print("   • Detecção automática por IP/país")
    print("   • Suporte: Português (pt) e Inglês (en)")
    print("   • Rota: /set-language/<lang> para mudança manual")

