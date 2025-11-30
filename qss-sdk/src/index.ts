/**
 * @allianza/qss-js
 * Quantum Security Service SDK
 * 
 * Bring quantum-resistant security to any blockchain
 * 
 * @example
 * ```typescript
 * import QSS from '@allianza/qss-js';
 * 
 * const proof = await QSS.generateProof('bitcoin', txid);
 * await QSS.verifyProof(proof);
 * await QSS.anchorOnBitcoin(proof);
 * ```
 */

import axios, { AxiosInstance } from 'axios';
import { ethers } from 'ethers';

// ============================================================================
// TYPES
// ============================================================================

export interface QuantumProof {
  asset_chain: string;
  asset_tx: string;
  quantum_signature: string;
  quantum_signature_scheme: string;
  merkle_root?: string;
  merkle_proof?: MerkleProof;
  consensus_proof?: ConsensusProof;
  verified_by: string;
  block_height: number;
  timestamp: number;
  proof_hash: string;
  valid: boolean;
  keypair_id?: string;
}

export interface MerkleProof {
  merkle_root: string;
  leaf_hash: string;
  proof_path: string[];
  tree_depth: number;
  chain_id: string;
}

export interface ConsensusProof {
  consensus_type: string;
  block_height: number;
  validator_set_hash?: string;
}

export interface GenerateProofRequest {
  chain: string;
  tx_hash: string;
  metadata?: {
    block_height?: number;
    timestamp?: number;
    from?: string;
    to?: string;
    amount?: string;
    [key: string]: any;
  };
}

export interface VerifyProofRequest {
  quantum_proof: QuantumProof;
}

export interface AnchorProofRequest {
  quantum_proof: QuantumProof;
  target_chain: string;
  target_address?: string;
}

export interface AnchorInstructions {
  method: string;
  data?: string;
  format?: string;
  max_size?: number;
  transaction_template?: any;
  note?: string;
  contract_function?: string;
  proof_hash?: string;
  gas_estimate?: number;
  instruction?: string;
  account_size?: number;
  rent_exempt?: boolean;
}

export interface QSSConfig {
  apiUrl?: string;
  timeout?: number;
  apiKey?: string;
}

export interface VerificationResult {
  success: boolean;
  valid: boolean;
  verification_details?: {
    signature_valid: boolean;
    merkle_proof_valid: boolean;
    consensus_proof_valid: boolean;
    proof_hash_valid: boolean;
    timestamp_valid: boolean;
  };
  proof_info?: {
    asset_chain: string;
    asset_tx: string;
    verified_by: string;
    timestamp: number;
  };
  error?: string;
}

// ============================================================================
// QSS CLIENT
// ============================================================================

export class QSSClient {
  private apiUrl: string;
  private axiosInstance: AxiosInstance;
  private apiKey?: string;

