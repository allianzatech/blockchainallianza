/**
 * Teste local do SDK QSS
 * Testa funcionalidades sem depender da API remota
 */

const axios = require('axios');

// Testar com API local
const API_URL = 'http://localhost:5008/api/qss';

async function testLocalConnection() {
  console.log('🔍 Testando conexão local com QSS API...\n');
  console.log('   URL:', API_URL);
  console.log('');
  
  try {
    const response = await axios.get(`${API_URL}/status`, {
      timeout: 5000
    });
    
    console.log('✅ Conexão estabelecida!');
    console.log('\n📊 Status do serviço:');
    console.log(JSON.stringify(response.data, null, 2));
    return true;
  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.log('⚠️  Servidor local não está rodando.');
      console.log('   Para iniciar:');
      console.log('   1. Execute: python allianza_blockchain.py');
      console.log('   2. Ou: python wsgi.py');
      console.log('   3. Aguarde a mensagem: "🔐 Quantum Security Service (QSS) - API registrada!"');
    } else if (error.response) {
      console.log('⚠️  Servidor respondeu, mas endpoint não encontrado.');
      console.log('   Status:', error.response.status);
    } else {
      console.log('⚠️  Erro de conexão:', error.message);
    }
    return false;
  }
}

async function testSDKStructure() {
  console.log('\n📦 Testando estrutura do SDK...\n');
  
  try {
    // Verificar se o build foi criado
    const fs = require('fs');
    const path = require('path');
    
    const distPath = path.join(__dirname, 'dist');
    const indexJs = path.join(distPath, 'index.js');
    const indexDts = path.join(distPath, 'index.d.ts');
    
    console.log('🔍 Verificando arquivos compilados...');
    
    if (fs.existsSync(indexJs)) {
      const stats = fs.statSync(indexJs);
      console.log('   ✅ dist/index.js existe (' + (stats.size / 1024).toFixed(2) + ' KB)');
    } else {
      console.log('   ❌ dist/index.js não encontrado');
      return false;
    }
    
    if (fs.existsSync(indexDts)) {
      const stats = fs.statSync(indexDts);
      console.log('   ✅ dist/index.d.ts existe (' + (stats.size / 1024).toFixed(2) + ' KB)');
    } else {
      console.log('   ❌ dist/index.d.ts não encontrado');
      return false;
    }
    
    // Verificar conteúdo básico
    const indexJsContent = fs.readFileSync(indexJs, 'utf8');
    if (indexJsContent.includes('QSSClient') && indexJsContent.includes('generateProof')) {
      console.log('   ✅ Código compilado contém funcionalidades principais');
    } else {
      console.log('   ⚠️  Código compilado pode estar incompleto');
    }
    
    return true;
  } catch (error) {
    console.error('   ❌ Erro ao verificar estrutura:', error.message);
    return false;
  }
}

async function testPackageJson() {
  console.log('\n📄 Verificando package.json...\n');
  
  try {
    const fs = require('fs');
    const path = require('path');
    const packageJson = JSON.parse(
      fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8')
    );
    
    console.log('✅ package.json válido');
    console.log('   Nome:', packageJson.name);
    console.log('   Versão:', packageJson.version);
    console.log('   Descrição:', packageJson.description);
    console.log('   Main:', packageJson.main);
    console.log('   Types:', packageJson.types);
    console.log('   Dependencies:', Object.keys(packageJson.dependencies || {}).length, 'pacotes');
    
    return true;
  } catch (error) {
    console.error('   ❌ Erro ao verificar package.json:', error.message);
    return false;
  }
}

async function runAllTests() {
  console.log('🚀 Testes do SDK QSS - Versão Local\n');
  console.log('='.repeat(60));
  console.log('');
  
  // Teste 1: Estrutura do SDK
  const structureOk = await testSDKStructure();
  
  // Teste 2: package.json
  const packageOk = await testPackageJson();
  
  // Teste 3: Conexão local (opcional)
  const connectionOk = await testLocalConnection();
  
  console.log('\n' + '='.repeat(60));
  console.log('\n📊 Resumo dos Testes:\n');
  console.log('   Estrutura do SDK:', structureOk ? '✅ OK' : '❌ FALHOU');
  console.log('   package.json:', packageOk ? '✅ OK' : '❌ FALHOU');
  console.log('   Conexão Local:', connectionOk ? '✅ OK' : '⚠️  Não disponível');
  
  if (structureOk && packageOk) {
    console.log('\n✅ SDK está pronto para uso!');
    console.log('\n📚 Próximos passos:');
    console.log('   1. Para testar com API local:');
    console.log('      - Inicie o servidor: python allianza_blockchain.py');
    console.log('      - Execute: node test-sdk.js');
    console.log('   2. Para publicar no NPM:');
    console.log('      - npm login');
    console.log('      - npm publish --access public');
  } else {
    console.log('\n⚠️  Alguns testes falharam. Verifique os erros acima.');
  }
}

// Executar testes
runAllTests().catch(error => {
  console.error('\n❌ Erro fatal:', error);
  process.exit(1);
});

