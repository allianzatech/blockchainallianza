"""
Script para atualizar todos os links /testnet para / nos templates
"""

import re
from pathlib import Path

def atualizar_links(arquivo_path):
    """Atualiza links /testnet para /"""
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        conteudo_original = conteudo
        
        # Substituir href="/testnet" por href="/"
        conteudo = re.sub(r'href="/testnet"', 'href="/"', conteudo)
        
        # Substituir href="/testnet/ por href="/"
        conteudo = re.sub(r'href="/testnet/', 'href="/', conteudo)
        
        # Substituir fetch('/testnet/ por fetch('/'
        conteudo = re.sub(r"fetch\('/testnet/", "fetch('/", conteudo)
        
        # Substituir fetch("/testnet/ por fetch("/
        conteudo = re.sub(r'fetch\("/testnet/', 'fetch("/', conteudo)
        
        if conteudo != conteudo_original:
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            substituicoes = len(re.findall(r'/testnet', conteudo_original))
            print(f"✅ {arquivo_path.name}: {substituicoes} links atualizados")
            return True
        else:
            print(f"ℹ️  {arquivo_path.name}: Nenhum link para atualizar")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo_path.name}: {e}")
        return False

def main():
    """Atualiza links em todos os templates"""
    templates_dir = Path('templates/testnet')
    
    if not templates_dir.exists():
        print(f"❌ Diretório {templates_dir} não encontrado")
        return
    
    arquivos_html = list(templates_dir.glob('*.html'))
    
    if not arquivos_html:
        print("❌ Nenhum arquivo HTML encontrado")
        return
    
    print(f"🔍 Encontrados {len(arquivos_html)} arquivos HTML")
    print("=" * 60)
    
    atualizados = 0
    for arquivo in arquivos_html:
        if atualizar_links(arquivo):
            atualizados += 1
    
    print("=" * 60)
    print(f"✅ Processamento concluído: {atualizados} arquivos atualizados de {len(arquivos_html)}")

if __name__ == '__main__':
    main()

