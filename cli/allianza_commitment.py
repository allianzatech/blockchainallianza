#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Amigável para Sistema de Commitment
Interface de linha de comando para gerenciar commitments
"""

import sys
import argparse
from pathlib import Path

# Adicionar ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from commercial_repo.adapters.commitment_integration import CommitmentManager
from commercial_repo.adapters.commitment_database import CommitmentDatabase
from commercial_repo.adapters.commitment_monitor import CommitmentMonitor
from commercial_repo.adapters.commitment_retry_manager import CommitmentRetryManager
import os
from dotenv import load_dotenv

load_dotenv()


def print_success(msg):
    print(f"✅ {msg}")


def print_error(msg):
    print(f"❌ {msg}")


def print_info(msg):
    print(f"ℹ️  {msg}")


def cmd_create(args):
    """Cria um novo commitment"""
    print_info(f"Criando commitment: {args.source_chain} → {args.target_chain}")
    
    # Obter configurações
    if args.source_chain.lower() == "polygon":
        rpc_url = os.getenv('POLYGON_RPC_URL', 'https://rpc-amoy.polygon.technology')
        private_key = os.getenv('POLYGON_PRIVATE_KEY')
        contract_address = os.getenv('POLYGON_COMMITMENT_CONTRACT', '0x0b5AB34be0f5734161E608885e139AE2b72a07AE')
    elif args.source_chain.lower() in ["ethereum", "eth"]:
        rpc_url = os.getenv('ETH_RPC_URL', 'https://sepolia.infura.io/v3/')
        private_key = os.getenv('ETH_PRIVATE_KEY')
        contract_address = os.getenv('ETH_COMMITMENT_CONTRACT', '0x00077a4bF0d73f398C808fe8e5e9763Bf59915fb')
    else:
        print_error(f"Chain não suportada: {args.source_chain}")
        return
    
    if not private_key:
        print_error(f"Private key não configurada para {args.source_chain}")
        return
    
    # Criar manager
    manager = CommitmentManager(
        rpc_url=rpc_url,
        private_key=private_key,
        commitment_contract_address=contract_address
    )
    
    # Criar commitment
    result = manager.create_commitment(
        target_chain=args.target_chain,
        target_recipient=args.recipient,
        amount=int(args.amount),
        nonce=None
    )
    
    if result.get('success'):
        print_success("Commitment criado com sucesso!")
        print_info(f"Commitment Hash: {result['commitment_hash']}")
        print_info(f"UChainID: {result['uchain_id']}")
        print_info(f"TX Hash: {result['tx_hash']}")
        
        # Registrar no monitor
        monitor = CommitmentMonitor()
        monitor.record_commitment_created(
            commitment_hash=result['commitment_hash'],
            source_chain=args.source_chain,
            target_chain=args.target_chain
        )
    else:
        print_error(f"Falha: {result.get('error')}")


def cmd_get(args):
    """Obtém detalhes de um commitment"""
    print_info(f"Consultando commitment: {args.hash[:16]}...")
    
    # Tentar ambas as chains
    chains = [
        ("polygon", os.getenv('POLYGON_RPC_URL'), os.getenv('POLYGON_PRIVATE_KEY'),
         os.getenv('POLYGON_COMMITMENT_CONTRACT', '0x0b5AB34be0f5734161E608885e139AE2b72a07AE')),
        ("ethereum", os.getenv('ETH_RPC_URL'), os.getenv('ETH_PRIVATE_KEY'),
         os.getenv('ETH_COMMITMENT_CONTRACT', '0x00077a4bF0d73f398C808fe8e5e9763Bf59915fb'))
    ]
    
    for chain_name, rpc_url, private_key, contract_address in chains:
        if not private_key or not rpc_url:
            continue
        
        try:
            manager = CommitmentManager(
                rpc_url=rpc_url,
                private_key=private_key,
                commitment_contract_address=contract_address
            )
            
            result = manager.get_commitment(args.hash)
            if result.get('success'):
                commitment = result['commitment']
                print_success("Commitment encontrado!")
                print_info(f"Source Address: {commitment['source_address']}")
                print_info(f"Target Chain: {commitment['target_chain']}")
                print_info(f"Amount: {commitment['amount']} wei")
                print_info(f"UChainID: {commitment['uchain_id']}")
                print_info(f"Executed: {commitment['executed']}")
                print_info(f"Block Number: {commitment['block_number']}")
                return
        except:
            continue
    
    print_error("Commitment não encontrado")


def cmd_verify(args):
    """Verifica um commitment"""
    print_info(f"Verificando commitment: {args.hash[:16]}...")
    
    # Tentar ambas as chains
    chains = [
        ("polygon", os.getenv('POLYGON_RPC_URL'), os.getenv('POLYGON_PRIVATE_KEY'),
         os.getenv('POLYGON_COMMITMENT_CONTRACT', '0x0b5AB34be0f5734161E608885e139AE2b72a07AE')),
        ("ethereum", os.getenv('ETH_RPC_URL'), os.getenv('ETH_PRIVATE_KEY'),
         os.getenv('ETH_COMMITMENT_CONTRACT', '0x00077a4bF0d73f398C808fe8e5e9763Bf59915fb'))
    ]
    
    for chain_name, rpc_url, private_key, contract_address in chains:
        if not private_key or not rpc_url:
            continue
        
        try:
            manager = CommitmentManager(
                rpc_url=rpc_url,
                private_key=private_key,
                commitment_contract_address=contract_address
            )
            
            result = manager.verify_commitment(args.hash, args.target_tx)
            if result.get('success'):
                print_success("Commitment verificado com sucesso!")
                print_info(f"TX Hash: {result['tx_hash']}")
                print_info(f"Block Number: {result['block_number']}")
                
                # Registrar no monitor
                monitor = CommitmentMonitor()
                monitor.record_commitment_verified(
                    commitment_hash=args.hash,
                    success=True
                )
                return
        except Exception as e:
            print_error(f"Erro: {e}")
            continue
    
    print_error("Falha ao verificar commitment")


def cmd_status(args):
    """Mostra status do sistema"""
    monitor = CommitmentMonitor()
    retry_manager = CommitmentRetryManager()
    
    stats = monitor.get_stats(hours=24)
    retry_stats = retry_manager.get_stats()
    
    print("\n" + "="*70)
    print("📊 STATUS DO SISTEMA")
    print("="*70)
    
    print(f"\n📈 Métricas (últimas 24h):")
    print(f"   Total: {stats['total']}")
    print(f"   Verificados: {stats['verified']}")
    print(f"   Taxa de sucesso: {stats['success_rate']:.1f}%")
    print(f"   Tempo médio: {stats['avg_verification_time_seconds']:.1f}s")
    
    print(f"\n🔄 Fila de Retry:")
    print(f"   Pendentes: {retry_stats['total']}")
    print(f"   Prontos: {retry_stats['ready_for_retry']}")


def main():
    parser = argparse.ArgumentParser(
        description='CLI para Sistema de Commitment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s create --source polygon --target bitcoin --recipient bc1q... --amount 1000000000000000
  %(prog)s get --hash 0xabc123...
  %(prog)s verify --hash 0xabc123... --target-tx 0xdef456...
  %(prog)s status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Cria um novo commitment')
    create_parser.add_argument('--source', dest='source_chain', required=True, help='Chain de origem')
    create_parser.add_argument('--target', dest='target_chain', required=True, help='Chain de destino')
    create_parser.add_argument('--recipient', required=True, help='Endereço do destinatário')
    create_parser.add_argument('--amount', required=True, help='Valor em wei')
    create_parser.set_defaults(func=cmd_create)
    
    # Get
    get_parser = subparsers.add_parser('get', help='Obtém detalhes de um commitment')
    get_parser.add_argument('--hash', required=True, help='Hash do commitment')
    get_parser.set_defaults(func=cmd_get)
    
    # Verify
    verify_parser = subparsers.add_parser('verify', help='Verifica um commitment')
    verify_parser.add_argument('--hash', required=True, help='Hash do commitment')
    verify_parser.add_argument('--target-tx', dest='target_tx', required=True, help='Hash da transação no target chain')
    verify_parser.set_defaults(func=cmd_verify)
    
    # Status
    status_parser = subparsers.add_parser('status', help='Mostra status do sistema')
    status_parser.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()

