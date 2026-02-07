#!/bin/bash
# Run Streamlit App Script
# This script runs the GDAL Image Processing Streamlit app

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🖼️  Starting GDAL Image Processor App..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Run setup first: ./setup.sh"
    exit 1
fi

# Check if GDAL is available
if command -v uv &> /dev/null; then
    echo "Using uv to run the app..."
    echo ""
    echo "App will open at: http://localhost:8501"
    echo "Press Ctrl+C to stop the app"
    echo ""
    
    uv run streamlit run streamlit_app.py
else
    echo "Using standard Python environment..."
    echo ""
    
    # Activate virtual environment
    source .venv/bin/activate
    
    echo "App will open at: http://localhost:8501"
    echo "Press Ctrl+C to stop the app"
    echo ""
    
    streamlit run streamlit_app.py
fi

