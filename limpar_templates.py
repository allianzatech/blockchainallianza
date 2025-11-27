"""
Script para limpar templates HTML que têm múltiplos documentos concatenados
Mantém apenas o primeiro documento HTML de cada arquivo
"""

import os
from pathlib import Path

def limpar_template(arquivo_path):
    """Remove conteúdo após o primeiro </html>"""
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Encontrar o primeiro </html> seguido de quebra de linha
        primeiro_fim = conteudo.find('</html>')
        if primeiro_fim == -1:
            print(f"⚠️  {arquivo_path.name}: Não encontrou </html>")
            return False
        
        # Encontrar o final do primeiro documento (após </html> e possíveis espaços)
        fim_doc = primeiro_fim + 7  # 7 = len('</html>')
        
        # Pular espaços em branco e quebras de linha
        while fim_doc < len(conteudo) and conteudo[fim_doc] in ['\n', '\r', ' ', '\t']:
            fim_doc += 1
        
        # Se há mais conteúdo após o primeiro </html>, remover
        if fim_doc < len(conteudo):
            conteudo_limpo = conteudo[:fim_doc]
            
            # Verificar se há outro <!DOCTYPE após o primeiro </html>
            if '<!DOCTYPE' in conteudo[fim_doc:]:
                print(f"✅ {arquivo_path.name}: Removendo {len(conteudo) - len(conteudo_limpo)} caracteres duplicados")
                with open(arquivo_path, 'w', encoding='utf-8') as f:
                    f.write(conteudo_limpo)
                return True
            else:
                print(f"ℹ️  {arquivo_path.name}: Já está limpo")
                return False
        else:
            print(f"ℹ️  {arquivo_path.name}: Já está limpo")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo_path.name}: {e}")
        return False

def main():
    """Limpa todos os templates em templates/testnet/"""
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
    
    limpos = 0
    for arquivo in arquivos_html:
        if limpar_template(arquivo):
            limpos += 1
    
    print("=" * 60)
    print(f"✅ Processamento concluído: {limpos} arquivos limpos de {len(arquivos_html)}")

if __name__ == '__main__':
    main()

