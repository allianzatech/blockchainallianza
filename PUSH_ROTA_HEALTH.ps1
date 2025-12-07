# Script para fazer push da rota GET / para health check
# Execute: .\PUSH_ROTA_HEALTH.ps1

Write-Host "🚀 Push para GitHub - Rota GET / Health Check" -ForegroundColor Cyan
Write-Host ""

# Navegar para o diretório
Set-Location "C:\Users\notebook\Downloads\Allianza Blockchain"

# Verificar status
Write-Host "📊 Verificando status do repositório..." -ForegroundColor Yellow
git status --short

Write-Host "`n📝 Commit local:" -ForegroundColor Yellow
git log --oneline -1

Write-Host "`n🔐 Tentando push com credenciais do Windows..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "`n🌐 Verifique o repositório:" -ForegroundColor Cyan
    Write-Host "   https://github.com/dieisonmaach-lang/allianzablockchain/commits/main" -ForegroundColor White
} else {
    Write-Host "`n❌ Push falhou. Tente uma das opções abaixo:" -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 OPÇÃO 1: Push Manual via GitHub Web" -ForegroundColor Yellow
    Write-Host "   1. Acesse: https://github.com/dieisonmaach-lang/allianzablockchain" -ForegroundColor White
    Write-Host "   2. Vá em: allianza_blockchain.py" -ForegroundColor White
    Write-Host "   3. Clique em 'Edit' (lápis)" -ForegroundColor White
    Write-Host "   4. Adicione o código após linha 1310 (após socketio = ...)" -ForegroundColor White
    Write-Host "   5. Commit: '✅ Adicionar rota GET / para health check'" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 OPÇÃO 2: Usar Token com Permissões Corretas" -ForegroundColor Yellow
    Write-Host "   1. Acesse: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "   2. Gere novo token com permissão 'repo' (acesso completo)" -ForegroundColor White
    Write-Host "   3. Execute: git remote set-url origin https://SEU_TOKEN@github.com/dieisonmaach-lang/allianzablockchain.git" -ForegroundColor White
    Write-Host "   4. Execute: git push origin main" -ForegroundColor White
    Write-Host "   5. Execute: git remote set-url origin https://github.com/dieisonmaach-lang/allianzablockchain.git" -ForegroundColor White
}

Write-Host ""

