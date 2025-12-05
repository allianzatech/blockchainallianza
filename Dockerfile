# Dockerfile para Ambiente de Testes e Auditoria - Allianza Blockchain
# Versão: 1.0
# Data: 03 de Dezembro de 2025

FROM python:3.11-slim

# Metadados
LABEL maintainer="Allianza Blockchain Team"
LABEL description="Ambiente de testes e auditoria para Allianza Blockchain"
LABEL version="1.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libssl-dev \
    libffi-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Tentar instalar liboqs-python (opcional, mas recomendado)
RUN pip install --no-cache-dir liboqs-python || echo "⚠️ liboqs-python não disponível, usando simulação funcional"

# Copiar código fonte
COPY . .

# Criar diretórios necessários
RUN mkdir -p proofs/testnet/complete_validation \
    proofs/testnet/critical_tests \
    proofs/testnet/professional_suite \
    logs

# Script de execução de testes
COPY scripts/run_all_tests.sh /app/scripts/run_all_tests.sh
RUN chmod +x /app/scripts/run_all_tests.sh

# Expor porta (se necessário para API)
EXPOSE 5008

# Comando padrão: executar todos os testes
CMD ["/app/scripts/run_all_tests.sh"]



