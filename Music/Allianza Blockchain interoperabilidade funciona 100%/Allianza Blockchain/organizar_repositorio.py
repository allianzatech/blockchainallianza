#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 Script para Organizar Repositório GitHub de Forma Profissional
Organiza arquivos em estrutura limpa e profissional
"""

import os
import shutil
from pathlib import Path

# Estrutura profissional desejada
ESTRUTURA_PROFISSIONAL = {
    # Core - Código-fonte principal
    "core/": [
        "core/crypto/",
        "core/consensus/",
        "core/interoperability/",
    ],
    
    # Scripts - Organizar scripts auxiliares
    "scripts/": [
        "fix_encryption_key.py",
        "generate_test_key.py",
        "keep_alive.py",
        "keep_alive_simple.py",
        "sincronizar_repositorio_publico.py",
        "limpar_projeto.py",
        "preparar_repositorio_publico_novo.py",
    ],
    
    # Docs - Documentação adicional
    "docs/": [
        "ANALISE_CONSOLIDADA_MANUS_AI.md",
        "ANALISE_SEGURANCA_VULNERABILIDADES.md",
        "ANALISE_SUGESTOES_MELHORIAS.md",
        "DOCUMENTACAO_INPI_COMPLETA.md",
        "EXPLICACAO_TECNOLOGIA_LEIGOS_FINAL.md",
        "GUIA_KEEP_ALIVE.md",
        "GUIA_PASSO_A_PASSO_DEPOSITO_INPI.md",
        "GUIA_QSS_PARA_OUTRAS_BLOCKCHAINS.md",
        "GUIA_RESUMO_DIGITAL_HASH_INPI.md",
        "GUIA_SINCRONIZACAO_AUTOMATICA.md",
        "INSTALAR_LIBOQS.md",
        "INPI_PI_01_ALZ_NIEV_DESCRICAO_COMPLETA.md",
        "INPI_PI_02_QRS3_DESCRICAO_COMPLETA.md",
        "INPI_PI_03_QSS_DESCRICAO_COMPLETA.md",
        "INPI_RPC_01_ALZ_NIEV_MANUAL_TECNICO.md",
        "ORGANIZACAO_PROJETO.md",
        "OTIMIZAR_TESTNET_PERFORMANCE.md",
        "PLANO_ACAO_UNIFICADO_MVP_INVESTIVEL.md",
        "PLANO_MELHORIAS_POS_ANALISE_IA.md",
        "PUBLIC_REPOSITORY_STRUCTURE.md",
        "QUANTUM_SECURITY_SERVICE_LAYER.md",
        "QSS_SDK_IMPLEMENTATION.md",
        "QSS_SDK_TEST_RESULTS.md",
        "RELATORIO_REVISAO_FINAL.md",
        "RELATORIO_SEGURANCA_COMPLETO.md",
        "STATUS_MVP_INVESTIVEL.md",
    ],
    
    # Archive - Arquivos antigos/documentação histórica
    "archive/": [
        "ACAO_IMEDIATA_TOKEN.md",
        "ARQUIVOS_BACKEND_ATUALIZADOS.md",
        "ARQUIVOS_PARA_GITHUB_FINAL.md",
        "ARQUIVOS_PARA_GITHUB.md",
        "ATUALIZAR_TOKEN_RENDER_RAPIDO.md",
        "ATUALIZAR_TOKEN_RENDER.md",
        "CHECKLIST_3_ITEMS.md",
        "COMPLETE_IMPLEMENTATION.md",
        "CORRECAO_BALANCE_LEDGER.md",
        "CORRECAO_COLUNAS_INEXISTENTES.md",
        "CORRECAO_DATABASE_URL.md",
        "CORRECAO_ERRO_500.md",
        "CORRECAO_FINAL_DATABASE_URL.md",
        "CORRECAO_FRONTEND_HEALTH.md",
        "CORRECAO_HEALTH_ENDPOINT.md",
        "CORRECAO_INDENTACAO_REPORTS.md",
        "CORRECAO_METADATA.md",
        "CORRECAO_REPORTS_DATABASE.md",
        "CORRECAO_VALOR_TOKEN_USD.md",
        "CORRECOES_DEPLOY_RENDER.md",
        "CORRIGIR_RENDER_VARIAVEIS.md",
        "DEBUG_TOKEN_BACKEND.md",
        "DEMO_GIF_GUIDE.md",
        "ESTRATEGIA_DOIS_REPOSITORIOS.md",
        "FEEDBACK_OUTLIER_VENTURES.md",
        "FORCAR_DEPLOY_RENDER.md",
        "INSTRUCOES_ATUALIZAR_TOKEN_RENDER.md",
        "LISTA_ARQUIVOS_GITHUB.md",
        "MELHORIAS_ADMIN_DASHBOARD.md",
        "MELHORIAS_APLICADAS.md",
        "MELHORIAS_IMPLEMENTADAS.md",
        "MELHORIAS_MATURIDADE_IMPLEMENTADAS.md",
        "MELHORIAS_TESTNET.md",
        "MIGRACAO_EXPIRES_AT.md",
        "PROBLEMA_RESOLVIDO.md",
        "PROBLEMA_TOKEN_GITHUB.md",
        "RESUMO_ARQUIVOS_GITHUB.md",
        "RESUMO_EXPIRACAO_PAGAMENTOS.md",
        "RESUMO_FINAL_ADMIN.md",
        "RESUMO_FINAL_MELHORIAS.md",
        "RESUMO_MELHORIAS.md",
        "RESUMO_PUSH_GITHUB.md",
        "REVISAO_FLUXO_COMPRA_SALDO.md",
        "SENHA_ADMIN.md",
        "SISTEMA_EXPIRACAO_PAGAMENTOS.md",
        "SISTEMA_I18N_STRESS_TEST.md",
        "SISTEMA_MODAIS_MODERNO.md",
        "SOLUCAO_CORRETA_MIGRACAO.md",
        "SOLUCAO_FINAL_INDENTACAO.md",
        "SOLUCAO_FINAL_PUSH.md",
        "SOLUCAO_FINAL_TOKEN.md",
        "TROUBLESHOOTING_TOKEN_401.md",
        "VERIFICAR_REPOSITORIO_PUBLICO.md",
    ],
}

def criar_estrutura():
    """Cria estrutura de diretórios"""
    for diretorio in ESTRUTURA_PROFISSIONAL.keys():
        Path(diretorio).mkdir(parents=True, exist_ok=True)
        print(f"✅ Criado: {diretorio}")

def mover_arquivos():
    """Move arquivos para estrutura profissional"""
    movidos = 0
    for diretorio_destino, arquivos in ESTRUTURA_PROFISSIONAL.items():
        for arquivo in arquivos:
            origem = Path(arquivo)
            if origem.exists():
                destino = Path(diretorio_destino) / origem.name
                if not destino.exists():
                    shutil.move(str(origem), str(destino))
                    print(f"✅ Movido: {arquivo} → {destino}")
                    movidos += 1
                else:
                    print(f"⚠️  Já existe: {destino}")
    return movidos

def main():
    print("📁 Organizando repositório de forma profissional...\n")
    criar_estrutura()
    print("\n📦 Movendo arquivos...\n")
    movidos = mover_arquivos()
    print(f"\n✅ Organização concluída! {movidos} arquivos movidos.")

if __name__ == "__main__":
    main()

