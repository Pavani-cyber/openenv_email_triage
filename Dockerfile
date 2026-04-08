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
# Expose Gradio port
# ==========================
EXPOSE 7860

# ==========================
# Health check
# ==========================
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('inference.py') else 1)"

# ==========================
# Run inference script
# ==========================
CMD ["python", "inference.py", "--validate-only"]