FROM python:3.10-slim

WORKDIR /app

# ==========================
# System dependencies
# ==========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# ==========================
# Python dependencies
# ==========================
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --force-reinstall --no-cache-dir numpy==1.24.3

# ==========================
# Copy project files
# ==========================
COPY . .

# ==========================
# Expose FastAPI port
# ==========================
EXPOSE 8000

# ==========================
# Health check
# ==========================
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5).status == 200 else 1)"

# ==========================
# Run FastAPI server
# ==========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]