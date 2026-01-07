# 🚫 Arquivos Excluídos do Repositório Público

Este documento lista **todos os arquivos e diretórios que NÃO devem estar** no repositório público. Esses arquivos são de produção/comerciais e ficam apenas no repositório privado.

## ⚠️ Importante

**O repositório público é para:**
- ✅ Código do protocolo (open core)
- ✅ Documentação técnica
- ✅ Provas verificáveis
- ✅ Exemplos de código
- ✅ Guias de auditoria

**O repositório privado contém:**
- ❌ Sistema completo de produção
- ❌ Testnet funcional
- ❌ Código comercial
- ❌ Infraestrutura de deploy
- ❌ Configurações de produção

---

## 📋 Lista de Exclusões

### 1. Arquivos de Produção/Comerciais

#### Bridge e Código Comercial
- ❌ `real_cross_chain_bridge.py` - Bridge de produção
- ❌ `allianza_bridge_config.py` - Configuração comercial
- ❌ `db_manager.py` - Gerenciador de banco comercial
- ❌ `bridge_free_interop.py` (versão da raiz) - Versão comercial

#### Diretório Comercial
- ❌ `commercial_repo/` - **TODO o diretório**
  - `commercial_repo/adapters/` - Adaptadores comerciais
  - `commercial_repo/contracts/` - Contratos comerciais
  - `commercial_repo/production/` - Código de produção

#### Diretório de Deploy
- ❌ `deploy/` - **TODO o diretório**
  - Contém toda a infraestrutura de produção
  - Arquivos de deploy e configuração
  - Código de produção

### 2. Arquivos da Testnet

#### Arquivos testnet_*.py
- ❌ `testnet_routes.py`
- ❌ `testnet_explorer.py`
- ❌ `testnet_explorer_enhanced.py`
- ❌ `testnet_interoperability.py`
- ❌ `testnet_faucet.py`
- ❌ `testnet_config.py`
- ❌ `testnet_status.py`
- ❌ `testnet_wallet_generator.py`
- ❌ `testnet_proofs.py`
- ❌ `testnet_professional_proofs.py`
- ❌ `testnet_professional_tests.py`
- ❌ `testnet_professional_test_suite.py`
- ❌ `testnet_public_tests_interface.py`
- ❌ `testnet_quantum_dashboard.py`
- ❌ `testnet_qrs3_demo.py`
- ❌ `testnet_leaderboard.py`
- ❌ `testnet_auto_transaction_generator.py`
- ❌ `testnet_stress_test.py`
- ❌ `testnet_real_transfer_helper.py`

**Nota:** A testnet roda no repositório privado. O repositório público tem apenas as **provas** de que a testnet funciona.

### 3. Arquivos de Infraestrutura/Deploy

#### Arquivos de Deploy
- ❌ `wsgi.py` - WSGI para produção
- ❌ `wsgi_optimized.py` - WSGI otimizado
- ❌ `gunicorn_config.py` - Configuração Gunicorn
- ❌ `Procfile` - Configuração Heroku/Render
- ❌ `render.yaml` - Configuração Render
- ❌ `docker-compose.yml` - Docker Compose
- ❌ `Dockerfile` - Dockerfile
- ❌ `runtime.txt` - Runtime Python
- ❌ `.htaccess` - Configuração Apache
- ❌ `start_server.sh` - Script de inicialização
- ❌ `nginx_*.conf` - Configurações Nginx

### 4. Arquivos de Banco de Dados

#### Bancos de Dados
- ❌ `*.db` - Arquivos SQLite
- ❌ `*.sqlite` - Arquivos SQLite
- ❌ `*.sqlite3` - Arquivos SQLite
- ❌ `allianza_blockchain.db` - Banco principal
- ❌ `allianza_blockchain_*.db` - Bancos de backup

### 5. Arquivos de Logs

#### Logs de Produção
- ❌ `*.log` - Arquivos de log
- ❌ `logs/` - Diretório de logs
- ❌ `allianza_blockchain*.log` - Logs do sistema

### 6. Arquivos de Segurança/Secrets

#### Secrets e Chaves
- ❌ `secrets/` - Diretório de secrets
- ❌ `*.key` - Arquivos de chave
- ❌ `*.pem` - Certificados PEM
- ❌ `*.p12` - Certificados P12
- ❌ `*.pfx` - Certificados PFX
- ❌ `.env` - Variáveis de ambiente
- ❌ `.env.production` - Variáveis de produção
- ❌ `.env.local` - Variáveis locais
- ❌ `*.secret` - Arquivos secretos
- ❌ `exposed_keys_report.json` - Relatório de chaves

