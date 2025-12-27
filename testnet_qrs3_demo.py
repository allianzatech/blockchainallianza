"""
🔐 Gerador de Assinaturas QRS-3 para Demonstração
Gera assinaturas reais para testar o verificador
"""

from quantum_security import QuantumSecuritySystem
import time
import json

class QRS3DemoGenerator:
    def __init__(self):
        self.quantum_security = QuantumSecuritySystem()
        self.keypair_id = f"demo_{int(time.time())}"
        self._initialize_keypair()
    
    def _initialize_keypair(self):
        """Inicializa keypair QRS-3"""
        try:
            self.quantum_security.generate_qrs3_keypair(self.keypair_id)
        except Exception as e:
            print(f"⚠️  Erro ao gerar keypair: {e}")
    
    def generate_demo_signature(self, message: str = None):
        """
        Gera uma assinatura QRS-3 de demonstração
        
        Args:
            message: Mensagem opcional. Se None, usa mensagem padrão.
        
        Returns:
            Dict com message, signature, keypair_id, proof
        """
        if message is None:
            message = f"Allianza Testnet Demo - {time.time()}"
        
        try:
            # Assinar com QRS-3
            signature = self.quantum_security.sign_qrs3(
                keypair_id=self.keypair_id,
                message=message.encode('utf-8'),
                use_hybrid=True
            )
            
            # Verificar a assinatura para garantir que é válida
            verified = self.quantum_security.verify_qrs3(
                keypair_id=self.keypair_id,
                message=message.encode('utf-8'),
                signature=signature
            )
            
            return {
                "success": True,
                "message": message,
                "signature": signature,
                "keypair_id": self.keypair_id,
                "verified": verified,
                "timestamp": time.time(),
                "proof": {
                    "message_hash": hashlib.sha256(message.encode('utf-8')).hexdigest(),
                    "signature_hash": hashlib.sha256(json.dumps(signature, sort_keys=True).encode()).hexdigest()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": message
            }
    
    def get_demo_example(self):
        """Retorna um exemplo completo para demonstração"""
        demo = self.generate_demo_signature()
        
        return {
            "example": {
                "message": demo.get("message"),
                "signature": demo.get("signature"),
                "instructions": {
                    "step1": "Copie a mensagem abaixo",
                    "step2": "Copie a assinatura QRS-3 (JSON)",
                    "step3": "Cole no verificador QRS-3",
                    "step4": "Clique em 'Verificar Assinatura'",
                    "step5": "Veja o resultado: ✅ Assinatura Válida!"
                }
            },
            "verified": demo.get("verified", False),
            "proof": demo.get("proof", {})
        }

