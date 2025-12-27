#!/usr/bin/env python3
"""
Script para limpar e organizar o projeto Allianza Blockchain
Remove arquivos desnecessários e organiza a estrutura
"""

import os
from pathlib import Path
from typing import List, Set

# Diretório raiz do projeto
ROOT = Path(".")

# Arquivos para EXCLUIR (organizados por categoria)

# 1. Documentação redundante sobre GitHub/Push/Topics (já resolvido)
GITHUB_DOCS = [
    "TOPICS_GITHUB_LIMPO.md",
    "TOPICS_GITHUB_UM_POR_UM.md",
    "TOPICS_GITHUB_PUBLICO.md",
    "DESCRICAO_REPOSITORIO_PUBLICO.md",
    "SINCRONIZACAO_AUTOMATICA_COMPLETA.md",
    "ESTRATEGIA_REPOSITORIO_PUBLICO_VALIDACAO.md",
    "ESTRATEGIA_GITHUB_NPM_POS_INPI.md",
    "O_QUE_SERA_VISIVEL_NO_GITHUB.md",
    "NPM_VS_GITHUB_EXPLICACAO.md",
    "SUCESSO_NPM_PUBLICADO.md",
    "SOLUCAO_ESCOPO_NPM.md",
    "GUIA_GITHUB_PRIVACIDADE_EMAIL.md",
    "GUIA_PUBLICAR_NPM.md",
    "preparar_repositorio_publico.py",  # Manter apenas o _novo
]

# 2. Documentação redundante sobre Deploy/Render (já implementado)
DEPLOY_DOCS = [
    "DEPLOY_HOSTINGER_PASSO_A_PASSO.md",
    "DEPLOY_RAILWAY.md",
    "DEPLOY_RENDER_AGORA_FINAL.md",
    "DEPLOY_RENDER_AGORA.md",
    "DEPLOY_RENDER_PASSO_A_PASSO.md",
    "DEPLOY_RENDER.md",
    "DEPLOY_VPS_HOSTINGER.md",
    "GUIA_DEPLOY_HOSTINGER_COMPLETO.md",
    "RENDER_FIX_PYTHON.md",
    "RENDER_SLEEP_MODE_SOLUCAO.md",
    "RENDER_TUDO_PRONTO.md",
    "README_RENDER.md",
    "OPCOES_RENDER_PAGAMENTO.md",
    "RECRIAR_SERVICO_RENDER.md",
    "SOLUCAO_ERRO_GEVENT.md",
    "FORCAR_DEPLOY_RENDER.md",
    "COMO_USAR_ENV_RENDER.md",
    "ADICIONAR_VARIAVEIS_RENDER.md",
    "VARIAVEIS_FINAIS_RENDER.md",
    "CONFIGURAR_RENDER_MANUAL.md",
    "CONFIGURAR_CHAVES_TESTNET.md",
    "CONFIGURAR_DNS_TESTNET.md",
    "DOMINIO_VERIFICADO.md",
    "INTEGRAR_TESTNET_HOSTINGER.md",
    "COMO_ACESSAR_TESTNET.md",
    "RESOLVER_CONFLITO_DNS.md",
    "PROXIMOS_PASSOS_DNS.md",
    "PROXIMOS_PASSOS_RENDER.md",
    "COMPARACAO_HOSPEDAGENS.md",
    "COMANDO_START_RENDER.txt",
    "COMANDOS_RENDER_RAPIDO.txt",
    "env_limpo_para_render.txt",
    "CORRIGIR_RENDER_AGORA.md",
    "CORRIGIR_POLYGON_PRIVATE_KEY_RENDER.md",
]

# 3. Scripts .bat temporários/duplicados (manter apenas os essenciais)
BAT_SCRIPTS = [
    "compilar_liboqs_dll.bat",
    "compilar_liboqs_python_alternativo.bat",
    "compilar_liboqs_python.bat",
    "compilar_liboqs.bat",
    "reiniciar_compilacao_liboqs.bat",
    "verificar_progresso_compilacao.bat",
    "continuar_instalacao_sphincs.bat",
    "verificar_instalacao_sphincs.bat",
    "instalar_sphincs_com_vs.bat",
    "instalar_sphincs_real_continuar.bat",
    "instalar_sphincs_real.bat",
    "verificar_build_tools.bat",
    "instalar_build_tools.bat",
    "CONFIGURAR_TOKEN_PUBLICO.bat",  # Já não é mais necessário
]

