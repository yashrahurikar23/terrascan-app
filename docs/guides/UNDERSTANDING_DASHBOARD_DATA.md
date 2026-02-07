# Understanding Dashboard Data

## Overview

This guide explains what all the metrics, visualizations, and data in the Terrascan dashboard mean and how to interpret them for practical use.

---

## 📊 Tab 1: Overview

### Basic Metrics

**Width & Height (pixels)**
- **What it means:** The dimensions of your image in pixels
- **Why it matters:** 
  - Larger images = more detail but slower processing
  - Common sizes: 1920×1080 (HD), 3840×2160 (4K), satellite images can be 10,000+ pixels
- **Example:** A 5000×5000 pixel image has 25 million pixels per band

**Bands (channels)**
- **What it means:** Number of color/spectral channels
- **Common values:**
  - **1 band** = Grayscale (black & white)
  - **3 bands** = RGB (Red, Green, Blue) - standard color photos
  - **4 bands** = RGBA (RGB + Alpha/transparency)
  - **5+ bands** = Multispectral (satellite imagery, scientific data)
- **Why it matters:** More bands = more information, but larger file sizes

**Total Pixels**
- **What it means:** Width × Height = total data points per band
- **Why it matters:** Helps estimate file size and processing time

**Driver**
- **What it means:** The file format (GTiff, JPEG, PNG, etc.)
- **Why it matters:** Different formats support different features (geospatial data, compression, etc.)

---

## 🌍 Tab 2: Geospatial Information

*Only shown if your image has geospatial data (coordinates, projection)*

### Geotransform Parameters

**Origin X & Y**
- **What it means:** The real-world coordinates of the top-left pixel
- **Example:** 
  - X = -122.4194 (longitude, San Francisco)
  - Y = 37.7749 (latitude, San Francisco)
- **Why it matters:** Tells you WHERE on Earth the image is located

**Pixel Width & Height**
- **What it means:** How much ground distance one pixel represents
- **Example:**
  - Pixel Width = 0.0001 degrees = ~11 meters (at equator)
  - Pixel Height = -0.0001 degrees (negative = northward)
- **Why it matters:** 
  - Smaller values = higher resolution (more detail)
  - Larger values = lower resolution (less detail)
  - Helps understand image scale

### Spatial Bounds

**Min/Max X & Y**
- **What it means:** The geographic extent of your image
- **Example:**
  - Min X = -122.5 (western edge)
  - Max X = -122.3 (eastern edge)
  - Min Y = 37.7 (southern edge)
  - Max Y = 37.9 (northern edge)
- **Why it matters:** Defines the exact area covered by your image

### Projection

**EPSG Code**
- **What it means:** Standard coordinate system identifier
- **Common codes:**
  - EPSG:4326 = WGS84 (latitude/longitude, used by GPS)
  - EPSG:3857 = Web Mercator (used by Google Maps)
  - EPSG:32633 = UTM Zone 33N (meters, for Europe)
- **Why it matters:** Ensures accurate mapping and alignment with other geospatial data

---

## 🎨 Tab 3: Band Details

### Statistics for Each Band

**Min & Max**
- **What it means:** The lowest and highest pixel values in the band
- **Example:** Min = 0, Max = 255 (8-bit image)
- **Why it matters:**
  - **Low min, high max** = Good contrast, wide dynamic range
  - **Min ≈ Max** = Low contrast, image may look flat
  - **Min = 0, Max = 255** = Full range used (good)
  - **Min = 50, Max = 200** = Not using full range (may need normalization)

**Mean (Average)**
- **What it means:** Average brightness/value across all pixels
- **Example:** Mean = 127.5 (middle gray for 8-bit)
- **Why it matters:**
  - **Low mean (< 50)** = Dark image overall
  - **High mean (> 200)** = Bright image overall
  - **Mean ≈ 128** = Well-balanced brightness
  - Compare means between bands to see which is brighter/darker

**Std Dev (Standard Deviation)**
- **What it means:** How much pixel values vary (spread)
- **Example:** Std Dev = 45.2
- **Why it matters:**
  - **High std dev (> 50)** = High contrast, lots of variation (good for detail)
  - **Low std dev (< 20)** = Low contrast, uniform values (may be flat/boring)
  - **Very low std dev (< 5)** = Almost uniform, may indicate a problem

**Median**
- **What it means:** The middle value when all pixels are sorted
- **Why it matters:** Less affected by outliers than mean. If median ≠ mean, indicates skewed distribution

