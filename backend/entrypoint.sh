#!/usr/bin/env sh
set -e

echo ">> Criando diretório de uploads..."
mkdir -p /app/media/transcripts

echo ">> Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

echo ">> Iniciando o servidor..."
exec "$@"
