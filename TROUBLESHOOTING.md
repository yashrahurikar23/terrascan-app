# Troubleshooting Guide

## 🐛 Common Issues and Solutions

### Issue 1: "No module named 'terrascan'"

**Error Message:**
```
Technical Error: No module named 'terrascan'
No image processors are available on this platform
```

**Cause:**
Python can't find the `terrascan` module because `src/` isn't in the Python path.

**Solutions (try in order):**

#### ✅ Solution 1: Use streamlit_app.py (Easiest)
```bash
streamlit run streamlit_app.py
```

This file automatically sets up the Python path.

#### ✅ Solution 2: Use run_app.sh
```bash
chmod +x run_app.sh
./run_app.sh
```

#### ✅ Solution 3: Use run_app.py
```bash
python run_app.py
```

#### ✅ Solution 4: Set PYTHONPATH manually
```bash
# macOS/Linux
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
streamlit run src/terrascan/app.py

# Windows (PowerShell)
$env:PYTHONPATH = "$PWD\src;$env:PYTHONPATH"
streamlit run src\terrascan\app.py
```

#### ✅ Solution 5: Install as package (Best for development)
```bash
pip install -e .
streamlit run src/terrascan/app.py
```

---

### Issue 2: "No image processors are available"

**Error Message:**
```
No image processors are available on this platform
```

**Possible Causes:**

1. **Pillow not installed** (most common)
   ```bash
   pip install pillow
   ```

2. **Python path issue** (see Issue 1 above)

3. **Import errors in processor modules**

**Check:**
```bash
python -c "from terrascan.processors import PillowImageProcessor; p = PillowImageProcessor(); print(f'Pillow available: {p.available}')"
```

---

### Issue 3: GDAL Installation Problems

**Symptoms:**
- GDAL processor not available
- Installation errors

**Solutions:**

1. **Use Pillow instead** (recommended for learning)
   - Pillow works without GDAL
   - Select "pillow" in sidebar

2. **Install GDAL** (when network allows)
   - See `docs/installation/` for guides
   - Or use Docker (see Dockerfile)

---

### Issue 4: App Runs But Shows Errors

**Check:**
1. Are you using the correct run command?
2. Is PYTHONPATH set correctly?
3. Are required packages installed?

**Debug:**
```bash
# Check if module can be imported
python -c "import sys; sys.path.insert(0, 'src'); from terrascan.processors import PillowImageProcessor; print('OK')"
```

---

## ✅ Quick Verification

Run these commands to verify setup:

```bash
# 1. Check Python path
python -c "import sys; print('\\n'.join(sys.path))"

# 2. Check if terrascan can be imported (from project root)
python -c "import sys; sys.path.insert(0, 'src'); import terrascan; print('✅ terrascan imported')"

# 3. Check Pillow processor
python -c "import sys; sys.path.insert(0, 'src'); from terrascan.processors import PillowImageProcessor; p = PillowImageProcessor(); print(f'✅ Pillow available: {p.available}')"

# 4. Check all processors
python -c "import sys; sys.path.insert(0, 'src'); from terrascan.processors import list_available_processors; print(f'✅ Available: {list_available_processors()}')"
```

---

## 🚀 Recommended Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **If that doesn't work:**
   ```bash
   ./run_app.sh
   ```

---

## 💡 Tips

- **Always run from project root** (where `streamlit_app.py` is)
- **Use `streamlit_app.py`** - it handles the path automatically
- **Check Pillow first** - it's the easiest to get working
- **Install as package** - best for development: `pip install -e .`

---

## 📞 Still Having Issues?

1. Check `QUICK_FIX.md` for the most common solution
2. Verify your Python environment
3. Check that all files are in the correct locations
4. Try installing as package: `pip install -e .`
