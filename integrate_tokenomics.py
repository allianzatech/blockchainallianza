#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 INTEGRAÇÃO DE TOKENOMICS COM BRIDGE
Integra sistema de Tokenomics com cross-chain bridge
"""

from tokenomics_system import TokenomicsSystem
from governance_system import GovernanceSystem

def integrate_tokenomics_with_bridge(bridge_instance, quantum_security=None):
    """
    Integrar Tokenomics e Governança com o bridge cross-chain
    
    Args:
        bridge_instance: Instância do RealCrossChainBridge
        quantum_security: Instância do QuantumSecuritySystem (opcional)
    """
    # Inicializar sistemas
    tokenomics = TokenomicsSystem()
    governance = GovernanceSystem(tokenomics, quantum_security=quantum_security)
    
    # Adicionar ao bridge
    bridge_instance.tokenomics = tokenomics
    bridge_instance.governance = governance
    
    print("✅ Tokenomics integrado com bridge!")
    print("✅ Governança integrada com bridge!")
    
    return tokenomics, governance

def apply_alz_discounts(bridge_instance, transaction_data: dict) -> dict:
    """
    Aplicar descontos ALZ em taxas de bridge
    
    Args:
        bridge_instance: Instância do bridge
        transaction_data: Dados da transação
        
    Returns:
        transaction_data com descontos aplicados
    """
    if not hasattr(bridge_instance, 'tokenomics'):
        return transaction_data
    
    # Obter balance ALZ do usuário (simulado - em produção buscar do blockchain)
    user_address = transaction_data.get('from_address', '')
    alz_balance = 0.0  # Em produção, buscar do blockchain
    
    # Calcular taxa base
    base_fee = transaction_data.get('bridge_fee', 0.001)  # 0.1% padrão
    
    # Aplicar desconto ALZ
    fee_calculation = bridge_instance.tokenomics.calculate_bridge_fee_with_alz(
        base_fee=base_fee,
        alz_balance=alz_balance
    )
    
    # Atualizar taxa na transação
    transaction_data['bridge_fee'] = fee_calculation['discounted_fee']
    transaction_data['bridge_fee_original'] = base_fee
    transaction_data['bridge_fee_discount'] = fee_calculation['discount_percent']
    transaction_data['bridge_fee_savings'] = fee_calculation['savings']
    
    return transaction_data

if __name__ == '__main__':
    print("="*70)
    print("🔗 INTEGRAÇÃO DE TOKENOMICS")
    print("="*70)
    
    # Exemplo de uso
    print("\n✅ Sistemas criados:")
    print("   • TokenomicsSystem")
    print("   • GovernanceSystem")
    print("\n✅ Pronto para integração com bridge!")



