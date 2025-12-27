# Script para organizar repositórios final
# PRIVADO: TUDO | PÚBLICO: Open Core apenas

param(
    [string]$PrivateRepoPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "`n🔧 Organizando Repositórios Final" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# 1. Encontrar ou criar repo privado
if ([string]::IsNullOrEmpty($PrivateRepoPath)) {
    $possiblePaths = @(
        "..\blockchainallianza-business",
        "..\..\blockchainallianza-business",
        "C:\Users\notebook\Music\blockchainallianza-business"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $PrivateRepoPath = $path
            Write-Host "✅ Repo privado encontrado: $PrivateRepoPath" -ForegroundColor Green
            break
        }
    }
    
    if ([string]::IsNullOrEmpty($PrivateRepoPath)) {
        Write-Host "⚠️  Repo privado não encontrado. Onde está?" -ForegroundColor Yellow
        $PrivateRepoPath = Read-Host "Digite o caminho completo"
    }
}

# 2. Copiar TUDO para repo privado
Write-Host "`n📦 Copiando TODOS os arquivos para repo privado..." -ForegroundColor Cyan

$excludePatterns = @(
    "\.git",
    "__pycache__",
    "node_modules",
    "\.venv",
    "commercial_repo",
    "\.db$",
    "\.log$",
    "\.pyc$"
)

$copied = 0
$skipped = 0

Get-ChildItem -Recurse -File | ForEach-Object {
    $shouldExclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($_.FullName -match $pattern) {
            $shouldExclude = $true
            break
        }
    }
    
    if (-not $shouldExclude) {
        $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
        $destPath = Join-Path $PrivateRepoPath $relativePath
        $destDir = Split-Path $destPath -Parent
        
        try {
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item $_.FullName $destPath -Force -ErrorAction Stop
            $copied++
        } catch {
            $skipped++
        }
    }
}

Write-Host "✅ Copiados: $copied arquivos" -ForegroundColor Green
Write-Host "⚠️  Ignorados: $skipped arquivos" -ForegroundColor Yellow

# 3. Commit no repo privado
Write-Host "`n📝 Fazendo commit no repo privado..." -ForegroundColor Cyan
Push-Location $PrivateRepoPath

try {
    git add . 2>&1 | Out-Null
    git commit -m "Add all files for Render deployment and proof generation

- Complete codebase for production deployment
- All templates, static files, and configurations
- Ready for Render.com deployment" 2>&1 | Out-Null
    
    Write-Host "✅ Commit realizado!" -ForegroundColor Green
    
    Write-Host "`n📤 Fazendo push..." -ForegroundColor Cyan
    git push origin main 2>&1 | Out-Null
    Write-Host "✅ Push realizado!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Erro no commit/push: $_" -ForegroundColor Yellow
}

Pop-Location

Write-Host "`n✅ Repositório PRIVADO atualizado com TODOS os arquivos!" -ForegroundColor Green
Write-Host "`n📝 Próximo passo: Limpar repositório público (manter apenas open core)" -ForegroundColor Cyan

