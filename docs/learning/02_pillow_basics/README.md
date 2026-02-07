# Pillow (PIL) Basics - Lightweight Image Processing

## What You'll Learn

- What is Pillow and why use it?
- Pillow vs GDAL - when to use which
- Basic Pillow operations
- Reading and processing images with Pillow
- What you can do with Pillow

---

## 📖 Core Concepts

### 1. What is Pillow?

**Pillow (PIL)** is a lightweight, pure-Python image processing library.

**Key Features:**
- ✅ **No system dependencies** - Pure Python, easy to install
- ✅ **Fast installation** - Just `pip install pillow`
- ✅ **Wide format support** - JPEG, PNG, TIFF, BMP, GIF, and more
- ✅ **Simple API** - Easy to learn and use
- ✅ **Perfect for learning** - Great starting point for image processing

**Why Use Pillow?**
- When GDAL installation is problematic (network issues, system dependencies)
- For basic image operations (no geospatial data needed)
- Learning image processing concepts
- Quick prototyping and development
- When you need a lightweight solution

### 2. Pillow vs GDAL

| Feature | Pillow | GDAL |
|---------|--------|------|
| **Installation** | ✅ Easy (`pip install pillow`) | ❌ Complex (system dependencies) |
| **Download Size** | ✅ Small (~10MB) | ❌ Large (~100MB+) |
| **System Deps** | ✅ None | ❌ Required |
| **Geospatial** | ❌ No | ✅ Full support |
| **Formats** | ✅ Common (JPEG, PNG, TIFF) | ✅ 100+ formats |
| **Learning Curve** | ✅ Easy | ⚠️ Steeper |
| **Best For** | Basic processing, learning | Geospatial, production |

**When to Use Pillow:**
- Learning image processing
- Basic image operations
- No geospatial data needed
- Quick development
- Network/size constraints

**When to Use GDAL:**
- Geospatial data (coordinates, projections)
- Professional geospatial workflows
- Advanced format support
- Production applications

### 3. Basic Pillow Operations

#### Opening Images

```python
from PIL import Image

# Open an image file
img = Image.open('image.jpg')

# Get basic properties
print(f"Size: {img.size}")  # (width, height)
print(f"Mode: {img.mode}")  # RGB, RGBA, L (grayscale), etc.
print(f"Format: {img.format}")  # JPEG, PNG, etc.
```

#### Reading Image Data

```python
import numpy as np

# Convert to NumPy array
img_array = np.array(img)

# For RGB images: shape is (height, width, channels)
# For grayscale: shape is (height, width)

print(f"Array shape: {img_array.shape}")
print(f"Data type: {img_array.dtype}")
```

#### Image Statistics

```python
from PIL import ImageStat

# Get statistics
stats = ImageStat.Stat(img)

print(f"Mean: {stats.mean}")
print(f"Min: {stats.extrema[0]}")
print(f"Max: {stats.extrema[1]}")
print(f"Std Dev: {stats.stddev}")
```

#### Working with Bands

```python
# Get bands (for RGB: R, G, B)
bands = img.getbands()
print(f"Bands: {bands}")  # ('R', 'G', 'B') for RGB

# Split into individual bands
r, g, b = img.split()

# Get statistics for each band
r_stats = ImageStat.Stat(r)
print(f"Red band mean: {r_stats.mean[0]}")
```

---

## 🎯 What You Can Do with Pillow

### 1. Basic Image Operations

✅ **Image Reading & Writing**
- Open images in various formats
- Save images in different formats
- Convert between formats

✅ **Image Properties**
- Get dimensions (width, height)
- Get color mode (RGB, RGBA, grayscale)
- Get format information
- Read EXIF metadata

✅ **Image Statistics**
- Calculate min, max, mean, std dev
- Per-band statistics
- Histogram generation

### 2. Image Processing

✅ **Resizing & Scaling**
- Resize images
- Thumbnail generation
- Aspect ratio preservation

✅ **Color Operations**
- Convert color modes (RGB ↔ Grayscale)
- Adjust brightness/contrast
- Apply filters

✅ **Format Conversion**
- Convert between formats (JPEG ↔ PNG ↔ TIFF)
- Handle transparency
- Compression options

### 3. Advanced Operations (with NumPy)

✅ **Band Operations**
- Extract individual bands
- Combine bands
- Band math operations

✅ **Normalization**
- Min-max normalization
- Z-score normalization
- Histogram equalization

✅ **Visualization**
- Create histograms
- Generate statistics plots
- Band comparison

✅ **Spectral Indices**
- Calculate NDVI (if you have multi-band data)
- Other vegetation indices
- Band ratios

### 4. What Pillow CANNOT Do

❌ **Geospatial Data**
- No coordinate system support
- No geotransform parameters
- No projection information
- No spatial bounds

❌ **Advanced GeoTIFF Features**
- May not read all GeoTIFF metadata
- Limited support for geospatial tags

❌ **Professional Geospatial Workflows**
- Not suitable for GIS applications
- Limited for remote sensing

---

## 💻 Practical Examples

### Example 1: Basic Image Analysis

```python
from PIL import Image
import numpy as np

# Open image
img = Image.open('satellite_image.jpg')

# Get basic info
print(f"Size: {img.size}")
print(f"Mode: {img.mode}")
print(f"Format: {img.format}")

# Convert to array
arr = np.array(img)

# Calculate statistics
print(f"Min: {arr.min()}")
print(f"Max: {arr.max()}")
print(f"Mean: {arr.mean():.2f}")
print(f"Std Dev: {arr.std():.2f}")
```

### Example 2: Multi-Band Analysis

