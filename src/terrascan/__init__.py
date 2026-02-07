"""
Terrascan - Geospatial Image Processing Application

A professional-grade application for processing and analyzing geospatial imagery
using GDAL, Rasterio, Pillow and other geospatial libraries.
"""

__version__ = "0.1.0"
__author__ = "Terrascan Team"

# Import processors (with graceful fallback)
# Use relative imports to avoid circular import issues
try:
    from .processors import GDALImageProcessor, GDAL_AVAILABLE
except ImportError:
    GDALImageProcessor = None
    GDAL_AVAILABLE = False

try:
    from .processors import RasterioImageProcessor, RASTERIO_AVAILABLE
except ImportError:
    RasterioImageProcessor = None
    RASTERIO_AVAILABLE = False

try:
    from .processors import PillowImageProcessor, PILLOW_AVAILABLE
except ImportError:
    PillowImageProcessor = None
    PILLOW_AVAILABLE = False

__all__ = [
    "GDALImageProcessor",
    "RasterioImageProcessor",
    "PillowImageProcessor",
    "GDAL_AVAILABLE",
    "RASTERIO_AVAILABLE",
    "PILLOW_AVAILABLE",
]
