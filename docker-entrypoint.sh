#!/bin/bash

# Start PostgreSQL
service postgresql start

# Wait for PostgreSQL to be ready
until pg_isready -h localhost -p 5432 -U postgres; do
    echo "Waiting for PostgreSQL to start..."
    sleep 2
done

echo "PostgreSQL is running!"

# ✅ Corrected password syntax (MUST use single quotes)
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'ex4KjgDLFgygyat1EcV3';"

# Ensure the database exists
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'newsletter_db'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE newsletter_db;"

# Run database migrations (if using Flask + SQLAlchemy)
if [ -f "migrations/env.py" ]; then
    echo "Running database migrations..."
    flask db upgrade
fi

# Start Flask
echo "Starting Flask..."
exec python app/main.py
