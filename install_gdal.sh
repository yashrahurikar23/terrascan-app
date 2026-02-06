#!/bin/bash
# GDAL Installation Script for Fedora/RHEL
# Updated with proper installation steps

set -e

echo "🔧 Installing GDAL for Fedora/RHEL"
echo "=================================="
echo ""

# Step 1: Install build tools and GDAL system libraries
echo "Step 1: Installing build tools and GDAL system libraries..."
echo "This requires sudo privileges."
echo ""
echo "Installing: gcc-c++ make python3-devel gdal gdal-devel python3-gdal"
echo ""

sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

echo ""
echo "✅ GDAL system libraries installed!"
echo ""

# Step 2: Verify gdal-config is available
if ! command -v gdal-config &> /dev/null; then
    echo "❌ Error: gdal-config not found after installation"
    echo "Please check the installation and try again."
    exit 1
fi

GDAL_VERSION=$(gdal-config --version)
echo "✓ Found GDAL version: $GDAL_VERSION"
echo ""

# Step 3: Install GDAL Python package in virtual environment
echo "Step 2: Installing GDAL Python package..."
echo ""

if [ -d ".venv" ]; then
    echo "Using existing virtual environment: .venv"
    
    if command -v uv &> /dev/null; then
        echo "Installing with uv..."
        # Install with the matching version
        uv pip install "gdal==${GDAL_VERSION}.*"
    else
        echo "Activating virtual environment and installing with pip..."
        source .venv/bin/activate
        pip install "gdal==${GDAL_VERSION}.*"
    fi
    echo "✅ GDAL Python package installed!"
else
    echo "⚠️  No virtual environment found. Creating one..."
    if command -v uv &> /dev/null; then
        uv venv
        uv pip install "gdal==${GDAL_VERSION}.*"
    else
        python3 -m venv .venv
        source .venv/bin/activate
        pip install "gdal==${GDAL_VERSION}.*"
    fi
    echo "✅ Virtual environment created and GDAL installed!"
fi

echo ""
echo "🎉 GDAL installation complete!"
echo ""

# Step 4: Verify installation
echo "Step 3: Verifying installation..."
echo ""

if command -v uv &> /dev/null; then
    uv run python -c "from osgeo import gdal; print('✅ GDAL Python package version:', gdal.__version__)"
else
    source .venv/bin/activate
    python -c "from osgeo import gdal; print('✅ GDAL Python package version:', gdal.__version__)"
fi

echo ""
echo "✨ All done! You can now run the Streamlit app."
echo ""
