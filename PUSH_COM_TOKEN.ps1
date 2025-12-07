# Script para fazer push com token
# Execute: .\PUSH_COM_TOKEN.ps1

Write-Host "🚀 Push para GitHub - allianza-wallet-backend" -ForegroundColor Cyan
Write-Host ""

# Solicitar token
$token = Read-Host "Cole seu Personal Access Token do GitHub"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "❌ Token não fornecido. Abortando." -ForegroundColor Red
    exit 1
}

# Navegar para o diretório
Set-Location "C:\Users\notebook\Downloads\allianza-wallet1"

# Configurar remote com token
Write-Host "`n🔧 Configurando remote com token..." -ForegroundColor Yellow
git remote set-url origin "https://$token@github.com/brunosmaach-spec/allianza-wallet-backend.git"

# Fazer push
Write-Host "📤 Fazendo push..." -ForegroundColor Yellow
git push origin main

# Verificar resultado
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "`n🔒 Removendo token do URL por segurança..." -ForegroundColor Yellow
    git remote set-url origin "https://github.com/brunosmaach-spec/allianza-wallet-backend.git"
    Write-Host "✅ Token removido do URL" -ForegroundColor Green
} else {
    Write-Host "`n❌ Erro ao fazer push. Verifique o token e as permissões." -ForegroundColor Red
    Write-Host "`n🔒 Removendo token do URL por segurança..." -ForegroundColor Yellow
    git remote set-url origin "https://github.com/brunosmaach-spec/allianza-wallet-backend.git"
}

Write-Host "`n📝 Verifique o repositório:" -ForegroundColor Cyan
Write-Host "   https://github.com/brunosmaach-spec/allianza-wallet-backend/commits/main" -ForegroundColor White