### 7. Arquivos de Dados de Produção

#### Dados de Produção
- ❌ `data/` - Diretório de dados (exceto .gitkeep)
- ❌ `faucet_last_requests.json` - Dados do faucet
- ❌ `pending_commitments.json` - Commitments pendentes
- ❌ `commitment_metrics.json` - Métricas de commitment

### 8. Arquivos Temporários/Cache

#### Cache e Temporários
- ❌ `__pycache__/` - Cache Python
- ❌ `*.pyc` - Bytecode Python
- ❌ `*.pyo` - Bytecode otimizado
- ❌ `*.pyd` - Extensões Python
- ❌ `*.so` - Bibliotecas compartilhadas
- ❌ `.Python` - Python cache

---

## ✅ O que DEVE estar no Repositório Público

### Código do Protocolo
- ✅ `core/` - Protocolo core completo
- ✅ Arquivos principais do protocolo (se na raiz)
- ✅ `contracts/` - Contratos inteligentes (open core)

### Documentação
- ✅ `README.md` - README principal
- ✅ `LICENSE` - Licença MIT
- ✅ `CONTRIBUTING.md` - Guia de contribuição
- ✅ `SECURITY.md` - Política de segurança
- ✅ `ROADMAP.md` - Roadmap
- ✅ `docs/` - Documentação técnica
- ✅ Todos os arquivos `.md` de documentação

### Provas Verificáveis
- ✅ `proofs/` - Provas verificáveis
  - ✅ `proofs/testnet/` - Provas da testnet
  - ✅ `proofs/interoperability_real/` - Provas reais
  - ✅ `proofs/testnet/professional/` - Provas profissionais

### Exemplos e Ferramentas
- ✅ `examples/` - Exemplos de código (se existir)
- ✅ `cli/` - Ferramentas CLI
- ✅ `api/` - Exemplos de API
- ✅ `scripts/` - Scripts utilitários (não comerciais)
- ✅ `qss-sdk/` - SDK Quantum-Safe

### Configuração
- ✅ `requirements.txt` - Dependências Python
- ✅ `.gitignore` - Arquivo de exclusões
- ✅ Arquivos de configuração não-sensíveis

---

## 🔍 Como Verificar

### Antes de Fazer Push

1. **Verificar .gitignore**
   ```bash
   git status
   # Verificar se arquivos comerciais não aparecem
   ```

2. **Usar Scripts de Verificação**
   ```bash
   python verificar_e_remover_deploy_publico.py
   python remover_arquivos_testnet_publico.py
   ```

3. **Verificar Manualmente**
   - Confirmar que `commercial_repo/` não está
   - Confirmar que `deploy/` não está
   - Confirmar que `testnet_*.py` não estão
   - Confirmar que arquivos de deploy não estão

### Checklist Pré-Push

- [ ] `commercial_repo/` não está no commit
- [ ] `deploy/` não está no commit
- [ ] Nenhum arquivo `testnet_*.py` está no commit
- [ ] Nenhum arquivo de deploy está no commit
- [ ] Nenhum arquivo `.db` está no commit
- [ ] Nenhum arquivo `.log` está no commit
- [ ] Nenhum arquivo de secrets está no commit
- [ ] `.gitignore` está atualizado

---

## 📝 Notas Importantes

### Por que Excluir?

1. **Segurança** - Secrets e chaves não devem ser públicos
2. **Estratégia** - Open core vs. comercial
3. **Proteção** - Infraestrutura de produção protegida
4. **Clareza** - Repositório público focado em protocolo

### O que Fazer se Acidentalmente Incluído?

1. **Remover do Git**
   ```bash
   git rm --cached arquivo_comercial.py
   git commit -m "Remove: arquivo comercial do público"
   ```

2. **Atualizar .gitignore**
   - Adicionar padrão ao .gitignore
   - Commit da atualização

3. **Verificar Histórico**
   - Arquivos no histórico Git ainda estão acessíveis
   - Considerar limpar histórico se necessário

---

## 🔄 Manutenção

Este documento deve ser atualizado quando:
- Novos arquivos comerciais são criados
- Novos diretórios de produção são adicionados
- Estrutura do projeto muda

---

**Este documento garante que o repositório público contenha apenas o necessário para auditoria e demonstração da tecnologia.**

