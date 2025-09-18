FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=3001

# Default environment variables (override these when running the container)
ENV LIVEKIT_API_KEY=""
ENV LIVEKIT_API_SECRET=""
ENV LIVEKIT_WS_URL=""
ENV GEMINI_API_KEY=""
ENV GEMINI_MODEL="gemini-1.5-flash"
ENV AGENT_IDENTITY="assistant"
ENV CORS_ORIGINS="http://localhost:8080,http://localhost:3000,http://localhost:5173"

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]



