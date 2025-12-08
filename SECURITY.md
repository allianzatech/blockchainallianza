# 🔐 Política de Segurança - Allianza Blockchain

## 🛡️ Reportar Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança, **NÃO** abra uma issue pública. Em vez disso:

1. **Envie um email** para: security@allianza.tech
2. **Ou use** o GitHub Security Advisory: https://github.com/dieisonmaach-lang/allianzablockchain/security/advisories/new

### O que incluir no relatório:

- Descrição detalhada da vulnerabilidade
- Passos para reproduzir
- Impacto potencial
- Sugestões de correção (se houver)

### Processo de Resposta:

- **Acknowledgment**: Dentro de 48 horas
- **Status Update**: Semanal até resolução
- **Fix Timeline**: Baseado na severidade

## 🔒 Proteção de Segredos

### ⚠️ NUNCA Commitar:

- ❌ Chaves privadas (`.key`, `.pem`, `.wif`)
- ❌ Seeds de wallets
- ❌ Tokens de API
- ❌ Credenciais de banco de dados
- ❌ Senhas ou secrets
- ❌ Arquivos `.env` com valores reais

### ✅ O que está protegido:

O arquivo `.gitignore` protege automaticamente:
- Arquivos `.env`
- Diretório `secrets/`
- Chaves privadas (`*.key`, `*.pem`, `*.wif`)
- Credenciais (`*_token*`, `*_password*`, `*_secret*`)

### 🔍 Verificar antes de commitar:

```bash
# Verificar se há segredos no código
git diff --cached | grep -iE "password|secret|key|token|private"

# Verificar arquivos que serão commitados
git status
```

## 🔐 Boas Práticas de Segurança

### 1. Gerenciamento de Chaves

**✅ FAZER:**
- Usar variáveis de ambiente para secrets
- Armazenar chaves privadas em `secrets/` (não versionado)
- Usar criptografia para chaves em repouso
- Rotacionar chaves regularmente

**❌ NÃO FAZER:**
- Hardcodar secrets no código
- Commitar arquivos `.env` com valores reais
- Compartilhar chaves privadas
- Usar a mesma chave em múltiplos ambientes

### 2. Desenvolvimento

**✅ FAZER:**
- Usar testnet para testes
- Validar todas as entradas
- Usar HTTPS em produção
- Implementar rate limiting

**❌ NÃO FAZER:**
- Usar chaves de produção em desenvolvimento
- Expor APIs sem autenticação
- Ignorar validação de entrada
- Logar informações sensíveis

### 3. Deploy

**✅ FAZER:**
- Usar variáveis de ambiente no deploy
- Habilitar HTTPS/TLS
- Configurar firewall adequadamente
- Monitorar logs de segurança

**❌ NÃO FAZER:**
- Expor portas desnecessárias
- Usar credenciais padrão
- Ignorar atualizações de segurança
- Desabilitar logs de segurança

## 🔍 Auditoria de Segurança

### Verificação Regular

Execute regularmente:

```bash
# Verificar se há segredos no código
grep -r "PRIVATE_KEY\|SECRET\|PASSWORD" --exclude-dir=.git --exclude="*.md"

# Verificar dependências vulneráveis
pip install safety
safety check

# Verificar configuração de segurança
python -m security_audit
```

### Checklist de Segurança

Antes de cada release:

- [ ] Verificar que não há secrets no código
- [ ] Atualizar dependências vulneráveis
- [ ] Revisar permissões de arquivos
- [ ] Testar em ambiente isolado
- [ ] Validar configurações de segurança

## 🚨 Incidentes de Segurança

### Se uma chave privada foi exposta:

1. **Imediatamente**: Revogue a chave exposta
2. **Rotacione**: Gere novas chaves
3. **Notifique**: Usuários afetados (se aplicável)
4. **Documente**: O incidente e ações tomadas

### Se há um comprometimento:

1. **Isolar**: Sistema comprometido
2. **Investigar**: Escopo do comprometimento
3. **Corrigir**: Vulnerabilidade explorada
4. **Comunicar**: Stakeholders afetados

## 📋 Classificação de Vulnerabilidades

### Crítica (P0)
- Exposição de chaves privadas
- Bypass de autenticação
- Execução remota de código

**Resposta**: < 24 horas

### Alta (P1)
- Acesso não autorizado
- Manipulação de dados
- Denial of Service

**Resposta**: < 7 dias

### Média (P2)
- Exposição de informações
- Vulnerabilidades de validação
- Rate limiting inadequado

**Resposta**: < 30 dias

### Baixa (P3)
- Melhorias de segurança
- Informações de debug
- Configurações não ideais

**Resposta**: Próximo release

## 🔗 Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 📧 Contato

- **Security Email**: security@allianza.tech
- **GitHub Security**: https://github.com/dieisonmaach-lang/allianzablockchain/security

---

**Última atualização**: 2025-12-07

