#!/usr/bin/env python3
"""
Remove todos os arquivos .md do GitHub, exceto os que contêm provas
"""
import os
import subprocess

# Arquivos/pastas que DEVEM ser mantidos (contêm provas)
KEEP_PATTERNS = [
    'provas_fase2',
    'proofs',
    'VERIFIABLE_ON_CHAIN_PROOFS.md',
    'VERIFICATION.md',
    'IMPLEMENTACAO_UCHAINID_ZK_PROOFS.md',
    'GUIA_VERIFICACAO_ON_CHAIN.md',
    'EXEMPLOS_HASHES_TESTE_QSS.md',
    '.github',  # Templates do GitHub
    'node_modules',  # Dependências
    'liboqs',  # Biblioteca externa
    'qss-verifier',
    'qss-canonicalizer',
]

def should_keep(filepath):
    """Verifica se o arquivo deve ser mantido"""
    for pattern in KEEP_PATTERNS:
        if pattern in filepath:
            return True
    return False

def main():
    print("🔍 Procurando arquivos .md para remover...")
    print("="*70)
    
    # Encontrar todos os arquivos .md
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Ignorar .git e outras pastas
        if '.git' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                # Normalizar caminho
                rel_path = os.path.relpath(filepath, '.')
                
                if not should_keep(rel_path):
                    md_files.append(rel_path)
    
    print(f"\n📋 Encontrados {len(md_files)} arquivos .md para remover")
    print("\nArquivos que serão removidos:")
    for f in sorted(md_files)[:20]:  # Mostrar primeiros 20
        print(f"  - {f}")
    if len(md_files) > 20:
        print(f"  ... e mais {len(md_files) - 20} arquivos")
    
    # Remover arquivos automaticamente (usuário pediu explicitamente)
    print("\n" + "="*70)
    print("🗑️  Removendo arquivos automaticamente...")
    
    # Remover arquivos
    print("\n🗑️  Removendo arquivos...")
    removed = 0
    for filepath in md_files:
        try:
            os.remove(filepath)
            removed += 1
            print(f"  ✅ Removido: {filepath}")
        except Exception as e:
            print(f"  ❌ Erro ao remover {filepath}: {e}")
    
    print("\n" + "="*70)
    print(f"✅ {removed} arquivos removidos com sucesso!")
    print("\n💡 Execute 'git add -A' e 'git commit' para aplicar as mudanças")

if __name__ == '__main__':
    main()

