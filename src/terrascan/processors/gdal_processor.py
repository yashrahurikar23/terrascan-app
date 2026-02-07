"""
GDAL Utility Functions

This module provides reusable functions for common GDAL image processing operations.
Implements BaseImageProcessor interface for pluggable architecture.
"""

from osgeo import gdal
from osgeo import osr
import numpy as np
from typing import Dict, Optional, Tuple, Any, List
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats as scipy_stats

from terrascan.processors.base import BaseImageProcessor


class GDALImageProcessor(BaseImageProcessor):
    """
    GDAL-based image processor.
    
    Implements BaseImageProcessor interface using GDAL library.
    Maintains backward compatibility with static method calls.
    """
    
    @property
    def name(self) -> str:
        """Return processor name."""
        return "gdal"
    
    @property
    def available(self) -> bool:
        """Check if GDAL is available."""
        try:
            from osgeo import gdal
            return True
        except ImportError:
            return False
    
    def open_image(self, file_path: str) -> gdal.Dataset:
        """
        Open a raster image file using GDAL.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            GDAL Dataset object
            
        Raises:
            ValueError: If the file cannot be opened
        """
        dataset = gdal.Open(file_path)
        if dataset is None:
            raise ValueError(f"Could not open file: {file_path}")
        return dataset
    
    def open_image_from_bytes(self, file_bytes: bytes, filename: str = "uploaded_image") -> gdal.Dataset:
        """
        Open a raster image from bytes (useful for uploaded files).
        
        Args:
            file_bytes: Image file as bytes
            filename: Temporary filename for GDAL
            
        Returns:
            GDAL Dataset object
        """
        # Create a virtual file system path
        vsi_path = f"/vsimem/{filename}"
        gdal.FileFromMemBuffer(vsi_path, file_bytes)
        dataset = gdal.Open(vsi_path)
        if dataset is None:
            raise ValueError(f"Could not open image from bytes")
        return dataset
    
    def get_image_info(self, dataset: gdal.Dataset) -> Dict[str, Any]:
        """
        Extract comprehensive information from a GDAL dataset.
        
        Args:
            dataset: GDAL Dataset object
            
        Returns:
            Dictionary containing image information
        """
        info = {
            'driver': dataset.GetDriver().ShortName,
            'width': dataset.RasterXSize,
            'height': dataset.RasterYSize,
            'bands': dataset.RasterCount,
            'geotransform': None,
            'projection': None,
            'projection_name': None,
            'origin_x': None,
            'origin_y': None,
            'pixel_width': None,
            'pixel_height': None,
            'band_info': []
        }
        
        # Get geotransform information
        geotransform = dataset.GetGeoTransform()
        if geotransform and geotransform[0] != 0:
            info['geotransform'] = geotransform
            info['origin_x'] = geotransform[0]
            info['origin_y'] = geotransform[3]
            info['pixel_width'] = geotransform[1]
            info['pixel_height'] = abs(geotransform[5])
        
        # Get projection information
        projection = dataset.GetProjection()
        if projection:
            info['projection'] = projection
            srs = osr.SpatialReference()
            srs.ImportFromWkt(projection)
            info['projection_name'] = srs.GetAttrValue('PROJCS') or srs.GetAttrValue('GEOGCS')
        
        # Get dataset metadata
        metadata = dataset.GetMetadata()
        info['metadata'] = metadata if metadata else {}
        
        # Get dataset description
        info['description'] = dataset.GetDescription()
        
        # Get driver information
        driver = dataset.GetDriver()
        info['driver_long_name'] = driver.LongName
        info['driver_help'] = driver.GetMetadataItem('DMD_HELPTOPIC')
        
        # Get band information with more details
        for i in range(1, dataset.RasterCount + 1):
            band = dataset.GetRasterBand(i)
            band_info = {
                'band_number': i,
                'data_type': gdal.GetDataTypeName(band.DataType),
                'data_type_size': gdal.GetDataTypeSize(band.DataType),
                'no_data_value': band.GetNoDataValue(),
                'color_interpretation': gdal.GetColorInterpretationName(band.GetColorInterpretation()),
                'block_size': band.GetBlockSize(),
                'block_size_x': band.GetBlockSize()[0],
                'block_size_y': band.GetBlockSize()[1],
                'overview_count': band.GetOverviewCount(),
                'unit_type': band.GetUnitType(),
                'scale': band.GetScale(),
                'offset': band.GetOffset(),
                'description': band.GetDescription(),
                'category_names': band.GetCategoryNames(),
                'has_color_table': band.GetColorTable() is not None,
            }
            
            # Get color table if available
            color_table = band.GetColorTable()
            if color_table:
                band_info['color_table_count'] = color_table.GetCount()
                band_info['color_table_palette'] = color_table.GetPaletteInterpretation()
            
            # Get band metadata
            band_metadata = band.GetMetadata()
            band_info['metadata'] = band_metadata if band_metadata else {}
            
            # Get statistics if available
            try:
                stats = band.GetStatistics(True, True)
                band_info['min'] = stats[0]
                band_info['max'] = stats[1]
                band_info['mean'] = stats[2]
                band_info['std_dev'] = stats[3]
            except:
                # Calculate statistics manually if not cached
                array = band.ReadAsArray()
                band_info['min'] = float(array.min())
                band_info['max'] = float(array.max())
                band_info['mean'] = float(array.mean())
                band_info['std_dev'] = float(array.std())
            
            # Calculate additional statistics
            try:
                array = band.ReadAsArray()
                band_info['median'] = float(np.median(array))
                band_info['unique_values_count'] = len(np.unique(array))
            except:
                pass
            
            info['band_info'].append(band_info)
        
        # Get geospatial bounds
        if geotransform and geotransform[0] != 0:
            info['bounds'] = {
                'min_x': geotransform[0],
                'max_x': geotransform[0] + (info['width'] * geotransform[1]),
                'min_y': geotransform[3] + (info['height'] * geotransform[5]),
                'max_y': geotransform[3]
            }
        
        # Get projection details
        if projection:
            srs = osr.SpatialReference()
            srs.ImportFromWkt(projection)
            info['srs_wkt'] = projection
            info['epsg_code'] = srs.GetAttrValue('AUTHORITY', 1) if srs.GetAttrValue('AUTHORITY', 0) == 'EPSG' else None
            info['proj4_string'] = srs.ExportToProj4() if srs.ExportToProj4() else None
        
        return info
    
    def read_band_as_array(self, dataset: gdal.Dataset, band_number: int = 1) -> np.ndarray:
        """
        Read a specific band from the dataset as a NumPy array.
        
        Args:
            dataset: GDAL Dataset object
            band_number: Band number to read (1-indexed)
            
        Returns:
            NumPy array containing band data
        """
        band = dataset.GetRasterBand(band_number)
        return band.ReadAsArray()
    
    def read_all_bands(self, dataset: gdal.Dataset) -> np.ndarray:
        """
        Read all bands from the dataset as a NumPy array.
        
        Args:
            dataset: GDAL Dataset object
            
        Returns:
            NumPy array with shape (bands, height, width)
        """
        bands = []
        for i in range(1, dataset.RasterCount + 1):
            band = dataset.GetRasterBand(i)
            bands.append(band.ReadAsArray())
        return np.array(bands)
    
    def get_image_preview(self, dataset: gdal.Dataset, max_size: int = 1000) -> np.ndarray:
        """
        Get a preview of the image for display purposes.
        Handles RGB images and single band images.
        
        Args:
            dataset: GDAL Dataset object
            max_size: Maximum dimension for preview
            
        Returns:
            NumPy array suitable for display (RGB format)
        """
        width = dataset.RasterXSize
        height = dataset.RasterYSize
        
        # Calculate scaling factor
        scale = min(max_size / width, max_size / height, 1.0)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        if dataset.RasterCount >= 3:
            # RGB or multi-band image - use first 3 bands
            r = dataset.GetRasterBand(1).ReadAsArray(0, 0, width, height, new_width, new_height)
            g = dataset.GetRasterBand(2).ReadAsArray(0, 0, width, height, new_width, new_height)
            b = dataset.GetRasterBand(3).ReadAsArray(0, 0, width, height, new_width, new_height)
            
            # Normalize to 0-255 range
            def normalize(band):
                band_min = band.min()
                band_max = band.max()
                if band_max > band_min:
                    return ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
                return band.astype(np.uint8)
            
            r_norm = normalize(r)
            g_norm = normalize(g)
            b_norm = normalize(b)
            
            # Stack into RGB format (height, width, channels)
            return np.dstack([r_norm, g_norm, b_norm])
        else:
            # Single band - convert to grayscale RGB
            band = dataset.GetRasterBand(1).ReadAsArray(0, 0, width, height, new_width, new_height)
            band_min = band.min()
            band_max = band.max()
            if band_max > band_min:
                normalized = ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
            else:
                normalized = band.astype(np.uint8)
            # Convert grayscale to RGB
            return np.dstack([normalized, normalized, normalized])
    
    def format_info_for_display(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format image information for display in UI.
        Returns the raw info dictionary for better organization in tabs.
        """
        return info
    

# Backward compatibility: Create a singleton instance for static method calls
_GDAL_PROCESSOR_INSTANCE = GDALImageProcessor()

# Add static method wrappers for backward compatibility
# These allow old code using GDALImageProcessor.open_image() to still work
def _make_static_wrapper(method_name):
    """Create a static method wrapper for backward compatibility."""
    def wrapper(*args, **kwargs):
        return getattr(_GDAL_PROCESSOR_INSTANCE, method_name)(*args, **kwargs)
    return staticmethod(wrapper)

# Add static method aliases (backward compatibility)
# This allows existing code to continue working without changes
GDALImageProcessor.open_image = _make_static_wrapper('open_image')
GDALImageProcessor.open_image_from_bytes = _make_static_wrapper('open_image_from_bytes')
GDALImageProcessor.get_image_info = _make_static_wrapper('get_image_info')
GDALImageProcessor.read_band_as_array = _make_static_wrapper('read_band_as_array')
GDALImageProcessor.read_all_bands = _make_static_wrapper('read_all_bands')
GDALImageProcessor.get_image_preview = _make_static_wrapper('get_image_preview')
GDALImageProcessor.convert_image = _make_static_wrapper('convert_image')
GDALImageProcessor.get_band_histogram = _make_static_wrapper('get_band_histogram')
GDALImageProcessor.create_histogram_plot = _make_static_wrapper('create_histogram_plot')
GDALImageProcessor.create_band_comparison_plot = _make_static_wrapper('create_band_comparison_plot')
GDALImageProcessor.create_band_scatter_plot = _make_static_wrapper('create_band_scatter_plot')
GDALImageProcessor.create_band_correlation_matrix = _make_static_wrapper('create_band_correlation_matrix')
GDALImageProcessor.create_statistics_comparison_chart = _make_static_wrapper('create_statistics_comparison_chart')
GDALImageProcessor.apply_colormap_to_band = _make_static_wrapper('apply_colormap_to_band')
GDALImageProcessor.calculate_ndvi = _make_static_wrapper('calculate_ndvi')
GDALImageProcessor.normalize_band = _make_static_wrapper('normalize_band')
GDALImageProcessor.format_info_for_display = _make_static_wrapper('format_info_for_display')
