#!/usr/bin/env python3
"""
Simple script to run the Streamlit app with correct Python path.
"""
import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# Now run streamlit
import streamlit.web.cli as stcli

if __name__ == "__main__":
    app_file = src_dir / "terrascan" / "app.py"
    sys.argv = ["streamlit", "run", str(app_file)]
    stcli.main()
