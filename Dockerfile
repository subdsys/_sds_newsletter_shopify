# ✅ Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# ✅ Ensure `docker-entrypoint.sh` is copied correctly
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh  # ✅ Ensure execution permissions

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose Flask port
EXPOSE 8080

# ✅ Set the entrypoint (Fix Issue)
ENTRYPOINT ["/docker-entrypoint.sh"]
