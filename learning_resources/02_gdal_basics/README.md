# Phase 2: GDAL Basics

## What You'll Learn

- What GDAL is and why it's powerful
- How to open and read images with GDAL
- Understanding datasets and bands
- Extracting metadata
- Basic GDAL operations

---

## 📖 Core Concepts

### 1. What is GDAL?

**GDAL** = Geospatial Data Abstraction Library

**Key Points:**
- Open-source library for reading/writing geospatial raster and vector data
- Supports 200+ formats (GeoTIFF, JPEG, HDF, NetCDF, etc.)
- Used by QGIS, ArcGIS, Google Earth, and many other tools
- Python bindings available (`osgeo.gdal`)

**Why GDAL?**
- Handles geospatial metadata automatically
- Works with many formats
- Powerful processing capabilities
- Industry standard

### 2. GDAL Core Concepts

**Dataset:**
- The entire image file
- Contains one or more bands
- Has metadata (dimensions, projection, etc.)

**Band:**
- A single layer of data
- Like a channel in RGB (Red, Green, Blue)
- Each band has its own statistics and properties

**Geotransform:**
- Links pixel coordinates to real-world coordinates
- 6 parameters that define the transformation
- Allows you to know where each pixel is on Earth

### 3. Opening Images with GDAL

**Basic Pattern:**
```python
from osgeo import gdal

# Open dataset
dataset = gdal.Open('image.tif')

# Get basic info
width = dataset.RasterXSize
height = dataset.RasterYSize
bands = dataset.RasterCount

# Close when done
dataset = None
```

**Important:** Always close datasets when done!

### 4. Reading Band Data

**Reading a Single Band:**
```python
# Get band 1 (first band)
band = dataset.GetRasterBand(1)

# Read as array
data = band.ReadAsArray()

# Get statistics
stats = band.GetStatistics(True, True)  # min, max, mean, std dev
```

**Reading Multiple Bands:**
```python
# Read all bands
all_bands = []
for i in range(1, dataset.RasterCount + 1):
    band = dataset.GetRasterBand(i)
    data = band.ReadAsArray()
    all_bands.append(data)
```

### 5. Metadata

**Dataset Metadata:**
```python
# Get all metadata
metadata = dataset.GetMetadata()

# Get specific metadata
driver_name = dataset.GetDriver().ShortName
```

**Band Metadata:**
```python
band = dataset.GetRasterBand(1)
band_metadata = band.GetMetadata()
no_data = band.GetNoDataValue()
```

### 6. Geotransform

**What is it?**
- 6 numbers that define how pixels map to real-world coordinates
- [origin_x, pixel_width, rotation, origin_y, rotation, pixel_height]

**Getting Geotransform:**
```python
geotransform = dataset.GetGeoTransform()

origin_x = geotransform[0]      # Top-left X coordinate
origin_y = geotransform[3]      # Top-left Y coordinate
pixel_width = geotransform[1]    # Pixel width in X direction
pixel_height = geotransform[5]  # Pixel height in Y direction
```

---

## 🎯 Learning Objectives

By the end of this phase, you should be able to:

1. ✅ Open an image with GDAL
2. ✅ Extract basic properties (width, height, bands)
3. ✅ Read band data as numpy arrays
4. ✅ Extract statistics from bands
5. ✅ Understand what geotransform means
6. ✅ Extract metadata

---

## 📝 Exercises

### Exercise 1: Open and Examine an Image

**Goal:** Use GDAL to open an image and see its properties

**Steps:**
1. Open a GeoTIFF with GDAL
2. Print dimensions and band count
3. Get the driver name

**Code Template:**
```python
from osgeo import gdal

# Open dataset
dataset = gdal.Open('your_image.tif')

if dataset is None:
    print("Failed to open image")
else:
    print(f"Width: {dataset.RasterXSize}")
    print(f"Height: {dataset.RasterYSize}")
    print(f"Bands: {dataset.RasterCount}")
    print(f"Driver: {dataset.GetDriver().ShortName}")

# Close
dataset = None
```

### Exercise 2: Read Band Data

**Goal:** Read a band and calculate statistics

