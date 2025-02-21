# Use Python base image
FROM python:3.9

# Install system dependencies (PostgreSQL, required libraries)
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose PostgreSQL and Flask ports
EXPOSE 5432 8080

# Copy and set the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set the entrypoint
CMD ["/docker-entrypoint.sh"]