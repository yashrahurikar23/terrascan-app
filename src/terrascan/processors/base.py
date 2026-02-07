"""
Base Image Processor Interface

This module defines the abstract base class that all image processors must implement.
This allows the application to switch between different image processing libraries
(GDAL, Rasterio, etc.) without changing the application code.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import numpy as np


class BaseImageProcessor(ABC):
    """
    Abstract base class for image processors.
    
    All image processors (GDAL, Rasterio, etc.) must implement this interface
    to ensure consistent behavior across different libraries.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the processor (e.g., 'gdal', 'rasterio')."""
        pass
    
    @property
    @abstractmethod
    def available(self) -> bool:
        """Check if this processor is available (library installed)."""
        pass
    
    @abstractmethod
    def open_image(self, file_path: str) -> Any:
        """
        Open a raster image file.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dataset object (type depends on implementation)
            
        Raises:
            ValueError: If the file cannot be opened
        """
        pass
    
    @abstractmethod
    def open_image_from_bytes(self, file_bytes: bytes, filename: str = "uploaded_image") -> Any:
        """
        Open a raster image from bytes.
        
        Args:
            file_bytes: Image file as bytes
            filename: Temporary filename for the processor
            
        Returns:
            Dataset object
        """
        pass
    
    @abstractmethod
    def get_image_info(self, dataset: Any) -> Dict[str, Any]:
        """
        Extract comprehensive information from a dataset.
        
        Args:
            dataset: Dataset object from open_image()
            
        Returns:
            Dictionary containing image information with keys:
            - width, height, bands
            - driver, geotransform, projection
            - band_info (list of band information)
            - bounds, metadata, etc.
        """
        pass
    
    @abstractmethod
    def read_band_as_array(self, dataset: Any, band_number: int = 1) -> np.ndarray:
        """
        Read a specific band from the dataset as a NumPy array.
        
        Args:
            dataset: Dataset object
            band_number: Band number to read (1-indexed)
            
        Returns:
            NumPy array containing band data
        """
        pass
    
    @abstractmethod
    def read_all_bands(self, dataset: Any) -> np.ndarray:
        """
        Read all bands from the dataset.
        
        Args:
            dataset: Dataset object
            
        Returns:
            NumPy array with shape (bands, height, width)
        """
        pass
    
    @abstractmethod
    def get_image_preview(self, dataset: Any, max_size: int = 1000) -> np.ndarray:
        """
        Get a preview of the image for display purposes.
        
        Args:
            dataset: Dataset object
            max_size: Maximum dimension for preview
            
        Returns:
            NumPy array suitable for display (RGB format, shape: height, width, 3)
        """
        pass
    
    @abstractmethod
    def get_band_histogram(self, dataset: Any, band_number: int = 1, 
                          bins: int = 256, sample_size: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get histogram data for a band.
        
        Args:
            dataset: Dataset object
            band_number: Band number (1-indexed)
            bins: Number of bins for histogram
            sample_size: If provided, sample this many pixels
            
        Returns:
            Tuple of (histogram values, bin edges)
        """
        pass
    
    @abstractmethod
    def create_histogram_plot(self, dataset: Any, band_number: int = 1, 
                              bins: int = 256, sample_size: Optional[int] = 100000) -> Any:
        """
        Create a histogram plot for a band.
        
        Args:
            dataset: Dataset object
            band_number: Band number (1-indexed)
            bins: Number of bins
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        pass
    
    @abstractmethod
    def create_band_comparison_plot(self, dataset: Any, band_numbers: List[int] = None, 
                                    sample_size: int = 10000) -> Any:
        """
        Create a comparison plot showing distributions of multiple bands.
        
        Args:
            dataset: Dataset object
            band_numbers: List of band numbers to compare
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        pass
    
    @abstractmethod
    def create_band_scatter_plot(self, dataset: Any, band_x: int = 1, band_y: int = 2, 
                                 sample_size: int = 10000) -> Any:
        """
        Create a scatter plot comparing two bands.
        
        Args:
            dataset: Dataset object
            band_x: X-axis band number
            band_y: Y-axis band number
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        pass
    
    @abstractmethod
    def create_band_correlation_matrix(self, dataset: Any, sample_size: int = 10000) -> Any:
        """
        Create a correlation matrix heatmap for all bands.
        
        Args:
            dataset: Dataset object
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        pass
    
    @abstractmethod
    def create_statistics_comparison_chart(self, info: Dict[str, Any]) -> Any:
        """
        Create a bar chart comparing statistics across bands.
        
        Args:
            info: Image information dictionary from get_image_info()
            
        Returns:
            Plotly figure object
        """
        pass
    
    @abstractmethod
    def apply_colormap_to_band(self, dataset: Any, band_number: int = 1, 
                               colormap_name: str = 'viridis') -> np.ndarray:
        """
        Apply a colormap to a single-band image.
        
        Args:
            dataset: Dataset object
            band_number: Band number to apply colormap to
            colormap_name: Name of colormap
            
        Returns:
            RGB array with colormap applied
        """
        pass
    
    @abstractmethod
    def calculate_ndvi(self, dataset: Any, red_band: int = 1, nir_band: int = 2) -> np.ndarray:
        """
        Calculate NDVI (Normalized Difference Vegetation Index).
        
        Args:
            dataset: Dataset object
            red_band: Red band number (1-indexed)
            nir_band: Near-infrared band number (1-indexed)
            
        Returns:
            NDVI array (values from -1 to 1)
        """
        pass
    
    @abstractmethod
    def normalize_band(self, dataset: Any, band_number: int = 1, 
                      method: str = 'minmax', output_min: float = 0, 
                      output_max: float = 255) -> np.ndarray:
        """
        Normalize a band using different methods.
        
        Args:
            dataset: Dataset object
            band_number: Band number to normalize
            method: 'minmax' or 'zscore'
            output_min: Minimum output value (for minmax)
            output_max: Maximum output value (for minmax)
            
        Returns:
            Normalized array
        """
        pass
    
    @abstractmethod
    def convert_image(self, input_file: str, output_file: str, output_format: str = 'GTiff') -> bool:
        """
        Convert an image from one format to another.
        
        Args:
            input_file: Path to input image
            output_file: Path to output image
            output_format: Output format driver name
            
        Returns:
            True if conversion successful, False otherwise
        """
        pass
