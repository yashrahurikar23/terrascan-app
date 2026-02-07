# Image Processing with GDAL and Python

This project demonstrates how to use GDAL (Geospatial Data Abstraction Library) with Python for image processing tasks.

## Installation

### Cloud Deployment (Streamlit Cloud, etc.)

For cloud platforms like Streamlit Cloud, the `packages.txt` file is automatically used to install system dependencies.

**Requirements:**
- The `packages.txt` file is already included in the repository
- GDAL system libraries will be installed automatically
- Python packages from `requirements.txt` will be installed after system packages

**Deploy to Streamlit Cloud:**
1. Fork or connect this repository to Streamlit Cloud
2. Streamlit Cloud will automatically:
   - Install system packages from `packages.txt`
   - Install Python packages from `requirements.txt`
   - Deploy your app

**Note:** If GDAL installation fails on cloud platforms, ensure:
- `packages.txt` includes: `libgdal-dev`, `gdal-bin`, `python3-gdal`
- The platform supports system package installation
- Check platform-specific documentation for GDAL installation

### Quick Setup with uv (Recommended for Local Development)

This project uses `uv` for fast Python package management. The setup script will guide you through the installation:

```bash
# Run the setup script
./setup.sh
```

Or manually:

```bash
# Create virtual environment
uv venv

# Install build tools and GDAL system libraries first (required)
# For Fedora/RHEL:
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# For Ubuntu/Debian:
sudo apt-get update && sudo apt-get install gdal-bin libgdal-dev python3-gdal

# For macOS (Homebrew):
brew install gdal

# Then install Python packages
uv pip install -r requirements.txt
```

**Note:** GDAL requires system libraries to be installed before the Python package can be built. The setup script will check for this and provide instructions.

### Alternative Installation Methods

#### Option 1: Using pip (requires GDAL system libraries)

First, install GDAL system libraries:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal
```

**Fedora/RHEL:**
```bash
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal
```

**macOS (using Homebrew):**
```bash
brew install gdal
```

Then install Python package:
```bash
pip install -r requirements.txt
```

#### Option 2: Using conda (handles dependencies automatically)

```bash
conda install -c conda-forge gdal
```

## Usage

### Streamlit Web App (Recommended)

Run the interactive web application:

**⭐ Option 1: Use streamlit_app.py (Simplest)**
```bash
streamlit run streamlit_app.py
```
This automatically sets up the Python path - just run this!

**Option 2: Using the run script**
```bash
# Make sure script is executable
chmod +x run_app.sh

# Run the app
./run_app.sh
```

**Option 3: Using Python script**
```bash
python run_app.py
```

**Option 4: Manual (set PYTHONPATH)**
```bash
# Set Python path and run
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
streamlit run src/terrascan/app.py
```

**Option 5: Install as package (Best for Development)**
```bash
# Install in development mode
pip install -e .

# Then run normally
streamlit run src/terrascan/app.py
```

**Note:** If you see "No module named 'terrascan'", use Option 1, 2, 3, or 5. Option 4 requires setting PYTHONPATH manually.

The app will open in your browser where you can:
- Upload image files (GeoTIFF, JPEG, PNG, etc.)
- View image preview
- See detailed image information in the right pane including:
  - Basic information (dimensions, bands, driver)
  - Geospatial information (coordinates, pixel size)
  - Projection details
  - Band statistics and metadata

### Command Line Example

Run the example script:
```bash
python src/examples/gdal_example.py
```

### Using the GDAL Processor Module

The `terrascan.processors.gdal_processor` module provides reusable functions for GDAL operations:

```python
from terrascan.processors import GDALImageProcessor

# Initialize processor
processor = GDALImageProcessor()

# Open and analyze an image
dataset = processor.open_image('image.tif')
info = processor.get_image_info(dataset)
formatted_info = processor.format_info_for_display(info)

# Read band data
band_array = processor.read_band_as_array(dataset, band_number=1)

# Get preview for display
preview = processor.get_image_preview(dataset)
```

## Common GDAL Operations

### 1. Opening and Reading Images
```python
from osgeo import gdal

dataset = gdal.Open('image.tif')
band = dataset.GetRasterBand(1)
array = band.ReadAsArray()
```

### 2. Getting Image Metadata
```python
width = dataset.RasterXSize
height = dataset.RasterYSize
num_bands = dataset.RasterCount
geotransform = dataset.GetGeoTransform()
projection = dataset.GetProjection()
```

### 3. Converting Image Formats
```python
input_ds = gdal.Open('input.jpg')
driver = gdal.GetDriverByName('GTiff')
output_ds = driver.CreateCopy('output.tif', input_ds)
```

### 4. Creating New Images
```python
driver = gdal.GetDriverByName('GTiff')
out_dataset = driver.Create('new_image.tif', width, height, bands, gdal.GDT_Float32)
out_band = out_dataset.GetRasterBand(1)
out_band.WriteArray(data_array)
```

## Supported Formats

GDAL supports 100+ raster formats including:
- GeoTIFF (.tif, .tiff)
- JPEG (.jpg, .jpeg)
- PNG (.png)
- NetCDF (.nc)
- HDF (.hdf, .h5)
- And many more!

## Project Structure

```
terrascan-app/
├── src/                    # Source code
│   ├── terrascan/         # Main package
│   │   ├── app.py         # Streamlit application
│   │   ├── processors/    # Image processing backends
│   │   │   └── gdal_processor.py
│   │   ├── utils/         # Utility functions
│   │   └── visualizations/ # Visualization helpers
│   └── examples/          # Example scripts
├── docs/                   # Documentation
│   ├── learning/         # Learning resources
│   ├── deployment/        # Deployment guides
│   ├── installation/      # Installation guides
│   └── guides/            # Feature guides
├── scripts/                # Utility scripts
├── streamlit_app.py       # Entry point
├── requirements.txt       # Python dependencies
├── setup.sh               # Setup script
└── README.md              # This file
```

For detailed structure information, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Features

- **GDAL Processor Module** (`src/terrascan/processors/gdal_processor.py`): Reusable functions for:
  - Opening images (from file or bytes)
  - Extracting comprehensive image metadata
  - Reading band data as NumPy arrays
  - Generating image previews
  - Format conversion
  - Information formatting for display

- **Streamlit Web App** (`src/terrascan/app.py`): Interactive interface for:
  - Image upload and processing
  - Visual image preview
  - Detailed metadata display
  - Band information and statistics
  - Advanced visualizations
  - Image operations (NDVI, normalization, colormaps)

## Documentation

- **[Project Structure](PROJECT_STRUCTURE.md)** - Detailed project organization
- **[Learning Resources](docs/learning/README.md)** - Complete learning path
- **[Installation Guides](docs/installation/)** - Installation instructions
- **[Deployment Guides](docs/deployment/)** - Deployment options
- **[Feature Guides](docs/guides/)** - Feature documentation

## Resources

- [GDAL Python API Documentation](https://gdal.org/api/python.html)
- [GDAL Tutorial](https://gdal.org/tutorials/)
- [GDAL Python Examples](https://gdal.org/api/python/osgeo.gdal.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
