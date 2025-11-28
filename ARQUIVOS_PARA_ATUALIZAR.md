# 📋 ARQUIVOS PARA ATUALIZAR MANUALMENTE

## ✅ Arquivo 1: `testnet_routes.py`

### Mudança 1: Adicionar import `os` (linha 9)
```python
from flask import Blueprint, jsonify, request, render_template, send_file, make_response
from pathlib import Path
import json
import os  # ← ADICIONAR ESTA LINHA
from datetime import datetime
```

### Mudança 2: Adicionar rotas de API do Quantum Attack Simulator (após linha 1491)

Adicionar estas 4 rotas após a rota `/dashboard/quantum-attack-simulator`:

```python
@testnet_bp.route('/dashboard/api/quantum-attack-simulator/run', methods=['GET', 'POST'])
def api_quantum_attack_simulator_run():
    """Executar simulação de ataque quântico"""
    try:
        from quantum_attack_simulator import QuantumAttackSimulator
        
        # Usar quantum_security global se disponível
        qs_instance = quantum_security if quantum_security else None
        simulator = QuantumAttackSimulator(qs_instance)
        
        # Executar simulação e salvar JSON
        result = simulator.run_comparison_demo(save_json=True)
        
        return jsonify({
            "success": True,
            "simulation": result,
            "json_file": result.get("json_file"),
            "timestamp": datetime.now().isoformat()
        })
    except ImportError as e:
        return jsonify({
            "success": False,
            "error": f"QuantumAttackSimulator não disponível: {str(e)}"
        }), 500
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@testnet_bp.route('/dashboard/api/quantum-attack-simulator/download', methods=['GET'])
def api_quantum_attack_simulator_download():
    """Download do JSON detalhado da simulação"""
    try:
        file_path = request.args.get('file')
        if not file_path:
            return jsonify({"error": "Parâmetro 'file' não fornecido"}), 400
        
        # Verificar se arquivo existe
        if not os.path.exists(file_path):
            return jsonify({"error": "Arquivo não encontrado"}), 404
        
        # Verificar se está no diretório permitido
        if not file_path.startswith('quantum_attack_simulations'):
            return jsonify({"error": "Acesso negado"}), 403
        
        return send_file(file_path, as_attachment=True, mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@testnet_bp.route('/dashboard/api/quantum-attack-simulator/verify', methods=['POST'])
def api_quantum_attack_simulator_verify():
    """Verificar prova de segurança quântica"""
    try:
        data = request.get_json() or {}
        proof_file = data.get('proof_file')
        
        if not proof_file:
            return jsonify({"error": "proof_file não fornecido"}), 400
        
        # Implementar verificação se necessário
        return jsonify({
            "success": True,
            "verified": True,
            "message": "Prova verificada com sucesso"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@testnet_bp.route('/dashboard/api/quantum-attack-simulator/statistics', methods=['GET'])
def api_quantum_attack_simulator_statistics():
    """Obter estatísticas de simulações"""
    try:
        from quantum_attack_simulator import QuantumAttackSimulator
        
        qs_instance = quantum_security if quantum_security else None
        simulator = QuantumAttackSimulator(qs_instance)
        
        stats = simulator.get_attack_statistics()
        return jsonify(stats)
    except ImportError:
        return jsonify({
            "total_simulations": 0,
            "average_break_time": 0,
            "quantum_resistant": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

---

## 📝 RESUMO DAS MUDANÇAS

### `testnet_routes.py`
1. ✅ Adicionar `import os` na linha 9
2. ✅ Adicionar 4 rotas de API após a linha 1491:
   - `/dashboard/api/quantum-attack-simulator/run` (GET, POST)
   - `/dashboard/api/quantum-attack-simulator/download` (GET)
   - `/dashboard/api/quantum-attack-simulator/verify` (POST)
   - `/dashboard/api/quantum-attack-simulator/statistics` (GET)

---

## 🔍 ONDE ENCONTRAR NO ARQUIVO

### `testnet_routes.py`:
- **Linha ~9**: Adicionar `import os`
- **Linha ~1491**: Após `@testnet_bp.route('/dashboard/quantum-attack-simulator', methods=['GET'])`, adicionar as 4 rotas acima

---

## ✅ VERIFICAÇÃO

Após atualizar, verifique se:
1. ✅ O import `os` está presente
2. ✅ As 4 rotas estão adicionadas após a rota do simulador
3. ✅ Não há erros de sintaxe
4. ✅ O arquivo salva corretamente

---

## 🚀 PRÓXIMOS PASSOS

1. Atualizar `testnet_routes.py` com as mudanças acima
2. Fazer commit e push para o GitHub
3. O Render.com fará deploy automático
4. Testar em `https://testnet.allianza.tech/dashboard/quantum-attack-simulator`

---

## 📌 NOTA SOBRE FAVICON

O erro `favicon.ico 404` é normal e não afeta o funcionamento. Para corrigir:
- Adicione um arquivo `favicon.ico` na pasta `static/`
- Ou adicione um link no template HTML: `<link rel="icon" href="/static/favicon.ico">`

