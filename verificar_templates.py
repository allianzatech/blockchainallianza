"""
Script para verificar se os templates estão corretos
"""

from pathlib import Path

templates_dir = Path('templates/testnet')
expected_titles = {
    'status.html': 'Status',
    'explorer.html': 'Explorer',
    'explorer_enhanced.html': 'Explorer',
    'faucet.html': 'Faucet',
    'quantum_security.html': 'Segurança Quântica',
    'interoperability.html': 'Interoperabilidade',
    'professional_tests.html': 'Testes Profissionais',
    'public_tests.html': 'Testes Públicos',
    'qrs3_verifier.html': 'Verificador QRS-3',
    'alz_niev.html': 'ALZ-NIEV',
    'dashboard.html': 'Dashboard'
}

print("🔍 Verificando templates...")
print("=" * 60)

for template_file in templates_dir.glob('*.html'):
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se tem ALZ-NIEV quando não deveria
        if template_file.name != 'alz_niev.html':
            if 'ALZ-NIEV' in content and 'Non-Intermediate Execution Validation' in content:
                print(f"❌ {template_file.name}: Contém conteúdo do ALZ-NIEV (ERRO!)")
            elif 'ELNI' in content and 'ZKEF' in content and 'UP-NMT' in content:
                print(f"❌ {template_file.name}: Contém as 5 camadas do ALZ-NIEV (ERRO!)")
            else:
                # Verificar título
                expected = expected_titles.get(template_file.name, '?')
                if expected in content or template_file.name.replace('.html', '').title() in content:
                    print(f"✅ {template_file.name}: OK")
                else:
                    print(f"⚠️  {template_file.name}: Título pode estar incorreto")
        else:
            # Para alz_niev.html, verificar se TEM o conteúdo correto
            if 'ALZ-NIEV' in content and 'ELNI' in content:
                print(f"✅ {template_file.name}: OK (ALZ-NIEV)")
            else:
                print(f"❌ {template_file.name}: Falta conteúdo do ALZ-NIEV")
                
    except Exception as e:
        print(f"❌ {template_file.name}: Erro ao ler - {e}")

print("=" * 60)

