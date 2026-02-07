# GDAL Image Visualizations

This document describes the visualization capabilities available in the GDAL Image Processor.

## Available Visualizations

### 1. **Histogram with Gaussian Fit** 📊
- **Purpose**: Shows the distribution of pixel values in a selected band
- **Features**:
  - Histogram bars showing frequency of pixel values
  - Overlaid Gaussian (normal) distribution curve
  - Displays mean (μ) and standard deviation (σ) of the fitted curve
  - Adjustable number of bins (50-500)
- **Use Cases**:
  - Understanding data distribution
  - Detecting data quality issues
  - Identifying outliers
  - Quality control

### 2. **Band Distribution Comparison** 📈
- **Purpose**: Compare distributions of multiple bands side-by-side
- **Features**:
  - Overlaid line plots for selected bands
  - Color-coded by band
  - Fill areas under curves for better visibility
- **Use Cases**:
  - Comparing spectral bands
  - Identifying band relationships
  - Multi-spectral analysis

### 3. **Band Scatter Plot** 🔍
- **Purpose**: Analyze relationship between two bands
- **Features**:
  - Scatter plot of pixel values from two bands
  - Color-coded by Y-axis band values
  - Correlation coefficient displayed
  - Trend line showing linear relationship
- **Use Cases**:
  - Finding correlations between bands
  - Identifying linear relationships
  - Quality assessment
  - Feature extraction

### 4. **Band Correlation Matrix** 🔗
- **Purpose**: View correlation relationships between all bands
- **Features**:
  - Heatmap showing correlation coefficients
  - Color scale from -1 to +1
  - Numerical values displayed in cells
- **Use Cases**:
  - Identifying redundant bands
  - Understanding band relationships
  - Feature selection for analysis
  - Principal Component Analysis (PCA) preparation

### 5. **Statistics Comparison Chart** 📉
- **Purpose**: Compare key statistics across all bands
- **Features**:
  - Grouped bar chart
  - Shows Min, Max, Mean, and Std Dev for each band
  - Side-by-side comparison
- **Use Cases**:
  - Quick overview of band characteristics
  - Identifying bands with unusual statistics
  - Quality control

## Other GDAL-Based Comparisons You Can Create

### Spectral Indices
- **NDVI (Normalized Difference Vegetation Index)**: `(NIR - Red) / (NIR + Red)`
- **NDWI (Normalized Difference Water Index)**: `(Green - NIR) / (Green + NIR)`
- **EVI (Enhanced Vegetation Index)**: More complex formula using multiple bands

### Band Math Operations
- **Band Ratios**: Divide one band by another
- **Band Differences**: Subtract one band from another
- **Band Sums**: Add bands together
- **Normalized Differences**: Various indices

### Statistical Analysis
- **Principal Component Analysis (PCA)**: Reduce dimensionality
- **K-means Clustering**: Identify similar pixel groups
- **Texture Analysis**: GLCM (Gray-Level Co-occurrence Matrix)
- **Edge Detection**: Sobel, Canny filters

### Spatial Analysis
- **Slope and Aspect**: From DEM data
- **Hillshade**: 3D visualization
- **Viewshed Analysis**: Line of sight calculations
- **Watershed Delineation**: Hydrological analysis

### Time Series Analysis
- **Multi-temporal Comparison**: Compare same location over time
- **Change Detection**: Identify changes between dates
- **Trend Analysis**: Long-term patterns

## How to Use

1. **Upload and Process Image**: Upload your image file and click "Process Image"
2. **Navigate to Visualizations Tab**: Click on the "📈 Visualizations" tab
3. **Select Visualization Type**: Choose from the available options
4. **Configure Parameters**: Adjust settings (band selection, bins, etc.)
5. **Generate**: Click the generate button to create the visualization
6. **Interact**: Use Plotly's interactive features (zoom, pan, hover)

## Technical Details

- **Sampling**: Large images are automatically sampled for performance (default: 10,000-100,000 pixels)
- **NoData Handling**: NoData values are automatically excluded from analysis
- **Memory Efficient**: Visualizations use efficient NumPy operations
- **Interactive**: All charts are interactive Plotly figures

## Performance Tips

- For very large images, reduce sample size
- Use fewer bins for faster histogram generation
- Correlation matrix calculation may take time for many bands
- Scatter plots work best with sampled data

## Future Enhancements

Potential additions:
- NDVI/NDWI calculators
- PCA visualization
- Time series plots
- 3D surface plots
- Classification visualizations
- Custom band math expressions
