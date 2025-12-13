#!/bin/bash
# Script para iniciar no Render - encontra o diretório automaticamente
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1
export PYTHONPATH="$SCRIPT_DIR"
exec gunicorn -w 2 -b 0.0.0.0:${PORT:-5000} --timeout 300 --keep-alive 5 --preload wsgi_optimized:application

