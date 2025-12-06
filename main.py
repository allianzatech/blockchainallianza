from backend_wallet_integration import app
import os

# ✅ INICIAR SCHEDULER DE EXPIRAÇÃO DE PAGAMENTOS
try:
    from payment_expiration_job import start_expiration_scheduler
    # Iniciar scheduler que executa a cada 1 hora
    start_expiration_scheduler(interval_hours=1)
    print("✅ Scheduler de expiração de pagamentos iniciado")
except Exception as e:
    print(f"⚠️  Aviso: Não foi possível iniciar scheduler de expiração: {e}")

# Configurar variáveis de ambiente (Render vai substituir)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
