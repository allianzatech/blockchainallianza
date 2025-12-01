#!/usr/bin/env node
/**
 * @allianza/qss-canonicalizer
 * Canonicalizador de provas QSS conforme RFC8785
 * 
 * Gera proof_hash canônico para ancoragem on-chain
 */

const crypto = require('crypto');
const fs = require('fs');

// ============================================================================
// CANONICALIZAÇÃO RFC8785
// ============================================================================

function canonicalizeJSON(obj) {
    /**
     * Canonicaliza JSON conforme RFC8785
     */
    if (obj === null || typeof obj !== 'object') {
        return JSON.stringify(obj);
    }
    
    if (Array.isArray(obj)) {
        return '[' + obj.map(canonicalizeJSON).join(',') + ']';
    }
    
    const keys = Object.keys(obj).sort();
    const pairs = keys.map(key => {
        const value = canonicalizeJSON(obj[key]);
        return JSON.stringify(key) + ':' + value;
    });
    
    return '{' + pairs.join(',') + '}';
}

function computeProofHash(proof, canonicalFields = null) {
    /**
     * Calcula proof_hash usando campos canônicos
     */
    if (!canonicalFields) {
        canonicalFields = [
            'asset_chain',
            'asset_tx',
            'merkle_root',
            'block_hash',
            'timestamp'
        ];
    }
    
    const canonicalObj = {};
    for (const field of canonicalFields) {
        if (proof[field] !== undefined) {
            canonicalObj[field] = proof[field];
        }
    }
    
    const canonicalJSON = canonicalizeJSON(canonicalObj);
    const hash = crypto.createHash('sha256').update(canonicalJSON).digest('hex');
    
    return {
        proof_hash: hash,
        canonical_json: canonicalJSON,
        canonical_fields: canonicalFields
    };
}

// ============================================================================
// GERAÇÃO DE PAYLOAD PARA OP_RETURN
// ============================================================================

function generateOPReturnPayload(proofHash, ipfsCid = null) {
    /**
     * Gera payload para OP_RETURN no Bitcoin
     * Formato: ALZ:proofHash[:CID]
     */
    let payload = `ALZ:${proofHash}`;
    
    if (ipfsCid) {
        payload += `:${ipfsCid}`;
    }
    
    // OP_RETURN tem limite de 80 bytes
    if (payload.length > 80) {
        // Truncar se necessário
        payload = payload.substring(0, 80);
    }
    
    return payload;
}

// ============================================================================
// CLI
// ============================================================================

function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('Uso: node canonicalize.js <proof.json> [--fields field1,field2,...]');
        process.exit(1);
    }
    
    const proofFile = args[0];
    const fieldsArg = args.find(arg => arg.startsWith('--fields'));
    const canonicalFields = fieldsArg 
        ? fieldsArg.split('=')[1].split(',')
        : null;
    
    if (!fs.existsSync(proofFile)) {
        console.error(`Arquivo não encontrado: ${proofFile}`);
        process.exit(1);
    }
    
    const proof = JSON.parse(fs.readFileSync(proofFile, 'utf8'));
    
    console.log('🔐 Canonicalizando prova QSS...\n');
    
    const result = computeProofHash(proof, canonicalFields);
    
    console.log('📊 Resultado:\n');
    console.log(`Proof Hash: ${result.proof_hash}`);
    console.log(`\nCampos canônicos usados:`);
    result.canonical_fields.forEach(field => {
        console.log(`   - ${field}: ${proof[field] || '(não definido)'}`);
    });
    console.log(`\nJSON Canônico (RFC8785):`);
    console.log(result.canonical_json);
    
    // Gerar payload OP_RETURN
    const opReturnPayload = generateOPReturnPayload(result.proof_hash);
    console.log(`\n📡 Payload para OP_RETURN (Bitcoin):`);
    console.log(opReturnPayload);
    console.log(`Tamanho: ${opReturnPayload.length} bytes`);
    
    // Atualizar proof com proof_hash se não existir
    if (!proof.proof_hash) {
        proof.proof_hash = result.proof_hash;
        proof.canonicalization = {
            method: 'RFC8785',
            canonical_input_fields: result.canonical_fields
        };
        
        const outputFile = proofFile.replace('.json', '_canonical.json');
        fs.writeFileSync(outputFile, JSON.stringify(proof, null, 2));
        console.log(`\n✅ Prova atualizada salva em: ${outputFile}`);
    }
}

if (require.main === module) {
    main();
}

module.exports = { canonicalizeJSON, computeProofHash, generateOPReturnPayload };