**Steps:**
1. Open an image
2. Get the first band
3. Read as array
4. Calculate statistics manually

**Code Template:**
```python
from osgeo import gdal
import numpy as np

dataset = gdal.Open('your_image.tif')
band = dataset.GetRasterBand(1)

# Read data
data = band.ReadAsArray()

# Calculate statistics
print(f"Min: {data.min()}")
print(f"Max: {data.max()}")
print(f"Mean: {data.mean():.2f}")
print(f"Std Dev: {data.std():.2f}")

# Or use GDAL's built-in statistics
stats = band.GetStatistics(True, True)
print(f"GDAL Stats - Min: {stats[0]}, Max: {stats[1]}, Mean: {stats[2]}, Std: {stats[3]}")

dataset = None
```

### Exercise 3: Extract Geotransform

**Goal:** Understand the geospatial information

**Steps:**
1. Open a GeoTIFF
2. Get geotransform
3. Calculate spatial bounds
4. Calculate pixel resolution

**Code Template:**
```python
from osgeo import gdal

dataset = gdal.Open('your_image.tif')
gt = dataset.GetGeoTransform()

origin_x = gt[0]
origin_y = gt[3]
pixel_width = gt[1]
pixel_height = gt[5]

width = dataset.RasterXSize
height = dataset.RasterYSize

# Calculate bounds
min_x = origin_x
max_x = origin_x + (width * pixel_width)
min_y = origin_y + (height * pixel_height)
max_y = origin_y

print(f"Origin: ({origin_x}, {origin_y})")
print(f"Pixel Size: {pixel_width} x {pixel_height}")
print(f"Bounds: X({min_x} to {max_x}), Y({min_y} to {max_y})")

dataset = None
```

### Exercise 4: Read All Bands

**Goal:** Read and compare multiple bands

**Steps:**
1. Open a multi-band image
2. Read all bands
3. Compare statistics across bands

**Code Template:**
```python
from osgeo import gdal
import numpy as np

dataset = gdal.Open('multiband_image.tif')

for i in range(1, dataset.RasterCount + 1):
    band = dataset.GetRasterBand(i)
    data = band.ReadAsArray()
    
    print(f"\nBand {i}:")
    print(f"  Min: {data.min()}, Max: {data.max()}")
    print(f"  Mean: {data.mean():.2f}, Std: {data.std():.2f}")

dataset = None
```

---

## 🔗 Related to Our App

In our Streamlit app, these concepts appear in:

1. **Overview Tab**: Shows width, height, bands (from `dataset.RasterXSize`, etc.)
2. **Bands Tab**: Shows statistics for each band (from `band.GetStatistics()`)
3. **Geospatial Tab**: Shows geotransform parameters
4. **gdal_utils.py**: All the GDAL operations we use

**Try This:**
- Look at `gdal_utils.py` - see how we use GDAL
- Upload an image to the app
- Compare what you see in the app with what you learned here

---

## 🐛 Common Issues

**Issue: "Failed to open image"**
- Check file path is correct
- Check file format is supported
- Check file isn't corrupted

**Issue: "No geotransform"**
- Not all images have geospatial information
- Regular JPEG/PNG don't have geotransform
- Only GeoTIFF and similar formats have it

**Issue: "Memory error"**
- Large images can use lots of memory
- Read subsets instead of entire image
- Use `ReadAsArray(xoff, yoff, xsize, ysize)` for subsets

---

## 📚 Additional Resources

- [GDAL Python API](https://gdal.org/api/python_bindings.html)
- [GDAL Tutorial](https://gdal.org/tutorials/index.html)
- [GDAL Python Examples](https://gdal.org/api/python/osgeo.gdal.html)

---

## ✅ Check Your Understanding

Before moving to Phase 3, make sure you can:

- [ ] Open an image with GDAL
- [ ] Read band data as numpy arrays
- [ ] Extract statistics from bands
- [ ] Understand what a geotransform is
- [ ] Extract metadata from datasets and bands

**Ready for Phase 3?** Once you're comfortable with GDAL basics, move on to Geospatial Concepts!

