#!/usr/bin/env python3
"""
Script para atualizar todos os arquivos HTML removendo CDN do Tailwind
e substituindo por CSS compilado local
"""

import os
import re
from pathlib import Path

def atualizar_arquivo_html(caminho_arquivo):
    """Atualiza um arquivo HTML removendo CDN do Tailwind"""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar se já foi atualizado
        if 'static/css/output.css' in conteudo:
            print(f"⏭️  {caminho_arquivo} já atualizado")
            return False
        
        # Verificar se usa CDN do Tailwind
        if 'cdn.tailwindcss.com' not in conteudo:
            return False
        
        # Substituir CDN do Tailwind por CSS local
        conteudo_novo = re.sub(
            r'<script src="https://cdn\.tailwindcss\.com"></script>',
            '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/output.css\') }}">',
            conteudo
        )
        
        # Remover estilos inline duplicados (já estão no CSS compilado)
        # Mas manter se houver estilos específicos do arquivo
        
        if conteudo_novo != conteudo:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)
            print(f"✅ {caminho_arquivo} atualizado")
            return True
        
        return False
    except Exception as e:
        print(f"❌ Erro ao atualizar {caminho_arquivo}: {e}")
        return False

def main():
    """Processa todos os arquivos HTML"""
    templates_dir = Path('templates')
    arquivos_atualizados = 0
    
    # Processar todos os arquivos HTML
    for html_file in templates_dir.rglob('*.html'):
        if atualizar_arquivo_html(html_file):
            arquivos_atualizados += 1
    
    # Processar arquivos HTML na raiz
    for html_file in Path('.').glob('*.html'):
        if atualizar_arquivo_html(html_file):
            arquivos_atualizados += 1
    
    print(f"\n✅ Total de arquivos atualizados: {arquivos_atualizados}")

if __name__ == '__main__':
    main()










