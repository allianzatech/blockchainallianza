# Configuração do Favicon Allianza

## ✅ O que foi feito:

1. **Estrutura criada:**
   - Diretório `static/images/` criado para armazenar o favicon
   - Referências ao favicon adicionadas nos templates principais:
     - `templates/testnet/interoperability.html`
     - `templates/testnet/dashboard.html`
     - `templates/testnet/cross_chain_test.html`
     - `templates/testnet/public_proofs.html`

2. **Tags HTML adicionadas:**
   ```html
   <!-- Favicon Allianza -->
   <link rel="icon" type="image/png" href="{{ url_for('static', filename='images/favicon.png') }}">
   <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
   <link rel="apple-touch-icon" href="{{ url_for('static', filename='images/favicon.png') }}">
   ```

## 📋 Próximos passos:

### Opção 1: Usar PNG (Recomendado)
1. Salve a imagem do triângulo dourado como `favicon.png`
2. Coloque em `static/images/favicon.png`
3. Tamanho recomendado: 32x32, 64x64 ou 128x128 pixels

### Opção 2: Usar ICO (Tradicional)
1. Converta a imagem para formato `.ico`
2. Coloque em `static/favicon.ico` (raiz do diretório static)
3. O navegador usará automaticamente

### Opção 3: Ambos (Melhor compatibilidade)
1. Coloque `favicon.png` em `static/images/favicon.png`
2. Coloque `favicon.ico` em `static/favicon.ico`
3. O sistema tentará usar ambos

## 🔧 Conversão de imagem:

Se você tiver a imagem em outro formato, pode converter usando:

### Online:
- https://favicon.io/favicon-converter/
- https://www.favicon-generator.org/

### Python (se tiver Pillow instalado):
```python
from PIL import Image

# Converter PNG para ICO
img = Image.open('triangulo_dourado.png')
img.save('static/favicon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48)])
```

## 📝 Nota:

Após adicionar a imagem, reinicie o servidor Flask para que as mudanças sejam aplicadas. O favicon aparecerá automaticamente na aba do navegador.

