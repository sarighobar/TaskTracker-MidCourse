$dockerfile = @'
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create non-root user and fix permissions for SQLite file creation
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Bind to 0.0.0.0 so port forwarding works across the container boundary
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'@
Set-Content -Path "Dockerfile" -Value $dockerfile -Encoding utf8