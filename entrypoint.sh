#!/bin/sh

: "${DATABASE_HOST:?Environment variable DATABASE_HOST not set}"
: "${DATABASE_PORT:?Environment variable DATABASE_PORT not set}"

echo "Waiting for PostgreSQL at $DATABASE_HOST:$DATABASE_PORT..."

while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
