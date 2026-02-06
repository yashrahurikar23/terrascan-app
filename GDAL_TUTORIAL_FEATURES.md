# GDAL Tutorial-Inspired Features

This document describes features added to the app inspired by "A Gentle Introduction to GDAL" and similar GDAL tutorials.

## New Operations Tab

Based on common GDAL tutorial topics, we've added an **Operations** tab with practical image processing capabilities:

### 1. Format Conversion 🔄
- Convert images between different formats
- Supported formats: GeoTIFF, JPEG, PNG, JPEG2000, HFA, ENVI
- Uses GDAL's built-in format conversion capabilities

### 2. Colormap Application 🎨
- Apply colormaps to single-band images for better visualization
- Available colormaps:
  - **Scientific**: viridis, plasma, inferno, magma
  - **Traditional**: jet, hot, cool
  - **Seasonal**: spring, summer, autumn, winter
- Automatically normalizes data and applies colormap
- Useful for visualizing single-band data (e.g., elevation, temperature)

### 3. Spectral Indices 🌱
- **NDVI (Normalized Difference Vegetation Index)**
  - Formula: `(NIR - Red) / (NIR + Red)`
  - Values range from -1 to 1
  - Visualized with Red-Yellow-Green colormap
  - Shows vegetation health and density
- Future additions: NDWI, EVI, SAVI, etc.

### 4. Band Normalization 📊
- **Min-Max Normalization**: Scale values to a specified range (e.g., 0-255)
- **Z-Score Normalization**: Standardize values using mean and standard deviation
- Useful for:
  - Preparing data for visualization
  - Comparing bands with different scales
  - Image enhancement

## Common GDAL Tutorial Topics Covered

### ✅ Basic Operations
- Opening and reading images
- Extracting metadata and information
- Band statistics

### ✅ Visualization
- Histograms with Gaussian fits
- Band comparisons
- Scatter plots
- Correlation matrices

### ✅ Image Processing
- Colormap application
- Band normalization
- Spectral index calculation

### 🔜 Future Enhancements (Common in Tutorials)
- **Reprojection**: Change coordinate reference systems
- **Resampling**: Change image resolution
- **Clipping/Subsetting**: Extract regions of interest
- **Image Warping**: Geometric transformations
- **Band Math**: Custom expressions (e.g., `(b2 - b1) / (b2 + b1)`)
- **Mosaicking**: Combine multiple images
- **Image Enhancement**: Contrast stretching, histogram equalization
- **Time Series**: Multi-temporal analysis

## How These Features Relate to GDAL Tutorials

GDAL tutorials typically cover:

1. **Getting Started**: Opening files, reading metadata ✅
2. **Basic Operations**: Reading bands, getting statistics ✅
3. **Visualization**: Creating visual representations ✅
4. **Transformations**: Reprojection, resampling 🔜
5. **Analysis**: Indices, band math ✅
6. **Advanced**: Complex workflows 🔜

Our app now covers the first 3 categories comprehensively and includes practical analysis tools from category 5.

## Usage Examples

### Applying a Colormap
1. Upload a single-band image
2. Go to **Operations** tab
3. Select a colormap (e.g., "viridis")
4. Click "Apply Colormap"
5. View the colorized result

### Calculating NDVI
1. Upload a multi-spectral image (with Red and NIR bands)
2. Go to **Operations** tab
3. Select Red and NIR band numbers
4. Click "Calculate NDVI"
5. View NDVI statistics and visualization

### Normalizing a Band
1. Upload an image
2. Go to **Operations** tab
3. Select band and normalization method
4. Set output range (for min-max)
5. Click "Normalize Band"
6. View normalized statistics and image

## References

- "A Gentle Introduction to GDAL" by Robert Simmon (Planet Stories)
- GDAL Python API Documentation
- Common GDAL workflows and best practices
