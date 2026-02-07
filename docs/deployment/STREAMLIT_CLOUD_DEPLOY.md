# Streamlit Cloud Deployment Guide

This guide helps you deploy the GDAL Image Processing app to Streamlit Cloud.

## Prerequisites

- A GitHub repository with this code (already done: https://github.com/yashrahurikar23/terrascan-app)
- A Streamlit Cloud account (free at https://streamlit.io/cloud)

## Deployment Steps

### 1. Connect Repository to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"
4. Select repository: `yashrahurikar23/terrascan-app`
5. Set main file path: `streamlit_app.py`
6. Click "Deploy!"

### 2. System Dependencies

Streamlit Cloud will automatically read `packages.txt` and install:
- `libgdal-dev` - GDAL development libraries
- `gdal-bin` - GDAL binaries
- `python3-gdal` - Python GDAL bindings

### 3. Python Dependencies

Streamlit Cloud will automatically install packages from `requirements.txt`:
- streamlit
- numpy
- pillow
- matplotlib
- plotly
- pandas
- scipy
- gdal (will build against system libraries)

## Troubleshooting

### GDAL Installation Fails

If you see `gdal-config` not found errors:

1. **Verify `packages.txt` exists** and contains:
   ```
   libgdal-dev
   gdal-bin
   python3-gdal
   ```

2. **Check build logs** in Streamlit Cloud dashboard for system package installation

3. **Alternative**: Use conda environment (if supported):
   ```yaml
   # environment.yml (if using conda)
   dependencies:
     - gdal
     - python=3.11
     - pip
     - pip:
       - streamlit
       - numpy
       - pillow
       - matplotlib
       - plotly
       - pandas
       - scipy
   ```

### App Shows "GDAL is not installed" Error

This means GDAL Python package didn't install correctly. Check:
- System packages installed successfully
- Python package build completed
- Check logs for compilation errors

### Memory Issues

GDAL can be memory-intensive. If the app crashes:
- Reduce image processing sample sizes in the code
- Use smaller test images
- Consider upgrading to a paid Streamlit Cloud tier

## Configuration Files

- **`packages.txt`**: System dependencies (Ubuntu/Debian packages)
- **`requirements.txt`**: Python dependencies
- **`.streamlit/config.toml`**: Streamlit configuration

## Alternative: Docker Deployment

If Streamlit Cloud doesn't work, you can use Docker:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin libgdal-dev python3-gdal \
    gcc g++ make python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app
WORKDIR /app

# Run app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Support

For Streamlit Cloud specific issues:
- Check Streamlit Cloud documentation
- Review build logs in the dashboard
- Contact Streamlit support if needed

For GDAL installation issues:
- See `INSTALL_GDAL.md` for detailed installation instructions
- Check `FIX_BUILD_ERROR.md` for common build errors
