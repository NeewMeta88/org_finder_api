#!/usr/bin/env sh
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  sleep 2
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding initial data..."
python -m app.initial_data

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
