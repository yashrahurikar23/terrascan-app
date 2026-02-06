# Phase 1: Fundamentals

## What You'll Learn

- What digital images are
- How computers represent images
- Basic image properties
- Image data types
- Basic statistics

---

## 📖 Core Concepts

### 1. What is a Digital Image?

A digital image is a grid of numbers called **pixels** (picture elements).

**Key Concepts:**
- **Pixel**: The smallest unit of an image (a single number or set of numbers)
- **Resolution**: The number of pixels (width × height)
- **Channels/Bands**: Different layers of information (e.g., Red, Green, Blue)

**Example:**
- A 1000×1000 image has 1,000,000 pixels
- Each pixel can have multiple values (bands)
- RGB image: 3 bands (Red, Green, Blue)
- Grayscale: 1 band

### 2. Raster vs Vector Data

**Raster Images:**
- Grid of pixels
- Each pixel has a value
- Examples: Photos, satellite imagery, scanned maps
- **What we're working with in this app**

**Vector Data:**
- Points, lines, polygons
- Mathematical representations
- Examples: Shapefiles, GeoJSON
- **Not covered in this app**

### 3. Image Formats

**Common Formats:**
- **TIFF/GeoTIFF**: Best for geospatial data, supports multiple bands, lossless
- **JPEG**: Good for photos, lossy compression, 3 bands (RGB)
- **PNG**: Good for graphics, lossless, supports transparency
- **JPEG2000**: Modern format, good compression, supports multiple bands

**For Geospatial Work:**
- **GeoTIFF** is the standard
- Contains both image data AND location information
- This is what GDAL excels at

### 4. Data Types

**Common Data Types:**
- **Byte (8-bit)**: Values 0-255 (most common for display)
- **UInt16 (16-bit)**: Values 0-65535 (satellite imagery)
- **Int16**: Values -32768 to 32767
- **Float32**: Decimal numbers (precise calculations)
- **Float64**: Very precise decimal numbers

**Why It Matters:**
- Determines the range of values
- Affects file size
- Affects precision
- Affects what operations you can do

### 5. Image Statistics

**Basic Statistics:**
- **Min**: Lowest pixel value
- **Max**: Highest pixel value
- **Mean**: Average of all pixel values
- **Std Dev**: How spread out the values are (contrast)
- **Median**: Middle value when sorted

**What They Tell Us:**
- **Min/Max**: Dynamic range of the image
- **Mean**: Overall brightness
- **Std Dev**: Contrast/variability
- **Median**: Typical value (less affected by outliers)

---

## 🎯 Learning Objectives

By the end of this phase, you should be able to:

1. ✅ Explain what a pixel is
2. ✅ Understand the difference between raster and vector
3. ✅ Identify common image formats
4. ✅ Understand data types and their ranges
5. ✅ Calculate and interpret basic statistics
6. ✅ Read an image and examine its properties

---

## 📝 Exercises

### Exercise 1: Examine an Image

**Goal:** Open an image and see its basic properties

**Steps:**
1. Use Python/PIL to open a simple image (JPEG or PNG)
2. Print its dimensions (width, height)
3. Print its mode (RGB, grayscale, etc.)
4. Convert to numpy array
5. Print the shape of the array

**Code Template:**
```python
from PIL import Image
import numpy as np

# Open image
img = Image.open('your_image.jpg')

# Basic properties
print(f"Size: {img.size}")  # (width, height)
print(f"Mode: {img.mode}")   # RGB, L (grayscale), etc.

# Convert to numpy array
arr = np.array(img)
print(f"Array shape: {arr.shape}")  # (height, width, channels)
```

### Exercise 2: Calculate Statistics

**Goal:** Calculate basic statistics for an image

**Steps:**
1. Load an image as numpy array
2. Calculate min, max, mean, std dev
3. For RGB images, calculate for each channel separately

**Code Template:**
```python
import numpy as np
from PIL import Image

img = Image.open('your_image.jpg')
arr = np.array(img)

# For grayscale
if len(arr.shape) == 2:
    print(f"Min: {arr.min()}")
    print(f"Max: {arr.max()}")
    print(f"Mean: {arr.mean():.2f}")
    print(f"Std Dev: {arr.std():.2f}")

# For RGB (3 channels)
elif len(arr.shape) == 3:
    for i, channel in enumerate(['Red', 'Green', 'Blue']):
        band = arr[:, :, i]
        print(f"{channel} - Min: {band.min()}, Max: {band.max()}, Mean: {band.mean():.2f}")
```

### Exercise 3: Create a Histogram

**Goal:** Visualize the distribution of pixel values

**Steps:**
1. Load an image
2. Create a histogram using matplotlib
3. Interpret the histogram

**Code Template:**
```python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

img = Image.open('your_image.jpg')
arr = np.array(img)

# For grayscale
if len(arr.shape) == 2:
    plt.hist(arr.flatten(), bins=256, range=(0, 256))
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Image Histogram')
    plt.show()
```

---

## 🔗 Related to Our App

In our Streamlit app, these concepts appear in:

1. **Overview Tab**: Width, Height, Bands, Total Pixels
2. **Bands Tab**: Min, Max, Mean, Std Dev statistics
3. **Visualizations Tab**: Histograms showing pixel value distributions

**Try This:**
- Upload an image to the app
- Look at the Overview tab - see how it shows dimensions
- Look at the Bands tab - see the statistics we just learned about
- Look at Visualizations - see the histogram

---

## 📚 Additional Resources

- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [NumPy Arrays Tutorial](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Digital Image Basics](https://en.wikipedia.org/wiki/Digital_image)

---

## ✅ Check Your Understanding

Before moving to Phase 2, make sure you can:

- [ ] Explain what a pixel is
- [ ] Understand the difference between 8-bit and 16-bit images
- [ ] Calculate min, max, mean, and std dev for an image
- [ ] Create a histogram
- [ ] Understand what "bands" or "channels" mean

**Ready for Phase 2?** Once you're comfortable with these concepts, move on to GDAL Basics!

