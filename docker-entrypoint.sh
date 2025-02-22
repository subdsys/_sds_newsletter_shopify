#!/bin/bash

# Run database migrations
if [ -f "migrations/env.py" ]; then
    echo "Running database migrations..."
    flask db upgrade
fi

# Start Flask
echo "Starting Flask..."
exec python app/main.py
