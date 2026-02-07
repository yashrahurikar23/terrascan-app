#!/bin/bash
# GDAL Installation Script for macOS

set -e

echo "🔧 Installing GDAL for macOS"
echo "============================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed"
    echo ""
    echo "Install it with:"
    echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
    exit 1
fi

echo "✓ Homebrew found"
echo ""

# Step 1: Install GDAL
echo "Step 1: Installing GDAL system libraries via Homebrew..."
echo "This may take a few minutes..."
echo ""

brew install gdal

echo ""
echo "✅ GDAL system libraries installed!"
echo ""

# Step 2: Verify gdal-config
if ! command -v gdal-config &> /dev/null; then
    echo "❌ Error: gdal-config not found after installation"
    echo ""
    echo "Try adding Homebrew to your PATH:"
    echo '  echo \'eval "$(/opt/homebrew/bin/brew shellenv)"\' >> ~/.zshrc'
    echo '  source ~/.zshrc'
    echo ""
    exit 1
fi

GDAL_VERSION=$(gdal-config --version)
echo "✓ Found GDAL version: $GDAL_VERSION"
echo ""

# Step 3: Install Python package
echo "Step 2: Installing GDAL Python package..."
echo ""

# Check for virtual environment
if [ -d ".venv" ]; then
    echo "Using existing virtual environment: .venv"
    if command -v uv &> /dev/null; then
        echo "Installing with uv..."
        uv pip install "gdal==${GDAL_VERSION}.*"
    else
        source .venv/bin/activate
        pip install "gdal==${GDAL_VERSION}.*"
    fi
elif command -v uv &> /dev/null; then
    echo "Using uv..."
    uv pip install "gdal==${GDAL_VERSION}.*"
else
    echo "⚠️  No virtual environment found. Installing globally..."
    echo "Consider creating a virtual environment first:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo ""
    pip3 install "gdal==${GDAL_VERSION}.*"
fi

echo "✅ GDAL Python package installed!"
echo ""

# Step 4: Verify
echo "Step 3: Verifying installation..."
echo ""

if command -v uv &> /dev/null; then
    uv run python -c "from osgeo import gdal; print('✅ GDAL Python version:', gdal.__version__)"
else
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        python -c "from osgeo import gdal; print('✅ GDAL Python version:', gdal.__version__)"
    else
        python3 -c "from osgeo import gdal; print('✅ GDAL Python version:', gdal.__version__)"
    fi
fi

echo ""
echo "🎉 GDAL installation complete!"
echo ""
echo "Next steps:"
echo "  1. Install other dependencies:"
if command -v uv &> /dev/null; then
    echo "     uv pip install -r requirements.txt"
else
    echo "     pip install -r requirements.txt"
fi
echo "  2. Run the app:"
echo "     streamlit run streamlit_app.py"
echo ""
