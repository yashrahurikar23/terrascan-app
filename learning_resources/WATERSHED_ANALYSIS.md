# Watershed Analysis Guide

## What is Watershed Analysis?

**Watershed analysis** (also called **drainage basin analysis**) is a geospatial operation that identifies and delineates watersheds (drainage basins) from elevation data.

### Key Concepts

**Watershed (Drainage Basin):**
- An area of land where all water flows to a common outlet (river, lake, ocean)
- Defined by topographic boundaries (ridges, hills)
- All precipitation within a watershed eventually drains to the same point

**Watershed Analysis Process:**
1. Start with a **Digital Elevation Model (DEM)** - elevation data
2. Calculate **flow direction** - which way water flows from each pixel
3. Calculate **flow accumulation** - how much water accumulates at each pixel
4. Identify **streams** - where flow accumulation exceeds a threshold
5. Delineate **watershed boundaries** - areas draining to specific outlets

---

## Why is Watershed Analysis Important?

### Applications

1. **Hydrology & Water Management**
   - Understand water flow patterns
   - Plan flood management
   - Design drainage systems
   - Water resource planning

2. **Environmental Science**
   - Study ecosystem boundaries
   - Analyze pollution pathways
   - Understand nutrient flow
   - Habitat analysis

3. **Urban Planning**
   - Design stormwater systems
   - Plan infrastructure
   - Flood risk assessment
   - Land use planning

4. **Agriculture**
   - Irrigation planning
   - Soil erosion analysis
   - Crop management
   - Drainage design

---

## How Watershed Analysis Works

### Step 1: Digital Elevation Model (DEM)

**Input:** A raster image where each pixel represents elevation
- Higher values = higher elevation
- Lower values = lower elevation (valleys, rivers)

**Example:**
```
DEM Image:
[1000, 1050, 1100, 1080]
[980,  1020, 1040, 1000]
[950,   980,  990,  960]
[920,   940,  950,  930]
```

### Step 2: Flow Direction

**Calculate:** Which direction water flows from each pixel

**8-Direction Flow Model (D8):**
- Each pixel flows to one of 8 neighbors
- Direction is toward the steepest downhill neighbor
- Directions: N, NE, E, SE, S, SW, W, NW

**Example:**
```
Elevation:    Flow Direction:
[1000, 1050]  [→, ↓]
[980,  1020]  [→, ↓]
```

### Step 3: Flow Accumulation

**Calculate:** How many upstream pixels contribute to each pixel

**Process:**
- Start from highest elevations
- Count pixels that flow into each cell
- Higher accumulation = more upstream area

**Result:**
- Low values = ridges, hilltops
- High values = streams, rivers
- Very high values = major rivers

### Step 4: Stream Identification

**Identify streams:**
- Where flow accumulation exceeds a threshold
- Example: All pixels with accumulation > 1000 cells

**Result:** Network of streams and rivers

### Step 5: Watershed Delineation

**Delineate watersheds:**
- For each stream segment or outlet point
- Trace upstream to find all contributing pixels
- Boundary = pixels that flow to different outlets

**Result:** Watershed boundaries as polygons

---

## Watershed Analysis in GDAL

### GDAL Tools for Watershed Analysis

GDAL doesn't have built-in watershed analysis, but you can use:

1. **GDALDEM** (command-line tool)
   - `gdaldem hillshade` - Create hillshade
   - `gdaldem slope` - Calculate slope
   - `gdaldem aspect` - Calculate aspect
   - `gdaldem TRI` - Terrain Ruggedness Index

2. **Python Libraries**
   - **WhiteboxTools** - Has watershed analysis functions
   - **RichDEM** - Advanced DEM processing
   - **GRASS GIS** - Full GIS capabilities via Python
   - **PySheds** - Python watershed analysis library

3. **QGIS**
   - SAGA GIS tools (via QGIS Processing)
   - GRASS tools
   - Raster Calculator for custom operations

---

## Example: Basic Watershed Analysis Workflow

### Using GDAL + Python

```python
from osgeo import gdal
import numpy as np

# 1. Open DEM
dem = gdal.Open('elevation.tif')
dem_band = dem.GetRasterBand(1)
elevation = dem_band.ReadAsArray()

# 2. Calculate flow direction (simplified)
# (In practice, use specialized tools like WhiteboxTools)
def calculate_flow_direction(elevation):
    """
    Simplified flow direction calculation.
    In practice, use established algorithms (D8, D-infinity, etc.)
    """
    rows, cols = elevation.shape
    flow_dir = np.zeros_like(elevation)
    
    # For each pixel, find steepest downhill neighbor
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            center = elevation[i, j]
            neighbors = [
                elevation[i-1, j-1], elevation[i-1, j], elevation[i-1, j+1],
                elevation[i, j-1],                     elevation[i, j+1],
                elevation[i+1, j-1], elevation[i+1, j], elevation[i+1, j+1]
            ]
            # Find direction of steepest descent
            # (Simplified - real algorithm is more complex)
            min_neighbor = min(neighbors)
            if min_neighbor < center:
                flow_dir[i, j] = 1  # Simplified: 1 = flows, 0 = doesn't
    
    return flow_dir

# 3. Calculate flow accumulation
def calculate_flow_accumulation(flow_dir):
    """
    Count upstream pixels contributing to each cell.
    Simplified version - real algorithm traces flow paths.
    """
    # This is a simplified example
    # Real flow accumulation requires tracing flow paths
    accumulation = np.zeros_like(flow_dir)
    # ... complex algorithm to trace upstream paths ...
    return accumulation

# 4. Identify streams (threshold)
def identify_streams(accumulation, threshold=1000):
    """
    Identify pixels where flow accumulation exceeds threshold.
    """
    streams = accumulation > threshold
    return streams.astype(np.uint8) * 255

# 5. Delineate watersheds
def delineate_watershed(flow_dir, outlet_point):
    """
    Trace upstream from outlet to find all contributing pixels.
    """
    watershed = np.zeros_like(flow_dir)
    # ... trace upstream from outlet ...
    return watershed
```

