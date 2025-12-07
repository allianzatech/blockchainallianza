# 🎬 Guia para Criar Demo GIF - Allianza Blockchain

**Objetivo:** Criar um GIF de 15 segundos mostrando o testnet funcionando com 82+ transações.

---

## 📋 Checklist Pré-Gravação

- [ ] Testnet rodando e acessível
- [ ] Faucet funcionando
- [ ] Explorer mostrando transações
- [ ] API QSS respondendo
- [ ] Navegador aberto e pronto

---

## 🎥 Script de Gravação (15 segundos)

### Segunda 0-3: Dashboard Principal
1. Abrir testnet no navegador (ex: `https://testnet.allianza.tech`)
2. Mostrar dashboard com métricas:
   - Total de Blocos: 8+
   - Total de Transações: 82+
   - TPS: 0.02/s
   - Latência: 0.02ms
3. **Zoom suave** nas métricas principais

### Segunda 3-6: Faucet Funcionando
1. Clicar em "Faucet" no menu
2. Mostrar página do faucet
3. Gerar uma carteira (ou usar uma existente)
4. Solicitar tokens (clicar em "Request Tokens")
5. Mostrar mensagem de sucesso: "✅ Tokens enviados!"
6. Mostrar TX Hash gerado

### Segunda 6-9: Explorer com Transações
1. Clicar em "Explorer" no menu
2. Mostrar lista de transações recentes
3. **Scroll suave** pela lista mostrando múltiplas transações
4. Destacar uma transação específica (a que acabou de ser criada)
5. Mostrar detalhes: De → Para, Valor, Timestamp

### Segunda 9-12: Download de Proof
1. Na transação destacada, clicar em "Download Proof"
2. Mostrar que o download funciona (ou mostrar JSON da proof)
3. Destacar que é uma prova quântica válida

### Segunda 12-15: Fechamento
1. Voltar ao dashboard
2. Mostrar que o número de transações aumentou (83+)
3. **Zoom out** mostrando todo o dashboard
4. Fade out suave

---

## 🛠️ Ferramentas Recomendadas

### Para Gravar Tela (Windows)
- **OBS Studio** (gratuito, melhor qualidade)
- **ScreenToGif** (gratuito, direto para GIF)
- **ShareX** (gratuito, fácil de usar)
- **Camtasia** (pago, profissional)

### Para Editar GIF
- **ScreenToGif** (edição básica)
- **GIMP** (gratuito, edição avançada)
- **Photoshop** (pago, profissional)
- **EZGIF.com** (online, gratuito)

---

## 📐 Configurações Recomendadas

### Resolução
- **1920x1080** (Full HD) ou **1280x720** (HD)
- Proporção: 16:9

### FPS (Frames Per Second)
- **10-15 FPS** para GIF (menor tamanho)
- **30 FPS** se for converter para vídeo depois

### Duração
- **Exatamente 15 segundos**
- Não mais, não menos

### Tamanho do Arquivo
- **Máximo: 10 MB** (para GitHub)
- **Ideal: 5-8 MB**

---

## 🎨 Dicas de Produção

### 1. Preparação
- Feche abas desnecessárias do navegador
- Use modo escuro (já está no projeto)
- Aumente zoom do navegador para 125% (melhor visualização)
- Limpe cache se necessário

### 2. Durante a Gravação
- **Movimentos suaves** (não mova o mouse muito rápido)
- **Pause de 0.5s** antes de cada clique (para clareza)
- **Highlight visual** nos elementos importantes (cursor, botões)
- **Narração opcional** (pode adicionar depois)

### 3. Pós-Produção
- **Cortar** início/fim desnecessários
- **Acelerar** partes lentas (se necessário)
- **Adicionar texto** (opcional): "Live Testnet", "82+ Transactions"
- **Otimizar** tamanho do arquivo

---

## 📝 Passo a Passo Detalhado

### Passo 1: Preparar Ambiente
```bash
# 1. Certifique-se que o testnet está rodando
# 2. Abra o navegador em modo anônimo (para não ter cache)
# 3. Acesse: https://testnet.allianza.tech
# 4. Verifique que há 82+ transações no explorer
```

### Passo 2: Configurar Ferramenta de Gravação

**Usando ScreenToGif (Recomendado):**
1. Baixe: https://www.screentogif.com/
2. Abra o programa
3. Clique em "Recorder"
4. Selecione a área do navegador
5. Configure:
   - FPS: 10-15
   - Resolução: 1920x1080 ou menor
   - Codec: GIF

### Passo 3: Gravar
1. Inicie a gravação
2. Siga o script acima (15 segundos)
3. Pare a gravação

### Passo 4: Editar
1. No ScreenToGif, você pode:
   - Remover frames desnecessários
   - Adicionar texto
   - Ajustar velocidade
   - Redimensionar
2. Exporte como GIF

### Passo 5: Otimizar
1. Use https://ezgif.com/optimize
2. Upload o GIF
3. Otimize (pode reduzir 50-70% do tamanho)
4. Baixe o resultado

---

## 🎯 Resultado Esperado

O GIF final deve mostrar:
- ✅ Dashboard com métricas (82+ transações)
- ✅ Faucet funcionando (solicitar tokens)
- ✅ Explorer mostrando transações
- ✅ Download de proof funcionando
- ✅ Tudo em 15 segundos, suave e profissional

---

## 📦 Onde Salvar

Salve o arquivo como:
- `demo.gif` na raiz do repositório
- Ou `docs/demo.gif` se preferir organizar

---

## ✅ Checklist Final

- [ ] GIF gravado (15 segundos)
- [ ] Mostra dashboard com 82+ transações
- [ ] Mostra faucet funcionando
- [ ] Mostra explorer com transações
- [ ] Mostra download de proof
- [ ] Tamanho < 10 MB
- [ ] Qualidade boa (legível)
- [ ] Movimentos suaves
- [ ] Salvo como `demo.gif`

---

## 🚀 Próximo Passo

Depois de criar o GIF:
1. Adicione no README.md (no topo)
2. Commit e push:
   ```bash
   git add demo.gif README.md
   git commit -m "Adicionar demo GIF do testnet funcionando"
   git push origin main
   ```

---

**Dica:** Se não conseguir gravar agora, pode usar um serviço online como **Loom** ou **CloudApp** para gravar e depois converter para GIF.

