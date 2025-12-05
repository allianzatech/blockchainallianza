#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adiciona hover ao botão voltar se não existir"""

from pathlib import Path
import re

template_dir = Path('templates')

for html_file in template_dir.rglob('*.html'):
    content = html_file.read_text(encoding='utf-8')
    
    # Verificar se tem .btn-back mas não tem .btn-back:hover
    if '.btn-back {' in content and '.btn-back:hover' not in content:
        # Adicionar hover após .btn-back
        content = re.sub(
            r'(\.btn-back \{[^}]+\})',
            r'\1\n        .btn-back:hover {\n            background: #4b5563;\n        }',
            content,
            flags=re.DOTALL
        )
        html_file.write_text(content, encoding='utf-8')
        print(f"✅ Adicionado hover em: {html_file}")

print("✅ Concluído!")

