# ⚠️ IMPORTANT: How to Run the App

## 🚨 If You See "No module named 'terrascan'"

This error means Python can't find the `terrascan` module. **Use the correct run command!**

---

## ✅ Correct Way to Run

### **Option 1: Use streamlit_app.py (Recommended)** ⭐

```bash
streamlit run streamlit_app.py
```

**This is the easiest!** The file automatically sets up the Python path.

---

### Option 2: Use run_app.sh

```bash
chmod +x run_app.sh
./run_app.sh
```

---

### Option 3: Use run_app.py

```bash
python run_app.py
```

---

## ❌ Don't Use This (Unless PYTHONPATH is Set)

```bash
# This WON'T work without PYTHONPATH:
streamlit run src/terrascan/app.py
```

---

## 🔍 Why This Happens

The app uses imports like:
```python
from terrascan.processors import ...
```

Python needs to know where `terrascan` is. Since it's in `src/terrascan/`, we need to add `src/` to Python's path.

The helper scripts (`streamlit_app.py`, `run_app.sh`, `run_app.py`) do this automatically!

---

## ✅ After Running Correctly

You should see:
- ✅ **No error messages**
- ✅ **Sidebar shows "⚙️ Processor Settings"**
- ✅ **Pillow processor available** (if installed)
- ✅ **Upload button works**

---

## 💡 Pillow Should Work!

If Pillow is installed (`pip install pillow`), it should be detected automatically when you run with the correct command.

**Pillow is in `requirements.txt`**, so if you installed dependencies, Pillow should be available!

---

## 🚀 Quick Test

1. **Run the app correctly:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Check the sidebar** - you should see processor selection

3. **Upload an image** - it should work with Pillow!

---

## 📚 More Help

- See `QUICK_FIX.md` for quick solutions
- See `TROUBLESHOOTING.md` for detailed help
- See `README.md` for full documentation
