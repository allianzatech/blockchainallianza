# 📁 Organização do Projeto Allianza Blockchain

## ✅ Limpeza Realizada

Foram excluídos **104 arquivos desnecessários**, incluindo:

### 🗑️ Arquivos Removidos

1. **Documentação Redundante sobre GitHub/Push/Topics** (14 arquivos)
   - Guias de push, topics, sincronização que já foram implementados

2. **Documentação Redundante sobre Deploy/Render** (30 arquivos)
   - Múltiplos guias de deploy que já foram concluídos
   - Documentação sobre configuração do Render que já está funcionando

3. **Scripts .bat Temporários** (13 arquivos)
   - Scripts de compilação duplicados
   - Scripts de instalação que já foram executados

4. **Arquivos Temporários/Logs** (12 arquivos)
   - Logs, bancos de dados temporários, arquivos ZIP

5. **Documentação Duplicada** (20 arquivos)
   - Múltiplos resumos de melhorias
   - Relatórios duplicados

6. **Scripts Python Temporários** (9 arquivos)
   - Utilitários de atualização que já foram executados

## 📂 Estrutura Organizada

### Diretórios Principais

```
Allianza Blockchain/
├── cli/                    # CLI tools
├── contracts/              # Smart contracts
├── data/                   # Dados estáticos
├── deploy/                 # Scripts de deploy
├── docs/                   # Documentação técnica
├── proofs/                 # Provas técnicas
├── qss-sdk/                # SDK do QSS
├── qss-canonicalizer/      # Canonicalizer
├── qss-verifier/           # Verificador
├── scripts/                # Scripts utilitários
├── sdk/                    # SDK principal
├── templates/              # Templates HTML
└── tests/                  # Testes (se existir)
```

### Arquivos Principais na Raiz

- `allianza_blockchain.py` - Core da blockchain
- `real_cross_chain_bridge.py` - Bridge cross-chain
- `qss_api_service.py` - API do QSS
- `testnet_routes.py` - Rotas da testnet
- `sincronizar_repositorio_publico.py` - Sincronização com repo público
- `traduzir_e_sincronizar.py` - Tradução e sincronização
- `revisar_tudo_publico_completo.py` - Revisão completa do repo público

### Documentação Essencial Mantida

- `WHITEPAPER_ALLIANZA_BLOCKCHAIN.md` - Whitepaper principal
- `CODE_OF_CONDUCT.md` - Código de conduta
- `ESTRATEGIA_DOIS_REPOSITORIOS.md` - Estratégia de repositórios
- `GUIA_SINCRONIZACAO_AUTOMATICA.md` - Guia de sincronização
- `INSTALAR_LIBOQS.md` - Instruções de instalação
- `OTIMIZAR_TESTNET_PERFORMANCE.md` - Otimizações
- Documentação INPI (patentes)
- Documentação técnica em `docs/`

## 🧪 Arquivos de Teste

Arquivos de teste temporários estão sendo ignorados pelo `.gitignore`:
- `TESTE_*.py`
- `teste_*.py`
- `*_teste.py`
- `testar_*.py`

Os testes principais devem estar em `scripts/` ou em uma pasta `tests/` dedicada.

## 📝 Próximos Passos Recomendados

1. **Organizar Testes**: Mover testes importantes para `tests/` ou `scripts/tests/`
2. **Consolidar Documentação**: Manter apenas a documentação mais atual
3. **Revisar Scripts**: Manter apenas scripts essenciais na raiz
4. **Atualizar README**: Refletir a nova estrutura organizada

## 🔒 Arquivos Protegidos pelo .gitignore

- Logs (`*.log`)
- Bancos de dados (`*.db`, `*.sqlite`)
- Arquivos ZIP (`*.zip`)
- Cache Python (`__pycache__/`)
- Node modules (`node_modules/`)
- Arquivos temporários (`*.tmp`, `*.temp`, `*.bak`)
- Arquivos de teste temporários (`TESTE_*.py`, etc.)

## 📊 Estatísticas

- **Arquivos excluídos**: 104
- **Espaço liberado**: Aproximadamente (depende do tamanho dos arquivos)
- **Organização**: Estrutura mais limpa e profissional

