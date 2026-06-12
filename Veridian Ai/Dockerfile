# Use Python 3.11 slim image
FROM python:3.11-slim

# Install Java (required for tabula-py)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app/app
COPY ./main.py /app/  # If you have a main.py at root, otherwise adjust

# Create non-root user
RUN useradd -m -u 1000 veridian && chown -R veridian:veridian /app
USER veridian

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]