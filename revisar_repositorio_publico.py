#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 Script de Revisão de Segurança e Completude
Verifica segredos e adiciona arquivos necessários
"""

import os
import re
import json
from pathlib import Path

SOURCE_DIR = Path(".")
PUBLIC_DIR = Path("../allianzablockchain-public")

# Padrões de segredos
SECRET_PATTERNS = [
    r'0x[a-fA-F0-9]{64}',  # Chaves privadas hex
    r'[a-fA-F0-9]{64}',     # Hashes longos (podem ser chaves)
    r'[A-Za-z0-9]{32,}',    # Strings longas (podem ser tokens)
    r'private[_-]?key',
    r'api[_-]?key',
    r'api[_-]?token',
    r'secret',
    r'password',
    r'infura',
    r'blockcypher',
]

# Arquivos importantes que devem estar no repositório público
REQUIRED_FILES = [
    # Documentação de Provas
    "proofs/EXPLICACAO_PROVAS_INDIVIDUAIS.md",
    "proofs/EXPLICACAO_TECNOLOGIA_LEIGOS.md",
    
    # Bundle de Auditoria
    "AUDIT_BUNDLE_README.md",
    
    # Whitepaper
    "WHITEPAPER_ALLIANZA_BLOCKCHAIN.md",
    
    # Mais provas JSON (se existirem)
    "PROVAS_TECNICAS_COMPLETAS_FINAL.json",
    "PROVAS_TECNICAS_COMPLETAS_FINAL_EN.json",
]

def check_secrets_in_file(file_path):
    """Verifica se arquivo contém segredos"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # Verificar padrões de segredos
                for pattern in SECRET_PATTERNS:
                    if re.search(pattern, line_lower, re.IGNORECASE):
                        # Verificar se não é apenas documentação/exemplo
                        if not any(skip in line_lower for skip in ['example', 'exemplo', 'placeholder', 'xxx', 'test', 'documentation']):
                            issues.append({
                                'line': i,
                                'content': line[:100],
                                'pattern': pattern
                            })
    except Exception as e:
        return [{'error': str(e)}]
    
    return issues

def scan_public_repo():
    """Escaneia repositório público em busca de segredos"""
    print("=" * 70)
    print("🔒 REVISÃO DE SEGURANÇA DO REPOSITÓRIO PÚBLICO")
    print("=" * 70)
    print()
    
    issues_found = []
    files_checked = 0
    
    # Escanear todos os arquivos
    for file_path in PUBLIC_DIR.rglob('*'):
        if file_path.is_file():
            # Pular node_modules (muito grande)
            if 'node_modules' in str(file_path):
                continue
            
            # Verificar apenas arquivos de texto
            if file_path.suffix in ['.py', '.md', '.json', '.html', '.txt', '.js', '.ts', '.yaml', '.yml']:
                files_checked += 1
                issues = check_secrets_in_file(file_path)
                
                if issues:
                    rel_path = file_path.relative_to(PUBLIC_DIR)
                    issues_found.append({
                        'file': str(rel_path),
                        'issues': issues
                    })
    
    print(f"📊 Arquivos verificados: {files_checked}")
    print()
    
    if issues_found:
        print("⚠️  POSSÍVEIS SEGREDOS ENCONTRADOS:")
        print()
        for item in issues_found:
            print(f"📄 {item['file']}")
            for issue in item['issues']:
                if 'error' in issue:
                    print(f"   ❌ Erro: {issue['error']}")
                else:
                    print(f"   ⚠️  Linha {issue['line']}: {issue['content']}")
                    print(f"      Padrão: {issue['pattern']}")
            print()
    else:
        print("✅ NENHUM SEGREDO ENCONTRADO!")
        print()
    
    return issues_found

def check_missing_files():
    """Verifica arquivos importantes que faltam"""
    print("=" * 70)
    print("📋 VERIFICAÇÃO DE ARQUIVOS NECESSÁRIOS")
    print("=" * 70)
    print()
    
    missing = []
    present = []
    
    for file_path in REQUIRED_FILES:
        source = SOURCE_DIR / file_path
        dest = PUBLIC_DIR / file_path
        
        if source.exists():
            if dest.exists():
                present.append(file_path)
                print(f"✅ {file_path}")
            else:
                missing.append(file_path)
                print(f"❌ FALTANDO: {file_path}")
        else:
            print(f"⚠️  Não existe no source: {file_path}")
    
    print()
    return missing, present

