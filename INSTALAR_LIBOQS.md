# 🔐 Como Instalar liboqs-python (Implementação REAL)

## 📋 Por que está "Simulado"?

O sistema mostra "⚠️ Simulado" porque a biblioteca `liboqs-python` não está instalada. O sistema funciona com simulação funcional, mas para máxima segurança quântica, você precisa instalar a biblioteca real.

---

## ✅ Instalação do liboqs-python

### **Opção 1: Instalação Direta (Recomendado)**

```bash
pip install liboqs-python
```

### **Opção 2: Se a instalação direta falhar**

Algumas plataformas (especialmente Windows) podem ter problemas. Use:

```bash
# Windows (com Visual Studio Build Tools)
pip install --upgrade pip
pip install cmake
pip install liboqs-python

# Linux/Mac
pip install --upgrade pip
pip install liboqs-python
```

### **Opção 3: Instalação via Conda**

```bash
conda install -c conda-forge liboqs-python
```

---

## 🔍 Verificar Instalação

Após instalar, reinicie o servidor e verifique os logs:

```
✅ liboqs-python carregado - Implementação PQC REAL!
🔐 QUANTUM SECURITY SYSTEM REAL: Inicializado!
✅ ML-DSA (Dilithium) - Implementação REAL
✅ ML-KEM (Kyber) - Implementação REAL
✅ SPHINCS+ - Implementação REAL
```

Se aparecer isso, está funcionando! ✅

---

## ⚠️ Problemas Comuns

### **Erro: "Microsoft Visual C++ 14.0 is required"**

**Solução:**
1. Instale [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
2. Selecione "C++ build tools"
3. Tente instalar novamente: `pip install liboqs-python`

### **Erro: "cmake not found"**

**Solução:**
```bash
pip install cmake
# Ou no Windows:
# Baixe de: https://cmake.org/download/
```

### **Erro: "liboqs library not found"**

**Solução:**
```bash
# Linux
sudo apt-get install liboqs-dev

# Mac
brew install liboqs

# Depois tente:
pip install liboqs-python
```

---

## 📊 Diferença: Simulado vs Real

| Característica | Simulado | Real (liboqs-python) |
|----------------|----------|----------------------|
| Segurança | ✅ Funcional | ✅✅✅ Máxima |
| Algoritmos PQC | Simulados | ✅ ML-DSA, ML-KEM, SPHINCS+ reais |
| Performance | Rápido | Otimizado |
| Auditoria | ⚠️ Não auditável | ✅ Auditável (NIST) |
| Produção | ⚠️ Não recomendado | ✅ Recomendado |

---

## 🚀 Após Instalação

1. **Reinicie o servidor**
2. **Acesse:** `https://testnet.allianza.tech/qss/status`
3. **Verifique:** Deve mostrar "✅ Disponível" ao invés de "⚠️ Simulado"

---

## 💡 Nota

- O sistema funciona perfeitamente em modo simulado para desenvolvimento/testnet
- Para produção, recomenda-se instalar `liboqs-python` para máxima segurança
- A simulação é funcional e segura, mas não usa algoritmos PQC reais auditados

