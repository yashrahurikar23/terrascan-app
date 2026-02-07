# Cloud Deployment Fix for ODBC Package Errors

## Issue
Streamlit Cloud was encountering dpkg errors when installing ODBC dependencies required by GDAL:
```
Errors were encountered while processing:
 /tmp/apt-dpkg-install-DEPyW7/040-libodbc2_2.3.11-2+deb12u1_amd64.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

## Solution Applied

### 1. Simplified packages.txt
Changed from installing multiple packages to just:
```
python3-gdal
```

The `python3-gdal` package automatically pulls in:
- `libgdal-dev` (as dependency)
- `gdal-bin` (as dependency)
- All other required dependencies

This reduces the chance of dependency conflicts.

### 2. Updated requirements.txt
Removed `gdal>=3.8.0` from requirements.txt because:
- The system `python3-gdal` package provides the Python bindings
- Installing GDAL via pip requires building from source, which needs system libraries
- Using the system package avoids build issues

## How It Works

1. **System packages** (`packages.txt`):
   - Installs `python3-gdal` which includes Python bindings
   - Automatically installs `libgdal-dev` and `gdal-bin` as dependencies

2. **Python packages** (`requirements.txt`):
   - Installs all other dependencies (streamlit, numpy, etc.)
   - GDAL is already available from the system package

3. **App behavior**:
   - The app imports `from osgeo import gdal`
   - This will work with the system `python3-gdal` package
   - No need to build GDAL from source

## If ODBC Errors Persist

If you still see ODBC package errors, try:

### Option 1: Install packages individually with fixes
Update `packages.txt` to:
```
libgdal-dev
gdal-bin
```

And add to `requirements.txt`:
```
gdal>=3.8.0
```

Then manually fix broken packages in a post-install script (if supported).

### Option 2: Use conda (if Streamlit Cloud supports it)
Create `environment.yml`:
```yaml
name: terrascan-app
dependencies:
  - conda-forge::gdal
  - python=3.11
  - pip
  - pip:
    - streamlit>=1.28.0
    - numpy>=1.24.0
    - pillow>=10.0.0
    - matplotlib>=3.7.0
    - plotly>=5.14.0
    - pandas>=2.0.0
    - scipy>=1.10.0
```

### Option 3: Make GDAL truly optional
The app already handles missing GDAL gracefully. You could:
- Remove GDAL from packages.txt entirely
- App will show installation instructions instead of crashing
- Users can install GDAL manually if needed

## Verification

After deployment, check logs for:
- ✅ `python3-gdal` installed successfully
- ✅ No ODBC package errors
- ✅ App starts without GDAL import errors
- ✅ App shows "GDAL is not installed" message if system package isn't accessible

## Current Status

The latest commit uses:
- `packages.txt`: `python3-gdal` only
- `requirements.txt`: All packages except GDAL (uses system package)

This should avoid the ODBC dependency conflicts while still providing GDAL functionality.
