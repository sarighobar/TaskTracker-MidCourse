$dockerfile = @'
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python path so imports resolve whether main.py is at root or inside app/
ENV PYTHONPATH=/app

# Create non-root user and grant write permissions to /app for SQLite (tasks.db)
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Bind explicitly to 0.0.0.0 so Docker forwards traffic from localhost:8000
CMD ["sh", "-c", "if [ -f app/main.py ]; then uvicorn app.main:app --host 0.0.0.0 --port 8000; else uvicorn main:app --host 0.0.0.0 --port 8000; fi"]
'@
Set-Content -Path "Dockerfile" -Value $dockerfile -Encoding utf8