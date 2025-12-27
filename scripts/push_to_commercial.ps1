# Script para fazer push dos arquivos comerciais para o repositório privado
# Uso: .\scripts\push_to_commercial.ps1 -CommercialRepoPath "C:\caminho\para\blockchainallianza-business"

param(
    [Parameter(Mandatory=$false)]
    [string]$CommercialRepoPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 Push para Repositório Comercial" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

# Verificar se commercial_repo existe
if (-not (Test-Path "commercial_repo")) {
    Write-Host "❌ Erro: Pasta commercial_repo não encontrada!" -ForegroundColor Red
    Write-Host "   Execute primeiro a migração dos arquivos." -ForegroundColor Yellow
    exit 1
}

# Se não forneceu caminho, perguntar ou usar padrão
if ([string]::IsNullOrEmpty($CommercialRepoPath)) {
    $defaultPath = Join-Path (Get-Location).Parent.FullName "blockchainallianza-business"
    
    Write-Host "`n📁 Caminho do repositório comercial:" -ForegroundColor Cyan
    Write-Host "   Padrão sugerido: $defaultPath" -ForegroundColor Yellow
    
    $CommercialRepoPath = Read-Host "   Digite o caminho (ou Enter para usar o padrão)"
    
    if ([string]::IsNullOrEmpty($CommercialRepoPath)) {
        $CommercialRepoPath = $defaultPath
    }
}

# Verificar se o caminho existe
if (-not (Test-Path $CommercialRepoPath)) {
    Write-Host "`n⚠️  Diretório não existe. Criar? (S/N)" -ForegroundColor Yellow
    $create = Read-Host
    
    if ($create -eq "S" -or $create -eq "s") {
        New-Item -ItemType Directory -Path $CommercialRepoPath -Force | Out-Null
        Write-Host "✅ Diretório criado!" -ForegroundColor Green
    } else {
        Write-Host "❌ Operação cancelada." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n📦 Copiando arquivos..." -ForegroundColor Cyan

# Copiar arquivos
try {
    Copy-Item -Path "commercial_repo\*" -Destination $CommercialRepoPath -Recurse -Force
    Write-Host "✅ Arquivos copiados com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao copiar arquivos: $_" -ForegroundColor Red
    exit 1
}

# Verificar se é repositório git
$isGitRepo = Test-Path (Join-Path $CommercialRepoPath ".git")

if (-not $isGitRepo) {
    Write-Host "`n📝 Inicializando repositório Git..." -ForegroundColor Cyan
    
    Push-Location $CommercialRepoPath
    
    try {
        git init
        git remote add origin https://github.com/allianzatech/blockchainallianza-business.git 2>$null
        Write-Host "✅ Repositório Git inicializado!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Aviso: Erro ao configurar Git. Configure manualmente." -ForegroundColor Yellow
    }
    
    Pop-Location
} else {
    Write-Host "`n✅ Repositório Git já existe" -ForegroundColor Green
}

Write-Host "`n📋 Próximos passos manuais:" -ForegroundColor Cyan
Write-Host "   1. Navegue para: $CommercialRepoPath" -ForegroundColor Yellow
Write-Host "   2. Execute: git add ." -ForegroundColor Yellow
Write-Host "   3. Execute: git commit -m 'Add commercial production code'" -ForegroundColor Yellow
Write-Host "   4. Execute: git push -u origin main" -ForegroundColor Yellow
Write-Host "`n   Ou execute os comandos automaticamente? (S/N)" -ForegroundColor Cyan

$auto = Read-Host

if ($auto -eq "S" -or $auto -eq "s") {
    Push-Location $CommercialRepoPath
    
    try {
        Write-Host "`n📤 Fazendo commit e push..." -ForegroundColor Cyan
        
        git add .
        git commit -m "Add commercial production code from public repository

- Production adapters (real_cross_chain_bridge, *_clm)
- Proprietary libraries (simple_bitcoin)
- Production orchestration (allianza_blockchain, uec_integration)
- Enterprise features (advanced_monitoring, banking_api_layer)
- Production contracts (ethereum_bridge, polygon_bridge, bitcoin_bridge)

Migrated from: https://github.com/allianzatech/blockchainallianza"
        
        Write-Host "✅ Commit realizado!" -ForegroundColor Green
        
        Write-Host "`n📤 Fazendo push..." -ForegroundColor Cyan
        git push -u origin main
        
        Write-Host "`n✅ Push concluído com sucesso!" -ForegroundColor Green
        Write-Host "`n🎉 Arquivos comerciais estão no repositório privado!" -ForegroundColor Green
        
    } catch {
        Write-Host "`n❌ Erro durante commit/push: $_" -ForegroundColor Red
        Write-Host "   Execute os comandos manualmente." -ForegroundColor Yellow
    }
    
    Pop-Location
} else {
    Write-Host "`n✅ Arquivos prontos para commit manual!" -ForegroundColor Green
}

Write-Host "`n📖 Veja PUSH_TO_COMMERCIAL_REPO.md para mais detalhes" -ForegroundColor Cyan
Write-Host "`n" -ForegroundColor White




