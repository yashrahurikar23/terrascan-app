"""
Image Processing Processors

This module contains different image processing backends:
- GDAL: Full-featured geospatial processing
- Rasterio: Pythonic GDAL wrapper

Use ProcessorManager to get processors - it handles availability and selection.
"""

# Import processors
try:
    from terrascan.processors.gdal_processor import GDALImageProcessor
    GDAL_AVAILABLE = True
except ImportError:
    GDAL_AVAILABLE = False
    GDALImageProcessor = None

try:
    from terrascan.processors.rasterio_processor import RasterioImageProcessor
    RASTERIO_AVAILABLE = True
except ImportError:
    RASTERIO_AVAILABLE = False
    RasterioImageProcessor = None

try:
    from terrascan.processors.pillow_processor import PillowImageProcessor
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    PillowImageProcessor = None

# Import manager
from terrascan.processors.manager import (
    ProcessorManager,
    get_processor,
    get_default_processor,
    list_available_processors
)

# Import base class
from terrascan.processors.base import BaseImageProcessor

__all__ = [
    # Base class
    "BaseImageProcessor",
    # Processors
    "GDALImageProcessor",
    "RasterioImageProcessor",
    "PillowImageProcessor",
    # Manager
    "ProcessorManager",
    "get_processor",
    "get_default_processor",
    "list_available_processors",
    # Availability flags
    "GDAL_AVAILABLE",
    "RASTERIO_AVAILABLE",
    "PILLOW_AVAILABLE",
]
