/**
 * Basic Usage Examples
 */

import QSS from '@allianza/qss-js';

async function example1_GenerateProof() {
  console.log('📝 Example 1: Generate Quantum Proof');
  
  // Generate proof for Bitcoin transaction
  const proof = await QSS.generateProof('bitcoin', 'abc123...', {
    block_height: 12345,
    amount: '0.01',
  });
  
  console.log('Proof generated:', {
    chain: proof.asset_chain,
    tx: proof.asset_tx,
    proof_hash: proof.proof_hash,
    signature_scheme: proof.quantum_signature_scheme,
  });
}

async function example2_VerifyProof() {
  console.log('✅ Example 2: Verify Quantum Proof');
  
  const proof = await QSS.generateProof('ethereum', '0x...');
  
  const result = await QSS.verifyProof(proof);
  
  if (result.valid) {
    console.log('✅ Proof is valid!');
    console.log('Details:', result.verification_details);
  } else {
    console.log('❌ Proof is invalid');
  }
}

async function example3_AnchorBitcoin() {
  console.log('₿ Example 3: Anchor on Bitcoin');
  
  const proof = await QSS.generateProof('bitcoin', 'txid...');
  
  const instructions = await QSS.anchorOnBitcoin(proof, 'tb1q...');
  
  console.log('Anchor instructions:', {
    method: instructions.method,
    data: instructions.data,
    note: instructions.note,
  });
  
  // Use instructions.data with your Bitcoin library
  // e.g., bitcoinjs-lib
}

async function example4_AnchorEVM() {
  console.log('🔷 Example 4: Anchor on Ethereum/Polygon');
  
  const proof = await QSS.generateProof('polygon', '0x...');
  
  const { instructions, transactionData } = await QSS.anchorOnEVM(
    proof,
    '0x...', // QuantumSecurityAdapter contract
    'polygon'
  );
  
  console.log('Transaction data:', transactionData);
  
  // Sign and send with ethers.js or web3.js
  // const signer = new ethers.Wallet(privateKey, provider);
  // const tx = await signer.sendTransaction(transactionData);
}

async function example5_CustomClient() {
  console.log('⚙️ Example 5: Custom Client Configuration');
  
  const client = new QSS.Client({
    apiUrl: 'https://api.allianza.tech/qss',
    timeout: 60000,
    apiKey: 'your-api-key',
  });
  
  const proof = await client.generateProof('solana', 'txid...');
  const status = await client.getStatus();
  
  console.log('Service status:', status);
}

// Run examples
async function main() {
  try {
    await example1_GenerateProof();
    await example2_VerifyProof();
    await example3_AnchorBitcoin();
    await example4_AnchorEVM();
    await example5_CustomClient();
  } catch (error) {
    console.error('Error:', error);
  }
}

if (require.main === module) {
  main();
}

