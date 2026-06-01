#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "🚀 Iniciando CAROL server en puerto 4486..."
python3 server.py
