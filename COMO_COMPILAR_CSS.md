# 🎨 Como Compilar o CSS do Tailwind

## Passo a Passo

### 1. Instalar Node.js e NPM
Certifique-se de ter Node.js instalado:
```bash
node --version
npm --version
```

### 2. Instalar Dependências
```bash
npm install
```

Isso instalará o Tailwind CSS como dependência de desenvolvimento.

### 3. Compilar CSS

#### Para Produção (minificado):
```bash
npm run build-css
```

Isso criará o arquivo `static/css/output.css` com o CSS compilado e minificado.

#### Para Desenvolvimento (com watch):
```bash
npm run watch-css
```

Isso compilará o CSS automaticamente sempre que você fizer alterações.

### 4. Verificar
Após compilar, verifique se o arquivo foi criado:
```bash
ls static/css/output.css
```

### 5. Atualizar Templates
Todos os templates HTML já foram atualizados para usar:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">
```

---

## ⚠️ Importante

- **Sempre compile o CSS antes de fazer deploy em produção**
- O arquivo `output.css` não está no repositório (deve ser gerado)
- Adicione `static/css/output.css` ao `.gitignore` se necessário
- Ou adicione ao repositório se preferir versionar o CSS compilado

---

## 🔄 Atualização Automática

Para atualizar todos os templates HTML automaticamente:
```bash
python atualizar_tailwind_html.py
```

---

## 📝 Estrutura de Arquivos

```
static/
  css/
    input.css      # Arquivo de entrada (com @tailwind directives)
    output.css     # Arquivo compilado (gerado pelo build)
```