  constructor(config: QSSConfig = {}) {
    this.apiUrl = config.apiUrl || 'https://testnet.allianza.tech/api/qss';
    this.apiKey = config.apiKey;

    this.axiosInstance = axios.create({
      baseURL: this.apiUrl,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        ...(this.apiKey && { 'Authorization': `Bearer ${this.apiKey}` }),
      },
    });
  }

  /**
   * Generate quantum proof for a transaction
   * 
   * @param chain - Blockchain name (bitcoin, ethereum, polygon, etc.)
   * @param txHash - Transaction hash
   * @param metadata - Optional metadata about the transaction
   * @returns Quantum proof object
   * 
   * @example
   * ```typescript
   * const proof = await qss.generateProof('bitcoin', 'abc123...', {
   *   block_height: 12345,
   *   amount: '0.01'
   * });
   * ```
   */
  async generateProof(
    chain: string,
    txHash: string,
    metadata?: GenerateProofRequest['metadata']
  ): Promise<QuantumProof> {
    try {
      const response = await this.axiosInstance.post<{
        success: boolean;
        quantum_proof: QuantumProof;
        verification_url?: string;
        explorer_url?: string;
        anchor_instructions?: Record<string, any>;
      }>('/generate-proof', {
        chain: chain.toLowerCase(),
        tx_hash: txHash,
        metadata: metadata || {},
      });

      if (!response.data.success || !response.data.quantum_proof) {
        throw new Error('Failed to generate quantum proof');
      }

      return response.data.quantum_proof;
    } catch (error: any) {
      if (error.response) {
        throw new Error(
          `QSS API Error: ${error.response.data?.error || error.message}`
        );
      }
      throw new Error(`Network Error: ${error.message}`);
    }
  }

  /**
   * Verify a quantum proof
   * 
   * @param proof - Quantum proof object to verify
   * @returns Verification result
   * 
   * @example
   * ```typescript
   * const result = await qss.verifyProof(proof);
   * if (result.valid) {
   *   console.log('Proof is valid!');
   * }
   * ```
   */
  async verifyProof(proof: QuantumProof): Promise<VerificationResult> {
    try {
      const response = await this.axiosInstance.post<VerificationResult>(
        '/verify-proof',
        {
          quantum_proof: proof,
        }
      );

      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new Error(
          `QSS API Error: ${error.response.data?.error || error.message}`
        );
      }
      throw new Error(`Network Error: ${error.message}`);
    }
  }

  /**
   * Get anchor instructions for a blockchain
   * 
   * @param proof - Quantum proof object
   * @param targetChain - Target blockchain to anchor the proof
   * @param targetAddress - Optional target address
   * @returns Anchor instructions
   * 
   * @example
   * ```typescript
   * const instructions = await qss.getAnchorInstructions(
   *   proof,
   *   'bitcoin',
   *   'tb1q...'
   * );
   * ```
   */
  async getAnchorInstructions(
    proof: QuantumProof,
    targetChain: string,
    targetAddress?: string
  ): Promise<AnchorInstructions> {
    try {
      const response = await this.axiosInstance.post<{
        success: boolean;
        target_chain: string;
        proof_hash: string;
        anchor_instructions: AnchorInstructions;
        verification_url?: string;
      }>('/anchor-proof', {
        quantum_proof: proof,
        target_chain: targetChain.toLowerCase(),
        target_address: targetAddress,
      });

      if (!response.data.success || !response.data.anchor_instructions) {
        throw new Error('Failed to get anchor instructions');
      }

      return response.data.anchor_instructions;
    } catch (error: any) {
      if (error.response) {
        throw new Error(
          `QSS API Error: ${error.response.data?.error || error.message}`
        );
      }
      throw new Error(`Network Error: ${error.message}`);
    }
  }

  /**
   * Get QSS service status
   * 
   * @returns Service status information
   */
  async getStatus(): Promise<any> {
    try {
      const response = await this.axiosInstance.get('/status');
      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new Error(
          `QSS API Error: ${error.response.data?.error || error.message}`
        );
      }
      throw new Error(`Network Error: ${error.message}`);
    }
  }
}

// ============================================================================
// BLOCKCHAIN-SPECIFIC HELPERS
// ============================================================================

export class BitcoinAnchor {
  /**
   * Create Bitcoin OP_RETURN transaction data
   * 
   * @param proofHash - Hash of the quantum proof
   * @returns OP_RETURN data string
   */
  static createOPReturnData(proofHash: string): string {
    // Format: ALZ-QSS:{proof_hash}
    const prefix = 'ALZ-QSS:';
    const data = `${prefix}${proofHash}`;
    
    // OP_RETURN limit is 80 bytes, truncate if necessary
    if (data.length > 80) {
      return data.substring(0, 80);
    }
    
    return data;
  }

  /**
   * Extract proof hash from OP_RETURN data
   * 
   * @param opReturnData - OP_RETURN data from Bitcoin transaction
   * @returns Proof hash or null
   */
  static extractProofHash(opReturnData: string): string | null {
    const prefix = 'ALZ-QSS:';
    if (opReturnData.startsWith(prefix)) {
      return opReturnData.substring(prefix.length);
    }
    return null;
  }
}

export class EVMAnchor {
  /**
   * Create Ethereum/Polygon transaction data for anchoring
   * 
   * @param contractAddress - QuantumSecurityAdapter contract address
   * @param proofHash - Hash of the quantum proof
   * @returns Transaction data
   */
  static createAnchorTransaction(
    contractAddress: string,
    proofHash: string
  ): {
    to: string;
    data: string;
    value: string;
  } {
    // Function signature: anchorQuantumProof(bytes32 proofHash)
    const functionSignature = 'anchorQuantumProof(bytes32)';
    const iface = new ethers.Interface([
      `function ${functionSignature}`,
    ]);

    const data = iface.encodeFunctionData('anchorQuantumProof', [
      ethers.hexlify(ethers.toUtf8Bytes(proofHash)),
    ]);

    return {
      to: contractAddress,
      data: data,
      value: '0x0',
    };
  }

