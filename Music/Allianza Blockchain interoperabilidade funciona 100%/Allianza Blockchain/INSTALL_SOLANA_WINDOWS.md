# Guia de Instalação das Bibliotecas Solana no Windows

## Problema Conhecido
A biblioteca `solders` é escrita em Rust e precisa ser compilada. Python 3.13 é muito recente e pode não ter wheels pré-compilados.

## Soluções

### Solução 1: Instalar com compilação (pode demorar)
```bash
pip install --upgrade pip setuptools wheel
pip install solders>=0.18.0 --no-binary :all:
pip install solana>=0.30.2
```

**Nota:** Isso requer que você tenha o Rust compiler instalado. Se não tiver:
1. Instale Rust: https://rustup.rs/
2. Ou use a Solução 2

### Solução 2: Usar Python 3.11 ou 3.12 (Recomendado)
Python 3.11 e 3.12 têm wheels pré-compilados disponíveis:

```bash
# Se usar pyenv ou similar
pyenv install 3.12.0
pyenv local 3.12.0

# Ou baixe Python 3.12 do site oficial
# https://www.python.org/downloads/

# Depois instale as bibliotecas
pip install --upgrade pip setuptools wheel
pip install solders>=0.18.0 solana>=0.30.2
```

### Solução 3: Instalar Rust e compilar
1. Baixe e instale Rust: https://rustup.rs/
2. Reinicie o terminal
3. Execute:
```bash
pip install solders>=0.18.0 solana>=0.30.2
```

### Solução 4: Usar ambiente virtual com Python 3.12
```bash
# Criar ambiente virtual com Python 3.12 (se disponível)
python3.12 -m venv venv_solana
venv_solana\Scripts\activate  # Windows
pip install --upgrade pip setuptools wheel
pip install solders>=0.18.0 solana>=0.30.2
```

## Verificar Instalação
```bash
python -c "import solders; print('✅ solders:', solders.__version__)"
python -c "import solana; print('✅ solana instalado')"
```

## Para o Render
No Render, o build script (`build.sh`) tentará instalar automaticamente. Se falhar, verifique os logs de build.

