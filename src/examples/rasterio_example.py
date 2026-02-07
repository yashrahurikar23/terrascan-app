"""
Rasterio Example - Lighter Alternative to GDAL

This file demonstrates how to use Rasterio, a more Pythonic wrapper around GDAL.
Rasterio is easier to use and has a cleaner API while still being powerful.

Installation:
    pip install rasterio

Note: Rasterio still requires GDAL system libraries, but the Python API is much simpler.
"""

import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt

def open_image_rasterio(file_path: str):
    """
    Open an image using Rasterio (simpler than GDAL).
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Rasterio dataset
    """
    # Much simpler than GDAL!
    dataset = rasterio.open(file_path)
    return dataset


def get_image_info_rasterio(dataset):
    """
    Extract image information using Rasterio.
    
    Compare this to the GDAL version - much cleaner!
    """
    info = {
        'width': dataset.width,
        'height': dataset.height,
        'bands': dataset.count,
        'driver': dataset.driver,
        'crs': dataset.crs,  # Coordinate Reference System
        'bounds': dataset.bounds,  # Spatial bounds
        'transform': dataset.transform,  # Geotransform
        'dtype': dataset.dtypes[0],  # Data type
        'nodata': dataset.nodata,  # No data value
    }
    
    # Get metadata
    info['metadata'] = dataset.meta
    info['tags'] = dataset.tags()
    
    return info


def read_band_rasterio(dataset, band_number: int = 1):
    """
    Read a band using Rasterio.
    
    Much simpler than GDAL's approach!
    """
    # Rasterio uses 1-based indexing like GDAL
    band_data = dataset.read(band_number)
    return band_data


def read_all_bands_rasterio(dataset):
    """
    Read all bands at once.
    
    Returns array with shape (bands, height, width)
    """
    # Read all bands in one call
    all_bands = dataset.read()
    return all_bands


def calculate_ndvi_rasterio(dataset, red_band: int = 1, nir_band: int = 2):
    """
    Calculate NDVI using Rasterio.
    
    Compare this to the GDAL version - cleaner!
    """
    # Read bands (returns numpy arrays directly)
    red = dataset.read(red_band).astype(np.float32)
    nir = dataset.read(nir_band).astype(np.float32)
    
    # Calculate NDVI
    denominator = red + nir
    ndvi = np.where(denominator != 0, (nir - red) / denominator, 0)
    
    return ndvi


def get_preview_rasterio(dataset, max_size: int = 1000):
    """
    Get a preview of the image for display.
    """
    width = dataset.width
    height = dataset.height
    
    # Calculate scaling
    scale = min(max_size / width, max_size / height, 1.0)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Read and resize
    if dataset.count >= 3:
        # RGB image
        r = dataset.read(1, out_shape=(new_height, new_width))
        g = dataset.read(2, out_shape=(new_height, new_width))
        b = dataset.read(3, out_shape=(new_height, new_width))
        
        # Normalize
        def normalize(band):
            band_min = band.min()
            band_max = band.max()
            if band_max > band_min:
                return ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
            return band.astype(np.uint8)
        
        r_norm = normalize(r)
        g_norm = normalize(g)
        b_norm = normalize(b)
        
        # Stack into RGB
        return np.dstack([r_norm, g_norm, b_norm])
    else:
        # Single band
        band = dataset.read(1, out_shape=(new_height, new_width))
        band_min = band.min()
        band_max = band.max()
        if band_max > band_min:
            normalized = ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
        else:
            normalized = band.astype(np.uint8)
        return np.dstack([normalized, normalized, normalized])


def write_image_rasterio(data, output_path: str, profile=None):
    """
    Write an image using Rasterio.
    
    Much simpler than GDAL's approach!
    """
    if profile is None:
        # Create default profile
        profile = {
            'driver': 'GTiff',
            'dtype': data.dtype,
            'count': 1 if len(data.shape) == 2 else data.shape[0],
            'width': data.shape[-1],
            'height': data.shape[-2],
        }
    
    with rasterio.open(output_path, 'w', **profile) as dst:
        if len(data.shape) == 2:
            dst.write(data, 1)
        else:
            dst.write(data)


def compare_gdal_vs_rasterio():
    """
    Comparison of GDAL vs Rasterio for common operations.
    """
    print("=" * 60)
    print("GDAL vs Rasterio Comparison")
    print("=" * 60)
    
    print("\n1. Opening an Image:")
    print("   GDAL:")
    print("     from osgeo import gdal")
    print("     dataset = gdal.Open('image.tif')")
    print("     if dataset is None:")
    print("         raise ValueError('Could not open file')")
    print("")
    print("   Rasterio:")
    print("     import rasterio")
    print("     dataset = rasterio.open('image.tif')")
    print("     # Automatically raises exception on error")
    
    print("\n2. Getting Image Dimensions:")
    print("   GDAL:")
    print("     width = dataset.RasterXSize")
    print("     height = dataset.RasterYSize")
    print("     bands = dataset.RasterCount")
    print("")
    print("   Rasterio:")
    print("     width = dataset.width")
    print("     height = dataset.height")
    print("     bands = dataset.count")
    
    print("\n3. Reading a Band:")
    print("   GDAL:")
    print("     band = dataset.GetRasterBand(1)")
    print("     array = band.ReadAsArray()")
    print("")
    print("   Rasterio:")
    print("     array = dataset.read(1)")
    
    print("\n4. Getting Coordinate System:")
    print("   GDAL:")
    print("     projection = dataset.GetProjection()")
    print("     # Returns WKT string, need to parse")
    print("")
    print("   Rasterio:")
    print("     crs = dataset.crs")
    print("     # Returns CRS object, easy to use")
    
    print("\n5. Getting Bounds:")
    print("   GDAL:")
    print("     geotransform = dataset.GetGeoTransform()")
    print("     # Need to calculate bounds manually")
    print("")
    print("   Rasterio:")
    print("     bounds = dataset.bounds")
    print("     # Returns BoundingBox object directly")
    
    print("\n6. Context Manager (Auto-close):")
    print("   GDAL:")
    print("     dataset = gdal.Open('image.tif')")
    print("     # Must manually close: dataset = None")
    print("")
    print("   Rasterio:")
    print("     with rasterio.open('image.tif') as dataset:")
    print("         # Automatically closes when done")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("  - Rasterio has a more Pythonic API")
    print("  - Rasterio has better error messages")
    print("  - Rasterio uses context managers (with statement)")
    print("  - Rasterio is easier to learn")
    print("  - Both use GDAL under the hood")
    print("  - GDAL has more advanced features")
    print("=" * 60)


if __name__ == "__main__":
    # Example usage
    print("Rasterio Example - Lighter Alternative to GDAL")
    print("\nThis demonstrates how Rasterio provides a simpler API")
    print("while still using GDAL under the hood.\n")
    
    # Show comparison
    compare_gdal_vs_rasterio()
    
    print("\n" + "=" * 60)
    print("To use Rasterio in your app:")
    print("1. Install: pip install rasterio")
    print("2. Import: import rasterio")
    print("3. Use instead of GDAL for simpler operations")
    print("4. Keep GDAL for advanced features")
    print("=" * 60)
