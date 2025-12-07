# Script para limpar credenciais do GitHub e fazer push
# Execute este script no PowerShell

Write-Host "🔧 Limpando credenciais antigas do GitHub..." -ForegroundColor Yellow

# Limpar credenciais do Git Credential Manager
cmdkey /list | ForEach-Object {
    if ($_ -match "git:https://github.com") {
        $line = $_.ToString()
        if ($line -match "target=(.+)") {
            $target = $matches[1]
            Write-Host "Removendo: $target" -ForegroundColor Gray
            cmdkey /delete:$target 2>$null
        }
    }
}

# Limpar credenciais do Windows Credential Manager
$creds = cmdkey /list | Select-String -Pattern "github"
if ($creds) {
    Write-Host "Credenciais encontradas. Removendo..." -ForegroundColor Yellow
    cmdkey /list | ForEach-Object {
        if ($_ -match "github") {
            $target = ($_ -split " ")[-1]
            cmdkey /delete:$target 2>$null
        }
    }
} else {
    Write-Host "Nenhuma credencial do GitHub encontrada." -ForegroundColor Green
}

Write-Host "`n✅ Credenciais limpas!" -ForegroundColor Green
Write-Host "`n📝 Agora execute:" -ForegroundColor Cyan
Write-Host "   cd `"C:\Users\notebook\Downloads\allianza-wallet1`"" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor White
Write-Host "`n💡 Quando pedir credenciais:" -ForegroundColor Yellow
Write-Host "   Username: brunosmaach-spec (ou seu username)" -ForegroundColor White
Write-Host "   Password: Seu Personal Access Token (NÃO sua senha normal!)" -ForegroundColor White

