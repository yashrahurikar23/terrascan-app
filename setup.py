"""
Setup script for Terrascan package.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="terrascan",
    version="0.1.0",
    description="Geospatial Image Processing Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Terrascan Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "matplotlib>=3.7.0",
        "plotly>=5.14.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "gdal": ["gdal"],  # Optional GDAL support
        "rasterio": ["rasterio"],  # Optional Rasterio support
    },
    entry_points={
        "console_scripts": [
            "terrascan=terrascan.app:main",
        ],
    },
)
