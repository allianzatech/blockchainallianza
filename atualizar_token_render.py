#!/usr/bin/env python3
"""
Script para atualizar a variável VITE_SITE_ADMIN_TOKEN no Render
via API do Render.

REQUISITOS:
1. Token de API do Render (obter em: https://dashboard.render.com/account/api-keys)
2. Service ID: srv-d3qp4mu3jp1c738pams0
"""

import requests
import json
import os
import sys

# Configurações
RENDER_API_KEY = os.getenv('RENDER_API_KEY')  # Você precisa configurar isso
SERVICE_ID = 'srv-d3qp4mu3jp1c738pams0'
NEW_TOKEN = 'vNFkVqGDZ4QOcrMLdEKPSx3upInRaTAstogl6Ch8HmYJyB5eb1wiWXf270z9jU'
VARIABLE_KEY = 'VITE_SITE_ADMIN_TOKEN'

# URL da API do Render
RENDER_API_BASE = 'https://api.render.com/v1'

def get_service_env_vars():
    """Buscar variáveis de ambiente atuais do serviço"""
    url = f'{RENDER_API_BASE}/services/{SERVICE_ID}/env-vars'
    headers = {
        'Authorization': f'Bearer {RENDER_API_KEY}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar variáveis: {e}")
        if hasattr(e.response, 'text'):
            print(f"Resposta: {e.response.text}")
        return None

def update_env_var():
    """Atualizar ou criar a variável de ambiente"""
    url = f'{RENDER_API_BASE}/services/{SERVICE_ID}/env-vars'
    headers = {
        'Authorization': f'Bearer {RENDER_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Primeiro, buscar variáveis existentes
    existing_vars = get_service_env_vars()
    if existing_vars is None:
        return False
    
    # Verificar se a variável já existe
    var_exists = False
    for var in existing_vars:
        if var.get('key') == VARIABLE_KEY:
            var_exists = True
            var_id = var.get('id')
            break
    
    if var_exists:
        # Atualizar variável existente
        update_url = f'{RENDER_API_BASE}/services/{SERVICE_ID}/env-vars/{var_id}'
        data = {
            'value': NEW_TOKEN
        }
        
        try:
            response = requests.patch(update_url, headers=headers, json=data)
            response.raise_for_status()
            print(f"✅ Variável {VARIABLE_KEY} atualizada com sucesso!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao atualizar variável: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Resposta: {e.response.text}")
            return False
    else:
        # Criar nova variável
        data = {
            'key': VARIABLE_KEY,
            'value': NEW_TOKEN
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"✅ Variável {VARIABLE_KEY} criada com sucesso!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao criar variável: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Resposta: {e.response.text}")
            return False

def trigger_deploy():
    """Disparar um novo deploy"""
    url = f'{RENDER_API_BASE}/services/{SERVICE_ID}/deploys'
    headers = {
        'Authorization': f'Bearer {RENDER_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    data = {
        'clearCache': True
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        deploy_data = response.json()
        print(f"✅ Deploy iniciado! ID: {deploy_data.get('id')}")
        print(f"📊 Acompanhe em: https://dashboard.render.com/web/srv-d3qp4mu3jp1c738pams0")
        return True
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Variável atualizada, mas não foi possível iniciar deploy automaticamente")
        print(f"   Por favor, inicie um deploy manual no dashboard do Render")
        if hasattr(e, 'response') and e.response:
            print(f"   Erro: {e.response.text}")
        return False

def main():
    print("=" * 60)
    print("🔐 Atualizar Token no Render")
    print("=" * 60)
    print()
    
    # Verificar se a API key está configurada
    if not RENDER_API_KEY:
        print("❌ ERRO: RENDER_API_KEY não configurada!")
        print()
        print("📝 Como configurar:")
        print("1. Acesse: https://dashboard.render.com/account/api-keys")
        print("2. Crie uma nova API key")
        print("3. Execute:")
        print(f"   export RENDER_API_KEY=sua_api_key_aqui")
        print("   (Windows PowerShell: $env:RENDER_API_KEY='sua_api_key_aqui')")
        print()
        print("Ou execute o script assim:")
        print(f"   RENDER_API_KEY=sua_api_key python atualizar_token_render.py")
        sys.exit(1)
    
    print(f"🔍 Service ID: {SERVICE_ID}")
    print(f"🔑 Variável: {VARIABLE_KEY}")
    print(f"📝 Novo token: {NEW_TOKEN[:20]}...")
    print()
    
    # Atualizar variável
    print("📤 Atualizando variável de ambiente...")
    if update_env_var():
        print()
        print("🚀 Iniciando deploy...")
        trigger_deploy()
        print()
        print("=" * 60)
        print("✅ Processo concluído!")
        print("=" * 60)
        print()
        print("⏳ Aguarde 2-5 minutos para o deploy completar")
        print("🔍 Acompanhe em: https://dashboard.render.com")
    else:
        print()
        print("❌ Falha ao atualizar variável")
        print("💡 Tente atualizar manualmente no dashboard do Render")
        sys.exit(1)

if __name__ == '__main__':
    main()

