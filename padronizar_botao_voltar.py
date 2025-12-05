#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para padronizar todos os botões "Voltar ao Dashboard" para apenas "Voltar"
e simplificar o estilo do botão
"""

import os
import re
from pathlib import Path

# Estilo simples do botão
SIMPLE_BUTTON_STYLE = """        .btn-back {
            display: inline-block;
            padding: 8px 16px;
            background: #374151;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            transition: background 0.2s;
        }
        .btn-back:hover {
            background: #4b5563;
        }"""

# Padrões para substituir
PATTERNS = [
    # Substituir texto
    (r'Voltar ao Dashboard', 'Voltar'),
    (r'voltar ao dashboard', 'Voltar'),
    
    # Substituir estilo complexo por simples
    (r'\.btn-back \{[^}]*\}', SIMPLE_BUTTON_STYLE),
    (r'\.btn-back:hover \{[^}]*\}', ''),
]

# Arquivos para processar
TEMPLATE_DIR = Path('templates')
FILES_TO_UPDATE = []

def find_html_files():
    """Encontra todos os arquivos HTML"""
    html_files = []
    for root, dirs, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return html_files

def update_file(file_path):
    """Atualiza um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Aplicar substituições
        for pattern, replacement in PATTERNS:
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Limpar linhas vazias duplicadas do estilo
        content = re.sub(r'\.btn-back:hover \{\s*\}', '', content)
        
        # Garantir que o texto do botão seja apenas "Voltar"
        content = re.sub(r'<i class="fas fa-arrow-left"></i>\s*Voltar ao Dashboard', '<i class="fas fa-arrow-left mr-1"></i>Voltar', content)
        content = re.sub(r'<i class="fas fa-arrow-left"></i>\s*Voltar', '<i class="fas fa-arrow-left mr-1"></i>Voltar', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return False

def main():
    """Função principal"""
    print("🔄 Padronizando botões 'Voltar'...")
    
    html_files = find_html_files()
    updated = 0
    
    for file_path in html_files:
        if update_file(file_path):
            print(f"✅ Atualizado: {file_path}")
            updated += 1
    
    print(f"\n✅ Concluído! {updated} arquivos atualizados.")

if __name__ == '__main__':
    main()

