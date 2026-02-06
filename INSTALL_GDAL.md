# Installing GDAL

GDAL requires system libraries to be installed before the Python package can be used.

## Quick Installation (Fedora/RHEL) - Updated Commands

### Option 1: Using the Installation Script (Recommended)

```bash
cd /home/metheus/projects/image_processing
./install_gdal.sh
```

### Option 2: Manual Installation

```bash
# Step 1: Install build tools and GDAL system libraries
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# Step 2: Get GDAL version (needed for Python package)
GDAL_VERSION=$(gdal-config --version)
echo "GDAL version: $GDAL_VERSION"

# Step 3: Install GDAL Python package matching system version
cd /home/metheus/projects/image_processing
uv pip install "gdal==${GDAL_VERSION}.*"
```

**Important:** The Python package version should match the system GDAL version. The script automatically detects and installs the matching version.

## Alternative: Using System Python Package

If you prefer to use the system-installed Python GDAL package:

```bash
# Install build tools and system package (includes Python bindings)
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# The Python package is already included, but you may need to link it
# Check if it's available:
python3 -c "from osgeo import gdal; print(gdal.__version__)"
```

## Verify Installation

After installation, verify GDAL is working:

```bash
# Activate virtual environment
source .venv/bin/activate

# Or use uv run
uv run python -c "from osgeo import gdal; print('GDAL version:', gdal.__version__)"
```

## Restart Streamlit

After installing GDAL, restart the Streamlit app:

```bash
# Stop the current app (Ctrl+C or kill the process)
# Then restart:
uv run streamlit run streamlit_app.py --server.headless=true
```
