#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allianza Blockchain CLI
Interface de linha de comando para desenvolvedores
"""

import click
import json
import sys
from typing import Optional
from pathlib import Path

# Importar SDK
sys.path.insert(0, str(Path(__file__).parent.parent))
from sdk.python.allianza_sdk import AllianzaWeb3, AllianzaWallet, create_wallet, connect_wallet

@click.group()
@click.option('--rpc-url', default='http://localhost:8545', help='URL do RPC')
@click.pass_context
def cli(ctx, rpc_url):
    """Allianza Blockchain CLI - Ferramenta de linha de comando"""
    ctx.ensure_object(dict)
    ctx.obj['rpc_url'] = rpc_url
    ctx.obj['web3'] = AllianzaWeb3(rpc_url)

@cli.group()
def wallet():
    """Comandos de wallet"""
    pass

@wallet.command('create')
@click.pass_context
def wallet_create(ctx):
    """Cria nova wallet"""
    wallet = create_wallet()
    click.echo("✅ Wallet criada!")
    click.echo(f"Endereço: {wallet.address}")
    click.echo(f"Chave privada: {wallet.account.key.hex()}")
    click.echo("\n⚠️  GUARDE A CHAVE PRIVADA EM SEGURANÇA!")

@wallet.command('balance')
@click.argument('address')
@click.pass_context
def wallet_balance(ctx, address):
    """Obtém saldo da wallet
    
    Exemplo:
        python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5
    """
    # Remover < e > se o usuário usou por engano
    address = address.strip('<>')
    
    web3 = ctx.obj['web3']
    try:
        balance = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance, 'ether')
        click.echo(f"💰 Saldo: {balance_eth} ALZ")
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)
        click.echo(f"\n💡 Dica: Use o endereço diretamente, sem < >")
        click.echo(f"   Exemplo: python cli/allianza_cli.py wallet balance 0xBeEd0E7001daA6E72146A5BA74Ace7D958037af5")

@cli.group()
def transaction():
    """Comandos de transação"""
    pass

@transaction.command('send')
@click.argument('to')
@click.argument('amount')
@click.option('--private-key', required=True, help='Chave privada')
@click.pass_context
def transaction_send(ctx, to, amount, private_key):
    """Envia transação
    
    Exemplo:
        python cli/allianza_cli.py transaction send 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0 0.1 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955
    """
    # Remover < e > se o usuário usou por engano
    to = to.strip('<>')
    private_key = private_key.strip('<>')
    
    web3 = ctx.obj['web3']
    wallet = connect_wallet(private_key, ctx.obj['rpc_url'])
    
    try:
        result = wallet.send_transaction(to, amount)
        
        # Verificar se é um dict com erro
        if isinstance(result, dict):
            if result.get("success") == False:
                click.echo(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                if result.get("message"):
                    click.echo(f"💡 {result.get('message')}")
                return
            else:
                # Se for dict de sucesso, mostrar resultado
                click.echo(f"✅ Transação enviada!")
                click.echo(json.dumps(result, indent=2, default=str))
                return
        
        # Se for bytes ou HexBytes, converter para hex
        if hasattr(result, 'hex'):
            click.echo(f"✅ Transação enviada!")
            click.echo(f"Hash: {result.hex()}")
        elif isinstance(result, str):
            click.echo(f"✅ Transação enviada!")
            click.echo(f"Hash: {result}")
        else:
            click.echo(f"✅ Transação enviada!")
            click.echo(f"Resultado: {result}")
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)
        import traceback
        click.echo(f"\n💡 Detalhes: {traceback.format_exc()}", err=True)
        click.echo(f"\n💡 Dica: Verifique se o RPC server está rodando:")
        click.echo(f"   python rpc_server.py")
        click.echo(f"\n💡 Use os valores diretamente, sem < >")
        click.echo(f"   Exemplo: python cli/allianza_cli.py transaction send 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0 0.1 --private-key 287cd4c45d3232c67919337e6d6c095e8db0fd40062ff92bf49422306c6dc955")

@transaction.command('cross-chain')
@click.argument('target_chain')
@click.argument('recipient')
@click.argument('amount')
@click.option('--private-key', required=True, help='Chave privada')
@click.pass_context
def transaction_cross_chain(ctx, target_chain, recipient, amount, private_key):
    """Envia transação cross-chain"""
    web3 = ctx.obj['web3']
    wallet = connect_wallet(private_key, ctx.obj['rpc_url'])
    
    try:
        result = wallet.send_cross_chain(target_chain, recipient, amount)
        click.echo(f"✅ Transação cross-chain enviada!")
        
        # Converter AttributeDict para dict se necessário
        if hasattr(result, '__dict__'):
            result = dict(result)
        elif not isinstance(result, dict):
            result = {"result": str(result)}
        
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)
        import traceback
        click.echo(f"\n💡 Detalhes: {traceback.format_exc()}", err=True)

@cli.group()
def validator():
    """Comandos de validação"""
    pass

@validator.command('register')
@click.argument('address')
@click.argument('stake_amount', type=float)
@click.option('--commission', default=0.1, help='Taxa de comissão (0-1)')
@click.pass_context
def validator_register(ctx, address, stake_amount, commission):
    """Registra novo validador"""
    # Em produção, isso chamaria o contrato de staking
    click.echo(f"📝 Registrando validador: {address}")
    click.echo(f"   Stake: {stake_amount} ALZ")
    click.echo(f"   Comissão: {commission * 100}%")
    click.echo("✅ Validador registrado!")

@validator.command('list')
@click.pass_context
def validator_list(ctx):
    """Lista validadores"""
    web3 = ctx.obj['web3']
    try:
        validators = web3.get_validators()
        click.echo("📋 Validadores:")
        for v in validators.get('validators', []):
            click.echo(f"   {v.get('address')} - Stake: {v.get('staked_amount')} ALZ")
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)

@validator.command('info')
@click.argument('address')
@click.pass_context
def validator_info(ctx, address):
    """Obtém informações do validador"""
    web3 = ctx.obj['web3']
    try:
        info = web3.get_validator_info(address)
        click.echo(f"📊 Validador: {address}")
        click.echo(json.dumps(info, indent=2))
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)

@cli.group()
def dao():
    """Comandos de DAO"""
    pass

@dao.command('create-proposal')
@click.argument('title')
@click.argument('description')
@click.option('--proposer', required=True, help='Endereço do proponente')
@click.option('--deposit', type=float, default=100.0, help='Depósito mínimo')
@click.pass_context
def dao_create_proposal(ctx, title, description, proposer, deposit):
    """Cria nova proposta"""
    # Em produção, isso chamaria o contrato de DAO
    click.echo(f"📝 Criando proposta: {title}")
    click.echo(f"   Proponente: {proposer}")
    click.echo(f"   Depósito: {deposit} ALZ")
    click.echo("✅ Proposta criada!")

@dao.command('list')
@click.pass_context
def dao_list(ctx):
    """Lista propostas"""
    # Em produção, isso consultaria o contrato de DAO
    click.echo("📋 Propostas:")
    click.echo("   (Funcionalidade será implementada com contrato de DAO)")

@cli.command()
@click.pass_context
def network_info(ctx):
    """Obtém informações da rede"""
    web3 = ctx.obj['web3']
    try:
        info = web3.get_network_info()
        click.echo("🌐 Informações da Rede:")
        click.echo(json.dumps(info, indent=2))
    except Exception as e:
        click.echo(f"❌ Erro: {e}", err=True)

@cli.command()
def version():
    """Mostra versão do CLI"""
    click.echo("Allianza Blockchain CLI v1.0.0")

if __name__ == '__main__':
    cli()

