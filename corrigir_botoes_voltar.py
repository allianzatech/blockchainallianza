#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Corrigir Botões Voltar - Usar history.back() em vez de href="/"
"""

import os
from pathlib import Path
import re

TEMPLATES_DIR = Path("templates/testnet")

def corrigir_botoes_voltar():
    """Corrige todos os botões Voltar para usar history.back()"""
    print("=" * 70)
    print("🔧 CORRIGINDO BOTÕES VOLTAR")
    print("=" * 70)
    print()
    
    arquivos = list(TEMPLATES_DIR.glob("*.html"))
    corrigidos = 0
    
    for arquivo in arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            conteudo_original = conteudo
            
            # Substituir href="/" por onclick="history.back()"
            conteudo = re.sub(
                r'<a\s+([^>]*?)href=["\']/["\']([^>]*?)class=["\']btn-back([^>]*?)>Voltar</a>',
                r'<a \1onclick="history.back(); return false;" \2class="btn-back\3>Voltar</a>',
                conteudo,
                flags=re.IGNORECASE
            )
            
            # Também substituir se não tiver class
            conteudo = re.sub(
                r'<a\s+([^>]*?)href=["\']/["\']([^>]*?)>Voltar</a>',
                r'<a \1onclick="history.back(); return false;">Voltar</a>',
                conteudo,
                flags=re.IGNORECASE
            )
            
            # Substituir padrões mais simples
            conteudo = re.sub(
                r'href=["\']/["\']\s*class=["\']btn-back',
                r'onclick="history.back(); return false;" class="btn-back',
                conteudo
            )
            
            if conteudo != conteudo_original:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                print(f"✅ {arquivo.name}")
                corrigidos += 1
            else:
                print(f"ℹ️  {arquivo.name} (sem mudanças)")
                
        except Exception as e:
            print(f"❌ Erro em {arquivo.name}: {e}")
    
    print()
    print("=" * 70)
    print(f"✅ {corrigidos} arquivo(s) corrigido(s)")
    print("=" * 70)

if __name__ == "__main__":
    corrigir_botoes_voltar()

