# 🔒 Relatório de Vulnerabilidades em Dependências

**Data:** 2025-12-20  
**Ferramenta:** pip-audit 2.10.0  
**Status:** ⚠️ **12 VULNERABILIDADES ENCONTRADAS**

---

## 📊 Resumo

- **Total de vulnerabilidades:** 12
- **Pacotes afetados:** 6
- **Pacotes não auditáveis:** 1 (liboqs-python - não está no PyPI)

---

## 🔴 Vulnerabilidades Encontradas

### 1. **ecdsa** (0.19.1)
- **CVE:** CVE-2024-23342
- **Status:** ⚠️ Vulnerável
- **Ação:** Atualizar para versão mais recente
- **Impacto:** Biblioteca usada para assinaturas criptográficas

### 2. **flask-cors** (4.0.0) - **5 VULNERABILIDADES**
- **CVE/PYSEC:**
  - PYSEC-2024-71 → Atualizar para 4.0.2
  - CVE-2024-1681 → Atualizar para 4.0.1
  - CVE-2024-6844 → Atualizar para 6.0.0
  - CVE-2024-6866 → Atualizar para 6.0.0
  - CVE-2024-6839 → Atualizar para 6.0.0
- **Status:** ⚠️ **CRÍTICO** - Múltiplas vulnerabilidades
- **Ação Recomendada:** Atualizar para 6.0.0 (versão mais recente)
- **Impacto:** CORS pode ser explorado para ataques cross-origin

### 3. **gunicorn** (21.2.0) - **2 VULNERABILIDADES**
- **CVE:**
  - CVE-2024-1135 → Atualizar para 22.0.0
  - CVE-2024-6827 → Atualizar para 22.0.0
- **Status:** ⚠️ Vulnerável
- **Ação Recomendada:** Atualizar para 22.0.0
- **Impacto:** Servidor WSGI pode ter vulnerabilidades de segurança

### 4. **python-socketio** (5.10.0)
- **CVE:** CVE-2025-61765
- **Status:** ⚠️ Vulnerável
- **Ação:** Atualizar para 5.14.0
- **Impacto:** Comunicação WebSocket pode ser comprometida

### 5. **urllib3** (2.5.0) - **2 VULNERABILIDADES**
- **CVE:**
  - CVE-2025-66418 → Atualizar para 2.6.0
  - CVE-2025-66471 → Atualizar para 2.6.0
- **Status:** ⚠️ Vulnerável
- **Ação Recomendada:** Atualizar para 2.6.0
- **Impacto:** Biblioteca HTTP pode ter vulnerabilidades

### 6. **werkzeug** (3.1.3)
- **CVE:** CVE-2025-66221
- **Status:** ⚠️ Vulnerável
- **Ação:** Atualizar para 3.1.4
- **Impacto:** Framework WSGI do Flask pode ter vulnerabilidades

---

## ⚠️ Pacotes Não Auditáveis

### **liboqs-python** (0.14.0)
- **Motivo:** Não está disponível no PyPI
- **Status:** ⚠️ Não pode ser auditado automaticamente
- **Ação:** Verificar manualmente no repositório do projeto
- **Nota:** Este é um pacote especializado para criptografia quântica

---

## 🔧 Correções Recomendadas

### Atualizações Prioritárias (Críticas)

1. **flask-cors** → **6.0.0** (5 vulnerabilidades)
   ```bash
   pip install --upgrade flask-cors==6.0.0
   ```

2. **gunicorn** → **22.0.0** (2 vulnerabilidades)
   ```bash
   pip install --upgrade gunicorn==22.0.0
   ```

3. **urllib3** → **2.6.0** (2 vulnerabilidades)
   ```bash
   pip install --upgrade urllib3==2.6.0
   ```

### Atualizações Importantes

4. **python-socketio** → **5.14.0**
   ```bash
   pip install --upgrade python-socketio==5.14.0
   ```

5. **werkzeug** → **3.1.4**
   ```bash
   pip install --upgrade werkzeug==3.1.4
   ```

6. **ecdsa** → **Versão mais recente**
   ```bash
   pip install --upgrade ecdsa
   ```

---

## 📋 Plano de Ação

### Fase 1: Atualizações Críticas (Imediato)
1. ✅ Atualizar `flask-cors` para 6.0.0
2. ✅ Atualizar `gunicorn` para 22.0.0
3. ✅ Atualizar `urllib3` para 2.6.0

### Fase 2: Atualizações Importantes (Curto Prazo)
4. ✅ Atualizar `python-socketio` para 5.14.0
5. ✅ Atualizar `werkzeug` para 3.1.4
6. ✅ Atualizar `ecdsa` para versão mais recente

### Fase 3: Verificação (Após Atualizações)
7. ✅ Executar `pip-audit` novamente para confirmar correções
8. ✅ Testar aplicação para garantir compatibilidade
9. ✅ Atualizar `requirements.txt` com novas versões

---

## ⚠️ Notas Importantes

1. **Testes Necessários:** Após atualizar, testar todas as funcionalidades críticas
2. **Compatibilidade:** Verificar se as novas versões são compatíveis com Python 3.13
3. **Breaking Changes:** `flask-cors` 6.0.0 pode ter breaking changes - revisar documentação
4. **liboqs-python:** Verificar manualmente no repositório oficial

---

## 🔄 Verificação Contínua

Execute regularmente:
```bash
python scripts/check_dependencies_security.py
```

Ou diretamente:
```bash
pip-audit
```

---

## 📚 Referências

- [pip-audit Documentation](https://pypi.org/project/pip-audit/)
- [CVE Database](https://cve.mitre.org/)
- [PyPI Security Advisories](https://pypi.org/security/)

---

**Próxima Verificação Recomendada:** Após aplicar todas as atualizações

