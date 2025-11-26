# gunicorn_config.py
# Configuração do Gunicorn para Allianza Blockchain

import multiprocessing
import os

# Número de workers (CPU cores * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1
if workers > 8:
    workers = 8  # Limitar a 8 workers máximo

# Classe de worker (gevent para async)
worker_class = "gevent"
worker_connections = 1000

# Binding (porta interna)
bind = f"127.0.0.1:{os.getenv('PORT', '5000')}"

# Timeouts
timeout = 120
keepalive = 5

# Max requests (reiniciar worker após N requests)
max_requests = 1000
max_requests_jitter = 50

# Preload app (carregar antes de forkar workers)
preload_app = True

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "allianza_blockchain"

# User/Group (ajustar conforme necessário)
# user = "usuario"
# group = "usuario"

# Chdir (diretório de trabalho)
chdir = os.path.dirname(os.path.abspath(__file__))

# PID file
pidfile = "gunicorn.pid"

# Daemon (não usar em systemd)
daemon = False

