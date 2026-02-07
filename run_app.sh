#!/bin/bash
# Run Streamlit App Script
# This script runs the Terrascan Image Processing Streamlit app

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🖼️  Starting Terrascan Image Processor App..."
echo ""

# Add src directory to Python path
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

# Check if virtual environment exists (optional check)
if [ -d ".venv" ]; then
    # Check if uv is available
    if command -v uv &> /dev/null; then
        echo "Using uv to run the app..."
        echo ""
        echo "App will open at: http://localhost:8501"
        echo "Press Ctrl+C to stop the app"
        echo ""
        
        uv run streamlit run "${SCRIPT_DIR}/src/terrascan/app.py"
    else
        echo "Using standard Python environment..."
        echo ""
        
        # Activate virtual environment
        source .venv/bin/activate
        
        echo "App will open at: http://localhost:8501"
        echo "Press Ctrl+C to stop the app"
        echo ""
        
        streamlit run "${SCRIPT_DIR}/src/terrascan/app.py"
    fi
else
    # No venv, just run with system Python
    echo "Using system Python..."
    echo ""
    echo "App will open at: http://localhost:8501"
    echo "Press Ctrl+C to stop the app"
    echo ""
    
    streamlit run "${SCRIPT_DIR}/src/terrascan/app.py"
fi