### Using WhiteboxTools (Recommended)

```python
from whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()

# 1. Calculate flow direction
wbt.d8_pointer(
    dem='elevation.tif',
    output='flow_direction.tif'
)

# 2. Calculate flow accumulation
wbt.d8_flow_accumulation(
    d8_pntr='flow_direction.tif',
    output='flow_accumulation.tif'
)

# 3. Extract streams
wbt.extract_streams(
    flow_accum='flow_accumulation.tif',
    output='streams.tif',
    threshold=1000
)

# 4. Delineate watersheds
wbt.watershed(
    d8_pntr='flow_direction.tif',
    pour_pts='outlets.shp',
    output='watersheds.tif'
)
```

---

## Adding Watershed Analysis to Your App

### Potential Features

1. **DEM Upload & Visualization**
   - Upload DEM (elevation) images
   - Display as hillshade or colored elevation map
   - Show elevation statistics

2. **Flow Direction Calculation**
   - Calculate flow direction from DEM
   - Visualize flow directions
   - Export flow direction raster

3. **Flow Accumulation**
   - Calculate flow accumulation
   - Visualize accumulation (darker = more accumulation)
   - Identify potential stream locations

4. **Stream Network Extraction**
   - Extract streams based on threshold
   - Visualize stream network
   - Calculate stream statistics

5. **Watershed Delineation**
   - Delineate watersheds from outlet points
   - Visualize watershed boundaries
   - Calculate watershed statistics (area, etc.)

### Implementation Considerations

**Libraries Needed:**
- **WhiteboxTools** - Best option for watershed analysis
- **RichDEM** - Advanced DEM processing
- **PySheds** - Python watershed library

**Challenges:**
- Watershed analysis is computationally intensive
- Large DEMs can take time to process
- May need to process subsets for web app
- Requires specialized algorithms

**Recommendation:**
- Start with DEM visualization (hillshade, slope)
- Add flow direction/accumulation later
- Use WhiteboxTools for complex operations
- Consider processing on server-side only

---

## Learning Path

### Phase 1: Understand DEMs
1. What is a DEM?
2. How to read DEM data
3. Visualizing elevation data
4. DEM statistics

### Phase 2: Basic Terrain Analysis
1. Calculate slope from DEM
2. Calculate aspect (direction)
3. Create hillshade visualization
4. Understand terrain features

### Phase 3: Flow Analysis
1. Understand flow direction
2. Calculate flow accumulation
3. Identify drainage patterns
4. Extract stream networks

### Phase 4: Watershed Delineation
1. Understand watershed concepts
2. Delineate watersheds from outlets
3. Calculate watershed properties
4. Visualize watershed boundaries

---

## Resources

### Tools & Libraries
- **WhiteboxTools**: https://www.whiteboxgeo.com/
- **RichDEM**: https://github.com/r-barnes/richdem
- **PySheds**: https://github.com/mdbartos/pysheds
- **GRASS GIS**: https://grass.osgeo.org/

### Tutorials
- [Watershed Analysis Tutorial (QGIS)](https://docs.qgis.org/)
- [WhiteboxTools Tutorial](https://www.whiteboxgeo.com/manual/wbt_book/)
- [PySheds Documentation](https://pysheds.readthedocs.io/)

### Data Sources
- **USGS DEM Data**: https://www.usgs.gov/
- **OpenDEM**: https://www.opendem.info/
- **SRTM Data**: NASA Shuttle Radar Topography Mission

---

## Summary

**Watershed analysis** is a powerful geospatial technique that:
- Identifies drainage basins from elevation data
- Calculates water flow patterns
- Delineates watershed boundaries
- Has many applications in hydrology, planning, and environmental science

**For your app:**
- Can be added as an advanced feature
- Requires specialized libraries (WhiteboxTools recommended)
- Start with DEM visualization, add analysis features gradually
- Great learning opportunity for advanced geospatial processing!

**Next Steps:**
1. Learn about DEMs and terrain analysis
2. Experiment with WhiteboxTools
3. Add DEM visualization to your app
4. Gradually add watershed analysis features

---

## Related to Your Learning Plan

Watershed analysis fits into:
- **Phase 4: Image Operations** - DEM processing
- **Phase 7: Advanced Topics** - Complex geospatial analysis

It's a great way to apply what you've learned about:
- Reading raster data (DEMs)
- Image operations (calculations on elevation data)
- Geospatial concepts (coordinate systems, projections)
- Visualization (hillshade, flow maps)

**This could be a great final project or advanced feature!** 🚀

