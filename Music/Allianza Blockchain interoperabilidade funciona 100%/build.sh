#!/bin/bash
# Script de build para Render
# Instala bibliotecas Solana manualmente

set -e  # Parar em caso de erro

echo "🔧 Iniciando build customizado..."

# Atualizar pip
pip install --upgrade pip setuptools wheel

# Lista de dependências críticas que devem ser instaladas PRIMEIRO
CRITICAL_DEPS=(
    "cryptography==41.0.7"
    "base58==2.1.1"
    "flask==2.3.3"
    "python-dotenv==1.0.0"
    "requests==2.31.0"
    "gunicorn==21.2.0"
)

# Instalar dependências críticas individualmente
echo "🔐 Instalando dependências críticas..."
for dep in "${CRITICAL_DEPS[@]}"; do
    echo "📦 Instalando $dep..."
    pip install --no-cache-dir --upgrade "$dep" || {
        echo "⚠️  Erro ao instalar $dep, tentando sem versão específica..."
        dep_name=$(echo "$dep" | cut -d'=' -f1)
        pip install --no-cache-dir --upgrade "$dep_name" || {
            echo "❌ Erro crítico ao instalar $dep_name!"
            exit 1
        }
    }
    
    # Verificar se foi instalado
    dep_name=$(echo "$dep" | cut -d'=' -f1)
    python -c "import ${dep_name//-/_}; print('✅ $dep_name instalado')" || {
        echo "❌ $dep_name não foi instalado corretamente!"
        exit 1
    }
done

# Instalar outras dependências do requirements.txt
echo "📦 Instalando outras dependências do requirements.txt..."
pip install --no-cache-dir -r requirements.txt || {
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
echo "✅ Verificando instalação de dependências críticas..."
python -c "import cryptography; print('✅ cryptography:', cryptography.__version__)" || {
    echo "❌ cryptography não instalado!"
    exit 1
}
python -c "import base58; print('✅ base58 instalado')" || {
    echo "❌ base58 não instalado!"
    exit 1
}
python -c "import flask; print('✅ flask instalado')" || {
    echo "❌ flask não instalado!"
    exit 1
}
python -c "import dotenv; print('✅ python-dotenv instalado')" || {
    echo "❌ python-dotenv não instalado!"
    exit 1
}

# Verificar dependências opcionais
echo "✅ Verificando dependências opcionais..."
python -c "import solders; print('✅ solders instalado:', solders.__version__)" || echo "⚠️  solders não instalado (opcional)"
python -c "import solana; print('✅ solana instalado')" || echo "⚠️  solana não instalado (opcional)"

echo "✅ Build concluído com sucesso!"

