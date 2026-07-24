FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Create non-root user and fix permissions
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "if [ -f app/main.py ]; then uvicorn app.main:app --host 0.0.0.0 --port 8000; else uvicorn main:app --host 0.0.0.0 --port 8000; fi"]
