# Dockerfile for GDAL Image Processing App
# This allows deployment with full GDAL support

FROM python:3.11-slim

# Install system dependencies for GDAL
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    gcc \
    g++ \
    make \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# GDAL version should match system version
RUN pip install --no-cache-dir -r requirements.txt || \
    (GDAL_VERSION=$(gdal-config --version 2>/dev/null || echo "3.6.0") && \
     pip install --no-cache-dir "gdal==${GDAL_VERSION}.*" && \
     pip install --no-cache-dir streamlit numpy pillow matplotlib plotly pandas scipy)

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
