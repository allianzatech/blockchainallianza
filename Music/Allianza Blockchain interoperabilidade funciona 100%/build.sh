#!/bin/bash
# Script de build para Render
# Instala bibliotecas Solana manualmente

set -e  # Parar em caso de erro

echo "🔧 Iniciando build customizado..."

# Atualizar pip
pip install --upgrade pip setuptools wheel

# Instalar cryptography PRIMEIRO (é crítico e pode precisar de dependências de sistema)
echo "🔐 Instalando cryptography (crítico)..."
pip install --upgrade cryptography==41.0.7 || {
    echo "⚠️  Tentando instalar cryptography sem versão específica..."
    pip install --upgrade cryptography || {
        echo "❌ Erro crítico ao instalar cryptography!"
        exit 1
    }
}

# Verificar se cryptography foi instalado
python -c "import cryptography; print('✅ cryptography instalado:', cryptography.__version__)" || {
    echo "❌ cryptography não foi instalado corretamente!"
    exit 1
}

# Instalar dependências do sistema (se necessário)
# Algumas bibliotecas Rust podem precisar de ferramentas de build
echo "📦 Instalando dependências base..."

# Instalar outras dependências do requirements.txt (cryptography já está instalado)
echo "📦 Instalando outras dependências do requirements.txt..."
pip install -r requirements.txt || {
    echo "⚠️  Algumas dependências falharam, mas continuando..."
}

# Tentar instalar solders (pode precisar de Rust)
echo "🔨 Tentando instalar solders..."
pip install --upgrade solders>=0.18.0 || {
    echo "⚠️  Instalação direta de solders falhou, tentando com build tools..."
    pip install --no-cache-dir solders>=0.18.0 || {
        echo "❌ Erro ao instalar solders. Continuando com outras dependências..."
    }
}

# Instalar solana (depende de solders)
echo "🔨 Instalando solana..."
pip install --upgrade solana>=0.30.2 || {
    echo "⚠️  Erro ao instalar solana. Continuando..."
}

# Verificar se as bibliotecas críticas foram instaladas
echo "✅ Verificando instalação..."
python -c "import cryptography; print('✅ cryptography:', cryptography.__version__)" || {
    echo "❌ cryptography não instalado!"
    exit 1
}
python -c "import flask; print('✅ flask instalado')" || echo "❌ flask não instalado"
python -c "import solders; print('✅ solders instalado:', solders.__version__)" || echo "⚠️  solders não instalado (opcional)"
python -c "import solana; print('✅ solana instalado')" || echo "⚠️  solana não instalado (opcional)"

echo "✅ Build concluído!"

