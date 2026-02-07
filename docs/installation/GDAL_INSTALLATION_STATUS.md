# GDAL Installation Status & Complete Setup Guide

## Current Status Check

Based on the system check, here's what we found:

### ❌ GDAL is NOT Currently Installed

**Missing Components:**
1. ❌ GDAL system libraries (not installed via Homebrew)
2. ❌ `gdal-config` command (not in PATH)
3. ❌ `gdalinfo` command (not available)
4. ❌ Python GDAL package (`osgeo` module not found)

---

## Complete Installation Guide for macOS

### Step 1: Install GDAL System Libraries

**Using Homebrew (Recommended):**

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install GDAL
brew install gdal

# Verify installation
gdal-config --version
gdalinfo --version
```

**What gets installed:**
- GDAL library (core)
- GDAL development headers
- GDAL command-line tools (`gdalinfo`, `gdal_translate`, etc.)
- All required dependencies

### Step 2: Install Python GDAL Package

After installing system GDAL, install the Python bindings:

```bash
# Get GDAL version
GDAL_VERSION=$(gdal-config --version)
echo "GDAL version: $GDAL_VERSION"

# Option A: Using uv (if you have it)
uv pip install "gdal==${GDAL_VERSION}.*"

# Option B: Using pip
pip install "gdal==${GDAL_VERSION}.*"

# Option C: Using conda (alternative)
conda install -c conda-forge gdal
```

**Important:** The Python package version must match the system GDAL version!

### Step 3: Verify Installation

```bash
# Check system GDAL
gdal-config --version
gdalinfo --version

# Check Python GDAL
python3 -c "from osgeo import gdal; print('GDAL version:', gdal.__version__)"

# Test import
python3 -c "from osgeo import gdal, osr; print('✅ GDAL is working!')"
```

### Step 4: Install Project Dependencies

```bash
# Navigate to project
cd /Users/yashrahurikar/yash/projects/personal/active/terrascan-app

# Install all dependencies
pip install -r requirements.txt

# Or with uv
uv pip install -r requirements.txt
```

---

## Installation Script for macOS

Create a macOS-specific installation script:

```bash
#!/bin/bash
# GDAL Installation Script for macOS

set -e

echo "🔧 Installing GDAL for macOS"
echo "============================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed"
    echo "Install it with:"
    echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi

# Step 1: Install GDAL
echo "Step 1: Installing GDAL system libraries via Homebrew..."
brew install gdal

echo ""
echo "✅ GDAL system libraries installed!"
echo ""

# Step 2: Verify gdal-config
if ! command -v gdal-config &> /dev/null; then
    echo "❌ Error: gdal-config not found after installation"
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
    source .venv/bin/activate
    pip install "gdal==${GDAL_VERSION}.*"
elif command -v uv &> /dev/null; then
    echo "Using uv..."
    uv pip install "gdal==${GDAL_VERSION}.*"
else
    echo "Installing globally (consider using a virtual environment)..."
    pip3 install "gdal==${GDAL_VERSION}.*"
fi

echo "✅ GDAL Python package installed!"
echo ""

# Step 4: Verify
echo "Step 3: Verifying installation..."
python3 -c "from osgeo import gdal; print('✅ GDAL Python version:', gdal.__version__)"

echo ""
echo "🎉 GDAL installation complete!"
echo ""
echo "Next steps:"
echo "  1. Install other dependencies: pip install -r requirements.txt"
echo "  2. Run the app: streamlit run streamlit_app.py"
```

---

## Troubleshooting

### Issue: `gdal-config: command not found`

**Solution:**
```bash
# Add Homebrew to PATH (if needed)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# Or for bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.bash_profile
source ~/.bash_profile
```

### Issue: Python can't find GDAL

**Solution:**
```bash
# Make sure Python package version matches system version
GDAL_VERSION=$(gdal-config --version)
pip uninstall gdal
pip install "gdal==${GDAL_VERSION}.*"
```

### Issue: ImportError: No module named 'osgeo'

**Solution:**
```bash
# Reinstall with correct version
GDAL_VERSION=$(gdal-config --version)
pip install --force-reinstall "gdal==${GDAL_VERSION}.*"
```

### Issue: Version mismatch

**Solution:**
```bash
# Check versions
gdal-config --version
python3 -c "from osgeo import gdal; print(gdal.__version__)"

# They should match! If not, reinstall Python package
```

---

## Quick Installation Checklist

- [ ] Homebrew installed
- [ ] GDAL system libraries installed (`brew install gdal`)
- [ ] `gdal-config --version` works
- [ ] `gdalinfo --version` works
- [ ] Python GDAL package installed (matching version)
- [ ] `python3 -c "from osgeo import gdal"` works
- [ ] Project dependencies installed (`pip install -r requirements.txt`)
- [ ] App runs successfully (`streamlit run streamlit_app.py`)

---

## Alternative: Using Conda

If you prefer conda (handles dependencies automatically):

```bash
# Install conda if needed
# Then:
conda install -c conda-forge gdal
conda install -c conda-forge python-gdal

# Verify
python -c "from osgeo import gdal; print(gdal.__version__)"
```

---

## Next Steps After Installation

1. **Test the installation:**
   ```bash
   python3 -c "from terrascan.processors import GDALImageProcessor; print('✅ Working!')"
   ```

2. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Try an example:**
   ```bash
   python src/examples/gdal_example.py
   ```

---

## Current System Status

**Your System:**
- OS: macOS (darwin 25.1.0) ✅
- Python: 3.13.1 ✅
- Homebrew: 5.0.13 ✅ (Installed)
- GDAL System: ❌ Not installed
- GDAL Python: ❌ Not installed

**Action Required:**
1. Install GDAL via Homebrew: `brew install gdal`
2. Install Python package: `pip install "gdal==$(gdal-config --version).*"`
3. Verify: `python3 -c "from osgeo import gdal; print(gdal.__version__)"`

**Quick Start:**
```bash
# Use the macOS installation script
./scripts/install_gdal_macos.sh
```

Or see [QUICK_INSTALL_MACOS.md](QUICK_INSTALL_MACOS.md) for step-by-step instructions.

---

## Need Help?

- Check [QUICK_INSTALL.md](QUICK_INSTALL.md) for quick reference
- Check [INSTALL_GDAL.md](INSTALL_GDAL.md) for detailed instructions
- Check [FIX_BUILD_ERROR.md](FIX_BUILD_ERROR.md) for troubleshooting
