#!/bin/bash
# Script para Executar Todos os Testes - Allianza Blockchain
# Versão: 1.0
# Data: 03 de Dezembro de 2025

set -e  # Parar em caso de erro

echo "============================================================"
echo "🧪 EXECUTANDO TODOS OS TESTES - ALLIANZA BLOCKCHAIN"
echo "============================================================"
echo ""

# Criar diretórios necessários
mkdir -p test_results/complete_validation
mkdir -p test_results/critical_tests
mkdir -p test_results/professional_suite
mkdir -p logs

# Timestamp de início
START_TIME=$(date +%s)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "📅 Início: $(date)"
echo "📂 Diretório de trabalho: $(pwd)"
echo ""

# Contador de testes
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Função para executar teste e contar resultados
run_test() {
    local test_name=$1
    local test_script=$2
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 Executando: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if python "$test_script" > "logs/${test_name}_${TIMESTAMP}.log" 2>&1; then
        echo "✅ $test_name: PASSOU"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo "❌ $test_name: FALHOU"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Executar testes principais
echo "📋 FASE 1: Provas Principais"
echo ""

# Executar testes de validação completa
echo "📋 FASE 2: Complete Validation Suite"
echo ""

# Executar testes críticos
echo "📋 FASE 3: Critical Tests Suite"
echo ""
run_test "Failure Scenarios" "test_failure_scenarios.py"
run_test "Atomicity Failure" "test_atomicity_failure.py"
echo ""

# Executar suite profissional
echo "📋 FASE 4: Professional Suite"
echo ""

# Calcular tempo total
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Gerar relatório final
echo ""
echo "============================================================"
echo "📊 RESULTADOS FINAIS"
echo "============================================================"
echo ""
echo "📅 Fim: $(date)"
echo "⏱️  Duração total: ${DURATION}s"
echo ""
echo "📈 Estatísticas:"
echo "   Total de testes: $TOTAL_TESTS"
echo "   ✅ Passou: $PASSED_TESTS"
echo "   ❌ Falhou: $FAILED_TESTS"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    SUCCESS_RATE=100.0
    echo "🎉 TAXA DE SUCESSO: ${SUCCESS_RATE}%"
    echo "✅ TODOS OS TESTES PASSARAM!"
else
    SUCCESS_RATE=$(echo "scale=2; ($PASSED_TESTS * 100) / $TOTAL_TESTS" | bc)
    echo "⚠️  TAXA DE SUCESSO: ${SUCCESS_RATE}%"
    echo "❌ Alguns testes falharam. Verifique os logs em logs/"
fi

# Gerar JSON de resultados
cat > "test_results/FINAL_RESULTS_${TIMESTAMP}.json" << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "duration_seconds": $DURATION,
  "summary": {
    "total_tests": $TOTAL_TESTS,
    "passed_tests": $PASSED_TESTS,
    "failed_tests": $FAILED_TESTS,
    "success_rate": $SUCCESS_RATE
  },
  "environment": {
    "python_version": "$(python --version)",
    "platform": "$(uname -s)",
    "architecture": "$(uname -m)"
  }
}
EOF

echo ""
echo "📄 Relatório salvo em: test_results/FINAL_RESULTS_${TIMESTAMP}.json"
echo ""

# Exit code baseado em sucesso
if [ $FAILED_TESTS -eq 0 ]; then
    exit 0
else
    exit 1
fi



