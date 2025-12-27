#!/usr/bin/env python3
"""
Script para tornar todos os templates da testnet responsivos para mobile
Adiciona viewport correto e link para CSS mobile em todos os templates
"""

import os
import re
from pathlib import Path

TEMPLATES_DIR = Path("templates/testnet")
CSS_LINK = '<link rel="stylesheet" href="/static/css/testnet-mobile.css">'
VIEWPORT_META = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">'
MOBILE_META = '<meta name="mobile-web-app-capable" content="yes">'

def update_template(file_path):
    """Atualiza um template para ser mobile responsivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # 1. Atualizar viewport meta tag
        viewport_patterns = [
            r'<meta\s+name="viewport"\s+content="[^"]*">',
            r'<meta\s+name=["\']viewport["\']\s+content=["\'][^"\']*["\']>',
        ]
        
        for pattern in viewport_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, VIEWPORT_META, content)
                changes_made.append("Viewport atualizado")
                break
        else:
            # Adicionar viewport se não existir
            if '<head>' in content:
                content = content.replace('<head>', f'<head>\n    {VIEWPORT_META}', 1)
                changes_made.append("Viewport adicionado")
        
        # 2. Adicionar mobile-web-app-capable meta
        if MOBILE_META not in content:
            if VIEWPORT_META in content:
                content = content.replace(VIEWPORT_META, f'{VIEWPORT_META}\n    {MOBILE_META}', 1)
                changes_made.append("Mobile meta adicionado")
        
        # 3. Adicionar link para CSS mobile (após viewport ou antes de </head>)
        if CSS_LINK not in content:
            # Tentar adicionar após viewport
            if VIEWPORT_META in content:
                content = content.replace(
                    VIEWPORT_META,
                    f'{VIEWPORT_META}\n    {CSS_LINK}',
                    1
                )
                changes_made.append("CSS mobile link adicionado")
            elif '</head>' in content:
                # Adicionar antes de </head>
                content = content.replace('</head>', f'    {CSS_LINK}\n</head>', 1)
                changes_made.append("CSS mobile link adicionado")
        
        # Só escrever se houver mudanças
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        
        return False, []
    
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False, []

def main():
    """Processa todos os templates"""
    if not TEMPLATES_DIR.exists():
        print(f"❌ Diretório não encontrado: {TEMPLATES_DIR}")
        return
    
    html_files = list(TEMPLATES_DIR.glob("*.html"))
    
    if not html_files:
        print(f"⚠️  Nenhum arquivo HTML encontrado em {TEMPLATES_DIR}")
        return
    
    print(f"📱 Tornando {len(html_files)} templates responsivos para mobile...\n")
    
    updated = 0
    skipped = 0
    
    for html_file in sorted(html_files):
        was_updated, changes = update_template(html_file)
        
        if was_updated:
            updated += 1
            print(f"✅ {html_file.name}")
            for change in changes:
                print(f"   • {change}")
        else:
            skipped += 1
            print(f"⏭️  {html_file.name} (já atualizado ou sem mudanças)")
    
    print(f"\n📊 Resumo:")
    print(f"   ✅ Atualizados: {updated}")
    print(f"   ⏭️  Pulados: {skipped}")
    print(f"   📁 Total: {len(html_files)}")
    
    if updated > 0:
        print(f"\n🎉 {updated} templates atualizados com sucesso!")
        print(f"💡 Certifique-se de que o arquivo /static/css/testnet-mobile.css existe")

if __name__ == "__main__":
    main()

