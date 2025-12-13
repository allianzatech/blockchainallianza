#!/bin/bash
# Script de build para Render
# Instala bibliotecas Solana manualmente

set -e  # Parar em caso de erro

echo "🔧 Iniciando build customizado..."

# Atualizar pip
pip install --upgrade pip setuptools wheel

# Instalar dependências do sistema (se necessário)
# Algumas bibliotecas Rust podem precisar de ferramentas de build
echo "📦 Instalando dependências base..."

# Tentar instalar solders primeiro (pode precisar de Rust)
echo "🔨 Tentando instalar solders..."
pip install solders>=0.18.0 || {
    echo "⚠️  Instalação direta de solders falhou, tentando com build tools..."
    # Se falhar, tentar com versão específica ou pré-compilada
    pip install --no-cache-dir solders>=0.18.0 || {
        echo "❌ Erro ao instalar solders. Continuando com outras dependências..."
    }
}

# Instalar solana (depende de solders)
echo "🔨 Instalando solana..."
pip install solana>=0.30.2 || {
    echo "⚠️  Erro ao instalar solana. Continuando..."
}

# Instalar outras dependências
echo "📦 Instalando outras dependências do requirements.txt..."
pip install -r requirements.txt

# Garantir que cryptography está instalado (pode precisar de dependências de sistema)
echo "🔐 Instalando cryptography..."
pip install cryptography==41.0.7 || pip install cryptography

# Verificar se as bibliotecas foram instaladas
echo "✅ Verificando instalação..."
python -c "import solders; print('✅ solders instalado:', solders.__version__)" || echo "❌ solders não instalado"
python -c "import solana; print('✅ solana instalado')" || echo "❌ solana não instalado"

echo "✅ Build concluído!"