  /**
   * Verify proof on-chain using QuantumSecurityAdapter
   * 
   * @param provider - Ethers provider
   * @param contractAddress - QuantumSecurityAdapter contract address
   * @param txHash - Transaction hash to verify
   * @param proofHash - Quantum proof hash
   * @returns Verification result
   */
  static async verifyOnChain(
    provider: ethers.Provider,
    contractAddress: string,
    txHash: string,
    proofHash: string
  ): Promise<boolean> {
    try {
      const iface = new ethers.Interface([
        'function verifyQuantumProof(bytes32 txHash, bytes32 proofHash) view returns (bool)',
      ]);

      const contract = new ethers.Contract(
        contractAddress,
        iface,
        provider
      );

      const result = await contract.verifyQuantumProof(
        ethers.hexlify(ethers.toUtf8Bytes(txHash)),
        ethers.hexlify(ethers.toUtf8Bytes(proofHash))
      );

      return result;
    } catch (error) {
      console.error('Error verifying on-chain:', error);
      return false;
    }
  }
}

// ============================================================================
// CONVENIENCE FUNCTIONS
// ============================================================================

let defaultClient: QSSClient | null = null;

/**
 * Initialize default QSS client
 */
export function init(config?: QSSConfig): QSSClient {
  defaultClient = new QSSClient(config);
  return defaultClient;
}

/**
 * Get or create default QSS client
 */
function getClient(): QSSClient {
  if (!defaultClient) {
    defaultClient = new QSSClient();
  }
  return defaultClient;
}

/**
 * Generate quantum proof (convenience function)
 */
export async function generateProof(
  chain: string,
  txHash: string,
  metadata?: GenerateProofRequest['metadata']
): Promise<QuantumProof> {
  return getClient().generateProof(chain, txHash, metadata);
}

/**
 * Verify quantum proof (convenience function)
 */
export async function verifyProof(
  proof: QuantumProof
): Promise<VerificationResult> {
  return getClient().verifyProof(proof);
}

/**
 * Get anchor instructions (convenience function)
 */
export async function getAnchorInstructions(
  proof: QuantumProof,
  targetChain: string,
  targetAddress?: string
): Promise<AnchorInstructions> {
  return getClient().getAnchorInstructions(proof, targetChain, targetAddress);
}

/**
 * Anchor proof on Bitcoin (convenience function)
 * 
 * Note: This returns instructions. Actual transaction creation
 * should be done using a Bitcoin library (e.g., bitcoinjs-lib)
 */
export async function anchorOnBitcoin(
  proof: QuantumProof,
  targetAddress?: string
): Promise<AnchorInstructions> {
  const instructions = await getAnchorInstructions(
    proof,
    'bitcoin',
    targetAddress
  );
  
  // Helper: Create OP_RETURN data
  if (instructions.proof_hash) {
    instructions.data = BitcoinAnchor.createOPReturnData(instructions.proof_hash);
  }
  
  return instructions;
}

/**
 * Anchor proof on Ethereum/Polygon (convenience function)
 * 
 * Note: This returns transaction data. You need to sign and send
 * using your wallet (e.g., MetaMask, ethers.js)
 */
export async function anchorOnEVM(
  proof: QuantumProof,
  contractAddress: string,
  targetChain: string = 'ethereum'
): Promise<{
  instructions: AnchorInstructions;
  transactionData: {
    to: string;
    data: string;
    value: string;
  };
}> {
  const instructions = await getAnchorInstructions(proof, targetChain);
  
  let transactionData;
  if (instructions.proof_hash) {
    transactionData = EVMAnchor.createAnchorTransaction(
      contractAddress,
      instructions.proof_hash
    );
  } else {
    throw new Error('Proof hash not found in anchor instructions');
  }
  
  return {
    instructions,
    transactionData,
  };
}

// ============================================================================
// DEFAULT EXPORT
// ============================================================================

const QSS = {
  // Client class
  Client: QSSClient,
  
  // Convenience functions
  generateProof,
  verifyProof,
  getAnchorInstructions,
  anchorOnBitcoin,
  anchorOnEVM,
  
  // Blockchain helpers
  Bitcoin: BitcoinAnchor,
  EVM: EVMAnchor,
  
  // Initialize
  init,
};

export default QSS;

