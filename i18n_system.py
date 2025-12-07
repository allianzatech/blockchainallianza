#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Sistema de Internacionalização (i18n) - Allianza Blockchain
Detecção automática de idioma por IP/país
"""

import json
import requests
from typing import Dict, Optional
from flask import request, g, session, jsonify, redirect
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
        # Network Info
        'network_id': 'Network ID',
        'chain_id': 'Chain ID',
        'version': 'Versão',
        # Developer Hub & Leaderboard
        'quick_start_guide': 'Quick Start Guide',
        'start_integrating': 'Comece a integrar em minutos',
        'ranking': 'Ranking',
        'developers': 'desenvolvedores',
        # Recent Activity
        'view_all': 'Ver todas',
        'ran_test': 'executou um teste',
        'generated_proof': 'gerou uma prova quântica',
        'made_qss_request': 'fez uma requisição QSS',
        'points': 'pontos',
        # Professional Features buttons
        'status': 'Status',
        'monitoring': 'Monitoramento',
        'qrs3_dashboard': 'Dashboard',
        'interop': 'Interop',
        'cross_chain': 'Cross-chain',
        '5_layers': '5 Camadas',
        'tests': 'Testes',
        'public': 'Públicos',
        'professional': 'Profissionais',
        'complete_suite_short': 'Suite completa',
        '41_validations': '41 Validações',
        'complete': 'Completas',
        # Network Status
        'network_status_title': 'Status da Rede',
        # Tests Complete
        'complete_tests_title': 'Testes Completos - 41 Validações',
        'complete_tests_subtitle': 'Execute todos os testes documentados e verifique os resultados',
        'back': 'Voltar',
        'complete_validation_suite': 'Complete Validation Suite',
        '8_validation_tests': '8 testes de validação completa',
        'execute_tests': 'Executar Testes',
        'critical_tests_suite': 'Critical Tests Suite',
        '6_critical_tests': '6 testes críticos',
        'professional_suite': 'Professional Suite',
        '14_professional_tests': '14 testes profissionais',
        'execute_all_41_tests': 'Executar Todos os 41 Testes',
        'execute_all_description': 'Execute todas as suites de uma vez (pode levar vários minutos)',
        'execute_all_button': 'Executar Todos',
        'results': 'Resultados',
        'executing_tests': 'Executando testes...',
        # Professional Tests
        'professional_tests_title': 'Testes Profissionais',
        'professional_tests_subtitle': 'Suite completa de testes obrigatórios para testnet profissional',
        'loading_tests': 'Carregando testes...',
        'quantum_layer_tests': 'Testes de Camada Quântica (PQC / QRS-3)',
        'pqc_key_generation': 'Geração de Chaves PQC (PQC Key Generation)',
        'qrs3_signature': 'Assinatura QRS-3 (QRS-3 Signature)',
        'pqc_audit': 'Auditoria PQC (PQC Audit)',
        'interoperability_tests': 'Testes de Interoperabilidade',
        'proof_of_lock': 'Proof-of-Lock',
        'gasless_interoperability': 'Gasless Interoperability',
        'bitcoin_to_evm': 'Bitcoin → EVM',
        'execute': 'Executar',
        'execute_all_tests': 'Executar Todos os Testes',
        'professional_tests_available': 'Testes Profissionais disponíveis',
        # Blockchain Core Tests
        'blockchain_core_tests': 'Testes de Blockchain Core',
        'consensus': 'Consenso',
        'node_synchronization': 'Sincronização de Nós',
        # Optional Tests
        'optional_tests': 'Testes Opcionais',
        'homomorphic_cryptography': 'Criptografia Homomórfica',
        'quantum_secure_identity': 'Identidade Quântico-Segura',
        'exploit_prevention': 'Prevenção de exploits',
        'real_conversion': 'Conversão real',
        # Results
        'complete_results': 'Resultados Completos',
        'copy': 'Copiar',
        'download': 'Baixar',
        # Public Tests
        'public_tests': 'Testes Públicos',
        'public_tests_subtitle': 'Execute testes reais e veja os resultados em tempo real',
        'execute_5_main_tests': 'Execute os 5 testes principais e veja os resultados detalhados',
        'block_validation': 'Validação de Blocos',
        'quantum_security': 'Segurança Quântica',
        'real_time_logs': 'Logs em Tempo Real',
        'waiting_test_execution': 'Aguardando execução de testes...',
        # ALZ-NIEV
        'alz_niev_subtitle': 'Non-Intermediate Execution Validation - Interoperabilidade Única no Mundo',
        'checking_status': 'Verificando status...',
        'the_5_layers': 'As 5 Camadas do ALZ-NIEV',
        'native_execution_no_bridges': 'Execução nativa sem bridges',
        'zk_proofs_no_relayers': 'Provas ZK sem relayers',
        'universal_merkle_proofs': 'Provas Merkle universais',
        'support_any_consensus': 'Suporte a qualquer consenso',
        'atomic_multi_chain_execution': 'Execução atômica multi-chain',
        'test_1_cross_chain': 'Teste 1: Execução Cross-Chain (ELNI + Todas as Provas)',
        'execute_with_alz_niev': 'Executar com ALZ-NIEV',
        'test_2_atomic': 'Teste 2: Execução Atômica Multi-Chain (AES)',
        'execute_atomically': 'Executar Atomicamente',
        'need_test_tokens': 'Precisa de Tokens de Teste?',
        'use_faucet_description': 'Para executar funções que requerem saldo, use o faucet:',
        'access_faucet': 'Acessar Faucet',
        # Interoperability
        'real_cross_chain_transfer': 'Transferência Real Cross-Chain',
        'send_real_tokens': 'Envie tokens REAIS entre blockchains diferentes',
        'transfers_appear_explorers': 'As transferências aparecem nos explorers e são 100% reais!',
        'checking_status': 'Verificando status...',
        'fill_transfer_data': 'Preencha os Dados da Transferência',
        'simple_instructions': 'Simples: escolha origem, destino, quantidade e endereço. É só isso!',
        'origin_blockchain': 'Blockchain de Origem',
        'destination_blockchain': 'Blockchain de Destino',
        'quantity': 'Quantidade',
        'token': 'Token',
        'recipient_address': 'Endereço Destinatário',
        'how_it_works': 'Como funciona:',
        'choose_origin': 'Escolha a blockchain de origem (ex: Polygon)',
        'choose_destination': 'Escolha a blockchain de destino (ex: Bitcoin)',
        'enter_amount_token': 'Digite a quantidade e o token',
        'paste_recipient': 'Cole o endereço do destinatário',
        'click_execute': 'Clique em "Executar Transferência REAL"',
        'transfer_will_appear': 'A transferência aparecerá nos explorers!',
        'important': 'Importante:',
        'real_transfer_warning': 'Esta é uma transferência REAL que aparecerá nos explorers',
        'need_sufficient_balance': 'Você precisa ter saldo suficiente na blockchain de origem',
        'no_balance_use_faucet': 'Não tem saldo? Use o Faucet para obter tokens de teste',
        'execute_real_transfer': 'Executar Transferência REAL',
        'alz_niev_technology': 'Tecnologia ALZ-NIEV',
        'interoperability_available': 'Sistema de interoperabilidade disponível e pronto para transferências REAIS!',
        # Quantum Security Dashboard
        'quantum_security_dashboard': 'Dashboard de Segurança Quântica',
        'qrs3_metrics_subtitle': 'Métricas QRS-3, Entropia Quântica e Performance PQC',
        'qrs3_status': 'Status QRS-3',
        'redundancy_level': 'Nível de Redundância',
        'usage_rate': 'Taxa de Uso',
        'qrs3_transactions': 'Transações QRS-3',
        'active_algorithms': 'Algoritmos Ativos:',
        'quantum_entropy': 'Entropia Quântica',
        'total_generated': 'Total Gerado',
        'generation_rate': 'Taxa de Geração',
        'source': 'Fonte',
        'quantum_secure': 'Quântico-Seguro',
        # Status Page
        'status_page': 'Status Page',
        'real_time_monitoring': 'Monitoramento em tempo real da Allianza Testnet',
        'general_status': 'Status Geral',
        'uptime': 'Uptime',
        'average_latency': 'Latência Média',
        'validators_online': 'Validadores Online',
        'components': 'Componentes',
        'response_time': 'Tempo de resposta',
        'online': 'Online',
        'blocks': 'Blocos',
        'shards': 'Shards',
        'realtime_metrics': 'Métricas em Tempo Real',
        'current_tps': 'TPS Atual',
        'tps_24h_avg_label': 'TPS 24h (Média)',
        'blocks_last_hour': 'Blocos (Última Hora)',
        'last_update': 'Última Atualização',
        'incident_history': 'Histórico de Incidentes',
        'no_incidents': 'Nenhum incidente registrado. Rede operacional! ✅',
        # QSS Dashboard
        'qss_subtitle': 'Segurança quântica para Bitcoin, Ethereum e outras blockchains',
        'service_status': 'Status do Serviço',
        'checking': 'Verificando...',
        'loading_service_info': 'Carregando informações do serviço...',
        'available': 'Disponível',
        'supported_chains': 'Chains Suportadas',
        'pqc_algorithms': 'Algoritmos PQC',
        'quantum_security_test_bitcoin': 'Teste de Segurança Quântica - Bitcoin',
        'generate_quantum_proof_bitcoin': 'Gere uma prova quântica para uma transação Bitcoin e ancore no OP_RETURN',
        'bitcoin_tx_hash': 'TX Hash Bitcoin',
        'use_real_hash_blockstream': 'Use um hash real do Blockstream Explorer',
        'quantum_security_test_ethereum': 'Teste de Segurança Quântica - Ethereum',
        'generate_quantum_proof_ethereum': 'Gere uma prova quântica para uma transação Ethereum e ancore via Smart Contract',
        'ethereum_tx_hash': 'TX Hash Ethereum',
        'use_real_hash_polygon': 'Use um hash real do Polygon Explorer ou Ethereum Sepolia',
        'generate_proof': 'Gerar Prova',
        'verify_proof': 'Verificar Prova',
        'anchor_proof': 'Ancorar Prova',
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
        # Network Info
        'network_id': 'Network ID',
        'chain_id': 'Chain ID',
        'version': 'Version',
        # Developer Hub & Leaderboard
        'quick_start_guide': 'Quick Start Guide',
        'start_integrating': 'Start integrating in minutes',
        'ranking': 'Ranking',
        'developers': 'developers',
        # Recent Activity
        'view_all': 'View all',
        'ran_test': 'ran a test',
        'generated_proof': 'generated a quantum proof',
        'made_qss_request': 'made a QSS request',
        'points': 'points',
        # Professional Features buttons
        'status': 'Status',
        'monitoring': 'Monitoring',
        'qrs3_dashboard': 'Dashboard',
        'interop': 'Interop',
        'cross_chain': 'Cross-chain',
        '5_layers': '5 Layers',
        'tests': 'Tests',
        'public': 'Public',
        'professional': 'Professional',
        'complete_suite_short': 'Complete suite',
        '41_validations': '41 Validations',
        'complete': 'Complete',
        # Network Status
        'network_status_title': 'Network Status',
        # Tests Complete
        'complete_tests_title': 'Complete Tests - 41 Validations',
        'complete_tests_subtitle': 'Execute all documented tests and verify results',
        'back': 'Back',
        'complete_validation_suite': 'Complete Validation Suite',
        '8_validation_tests': '8 complete validation tests',
        'execute_tests': 'Execute Tests',
        'critical_tests_suite': 'Critical Tests Suite',
        '6_critical_tests': '6 critical tests',
        'professional_suite': 'Professional Suite',
        '14_professional_tests': '14 professional tests',
        'execute_all_41_tests': 'Execute All 41 Tests',
        'execute_all_description': 'Execute all suites at once (may take several minutes)',
        'execute_all_button': 'Execute All',
        'results': 'Results',
        'executing_tests': 'Executing tests...',
        # Professional Tests
        'professional_tests_title': 'Professional Tests',
        'professional_tests_subtitle': 'Complete suite of mandatory tests for professional testnet',
        'loading_tests': 'Loading tests...',
        'quantum_layer_tests': 'Quantum Layer Tests (PQC / QRS-3)',
        'pqc_key_generation': 'PQC Key Generation',
        'qrs3_signature': 'QRS-3 Signature',
        'pqc_audit': 'PQC Audit',
        'interoperability_tests': 'Interoperability Tests',
        'proof_of_lock': 'Proof-of-Lock',
        'gasless_interoperability': 'Gasless Interoperability',
        'bitcoin_to_evm': 'Bitcoin → EVM',
        'execute': 'Execute',
        'execute_all_tests': 'Execute All Tests',
        'professional_tests_available': 'Professional Tests available',
        # Blockchain Core Tests
        'blockchain_core_tests': 'Blockchain Core Tests',
        'consensus': 'Consensus',
        'node_synchronization': 'Node Synchronization',
        # Optional Tests
        'optional_tests': 'Optional Tests',
        'homomorphic_cryptography': 'Homomorphic Cryptography',
        'quantum_secure_identity': 'Quantum-Secure Identity',
        'exploit_prevention': 'Exploit Prevention',
        'real_conversion': 'Real conversion',
        # Results
        'complete_results': 'Complete Results',
        'copy': 'Copy',
        'download': 'Download',
        # Public Tests
        'public_tests': 'Public Tests',
        'public_tests_subtitle': 'Execute real tests and see results in real time',
        'execute_5_main_tests': 'Execute the 5 main tests and see detailed results',
        'block_validation': 'Block Validation',
        'quantum_security': 'Quantum Security',
        'real_time_logs': 'Real-Time Logs',
        'waiting_test_execution': 'Waiting for test execution...',
        # ALZ-NIEV
        'alz_niev_subtitle': 'Non-Intermediate Execution Validation - Unique Interoperability in the World',
        'checking_status': 'Checking status...',
        'the_5_layers': 'The 5 Layers of ALZ-NIEV',
        'native_execution_no_bridges': 'Native execution without bridges',
        'zk_proofs_no_relayers': 'ZK proofs without relayers',
        'universal_merkle_proofs': 'Universal Merkle proofs',
        'support_any_consensus': 'Support for any consensus',
        'atomic_multi_chain_execution': 'Atomic multi-chain execution',
        'test_1_cross_chain': 'Test 1: Cross-Chain Execution (ELNI + All Proofs)',
        'execute_with_alz_niev': 'Execute with ALZ-NIEV',
        'test_2_atomic': 'Test 2: Atomic Multi-Chain Execution (AES)',
        'execute_atomically': 'Execute Atomically',
        'need_test_tokens': 'Need Test Tokens?',
        'use_faucet_description': 'To execute functions that require balance, use the faucet:',
        'access_faucet': 'Access Faucet',
        # Interoperability
        'real_cross_chain_transfer': 'Real Cross-Chain Transfer',
        'send_real_tokens': 'Send REAL tokens between different blockchains',
        'transfers_appear_explorers': 'Transfers appear on explorers and are 100% real!',
        'fill_transfer_data': 'Fill in the Transfer Data',
        'simple_instructions': 'Simple: choose origin, destination, quantity, and address. That\'s it!',
        'origin_blockchain': 'Origin Blockchain',
        'destination_blockchain': 'Destination Blockchain',
        'quantity': 'Quantity',
        'token': 'Token',
        'recipient_address': 'Recipient Address',
        'how_it_works': 'How it works:',
        'choose_origin': 'Choose the origin blockchain (e.g., Polygon)',
        'choose_destination': 'Choose the destination blockchain (e.g., Bitcoin)',
        'enter_amount_token': 'Enter the quantity and token',
        'paste_recipient': 'Paste the recipient address',
        'click_execute': 'Click "Execute REAL Transfer"',
        'transfer_will_appear': 'The transfer will appear on explorers!',
        'important': 'Important:',
        'real_transfer_warning': 'This is a REAL transfer that will appear on explorers',
        'need_sufficient_balance': 'You need sufficient balance on the origin blockchain',
        'no_balance_use_faucet': 'No balance? Use the Faucet to get test tokens',
        'execute_real_transfer': 'Execute REAL Transfer',
        'alz_niev_technology': 'ALZ-NIEV Technology',
        'interoperability_available': 'Interoperability system available and ready for REAL transfers!',
        # Quantum Security Dashboard
        'quantum_security_dashboard': 'Quantum Security Dashboard',
        'qrs3_metrics_subtitle': 'QRS-3 Metrics, Quantum Entropy and PQC Performance',
        'qrs3_status': 'QRS-3 Status',
        'redundancy_level': 'Redundancy Level',
        'usage_rate': 'Usage Rate',
        'qrs3_transactions': 'QRS-3 Transactions',
        'active_algorithms': 'Active Algorithms:',
        'quantum_entropy': 'Quantum Entropy',
        'total_generated': 'Total Generated',
        'generation_rate': 'Generation Rate',
        'source': 'Source',
        'quantum_secure': 'Quantum-Secure',
        # Status Page
        'status_page': 'Status Page',
        'real_time_monitoring': 'Real-time monitoring of Allianza Testnet',
        'general_status': 'General Status',
        'uptime': 'Uptime',
        'average_latency': 'Average Latency',
        'validators_online': 'Validators Online',
        'components': 'Components',
        'response_time': 'Response time',
        'online': 'Online',
        'blocks': 'Blocks',
        'shards': 'Shards',
        'realtime_metrics': 'Real-Time Metrics',
        'current_tps': 'Current TPS',
        'tps_24h_avg_label': 'TPS 24h (Average)',
        'blocks_last_hour': 'Blocks (Last Hour)',
        'last_update': 'Last Update',
        'incident_history': 'Incident History',
        'no_incidents': 'No incidents recorded. Network operational! ✅',
        # QSS Dashboard
        'qss_subtitle': 'Quantum security for Bitcoin, Ethereum and other blockchains',
        'service_status': 'Service Status',
        'checking': 'Checking...',
        'loading_service_info': 'Loading service information...',
        'available': 'Available',
        'supported_chains': 'Supported Chains',
        'pqc_algorithms': 'PQC Algorithms',
        'quantum_security_test_bitcoin': 'Quantum Security Test - Bitcoin',
        'generate_quantum_proof_bitcoin': 'Generate a quantum proof for a Bitcoin transaction and anchor it in OP_RETURN',
        'bitcoin_tx_hash': 'Bitcoin TX Hash',
        'use_real_hash_blockstream': 'Use a real hash from Blockstream Explorer',
        'quantum_security_test_ethereum': 'Quantum Security Test - Ethereum',
        'generate_quantum_proof_ethereum': 'Generate a quantum proof for an Ethereum transaction and anchor via Smart Contract',
        'ethereum_tx_hash': 'Ethereum TX Hash',
        'use_real_hash_polygon': 'Use a real hash from Polygon Explorer or Ethereum Sepolia',
        'generate_proof': 'Generate Proof',
        'verify_proof': 'Verify Proof',
        'anchor_proof': 'Anchor Proof',
        'alz_niev_behind_interface': 'Behind this simple interface is the ALZ-NIEV system with 5 layers of security and cryptographic proofs. You don\'t need to understand this - just make your transfer and everything works automatically!',
        'view_technical_details': 'View technical details (optional)',
        'real_transfer_executed': 'Real Transfer Executed',
        'error_executing': 'Error Executing',
        'transfer_success_explorers': 'Transfer executed successfully and will appear on explorers!',
        'transfer_error': 'Transfer Error',
        'error_executing_transfer': 'Error executing transfer',
        'system_limited_mode': 'System in limited mode:',
        'not_available': 'Not available',
        # QSS Dashboard
        'quantum_security_service': 'Quantum Security Service (QSS)',
        'quantum_proof_generated': 'Quantum Proof Generated',
        'anchor_instructions': 'Anchor Instructions',
        # QRS-3 Verifier
        'qrs3_verifier': 'QRS-3 Verifier',
        'verify_qrs3_signatures': 'Verify QRS-3 quantum signatures (ECDSA + ML-DSA + SPHINCS+)',
        'generate_example': 'Generate Example',
        'dont_know_how_to_test': 'Don\'t know how to test? Generate an example QRS-3 message and signature that you can verify.',
        'example_message_optional': 'Example Message (optional)',
        'generate_example_qrs3_signature': 'Generate Example QRS-3 Signature',
        'verify_qrs3_signature': 'Verify QRS-3 Signature',
        'message': 'Message',
        'enter_original_message': 'Enter the original message...',
        'qrs3_signature_json': 'QRS-3 Signature (JSON)',
        'verify_signature': 'Verify Signature',
        'generating': 'Generating...',
        'generating_qrs3_signature': 'Generating QRS-3 signature...',
        'fields_auto_filled': 'Fields were automatically filled. Click "Verify Signature" to test!',
        'valid_signature': 'Valid signature',
        'invalid_signature': 'Invalid signature',
        'signature_verified': 'Signature verified successfully',
        'signature_verification_failed': 'Signature verification failed. Please check if the message and signature are correct.',
        'qrs3_verification': 'QRS-3 Verification',
        'example_generated_success': 'Example Generated Successfully!',
        'verification_status': 'Verification Status',
        'instructions': 'Instructions:',
        'verifying': 'Verifying...',
        'error': 'Error',
        # Explorer
        'explorer': 'Explorer',
        'explore_blocks_transactions': 'Explore blocks, transactions and network statistics',
        'total_blocks': 'Total Blocks',
        'total_transactions': 'Total Transactions',
        'recent_blocks': 'Recent Blocks',
        'recent_transactions': 'Recent Transactions',
        # Faucet
        'faucet': 'Faucet',
        'get_test_tokens': 'Get test tokens to try out the Allianza Testnet',
        'no_address_generate': 'Don\'t have an address? Generate one now!',
        'generate_wallet_description': 'Click the button below to generate a new wallet and get your Allianza address.',
        'generate_new_wallet': 'Generate New Wallet',
        'request_tokens': 'Request Tokens',
        'allianza_address': 'Allianza Address',
        'must_start_alz1': 'Must start with ALZ1 and have 42 characters',
        'total_sent': 'Total Sent',
        'total_rejected': 'Total Rejected',
        'amount_per_request': 'Amount per Request',
        'recent_logs': 'Recent Logs',
        # Developer Hub
        'developer_hub': 'Developer Hub',
        'start_integrating_quantum': 'Start integrating quantum security in minutes',
        'sdk_available': 'SDK v1.0.0 Available',
        'view_on_npm': 'View on npm',
        'updated': 'Updated',
        'try_it_now': 'Try It Now',
        'changelog': 'Changelog',
        'quick_start_guide': 'Quick Start Guide',
        'install_sdk': 'Install the SDK',
        'npm_installation': 'Installation via npm:',
        'alternative_rest_api': 'Alternative: Direct REST API',
        # Leaderboard
        'leaderboard': 'Leaderboard',
        'developer_ranking': 'Ranking of developers and contributions',
        'total_users': 'Total Users',
        'total_points': 'Total Points',
        'tests_executed': 'Tests Executed',
        'proofs_generated': 'Proofs Generated',
        'top_developers': 'Top Developers',
        'no_developers_yet': 'No developer yet. Be the first!',
        'recent_activities': 'Recent Activities',
        # Quantum Attack Simulator
        'quantum_attack_simulator': 'Quantum Attack Simulator',
        'see_visually_how_attack_works': 'See visually how a quantum attack works and why Allianza is protected',
        'run_quantum_test': 'Run Quantum Test',
        # Developer Hub - API Examples
        'rest_api_examples': 'REST API Examples',
        'generate_quantum_proof': 'Generate Quantum Proof',
        'verify_the_proof': 'Verify the Proof',
        'generate_proof_api': 'Generate Proof',
        'verify_proof_api': 'Verify Proof',
        'anchor_proof_api': 'Anchor Proof',
        'service_status_api': 'Service Status',
        'alternative_rest_api': 'Alternative: Direct REST API',
        'javascript_example_rest': 'JavaScript Example (REST API)',
        'generate_proof_for_any_blockchain': 'Generate proof for any blockchain',
        'rest_api_complete_documented': 'Complete and documented REST API',
        # QSS Dashboard JavaScript
        'no_proof_to_verify': 'No proof to verify',
        'qss_proof_verification': 'QSS Proof Verification',
        'error_verifying': 'Error Verifying',
        'generating_quantum_proof': 'Generating quantum proof...',
        'proof_generated_success': 'Proof generated successfully!',
        'error_unknown': 'Unknown error',
        'service_not_available': 'Service not available',
        'please_enter_bitcoin_tx_hash': 'Please enter a Bitcoin TX Hash',
        'please_enter_ethereum_tx_hash': 'Please enter an Ethereum TX Hash',
        'method': 'Method',
        'data': 'Data',
        'proof_hash_label': 'Proof Hash',
        'anchor_on_blockchain': 'Anchor on Blockchain',
        'bitcoin_opreturn': 'Bitcoin (OP_RETURN)',
        'ethereum_polygon_smart_contract': 'Ethereum/Polygon (Smart Contract)',
        'works_with_blockchains': 'Works with Bitcoin, Ethereum, Polygon, BSC, Solana, Avalanche, Base and any blockchain!',
        'proof_valid': 'Proof valid!',
        'ml_dsa_signature': 'ML-DSA Signature',
        'merkle_proof': 'Merkle Proof',
        'use_instructions_data': 'Use instructions.data in OP_RETURN',
        'send_transaction': 'Send the transaction with transactionData',
        'support_bitcoin_ethereum': 'Support for Bitcoin, Ethereum, Polygon, BSC, Solana, Avalanche, Base',
        'quantum_proof_generation_verification': 'Quantum proof generation and verification (ML-DSA)',
        'anchoring_bitcoin_evm': 'Anchoring on Bitcoin (OP_RETURN) and EVM (Smart Contracts)',
        'typescript_definitions': 'TypeScript definitions included',
        'qss_api_status': 'QSS API Status',
        'loading': 'Loading...',
        'loading_information': 'Loading information...',
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
        from flask import redirect, url_for
        if language in ['en', 'pt']:
            session['language'] = language
            # Redirecionar de volta para a página anterior ou dashboard
            referer = request.headers.get('Referer', '/')
            # Se for requisição AJAX, retornar JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': True, 'language': language})
            # Caso contrário, redirecionar
            return redirect(referer if referer else '/')
        # Se idioma inválido, redirecionar de volta
        referer = request.headers.get('Referer', '/')
        return redirect(referer if referer else '/')
    
    logger.info("🌍 Sistema de i18n configurado!")
    print("🌍 Sistema de i18n configurado!")
    print("   • Detecção automática por IP/país")
    print("   • Suporte: Português (pt) e Inglês (en)")
    print("   • Rota: /set-language/<lang> para mudança manual")

