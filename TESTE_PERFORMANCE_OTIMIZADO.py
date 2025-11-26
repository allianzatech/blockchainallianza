#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Performance Otimizado - QRS-3
Compara performance antes e depois das otimizações
"""

import time
from quantum_security import QuantumSecuritySystem
from collections import defaultdict

print("=" * 70)
print("⚡ TESTE DE PERFORMANCE OTIMIZADO - QRS-3")
print("=" * 70)
print()

# Inicializar sistema
qs = QuantumSecuritySystem()

# Configurações do teste
NUM_TESTES = 50

print(f"📊 CONFIGURAÇÃO:")
print(f"   Testes por modo: {NUM_TESTES}")
print(f"   Total de operações: {NUM_TESTES * 2}")
print()

# ============================================================================
# TESTE 1: MODO NÃO OTIMIZADO (BASELINE)
# ============================================================================

print("=" * 70)
print("📊 TESTE 1: MODO NÃO OTIMIZADO (BASELINE)")
print("=" * 70)
print()

# Gerar keypair QRS-3
print("🔑 Gerando keypair QRS-3...")
qrs3_result = qs.generate_qrs3_keypair()
if not qrs3_result.get("success"):
    print(f"❌ Erro: {qrs3_result.get('error')}")
    exit(1)

qrs3_id = qrs3_result["keypair_id"]
print(f"✅ Keypair gerado: {qrs3_id[:30]}...")
print()

# Testes sem otimização
print("✍️  Criando assinaturas (modo não otimizado)...")
times_no_opt = []
message_template = b"Teste performance otimizado - Transacao #"

for i in range(NUM_TESTES):
    message = message_template + str(i).encode()
    start = time.time()
    result = qs.sign_qrs3(qrs3_id, message, optimized=False, parallel=False)
    elapsed = (time.time() - start) * 1000  # ms
    times_no_opt.append(elapsed)
    if (i + 1) % 10 == 0:
        print(f"   ✅ {i + 1}/{NUM_TESTES} assinaturas criadas...")

avg_no_opt = sum(times_no_opt) / len(times_no_opt)
min_no_opt = min(times_no_opt)
max_no_opt = max(times_no_opt)

print(f"\n✅ {NUM_TESTES} assinaturas criadas (modo não otimizado)")
print(f"   Tempo médio: {avg_no_opt:.2f} ms")
print(f"   Tempo mínimo: {min_no_opt:.2f} ms")
print(f"   Tempo máximo: {max_no_opt:.2f} ms")
print()

# ============================================================================
# TESTE 2: MODO OTIMIZADO
# ============================================================================

print("=" * 70)
print("⚡ TESTE 2: MODO OTIMIZADO (COM CACHE)")
print("=" * 70)
print()

# Gerar novo keypair para teste justo
print("🔑 Gerando novo keypair QRS-3...")
qrs3_result_opt = qs.generate_qrs3_keypair()
if not qrs3_result_opt.get("success"):
    print(f"❌ Erro: {qrs3_result_opt.get('error')}")
    exit(1)

qrs3_id_opt = qrs3_result_opt["keypair_id"]
print(f"✅ Keypair gerado: {qrs3_id_opt[:30]}...")
print()

# Testes com otimização
print("✍️  Criando assinaturas (modo otimizado)...")
times_opt = []

for i in range(NUM_TESTES):
    message = message_template + str(i).encode()
    start = time.time()
    result = qs.sign_qrs3(qrs3_id_opt, message, optimized=True, parallel=True)
    elapsed = (time.time() - start) * 1000  # ms
    times_opt.append(elapsed)
    if (i + 1) % 10 == 0:
        print(f"   ✅ {i + 1}/{NUM_TESTES} assinaturas criadas...")

avg_opt = sum(times_opt) / len(times_opt)
min_opt = min(times_opt)
max_opt = max(times_opt)

print(f"\n✅ {NUM_TESTES} assinaturas criadas (modo otimizado)")
print(f"   Tempo médio: {avg_opt:.2f} ms")
print(f"   Tempo mínimo: {min_opt:.2f} ms")
print(f"   Tempo máximo: {max_opt:.2f} ms")
print()

# ============================================================================
# COMPARAÇÃO
# ============================================================================

print("=" * 70)
print("📊 COMPARAÇÃO: NÃO OTIMIZADO vs OTIMIZADO")
print("=" * 70)
print()

improvement = ((avg_no_opt - avg_opt) / avg_no_opt) * 100
time_saved = avg_no_opt - avg_opt

print(f"⏱️  LATÊNCIA MÉDIA:")
print(f"   Não Otimizado: {avg_no_opt:.2f} ms")
print(f"   Otimizado:     {avg_opt:.2f} ms")
print(f"   Melhoria:      {improvement:.1f}%")
print(f"   Tempo economizado: {time_saved:.2f} ms por assinatura")
print()

print(f"📈 LATÊNCIA MÍNIMA:")
print(f"   Não Otimizado: {min_no_opt:.2f} ms")
print(f"   Otimizado:     {min_opt:.2f} ms")
print(f"   Melhoria:      {((min_no_opt - min_opt) / min_no_opt * 100):.1f}%")
print()

print(f"📉 LATÊNCIA MÁXIMA:")
print(f"   Não Otimizado: {max_no_opt:.2f} ms")
print(f"   Otimizado:     {max_opt:.2f} ms")
print(f"   Melhoria:      {((max_no_opt - max_opt) / max_no_opt * 100):.1f}%")
print()

# Calcular throughput
throughput_no_opt = 1000 / avg_no_opt if avg_no_opt > 0 else 0
throughput_opt = 1000 / avg_opt if avg_opt > 0 else 0
throughput_improvement = ((throughput_opt - throughput_no_opt) / throughput_no_opt * 100) if throughput_no_opt > 0 else 0

print(f"🚀 THROUGHPUT:")
print(f"   Não Otimizado: {throughput_no_opt:.2f} TPS")
print(f"   Otimizado:     {throughput_opt:.2f} TPS")
print(f"   Melhoria:      +{throughput_improvement:.1f}%")
print()

# Verificar se atingiu meta de 20%
if improvement >= 20:
    print("=" * 70)
    print("✅✅✅ META ATINGIDA!")
    print("=" * 70)
    print(f"   Redução de latência: {improvement:.1f}%")
    print(f"   Meta: ≥20%")
    print(f"   Status: ✅ ATINGIDA")
    print()
    print("🎉 Otimizações implementadas com sucesso!")
    print("   • Cache de chaves SPHINCS+ funcionando")
    print("   • Modo híbrido inteligente ativo")
    print("   • Performance melhorada significativamente")
else:
    print("=" * 70)
    print("⚠️  META PARCIALMENTE ATINGIDA")
    print("=" * 70)
    print(f"   Redução de latência: {improvement:.1f}%")
    print(f"   Meta: ≥20%")
    print(f"   Status: ⚠️  {20 - improvement:.1f}% abaixo da meta")
    print()
    print("💡 Sugestões:")
    print("   • Aumentar tamanho do cache")
    print("   • Implementar processamento paralelo")
    print("   • Otimizar variante SPHINCS+")

print()
print("=" * 70)

