/**
 * Tests for @allianza/qss-js
 */

import QSS, { QSSClient, BitcoinAnchor, EVMAnchor } from './index';

describe('QSS SDK', () => {
  const testConfig = {
    apiUrl: 'https://testnet.allianza.tech/api/qss',
  };

  describe('QSSClient', () => {
    let client: QSSClient;

    beforeEach(() => {
      client = new QSSClient(testConfig);
    });

    it('should initialize with default config', () => {
      const defaultClient = new QSSClient();
      expect(defaultClient).toBeInstanceOf(QSSClient);
    });

    it('should initialize with custom config', () => {
      const customClient = new QSSClient({
        apiUrl: 'https://custom.api.com',
        timeout: 60000,
        apiKey: 'test-key',
      });
      expect(customClient).toBeInstanceOf(QSSClient);
    });
  });

  describe('BitcoinAnchor', () => {
    it('should create OP_RETURN data', () => {
      const proofHash = 'abc123def456';
      const data = BitcoinAnchor.createOPReturnData(proofHash);
      expect(data).toContain('ALZ-QSS:');
      expect(data).toContain(proofHash);
    });

    it('should truncate data if too long', () => {
      const longHash = 'a'.repeat(100);
      const data = BitcoinAnchor.createOPReturnData(longHash);
      expect(data.length).toBeLessThanOrEqual(80);
    });

    it('should extract proof hash from OP_RETURN', () => {
      const opReturnData = 'ALZ-QSS:abc123';
      const hash = BitcoinAnchor.extractProofHash(opReturnData);
      expect(hash).toBe('abc123');
    });

    it('should return null for invalid OP_RETURN', () => {
      const invalidData = 'INVALID:abc123';
      const hash = BitcoinAnchor.extractProofHash(invalidData);
      expect(hash).toBeNull();
    });
  });

  describe('EVMAnchor', () => {
    it('should create anchor transaction data', () => {
      const contractAddress = '0x1234567890123456789012345678901234567890';
      const proofHash = 'abc123';
      const txData = EVMAnchor.createAnchorTransaction(contractAddress, proofHash);
      
      expect(txData.to).toBe(contractAddress);
      expect(txData.data).toBeDefined();
      expect(txData.value).toBe('0x0');
    });
  });

  describe('Convenience Functions', () => {
    it('should initialize default client', () => {
      const client = QSS.init(testConfig);
      expect(client).toBeInstanceOf(QSSClient);
    });
  });
});