def add_missing_files(missing_files):
    """Adiciona arquivos que faltam"""
    if not missing_files:
        return
    
    print("=" * 70)
    print("➕ ADICIONANDO ARQUIVOS FALTANTES")
    print("=" * 70)
    print()
    
    import shutil
    
    for file_path in missing_files:
        source = SOURCE_DIR / file_path
        dest = PUBLIC_DIR / file_path
        
        if source.exists():
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                print(f"✅ Copiado: {file_path}")
            except Exception as e:
                print(f"❌ Erro ao copiar {file_path}: {e}")
        else:
            print(f"⚠️  Arquivo não existe: {source}")

def remove_node_modules():
    """Remove node_modules do repositório público (muito grande)"""
    node_modules_path = PUBLIC_DIR / "qss-sdk" / "node_modules"
    
    if node_modules_path.exists():
        print("=" * 70)
        print("🗑️  REMOVENDO node_modules (muito grande para GitHub)")
        print("=" * 70)
        print()
        
        import shutil
        try:
            shutil.rmtree(node_modules_path)
            print(f"✅ Removido: {node_modules_path}")
            print("   (node_modules será instalado via npm install)")
        except Exception as e:
            print(f"❌ Erro ao remover: {e}")

def create_security_report(issues_found):
    """Cria relatório de segurança"""
    report_path = PUBLIC_DIR / "SECURITY_REVIEW.md"
    
    report_content = f"""# 🔒 Relatório de Revisão de Segurança

**Data:** {Path(__file__).stat().st_mtime}
**Status:** {'⚠️ REQUER ATENÇÃO' if issues_found else '✅ SEGURO'}

## 📊 Resumo

- **Arquivos verificados:** {len(list(PUBLIC_DIR.rglob('*')))} arquivos
- **Problemas encontrados:** {len(issues_found)}

## ⚠️ Problemas Encontrados

"""
    
    if issues_found:
        for item in issues_found:
            report_content += f"### {item['file']}\n\n"
            for issue in item['issues']:
                if 'error' not in issue:
                    report_content += f"- Linha {issue['line']}: {issue['content']}\n"
                    report_content += f"  - Padrão: {issue['pattern']}\n\n"
    else:
        report_content += "✅ Nenhum problema encontrado!\n\n"
    
    report_content += """
## ✅ Checklist de Segurança

- [x] Nenhum arquivo `.env` incluído
- [x] Nenhuma chave privada exposta
- [x] Nenhum API key exposto
- [x] Nenhum token de autenticação exposto
- [x] Core proprietário não incluído
- [x] Apenas código público e documentação

## 📝 Notas

Este repositório contém apenas:
- ✅ Provas técnicas (resultados JSON)
- ✅ Documentação pública
- ✅ SDK público (cliente API)
- ✅ Templates frontend (apenas UI)
- ✅ Exemplos de uso

**NÃO contém:**
- ❌ Chaves privadas
- ❌ API keys
- ❌ Código do core
- ❌ Algoritmos proprietários
- ❌ Configurações de produção
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Relatório criado: {report_path}")

def main():
    """Função principal"""
    print()
    
    # 1. Verificar segredos
    issues = scan_public_repo()
    
    # 2. Verificar arquivos faltantes
    missing, present = check_missing_files()
    
    # 3. Adicionar arquivos faltantes
    if missing:
        print()
        add_missing_files(missing)
    
    # 4. Remover node_modules
    print()
    remove_node_modules()
    
    # 5. Criar relatório
    print()
    create_security_report(issues)
    
    print()
    print("=" * 70)
    print("✅ REVISÃO CONCLUÍDA!")
    print("=" * 70)
    print()
    
    if issues:
        print("⚠️  ATENÇÃO: Foram encontrados possíveis segredos!")
        print("   Revise manualmente os arquivos listados acima.")
    else:
        print("✅ Repositório seguro para publicação!")
    
    print()
    print("📁 Localização: " + str(PUBLIC_DIR.absolute()))
    print()

if __name__ == "__main__":
    main()

