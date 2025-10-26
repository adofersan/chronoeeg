# Dockerfile for ChronoEEG
FROM python:3.10-slim

LABEL maintainer="your.email@example.com"
LABEL description="ChronoEEG - Advanced Multidimensional EEG Analysis Toolkit"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package source
COPY src/ ./src/
COPY pyproject.toml .
COPY MANIFEST.in .
COPY README.md .
COPY LICENSE .

# Install package in development mode
RUN pip install -e .

# Create directories for data and outputs
RUN mkdir -p /data /outputs /notebooks

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CHRONOEEG_DATA_PATH=/data
ENV CHRONOEEG_OUTPUT_PATH=/outputs

# Default command (can be overridden)
CMD ["python"]

# Expose port for Jupyter if needed
EXPOSE 8888
