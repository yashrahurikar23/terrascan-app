# Quick Fix: "No module named 'terrascan'" Error

## 🐛 Problem

When running the Streamlit app, you see:
- "No image processors are available on this platform"
- Technical Error: "No module named 'terrascan'"

## ✅ Solution

The app can't find the `terrascan` module because `src/` isn't in Python's path.

### Quick Fix (Choose One):

#### Option 1: Use the Run Script (Easiest) ⭐

```bash
# Make executable (if needed)
chmod +x run_app.sh

# Run the app
./run_app.sh
```

#### Option 2: Use Python Script

```bash
python run_app.py
```

#### Option 3: Set PYTHONPATH Manually

```bash
# On macOS/Linux:
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
streamlit run src/terrascan/app.py

# On Windows (PowerShell):
$env:PYTHONPATH = "$PWD\src;$env:PYTHONPATH"
streamlit run src/terrascan/app.py
```

#### Option 4: Install as Package (Best for Development)

```bash
# Install in development mode
pip install -e .

# Then run normally
streamlit run src/terrascan/app.py
```

---

## 🔍 Why This Happens

The app uses imports like:
```python
from terrascan.processors import ...
```

Python needs to know where `terrascan` is. Since it's in `src/terrascan/`, we need to add `src/` to Python's path.

---

## ✅ After Fixing

Once you run with the correct path, you should see:
- ✅ App loads successfully
- ✅ Processor selection in sidebar
- ✅ Pillow processor available (if installed)
- ✅ GDAL/Rasterio available (if installed)

---

## 🚀 Recommended: Use run_app.sh

The `run_app.sh` script handles everything automatically:
- Sets PYTHONPATH correctly
- Runs the app
- Works on macOS/Linux

Just run: `./run_app.sh`
