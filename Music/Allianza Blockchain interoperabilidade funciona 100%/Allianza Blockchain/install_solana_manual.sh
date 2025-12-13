#!/bin/bash
# Script para instalar bibliotecas Solana manualmente no Render
# Execute este script via SSH ou shell do Render

echo "🔧 Instalando bibliotecas Solana manualmente..."

# Atualizar pip
pip install --upgrade pip setuptools wheel

# Opção 1: Tentar instalar diretamente
echo "📦 Tentativa 1: Instalação direta..."
pip install solders>=0.18.0 solana>=0.30.2

# Verificar instalação
python -c "import solders; print('✅ solders:', solders.__version__)" 2>/dev/null || echo "❌ solders não instalado"
python -c "import solana; print('✅ solana instalado')" 2>/dev/null || echo "❌ solana não instalado"

# Se falhar, tentar com opções alternativas
if ! python -c "import solders" 2>/dev/null; then
    echo "📦 Tentativa 2: Instalação com --no-cache-dir..."
    pip install --no-cache-dir solders>=0.18.0
    
    echo "📦 Tentativa 3: Instalação com --no-binary (forçar compilação)..."
    pip install --no-binary :all: solders>=0.18.0 || echo "⚠️  Compilação falhou"
fi

echo "✅ Instalação concluída!"