```python
from PIL import Image
import numpy as np

# Open RGB image
img = Image.open('rgb_image.jpg')

# Split into bands
r, g, b = img.split()

# Convert to arrays
r_arr = np.array(r)
g_arr = np.array(g)
b_arr = np.array(b)

# Calculate statistics for each band
print("Red Band:")
print(f"  Mean: {r_arr.mean():.2f}")
print(f"  Std: {r_arr.std():.2f}")

print("Green Band:")
print(f"  Mean: {g_arr.mean():.2f}")
print(f"  Std: {g_arr.std():.2f}")

print("Blue Band:")
print(f"  Mean: {b_arr.mean():.2f}")
print(f"  Std: {b_arr.std():.2f}")
```

### Example 3: NDVI Calculation (Multi-Band)

```python
from PIL import Image
import numpy as np

# Open multispectral image (assuming bands are Red and NIR)
# Note: This is a simplified example
img = Image.open('multispectral.tif')

# For this example, assume:
# Band 1 = Red
# Band 2 = NIR (Near-Infrared)

# If image has multiple bands, you might need to split them
# For demonstration:
red = np.array(img)[:, :, 0]  # First band
nir = np.array(img)[:, :, 1]  # Second band

# Calculate NDVI
red = red.astype(np.float32)
nir = nir.astype(np.float32)

denominator = red + nir
ndvi = np.where(denominator != 0, (nir - red) / denominator, 0)

print(f"NDVI Min: {ndvi.min():.3f}")
print(f"NDVI Max: {ndvi.max():.3f}")
print(f"NDVI Mean: {ndvi.mean():.3f}")
```

### Example 4: Image Normalization

```python
from PIL import Image
import numpy as np

# Open image
img = Image.open('image.jpg')
arr = np.array(img).astype(np.float32)

# Min-max normalization
arr_min = arr.min()
arr_max = arr.max()
normalized = (arr - arr_min) / (arr_max - arr_min) * 255

# Convert back to image
normalized_img = Image.fromarray(normalized.astype(np.uint8))
normalized_img.save('normalized.jpg')
```

---

## 🎓 Learning Path with Pillow

### Phase 1: Fundamentals ✅
- **Perfect for Pillow!**
- Learn pixels, bands, resolution
- Basic image properties
- All concepts apply

### Phase 2: Image Processing Libraries
- **Start with Pillow** (this phase)
- Learn basic operations
- Understand image data
- **Then move to GDAL** (if needed for geospatial)

### Phase 3: Geospatial Concepts ⚠️
- **Pillow limitation**: No geospatial support
- Use GDAL for this phase
- Or skip if not needed

### Phase 4: Image Operations ✅
- **Great with Pillow!**
- Format conversion ✅
- Normalization ✅
- Colormaps ✅
- All work perfectly

### Phase 5: Spectral Indices ✅
- **Works with Pillow!**
- NDVI calculation ✅
- Band math ✅
- If you have multi-band data

### Phase 6: Visualization ✅
- **Perfect for Pillow!**
- Histograms ✅
- Statistics ✅
- All visualizations work

### Phase 7: Advanced Topics ⚠️
- **Mixed support**
- Performance: ✅ Works
- Metadata: ⚠️ Limited
- Batch processing: ✅ Works

---

## 🛠️ Using Pillow in the App

The app supports Pillow! Here's how:

### 1. Automatic Selection
- App automatically uses Pillow if GDAL isn't available
- No configuration needed

### 2. Manual Selection
- Go to sidebar → "⚙️ Processor Settings"
- Select "pillow" from dropdown

### 3. What Works
- ✅ All tabs work with Pillow
- ✅ Overview, Bands, Metadata tabs
- ✅ Visualizations tab
- ✅ Operations tab (most features)
- ⚠️ Geospatial tab (limited - no coordinates)

---

## 📚 Exercises

### Exercise 1: Basic Image Analysis
1. Open an image with Pillow
2. Print its dimensions and mode
3. Calculate min, max, mean, std dev
4. Display the image

### Exercise 2: Multi-Band Analysis
1. Open an RGB image
2. Split into individual bands
3. Calculate statistics for each band
4. Compare the bands

### Exercise 3: Histogram Creation
1. Open an image
2. Convert to NumPy array
3. Create a histogram
4. Visualize with matplotlib

### Exercise 4: Format Conversion
1. Open a JPEG image
2. Convert to PNG
3. Convert to TIFF
4. Compare file sizes

### Exercise 5: Normalization
1. Open an image
2. Apply min-max normalization
3. Apply z-score normalization
4. Compare results

---

## 🔗 Resources

### Official Documentation
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [PIL Handbook](https://pillow.readthedocs.io/en/stable/handbook/index.html)

### Tutorials
- [Pillow Tutorial](https://pillow.readthedocs.io/en/stable/handbook/tutorial.html)
- [Image Processing with Python](https://realpython.com/image-processing-with-the-python-pillow-library/)

### In This App
- See `src/terrascan/processors/pillow_processor.py` for implementation
- All features are available in the UI

---

## ✅ Key Takeaways

1. **Pillow is perfect for learning** - Simple, easy to install
2. **Great for basic operations** - Reading, statistics, conversion
3. **No geospatial support** - Use GDAL for coordinates/projections
4. **Works in the app** - All features available
5. **Start here** - Learn concepts, then move to GDAL if needed

---

## 🚀 Next Steps

1. **Try Pillow in the app** - Upload an image, select "pillow" processor
2. **Do the exercises** - Practice with real images
3. **Explore the code** - See `pillow_processor.py`
4. **Move to GDAL** - When you need geospatial features (Phase 2: GDAL Basics)

**Remember:** Pillow is a great starting point! Learn the concepts, then graduate to GDAL when you need geospatial capabilities.