**Unique Values**
- **What it means:** How many different pixel values exist
- **Example:** 256 unique values in an 8-bit image (0-255)
- **Why it matters:**
  - **Many unique values** = Rich detail, continuous data
  - **Few unique values** = May be classified/categorical data or heavily compressed

### Band Properties

**Data Type**
- **What it means:** How pixel values are stored
- **Common types:**
  - `Byte` (8-bit) = 0-255, most common for photos
  - `UInt16` (16-bit) = 0-65535, higher precision
  - `Float32` = Decimal numbers, scientific data
- **Why it matters:** Affects precision and file size

**Color Interpretation**
- **What it means:** What the band represents
- **Common values:**
  - `Gray` = Grayscale
  - `Red`, `Green`, `Blue` = RGB channels
  - `Undefined` = Unknown or custom
- **Why it matters:** Helps understand what each band shows

**No Data Value**
- **What it means:** Pixel value that represents missing/invalid data
- **Example:** `-9999` or `None`
- **Why it matters:** Important to exclude from calculations and visualizations

---

## 📈 Tab 5: Visualizations

### Band Histogram

**What it shows:** Distribution of pixel values in a band

**How to read:**
- **X-axis:** Pixel values (0-255 for 8-bit)
- **Y-axis:** Number of pixels with that value
- **Peaks:** Common values (e.g., peak at 0 = many black pixels)
- **Shape:**
  - **Normal distribution (bell curve)** = Natural variation
  - **Skewed left** = Mostly dark pixels
  - **Skewed right** = Mostly bright pixels
  - **Bimodal (two peaks)** = Two distinct classes (e.g., land vs water)

**What it tells you:**
- **Contrast:** Wide spread = good contrast, narrow = low contrast
- **Brightness:** Peak location = overall brightness
- **Data quality:** Unusual patterns may indicate issues

### Band Comparison Plot

**What it shows:** Overlayed histograms of multiple bands

**How to read:**
- Compare distributions between bands
- See which bands are brighter/darker
- Identify bands with similar patterns

**What it tells you:**
- **RGB images:** Red, Green, Blue should have different distributions
- **Multispectral:** Each band captures different information
- **Similar bands:** May be redundant (correlated)

### Scatter Plot

**What it shows:** Relationship between two bands

**How to read:**
- **X-axis:** Values from Band X
- **Y-axis:** Values from Band Y
- **Each point:** One pixel's values in both bands
- **Pattern:**
  - **Diagonal line** = Strong correlation (bands are similar)
  - **Cloud/random** = Low correlation (bands capture different information)
  - **Clusters** = Distinct classes (e.g., vegetation, water, soil)

**What it tells you:**
- **High correlation:** Bands contain similar information (may be redundant)
- **Low correlation:** Bands capture different features (good for analysis)
- **Clusters:** Can identify different land cover types

### Correlation Matrix

**What it shows:** How correlated each band pair is

**How to read:**
- **Color scale:** Red = high correlation, Blue = low correlation
- **Diagonal:** Always 1.0 (band correlated with itself)
- **Symmetric:** Correlation is the same both ways

**What it tells you:**
- **High correlation (> 0.9):** Bands are very similar (redundant)
- **Low correlation (< 0.3):** Bands capture different information (useful)
- **Negative correlation:** Bands are opposites (e.g., one bright where other is dark)

**Practical use:**
- Identify which bands to use for analysis
- Avoid using highly correlated bands together
- Find bands that complement each other

### Statistics Comparison Chart

**What it shows:** Bar chart comparing statistics across bands

**How to read:**
- Compare Mean, Std Dev, Min, Max across all bands
- See which bands have higher/lower values

**What it tells you:**
- **Mean comparison:** Which bands are brighter overall
- **Std Dev comparison:** Which bands have more variation/contrast
- **Range comparison:** Which bands use their full value range

---

## 🔧 Tab 6: Operations

### NDVI (Normalized Difference Vegetation Index)

**What it is:** A measure of vegetation health

**Formula:** `(NIR - Red) / (NIR + Red)`

**Value ranges:**
- **-1 to -0.1:** Water, clouds, snow
- **-0.1 to 0.1:** Bare soil, rock, urban areas
- **0.1 to 0.3:** Sparse vegetation, stressed crops
- **0.3 to 0.6:** Moderate vegetation, healthy crops
- **0.6 to 1.0:** Dense, healthy vegetation (forests, healthy crops)

