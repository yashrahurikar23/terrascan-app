# Quick GDAL Installation Guide

## Run These Commands

Copy and paste these commands into your terminal:

```bash
# 1. Install build tools and GDAL system libraries (requires sudo password)
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# 2. Get the GDAL version and install matching Python package
cd /home/metheus/projects/image_processing
GDAL_VERSION=$(gdal-config --version)
uv pip install "gdal==${GDAL_VERSION}.*"

# 3. Verify installation
uv run python -c "from osgeo import gdal; print('✅ GDAL version:', gdal.__version__)"

# 4. Restart Streamlit app (if running)
# Stop current app, then:
uv run streamlit run streamlit_app.py --server.headless=true
```

## Or Use the Installation Script

```bash
cd /home/metheus/projects/image_processing
./install_gdal.sh
```

The script will:
- Install GDAL system libraries (with sudo)
- Detect the GDAL version automatically
- Install the matching Python package
- Verify the installation

## After Installation

Once GDAL is installed, refresh your browser at http://localhost:8501 and the app will work!
