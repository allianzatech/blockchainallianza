"""
Job periódico para expirar pagamentos automaticamente
Executa a cada hora para verificar e expirar pagamentos pendentes há mais de 10 dias
"""

import time
import threading
from datetime import datetime, timezone
from payment_expiration import expire_old_payments, add_expires_at_column

def run_expiration_job():
    """Executa o job de expiração de pagamentos"""
    print(f"🔄 [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] Executando job de expiração de pagamentos...")
    
    try:
        # Garantir que a coluna expires_at existe
        add_expires_at_column()
        
        # Expirar pagamentos antigos
        result = expire_old_payments()
        
        if result['success']:
            if result['expired_count'] > 0:
                print(f"✅ [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] {result['expired_count']} pagamento(s) expirado(s)")
                print(f"💰 Total devolvido ao supply: R$ {result.get('total_amount_brl', 0):.2f}")
            else:
                print(f"✅ [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] Nenhum pagamento expirado")
        else:
            print(f"❌ [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] Erro ao expirar pagamentos: {result.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"❌ [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] Erro no job de expiração: {e}")

def start_expiration_scheduler(interval_hours=1):
    """
    Inicia o scheduler que executa o job de expiração periodicamente
    
    Args:
        interval_hours: Intervalo em horas entre execuções (padrão: 1 hora)
    """
    def scheduler_loop():
        while True:
            try:
                run_expiration_job()
            except Exception as e:
                print(f"❌ Erro no scheduler: {e}")
            
            # Aguardar o intervalo especificado
            time.sleep(interval_hours * 3600)  # Converter horas para segundos
    
    # Executar imediatamente na primeira vez
    print("🚀 Iniciando scheduler de expiração de pagamentos...")
    print(f"⏰ Intervalo: {interval_hours} hora(s)")
    run_expiration_job()
    
    # Iniciar thread em background
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("✅ Scheduler de expiração iniciado em background")

# Executar quando importado (para testes)
if __name__ == '__main__':
    print("🧪 Executando job de expiração manualmente...")
    run_expiration_job()