**How to interpret:**
- **High NDVI (> 0.6):** Healthy, dense vegetation
- **Low NDVI (< 0.1):** Non-vegetated (water, soil, urban)
- **Medium NDVI (0.3-0.6):** Moderate vegetation
- **Changes over time:** Can indicate crop growth, stress, or seasonal changes

**Practical applications:**
- Monitor crop health
- Detect vegetation stress
- Estimate biomass
- Plan irrigation

### Band Normalization

**What it does:** Scales pixel values to a new range

**Methods:**

1. **Min-Max Normalization**
   - Scales values from [min, max] to [output_min, output_max]
   - **Example:** Scale 0-1000 to 0-255
   - **Use when:** You want to standardize ranges or prepare for display

2. **Z-Score Normalization**
   - Centers data around 0 with standard deviation of 1
   - **Formula:** `(value - mean) / std_dev`
   - **Use when:** You want to compare bands with different scales

**Why normalize:**
- **Comparison:** Make different bands comparable
- **Display:** Scale to 0-255 for visualization
- **Analysis:** Prepare data for machine learning
- **Time series:** Compare images from different dates

### Colormap Application

**What it does:** Applies a color scheme to single-band images

**Common colormaps:**
- **Viridis:** Green to yellow (good for general data)
- **Plasma:** Purple to yellow (high contrast)
- **Jet:** Blue to red (traditional, but can be misleading)
- **Hot:** Black to red to yellow (good for heat/intensity)

**Why use colormaps:**
- **Visualization:** Make grayscale data easier to interpret
- **Pattern recognition:** Colors help identify features
- **Presentation:** More appealing than grayscale

---

## 💡 Tab 7: Use Cases

This tab provides context for how to use the data you're seeing:

### Agriculture & Vegetation
- Use **NDVI** to monitor crop health
- Compare **band statistics** to identify stressed areas
- Use **correlation analysis** to find best band combinations

### Urban Planning
- Use **band comparison** to identify building materials
- **Normalization** helps compare images over time
- **Statistics** help classify land use

### Water & Hydrology
- **NIR band** typically has low values for water (water absorbs NIR)
- Use **scatter plots** to separate water from land
- **Correlation** helps identify water features

### Disaster Monitoring
- **Before/after comparison** using statistics
- **NDVI changes** indicate vegetation loss (fire, drought)
- **Band differences** show damage

---

## ⚙️ Tab 8: Advanced

### Technical Details

**Driver Information:** File format details

**Memory Information:** 
- **Size:** How much memory the image uses
- **Why it matters:** Large images may cause performance issues

**Block Size:**
- **What it means:** How data is organized internally
- **Why it matters:** Affects read/write performance

---

## Practical Interpretation Guide

### Quick Health Check

1. **Check Overview:**
   - ✅ Image has reasonable dimensions
   - ✅ Bands match expected format (3 for RGB, etc.)

2. **Check Band Statistics:**
   - ✅ Min and Max use full range (not just 50-200)
   - ✅ Mean is reasonable (not too dark/bright)
   - ✅ Std Dev shows good variation (> 20)

3. **Check Visualizations:**
   - ✅ Histogram shows good distribution (not all one value)
   - ✅ Bands are not all identical (low correlation)
   - ✅ Scatter plots show meaningful patterns

### Common Issues & Solutions

**Problem: Low contrast (min ≈ max)**
- **Solution:** Use normalization to stretch values

**Problem: All bands look the same (high correlation)**
- **Solution:** May need different band combination or different image

**Problem: Image too dark (low mean)**
- **Solution:** Check if image is underexposed or needs enhancement

**Problem: NDVI all negative or very low**
- **Solution:** Check if you selected correct Red and NIR bands

---

## Next Steps

1. **Experiment:** Upload different images and compare their statistics
2. **Practice:** Try calculating NDVI on a satellite image
3. **Analyze:** Use correlation matrix to understand band relationships
4. **Visualize:** Create histograms and scatter plots to explore your data

---

## Resources

- See `docs/learning/` for detailed tutorials
- Check `docs/learning/NEXT_STEPS.md` for advanced features
- Review `docs/learning/PILLOW_VS_GDAL.md` for library comparison

---

**Remember:** The dashboard is a tool for exploration. The more you experiment with different images and operations, the better you'll understand what the data means!
