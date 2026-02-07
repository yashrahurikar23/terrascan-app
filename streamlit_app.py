"""
Streamlit App Entry Point

This is a convenience entry point that sets up the Python path and runs the app.
Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path

# Add src directory to path BEFORE any imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run the main function from the app
from terrascan.app import main

if __name__ == "__main__":
    main()
