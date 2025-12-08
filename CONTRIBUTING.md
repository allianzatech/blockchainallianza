# Contribuindo para Allianza Blockchain

Obrigado por seu interesse em contribuir para o Allianza Blockchain! 🚀

Este documento fornece diretrizes para contribuir com o projeto. Seguir essas diretrizes ajuda a garantir que o processo seja suave para todos.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Configuração de Desenvolvimento](#configuração-de-desenvolvimento)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Templates de Issue](#templates-de-issue)
- [Templates de Pull Request](#templates-de-pull-request)
- [Bounties e Recompensas](#bounties-e-recompensas)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)

## 📜 Código de Conduta

Este projeto adere ao nosso [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, você concorda em manter este código.

## 🤝 Como Posso Contribuir?

### Reportar Bugs

Se você encontrou um bug:

1. **Verifique se já existe uma issue** sobre o problema
2. Se não existir, **crie uma nova issue** usando o [template de bug report](#template-de-bug-report)
3. Forneça o máximo de detalhes possível:
   - Passos para reproduzir
   - Comportamento esperado vs. comportamento atual
   - Screenshots/logs (se aplicável)
   - Ambiente (OS, versão Python/Node, etc.)

### Sugerir Melhorias

Tem uma ideia para melhorar o projeto?

1. **Verifique se já existe uma issue** sobre a sugestão
2. Se não existir, **crie uma nova issue** usando o [template de feature request](#template-de-feature-request)
3. Explique:
   - O problema que a feature resolve
   - Como você imagina que funcionaria
   - Possíveis alternativas consideradas

### Contribuir com Código

1. **Fork o repositório**
2. **Crie uma branch** para sua feature (`git checkout -b feature/minha-feature`)
3. **Faça suas alterações**
4. **Adicione testes** (se aplicável)
5. **Atualize a documentação** (se necessário)
6. **Commit suas mudanças** com mensagens claras
7. **Push para sua branch** (`git push origin feature/minha-feature`)
8. **Abra um Pull Request** usando o [template de PR](#template-de-pull-request)

### Melhorar Documentação

Documentação é crucial! Você pode ajudar:

- Corrigindo erros de digitação
- Melhorando explicações
- Adicionando exemplos
- Traduzindo para outros idiomas
- Adicionando screenshots/diagramas

### Responder Issues

Ajude outros contribuidores respondendo questões, testando PRs, ou fornecendo feedback construtivo.

## 🛠️ Configuração de Desenvolvimento

### Pré-requisitos

- Python 3.9+ (para backend)
- Node.js 18+ (para SDK TypeScript)
- Git
- PostgreSQL ou SQLite (para desenvolvimento local)

### Setup Inicial

```bash
# 1. Clone o repositório
git clone https://github.com/dieisonmaach-lang/allianzablockchain.git
cd allianzablockchain

# 2. Crie um ambiente virtual (Python)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale dependências Python
pip install -r requirements.txt

# 4. Instale dependências Node.js (para SDK)
cd qss-sdk
npm install
npm run build
cd ..

# 5. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 6. Inicialize o banco de dados
python -c "from db_manager import DBManager; DBManager().initialize_database()"

# 7. Execute os testes
python -m pytest tests/
```

### Testnet Local

Para testar o testnet localmente:

```bash
# Inicie o servidor
python allianza_blockchain.py

# Acesse:
# - Dashboard: http://localhost:5000
# - Faucet: http://localhost:5000/faucet
# - Explorer: http://localhost:5000/explorer
```

## 🔄 Processo de Desenvolvimento

### Workflow Git

1. **Sempre trabalhe em uma branch separada** (nunca diretamente em `main`)
2. **Mantenha sua branch atualizada** com `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout sua-branch
   git rebase main
   ```
3. **Commits atômicos**: Cada commit deve fazer uma coisa bem feita
4. **Mensagens de commit claras**: Use o formato convencional:
   ```
   tipo(escopo): descrição curta
   
   Descrição detalhada (se necessário)
   
   Fixes #123
   ```

### Tipos de Commit

- `feat`: Nova feature
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

### Exemplos

```
feat(faucet): adicionar rate limiting por IP
fix(explorer): corrigir busca de transações em múltiplos shards
docs(readme): adicionar instruções de instalação
refactor(sdk): modularizar WalletManager
```

## 📝 Templates de Issue

### Template de Bug Report

```markdown
**Descrição do Bug**
Uma descrição clara e concisa do bug.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

**Comportamento Esperado**
O que você esperava que acontecesse.

**Comportamento Atual**
O que realmente aconteceu.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [ex: Windows 10, Ubuntu 22.04]
- Python: [ex: 3.11.0]
- Node: [ex: 18.17.0]
- Versão do projeto: [ex: v1.0.0]

**Logs Adicionais**
Cole logs relevantes aqui.
```

### Template de Feature Request

```markdown
**A Feature Resolve um Problema?**
Uma descrição clara do problema. Ex: "Fico frustrado quando [...]"

**Solução Proposta**
Uma descrição clara da solução que você gostaria.

**Alternativas Consideradas**
Outras soluções ou features que você considerou.

**Contexto Adicional**
Qualquer outro contexto, screenshots, ou mockups sobre a feature.
```

## 🔀 Templates de Pull Request

### Template de PR

```markdown
## Descrição
Breve descrição das mudanças.

## Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (correção ou feature que quebra compatibilidade)
- [ ] Documentação

## Checklist
- [ ] Meu código segue os padrões do projeto
- [ ] Realizei uma auto-revisão do meu código
- [ ] Comentei código complexo
- [ ] Minhas mudanças não geram warnings
- [ ] Adicionei testes que provam que minha correção é efetiva
- [ ] Testes novos e existentes passam localmente
- [ ] Atualizei a documentação conforme necessário

## Como Testar
Passos para testar as mudanças:
1. ...
2. ...

## Screenshots (se aplicável)
Adicione screenshots aqui.

## Issues Relacionadas
Fixes #(número da issue)
```

## 💰 Bounties e Recompensas

### Bounties Ativos

Mantemos uma lista de bounties para incentivar contribuições. Consulte [Issues com label `bounty`](https://github.com/dieisonmaach-lang/allianzablockchain/issues?q=is%3Aissue+is%3Aopen+label%3Abounty).

### Como Participar

1. **Escolha um bounty** que você pode completar
2. **Comente na issue** dizendo que você vai trabalhar nele
3. **Crie uma branch** e trabalhe na solução
4. **Abra um PR** quando estiver pronto
5. **Após aprovação**, o bounty será pago

### Tipos de Bounties

- 🐛 **Bug Fixes**: $50 - $200
- ✨ **Features Pequenas**: $100 - $500
- 🚀 **Features Grandes**: $500 - $2000
- 📚 **Documentação**: $25 - $100
- 🎨 **UI/UX**: $100 - $500
- 🔒 **Segurança**: $500 - $5000

*Valores são estimativas e podem variar.*

## 📐 Padrões de Código

### Python

- **PEP 8**: Siga o guia de estilo Python
- **Type Hints**: Use type hints sempre que possível
- **Docstrings**: Documente todas as funções e classes (Google style)
- **Linha máxima**: 100 caracteres
- **Imports**: Organize imports (stdlib, third-party, local)

```python
from typing import Dict, List, Optional
import os
from datetime import datetime

from flask import Flask
from db_manager import DBManager

def minha_funcao(param1: str, param2: int) -> Optional[Dict]:
    """
    Descrição curta da função.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2
    
    Returns:
        Dicionário com resultado ou None
    
    Raises:
        ValueError: Se param1 estiver vazio
    """
    if not param1:
        raise ValueError("param1 não pode estar vazio")
    return {"result": "ok"}
```

### TypeScript

- **ESLint**: Siga as regras configuradas
- **TypeScript Strict**: Use tipos explícitos (evite `any`)
- **JSDoc**: Documente funções públicas
- **Prettier**: Formatação automática

```typescript
/**
 * Gera uma prova quântica para uma transação
 * @param transaction - Dados da transação
 * @param options - Opções de geração
 * @returns Promise com a prova gerada
 */
async function generateProof(
  transaction: Transaction,
  options?: ProofOptions
): Promise<QuantumProof> {
  // Implementação
}
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python -m pytest

# Testes específicos
python -m pytest tests/test_faucet.py

# Com cobertura
python -m pytest --cov=. --cov-report=html

# Testes TypeScript
cd qss-sdk
npm test
```

### Escrever Testes

- **Cobertura mínima**: 80% para código novo
- **Testes unitários**: Para funções individuais
- **Testes de integração**: Para fluxos completos
- **Testes E2E**: Para funcionalidades críticas

```python
import pytest
from testnet_faucet import TestnetFaucet

def test_faucet_request_success():
    """Testa requisição bem-sucedida do faucet"""
    faucet = TestnetFaucet(blockchain, quantum_security)
    result = faucet.request_tokens("ALZ1Test...", mock_request)
    assert result["success"] is True
    assert "tx_hash" in result
```

## 📚 Documentação

### Atualizar Documentação

- **README.md**: Para mudanças significativas
- **Docstrings**: Sempre que adicionar/modificar funções
- **CHANGELOG.md**: Para releases
- **Wiki**: Para guias detalhados

### Formato de Docstrings (Python)

```python
def criar_transacao(sender: str, receiver: str, amount: float) -> Dict:
    """
    Cria uma nova transação na blockchain.
    
    Esta função valida os parâmetros, cria a transação e a adiciona
    à pool de transações pendentes.
    
    Args:
        sender: Endereço do remetente (formato ALZ1...)
        receiver: Endereço do destinatário (formato ALZ1...)
        amount: Quantidade de ALZ a transferir (deve ser > 0)
    
    Returns:
        Dicionário contendo:
            - success (bool): True se bem-sucedido
            - tx_hash (str): Hash da transação criada
            - error (str, opcional): Mensagem de erro se falhou
    
    Raises:
        ValueError: Se sender ou receiver forem inválidos
        InsufficientBalanceError: Se sender não tiver saldo suficiente
    
    Example:
        >>> result = criar_transacao("ALZ1Sender...", "ALZ1Receiver...", 100.0)
        >>> print(result["tx_hash"])
        "abc123..."
    """
    pass
```

## 🚀 Processo de Review

### Para Revisores

- Seja construtivo e respeitoso
- Foque no código, não na pessoa
- Explique o "porquê" das sugestões
- Aprove PRs que estão prontos

### Para Autores de PR

- Responda a todos os comentários
- Faça as mudanças solicitadas ou explique por que não
- Mantenha o PR focado (uma feature por PR)
- Atualize o PR conforme necessário

## 📞 Contato

- **Issues**: Use GitHub Issues para bugs e features
- **Discord**: [Link do servidor] (se houver)
- **Email**: [Email de contato] (se houver)

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).

---

**Obrigado por contribuir para o Allianza Blockchain! 🎉**

