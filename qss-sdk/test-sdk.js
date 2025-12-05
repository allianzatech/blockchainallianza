/**
 * Teste simples do SDK QSS
 * Testa conexão com a API e funcionalidades básicas
 */

const axios = require('axios');

const API_URL = 'https://testnet.allianza.tech/api/qss';

async function testQSSStatus() {
  console.log('🔍 Testando status do serviço QSS...\n');
  
  try {
    const response = await axios.get(`${API_URL}/status`);
    console.log('✅ Status do serviço:');
    console.log(JSON.stringify(response.data, null, 2));
    return true;
  } catch (error) {
    console.error('❌ Erro ao verificar status:', error.message);
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', error.response.data);
    }
    return false;
  }
}

async function testGenerateProof() {
  console.log('\n🔐 Testando geração de prova quântica...\n');
  
  const testData = {
    chain: 'bitcoin',
    tx_hash: 'test_tx_hash_' + Date.now(),
    metadata: {
      block_height: 12345,
      amount: '0.01',
      timestamp: Math.floor(Date.now() / 1000)
    }
  };
  
  console.log('📝 Dados de teste:');
  console.log(JSON.stringify(testData, null, 2));
  console.log('\n');
  
  try {
    const response = await axios.post(`${API_URL}/generate-proof`, testData, {
      timeout: 30000
    });
    
    if (response.data.success && response.data.quantum_proof) {
      console.log('✅ Prova quântica gerada com sucesso!');
      console.log('\n📊 Detalhes da prova:');
      const proof = response.data.quantum_proof;
      console.log('   Chain:', proof.asset_chain);
      console.log('   TX Hash:', proof.asset_tx);
      console.log('   Signature Scheme:', proof.quantum_signature_scheme);
      console.log('   Proof Hash:', proof.proof_hash);
      console.log('   Block Height:', proof.block_height);
      console.log('   Timestamp:', new Date(proof.timestamp * 1000).toISOString());
      console.log('   Valid:', proof.valid);
      
      return response.data.quantum_proof;
    } else {
      console.error('❌ Resposta inválida:', response.data);
      return null;
    }
  } catch (error) {
    console.error('❌ Erro ao gerar prova:', error.message);
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', JSON.stringify(error.response.data, null, 2));
    }
    return null;
  }
}

async function testVerifyProof(proof) {
  if (!proof) {
    console.log('\n⚠️  Pulando verificação (prova não gerada)');
    return;
  }
  
  console.log('\n✅ Testando verificação de prova...\n');
  
  try {
    const response = await axios.post(`${API_URL}/verify-proof`, {
      quantum_proof: proof
    }, {
      timeout: 30000
    });
    
    if (response.data.success !== undefined) {
      console.log('✅ Verificação concluída!');
      console.log('\n📊 Resultado:');
      console.log('   Success:', response.data.success);
      console.log('   Valid:', response.data.valid);
      
      if (response.data.verification_details) {
        console.log('\n🔍 Detalhes da verificação:');
        const details = response.data.verification_details;
        console.log('   Signature Valid:', details.signature_valid);
        console.log('   Merkle Proof Valid:', details.merkle_proof_valid);
        console.log('   Consensus Proof Valid:', details.consensus_proof_valid);
        console.log('   Proof Hash Valid:', details.proof_hash_valid);
        console.log('   Timestamp Valid:', details.timestamp_valid);
      }
      
      if (response.data.proof_info) {
        console.log('\n📝 Informações da prova:');
        const info = response.data.proof_info;
        console.log('   Chain:', info.asset_chain);
        console.log('   TX:', info.asset_tx);
        console.log('   Verified By:', info.verified_by);
      }
    } else {
      console.error('❌ Resposta inválida:', response.data);
    }
  } catch (error) {
    console.error('❌ Erro ao verificar prova:', error.message);
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', JSON.stringify(error.response.data, null, 2));
    }
  }
}

async function testAnchorInstructions(proof) {
  if (!proof) {
    console.log('\n⚠️  Pulando instruções de ancoragem (prova não gerada)');
    return;
  }
  
  console.log('\n🔗 Testando instruções de ancoragem...\n');
  
  const testChains = ['bitcoin', 'ethereum', 'polygon'];
  
  for (const chain of testChains) {
    console.log(`📡 Testando ancoragem em ${chain}...`);
    
    try {
      const response = await axios.post(`${API_URL}/anchor-proof`, {
        quantum_proof: proof,
        target_chain: chain
      }, {
        timeout: 30000
      });
      
      if (response.data.success && response.data.anchor_instructions) {
        console.log(`   ✅ Instruções geradas para ${chain}`);
        const instructions = response.data.anchor_instructions;
        console.log(`   Método: ${instructions.method}`);
        if (instructions.data) {
          console.log(`   Data: ${instructions.data.substring(0, 50)}...`);
        }
        if (instructions.proof_hash) {
          console.log(`   Proof Hash: ${instructions.proof_hash}`);
        }
      } else {
        console.log(`   ⚠️  Resposta inválida para ${chain}`);
      }
    } catch (error) {
      console.error(`   ❌ Erro ao obter instruções para ${chain}:`, error.message);
    }
    
    console.log('');
  }
}

async function runAllTests() {
  console.log('🚀 Iniciando testes do SDK QSS\n');
  console.log('='.repeat(60));
  console.log('');
  
  // Teste 1: Status
  const statusOk = await testQSSStatus();
  
  if (!statusOk) {
    console.log('\n⚠️  Serviço QSS não está disponível. Testes restantes podem falhar.');
    console.log('   Verifique se a API está rodando em:', API_URL);
    return;
  }
  
  // Teste 2: Gerar prova
  const proof = await testGenerateProof();
  
  // Teste 3: Verificar prova
  await testVerifyProof(proof);
  
  // Teste 4: Instruções de ancoragem
  await testAnchorInstructions(proof);
  
  console.log('='.repeat(60));
  console.log('\n✅ Testes concluídos!');
  console.log('\n📚 Próximos passos:');
  console.log('   1. Compilar TypeScript: npm run build');
  console.log('   2. Executar testes TypeScript: npm test');
  console.log('   3. Publicar no NPM: npm publish --access public');
}

// Executar testes
runAllTests().catch(error => {
  console.error('\n❌ Erro fatal:', error);
  process.exit(1);
});

