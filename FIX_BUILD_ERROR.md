# Fix: C++ Compiler Missing Error

## Problem

When installing GDAL, you may encounter this error:
```
error: command 'c++' failed: No such file or directory
```

This happens because GDAL Python package needs to be compiled from source, which requires C++ build tools.

## Solution

Install the required build tools along with GDAL:

```bash
# Install build tools and GDAL
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# Then install GDAL Python package
cd /home/metheus/projects/image_processing
GDAL_VERSION=$(gdal-config --version)
uv pip install "gdal==${GDAL_VERSION}.*"
```

## Required Packages

- **gcc-c++**: C++ compiler (replaces the missing `c++` command)
- **make**: Build automation tool
- **python3-devel**: Python development headers needed for building extensions
- **gdal**: GDAL library
- **gdal-devel**: GDAL development headers
- **python3-gdal**: System Python GDAL bindings (optional, but helpful)

## Alternative: Use Pre-built Package

If you want to avoid building from source, you can use the system's python3-gdal package:

```bash
sudo dnf install -y python3-gdal

# Then use system Python instead of virtual environment
python3 -c "from osgeo import gdal; print(gdal.__version__)"
```

However, for the Streamlit app in a virtual environment, you'll need to build the package.
