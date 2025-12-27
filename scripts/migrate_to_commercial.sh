#!/bin/bash
# Script para migrar arquivos comerciais para repositório privado
# Uso: ./scripts/migrate_to_commercial.sh /path/to/blockchainallianza-business

set -e  # Parar em caso de erro

COMMERCIAL_REPO="$1"

if [ -z "$COMMERCIAL_REPO" ]; then
    echo "❌ Erro: Caminho do repositório comercial não fornecido"
    echo "Uso: $0 /path/to/blockchainallianza-business"
    exit 1
fi

if [ ! -d "$COMMERCIAL_REPO" ]; then
    echo "❌ Erro: Diretório não encontrado: $COMMERCIAL_REPO"
    exit 1
fi

echo "🚀 Iniciando migração para: $COMMERCIAL_REPO"
echo ""

# Criar estrutura de pastas
echo "📁 Criando estrutura de pastas..."
mkdir -p "$COMMERCIAL_REPO/adapters"
mkdir -p "$COMMERCIAL_REPO/libraries"
mkdir -p "$COMMERCIAL_REPO/production"
mkdir -p "$COMMERCIAL_REPO/enterprise"
mkdir -p "$COMMERCIAL_REPO/contracts"
echo "✅ Estrutura criada"
echo ""

# Função para copiar arquivo com verificação
copy_file() {
    local source="$1"
    local dest="$2"
    
    if [ -f "$source" ]; then
        cp "$source" "$dest"
        echo "✅ Copiado: $source"
        return 0
    else
        echo "⚠️  Não encontrado: $source"
        return 1
    fi
}

# Adapters
echo "📦 Copiando adapters..."
copy_file "real_cross_chain_bridge.py" "$COMMERCIAL_REPO/adapters/"
copy_file "bitcoin_clm.py" "$COMMERCIAL_REPO/adapters/"
copy_file "polygon_clm.py" "$COMMERCIAL_REPO/adapters/"
copy_file "solana_clm.py" "$COMMERCIAL_REPO/adapters/"
copy_file "bsc_clm.py" "$COMMERCIAL_REPO/adapters/"
echo ""

# Libraries
echo "📚 Copiando bibliotecas..."
copy_file "simple_bitcoin.py" "$COMMERCIAL_REPO/libraries/"
copy_file "simple_bitcoin_direct.py" "$COMMERCIAL_REPO/libraries/"
echo ""

# Contracts
echo "📄 Copiando contratos..."
copy_file "contracts/ethereum_bridge.py" "$COMMERCIAL_REPO/contracts/"
copy_file "contracts/polygon_bridge.py" "$COMMERCIAL_REPO/contracts/"
copy_file "contracts/bitcoin_bridge.py" "$COMMERCIAL_REPO/contracts/"
copy_file "contracts/advanced_interoperability.py" "$COMMERCIAL_REPO/contracts/"
echo ""

# Production
echo "🏭 Copiando código de produção..."
copy_file "allianza_blockchain.py" "$COMMERCIAL_REPO/production/"
copy_file "uec_integration.py" "$COMMERCIAL_REPO/production/"
copy_file "blockchain_connector.py" "$COMMERCIAL_REPO/production/"
echo ""

# Enterprise
echo "💼 Copiando features enterprise..."
copy_file "advanced_monitoring.py" "$COMMERCIAL_REPO/enterprise/"
copy_file "advanced_gas_optimizer.py" "$COMMERCIAL_REPO/enterprise/"
copy_file "banking_api_layer.py" "$COMMERCIAL_REPO/enterprise/"
copy_file "qaas_enterprise.py" "$COMMERCIAL_REPO/enterprise/"
echo ""

echo "✅ Migração concluída!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Revisar arquivos copiados em: $COMMERCIAL_REPO"
echo "   2. Criar README.md no repo comercial"
echo "   3. Commit e push no repo comercial"
echo "   4. Remover arquivos do repo público (após confirmar backup)"
echo ""
echo "📖 Veja MIGRATE_TO_COMMERCIAL_REPO.md para instruções completas"




