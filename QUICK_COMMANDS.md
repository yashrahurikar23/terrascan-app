# Quick Command Reference

## 🚀 Running the App

### Option 1: Using the Run Script (Easiest)
```bash
cd /home/metheus/projects/image_processing
chmod +x run_app.sh
./run_app.sh
```

### Option 2: Using uv (Recommended)
```bash
cd /home/metheus/projects/image_processing
uv run streamlit run streamlit_app.py
```

### Option 3: Standard Python
```bash
cd /home/metheus/projects/image_processing
source .venv/bin/activate
streamlit run streamlit_app.py
```

---

## 📦 Setup & Installation

### Initial Setup
```bash
cd /home/metheus/projects/image_processing
./setup.sh
```

### Install GDAL (Fedora/RHEL)
```bash
cd /home/metheus/projects/image_processing
./install_gdal.sh
```

### Install GDAL (Manual)
```bash
# Install system libraries
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# Install Python package
cd /home/metheus/projects/image_processing
GDAL_VERSION=$(gdal-config --version)
uv pip install "gdal==${GDAL_VERSION}.*"
```

---

## 🔧 Common Commands

### Check GDAL Installation
```bash
uv run python -c "from osgeo import gdal; print('GDAL version:', gdal.__version__)"
```

### Install Dependencies
```bash
uv pip install -r requirements.txt
```

### Run with Custom Port
```bash
uv run streamlit run streamlit_app.py --server.port 8502
```

### Run in Headless Mode (No Browser)
```bash
uv run streamlit run streamlit_app.py --server.headless=true
```

---

## 📝 Quick Setup (All-in-One)

If starting fresh:

```bash
# 1. Navigate to project
cd /home/metheus/projects/image_processing

# 2. Install GDAL system libraries
sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal

# 3. Run setup
./setup.sh

# 4. Run the app
./run_app.sh
```

---

## 🐳 Docker Commands

### Build Docker Image
```bash
docker build -t gdal-app .
```

### Run Docker Container
```bash
docker run -p 8501:8501 gdal-app
```

### Use Docker Compose
```bash
docker-compose up
```

---

## ✅ Verification Commands

### Check if GDAL is installed
```bash
gdal-config --version
```

### Check if Python can import GDAL
```bash
uv run python -c "from osgeo import gdal; print('✅ GDAL works!')"
```

### Check Streamlit installation
```bash
uv run streamlit --version
```

---

## 🛑 Stopping the App

Press `Ctrl+C` in the terminal where the app is running.

---

## 📍 App URL

Once running, the app will be available at:
- **Local:** http://localhost:8501
- **Network:** http://0.0.0.0:8501 (if configured)

