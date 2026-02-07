# Quick GDAL Installation for macOS

## Prerequisites

- macOS (you're on macOS!)
- Homebrew installed (check with `brew --version`)
- Python 3.8+ (you have Python 3.13.1 ✅)

## Quick Installation (3 Steps)

### Option 1: Using the Installation Script (Recommended)

```bash
# Navigate to project
cd /Users/yashrahurikar/yash/projects/personal/active/terrascan-app

# Run the macOS installation script
./scripts/install_gdal_macos.sh
```

The script will:
- ✅ Install GDAL via Homebrew
- ✅ Install matching Python package
- ✅ Verify installation

### Option 2: Manual Installation

```bash
# Step 1: Install GDAL system libraries
brew install gdal

# Step 2: Get GDAL version
GDAL_VERSION=$(gdal-config --version)
echo "GDAL version: $GDAL_VERSION"

# Step 3: Install Python package (matching version)
pip3 install "gdal==${GDAL_VERSION}.*"

# Or if using uv:
uv pip install "gdal==${GDAL_VERSION}.*"

# Step 4: Verify
python3 -c "from osgeo import gdal; print('✅ GDAL version:', gdal.__version__)"
```

## Install Project Dependencies

After GDAL is installed:

```bash
# Using pip
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

## Run the App

```bash
streamlit run streamlit_app.py
```

## Troubleshooting

### Issue: `gdal-config: command not found`

**Solution:**
```bash
# Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# Or for bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.bash_profile
source ~/.bash_profile
```

### Issue: Python can't import GDAL

**Solution:**
```bash
# Make sure versions match
GDAL_VERSION=$(gdal-config --version)
pip3 uninstall gdal
pip3 install "gdal==${GDAL_VERSION}.*"
```

### Issue: Permission errors

**Solution:**
```bash
# Use virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install "gdal==$(gdal-config --version).*"
```

## Verification Checklist

- [ ] `brew install gdal` completed successfully
- [ ] `gdal-config --version` works
- [ ] `gdalinfo --version` works
- [ ] `python3 -c "from osgeo import gdal"` works
- [ ] `pip install -r requirements.txt` completed
- [ ] `streamlit run streamlit_app.py` works

## Need More Help?

- See [GDAL_INSTALLATION_STATUS.md](GDAL_INSTALLATION_STATUS.md) for detailed status
- See [INSTALL_GDAL.md](INSTALL_GDAL.md) for detailed instructions
- See [FIX_BUILD_ERROR.md](FIX_BUILD_ERROR.md) for troubleshooting
