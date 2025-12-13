#!/bin/bash
cd "$(dirname "$0")" || exit 1
exec gunicorn -w 2 -b 0.0.0.0:${PORT:-5000} --timeout 300 --keep-alive 5 --preload wsgi_optimized:application

