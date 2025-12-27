# Script PowerShell para migrar arquivos comerciais para repositório privado
# Uso: .\scripts\migrate_to_commercial.ps1 -CommercialRepo "C:\path\to\blockchainallianza-business"

param(
    [Parameter(Mandatory=$true)]
    [string]$CommercialRepo
)

# Verificar se o diretório existe
if (-not (Test-Path $CommercialRepo)) {
    Write-Host "❌ Erro: Diretório não encontrado: $CommercialRepo" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Iniciando migração para: $CommercialRepo" -ForegroundColor Green
Write-Host ""

# Criar estrutura de pastas
Write-Host "📁 Criando estrutura de pastas..." -ForegroundColor Cyan
$folders = @("adapters", "libraries", "production", "enterprise", "contracts")
foreach ($folder in $folders) {
    $path = Join-Path $CommercialRepo $folder
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "✅ Criado: $folder" -ForegroundColor Green
    }
}
Write-Host ""

# Função para copiar arquivo com verificação
function Copy-FileSafe {
    param(
        [string]$Source,
        [string]$Dest
    )
    
    if (Test-Path $Source) {
        Copy-Item $Source $Dest -Force
        Write-Host "✅ Copiado: $Source" -ForegroundColor Green
        return $true
    } else {
        Write-Host "⚠️  Não encontrado: $Source" -ForegroundColor Yellow
        return $false
    }
}

# Adapters
Write-Host "📦 Copiando adapters..." -ForegroundColor Cyan
Copy-FileSafe "real_cross_chain_bridge.py" (Join-Path $CommercialRepo "adapters\real_cross_chain_bridge.py")
Copy-FileSafe "bitcoin_clm.py" (Join-Path $CommercialRepo "adapters\bitcoin_clm.py")
Copy-FileSafe "polygon_clm.py" (Join-Path $CommercialRepo "adapters\polygon_clm.py")
Copy-FileSafe "solana_clm.py" (Join-Path $CommercialRepo "adapters\solana_clm.py")
Copy-FileSafe "bsc_clm.py" (Join-Path $CommercialRepo "adapters\bsc_clm.py")
Write-Host ""

# Libraries
Write-Host "📚 Copiando bibliotecas..." -ForegroundColor Cyan
Copy-FileSafe "simple_bitcoin.py" (Join-Path $CommercialRepo "libraries\simple_bitcoin.py")
Copy-FileSafe "simple_bitcoin_direct.py" (Join-Path $CommercialRepo "libraries\simple_bitcoin_direct.py")
Write-Host ""

# Contracts
Write-Host "📄 Copiando contratos..." -ForegroundColor Cyan
Copy-FileSafe "contracts\ethereum_bridge.py" (Join-Path $CommercialRepo "contracts\ethereum_bridge.py")
Copy-FileSafe "contracts\polygon_bridge.py" (Join-Path $CommercialRepo "contracts\polygon_bridge.py")
Copy-FileSafe "contracts\bitcoin_bridge.py" (Join-Path $CommercialRepo "contracts\bitcoin_bridge.py")
Copy-FileSafe "contracts\advanced_interoperability.py" (Join-Path $CommercialRepo "contracts\advanced_interoperability.py")
Write-Host ""

# Production
Write-Host "🏭 Copiando código de produção..." -ForegroundColor Cyan
Copy-FileSafe "allianza_blockchain.py" (Join-Path $CommercialRepo "production\allianza_blockchain.py")
Copy-FileSafe "uec_integration.py" (Join-Path $CommercialRepo "production\uec_integration.py")
Copy-FileSafe "blockchain_connector.py" (Join-Path $CommercialRepo "production\blockchain_connector.py")
Write-Host ""

# Enterprise
Write-Host "💼 Copiando features enterprise..." -ForegroundColor Cyan
Copy-FileSafe "advanced_monitoring.py" (Join-Path $CommercialRepo "enterprise\advanced_monitoring.py")
Copy-FileSafe "advanced_gas_optimizer.py" (Join-Path $CommercialRepo "enterprise\advanced_gas_optimizer.py")
Copy-FileSafe "banking_api_layer.py" (Join-Path $CommercialRepo "enterprise\banking_api_layer.py")
Copy-FileSafe "qaas_enterprise.py" (Join-Path $CommercialRepo "enterprise\qaas_enterprise.py")
Write-Host ""

Write-Host "✅ Migração concluída!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Revisar arquivos copiados em: $CommercialRepo"
Write-Host "   2. Criar README.md no repo comercial"
Write-Host "   3. Commit e push no repo comercial"
Write-Host "   4. Remover arquivos do repo público (após confirmar backup)"
Write-Host ""
Write-Host "📖 Veja MIGRATE_TO_COMMERCIAL_REPO.md para instruções completas" -ForegroundColor Yellow




