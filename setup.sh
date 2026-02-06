#!/bin/bash
# Setup script for GDAL Image Processing project using uv

set -e

echo "🚀 Setting up GDAL Image Processing project with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
else
    echo "✓ Virtual environment already exists"
fi

# Check if GDAL system libraries are installed
if ! command -v gdal-config &> /dev/null; then
    echo ""
    echo "⚠️  GDAL system libraries are not installed"
    echo ""
    echo "Please install GDAL system libraries first:"
    echo ""
    echo "For Fedora/RHEL:"
    echo "  sudo dnf install gdal gdal-devel python3-gdal"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install gdal-bin libgdal-dev python3-gdal"
    echo ""
    echo "For macOS (Homebrew):"
    echo "  brew install gdal"
    echo ""
    echo "After installing GDAL system libraries, run:"
    echo "  uv pip install -r requirements.txt"
    echo ""
    
    # Install other packages that don't require GDAL
    echo "📥 Installing other dependencies (streamlit, numpy, pillow)..."
    uv pip install streamlit numpy pillow
    
    echo ""
    echo "✓ Other dependencies installed"
    echo "⚠️  GDAL Python package will be installed after you install system GDAL libraries"
else
    echo "✓ GDAL system libraries found"
    echo "📥 Installing all dependencies..."
    uv pip install -r requirements.txt
    echo "✓ All dependencies installed successfully!"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the Streamlit app:"
echo "  streamlit run streamlit_app.py"
echo ""