# 4. Arquivos temporários/logs
TEMP_FILES = [
    "allianza_blockchain_structured.log",
    "allianza_blockchain.log",
    "allianza_blockchain.db",
    "qaas_audit.db",
    "qaas_enterprise.log",
    "deploy.zip",
    "proofs.zip",
    "faucet_last_requests.json",
    "gas_cost_analysis_1764379694.json",
    "CORRECAO_REAL_METAPROGRAMMABLE.txt",
    "HASH_FINAL_TODOS_PROGRAMAS_INPI.txt",
    "HASHES_CONSOLIDADOS_INPI.txt",
    "HASHES_INPI_RESUMO.txt",
]

# 5. Documentação duplicada/redundante
DUPLICATE_DOCS = [
    "RESUMO_MELHORIAS.md",
    "RESUMO_MELHORIAS_IMPLEMENTADAS.md",
    "TODAS_MELHORIAS_IMPLEMENTADAS.md",
    "MELHORIAS_APLICADAS.md",
    "MELHORIAS_APOS_ANALISE.md",
    "MELHORIAS_CRITICAS_INTEROPERABILIDADE.md",
    "MELHORIAS_SEGURANCA_QUANTICA.md",
    "IMPLEMENTACOES_REALIZADAS.md",
    "ARQUIVOS_PARA_ATUALIZAR.md",
    "CORRECOES_APLICADAS.md",
    "CORRECOES_BOTOES_TESTES.md",
    "BITCOINLIB_ADICIONADO.md",
    "BITCOINLIB_CORRIGIDO.md",
    "PROVA_JSON_SEGURA_IMPLEMENTADA.md",
    "VERIFICACAO_TRANSFERENCIA_SUCESSO.md",
    "ANALISE_COMBINADA_TESTES_CRITICA.md",
    "ANALISE_TECNICA_RESPOSTA.md",
    "ANALISE_TECNICA_INTEROPERABILIDADE.md",
    "RELATORIO_SEGURANCA_NOTAA.md",  # Manter apenas o COMPLETO
    "COMO_COMPILAR_CSS.md",  # Já não é mais necessário
]

# 6. Scripts Python temporários/utilitários antigos
TEMP_SCRIPTS = [
    "adicionar_hover_botao.py",
    "atualizar_links_templates.py",
    "atualizar_tailwind_html.py",
    "criar_htaccess.py",
    "criar_start_server.py",
    "limpar_templates.py",
    "padronizar_botao_voltar.py",
    "gerar_hashes_inpi.py",
    "revisar_repositorio_publico.py",  # Manter apenas o _completo
]

# Consolidar todos os arquivos para excluir
FILES_TO_DELETE = set(
    GITHUB_DOCS + DEPLOY_DOCS + BAT_SCRIPTS + TEMP_FILES + 
    DUPLICATE_DOCS + TEMP_SCRIPTS
)

def main():
    """Executa a limpeza do projeto"""
    print("=" * 70)
    print("🧹 LIMPEZA E ORGANIZAÇÃO DO PROJETO ALLIANZA BLOCKCHAIN")
    print("=" * 70)
    print()
    
    deleted = []
    not_found = []
    errors = []
    
    for file_path in sorted(FILES_TO_DELETE):
        full_path = ROOT / file_path
        if full_path.exists():
            try:
                if full_path.is_file():
                    full_path.unlink()
                    deleted.append(file_path)
                    print(f"✅ Excluído: {file_path}")
                elif full_path.is_dir():
                    # Para diretórios, usar shutil.rmtree seria mais seguro
                    print(f"⚠️  Diretório encontrado (não excluído automaticamente): {file_path}")
            except Exception as e:
                errors.append((file_path, str(e)))
                print(f"❌ Erro ao excluir {file_path}: {e}")
        else:
            not_found.append(file_path)
    
    print()
    print("=" * 70)
    print("📊 RESUMO DA LIMPEZA")
    print("=" * 70)
    print(f"✅ Arquivos excluídos: {len(deleted)}")
    print(f"⚠️  Arquivos não encontrados: {len(not_found)}")
    print(f"❌ Erros: {len(errors)}")
    print()
    
    if deleted:
        print("📋 Arquivos excluídos:")
        for f in deleted:
            print(f"   - {f}")
        print()
    
    if not_found:
        print("ℹ️  Arquivos não encontrados (já foram excluídos ou não existem):")
        for f in not_found[:10]:  # Mostrar apenas os primeiros 10
            print(f"   - {f}")
        if len(not_found) > 10:
            print(f"   ... e mais {len(not_found) - 10} arquivos")
        print()
    
    if errors:
        print("❌ Erros encontrados:")
        for f, e in errors:
            print(f"   - {f}: {e}")
        print()
    
    print("=" * 70)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("=" * 70)
    print()
    print("💡 PRÓXIMOS PASSOS:")
    print("   1. Revisar os arquivos excluídos")
    print("   2. Verificar se não há dependências quebradas")
    print("   3. Fazer commit das mudanças")
    print()

if __name__ == "__main__":
    main()

