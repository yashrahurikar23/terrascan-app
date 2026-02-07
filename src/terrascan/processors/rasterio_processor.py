"""
Rasterio Image Processor

This module provides a Rasterio-based implementation of the BaseImageProcessor interface.
Rasterio is a more Pythonic wrapper around GDAL with a cleaner API.
"""

try:
    import rasterio
    from rasterio.transform import from_bounds
    from rasterio.crs import CRS
    RASTERIO_AVAILABLE = True
except ImportError:
    RASTERIO_AVAILABLE = False
    rasterio = None

import numpy as np
from typing import Dict, Optional, Tuple, Any, List
import tempfile
import os
import matplotlib
matplotlib.use('Agg')
import plotly.graph_objects as go
import plotly.express as px

from terrascan.processors.base import BaseImageProcessor


class RasterioImageProcessor(BaseImageProcessor):
    """
    Rasterio-based image processor.
    
    Implements BaseImageProcessor interface using Rasterio library.
    Provides a more Pythonic API than GDAL while maintaining the same functionality.
    """
    
    @property
    def name(self) -> str:
        """Return processor name."""
        return "rasterio"
    
    @property
    def available(self) -> bool:
        """Check if Rasterio is available."""
        return RASTERIO_AVAILABLE
    
    def open_image(self, file_path: str) -> Any:
        """
        Open a raster image file using Rasterio.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Rasterio DatasetReader object
            
        Raises:
            ValueError: If the file cannot be opened
        """
        if not self.available:
            raise ImportError("Rasterio is not available")
        
        try:
            dataset = rasterio.open(file_path)
            return dataset
        except Exception as e:
            raise ValueError(f"Could not open file: {file_path} - {str(e)}")
    
    def open_image_from_bytes(self, file_bytes: bytes, filename: str = "uploaded_image") -> Any:
        """
        Open a raster image from bytes.
        
        Args:
            file_bytes: Image file as bytes
            filename: Temporary filename for Rasterio
            
        Returns:
            Rasterio DatasetReader object
        """
        if not self.available:
            raise ImportError("Rasterio is not available")
        
        # Create temporary file (Rasterio works better with actual files)
        file_extension = os.path.splitext(filename)[1] or '.tif'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name
        
        try:
            dataset = rasterio.open(tmp_path)
            # Store temp path for cleanup
            dataset._temp_path = tmp_path
            return dataset
        except Exception as e:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise ValueError(f"Could not open image from bytes: {str(e)}")
    
    def get_image_info(self, dataset: Any) -> Dict[str, Any]:
        """
        Extract comprehensive information from a Rasterio dataset.
        
        Args:
            dataset: Rasterio DatasetReader object
            
        Returns:
            Dictionary containing image information
        """
        info = {
            'driver': dataset.driver,
            'width': dataset.width,
            'height': dataset.height,
            'bands': dataset.count,
            'geotransform': None,
            'projection': None,
            'projection_name': None,
            'origin_x': None,
            'origin_y': None,
            'pixel_width': None,
            'pixel_height': None,
            'band_info': []
        }
        
        # Get transform (geotransform equivalent)
        transform = dataset.transform
        if transform:
            info['geotransform'] = (
                transform.c,  # origin_x
                transform.a,  # pixel_width
                transform.b,  # rotation
                transform.f,  # origin_y
                transform.d,  # rotation
                transform.e   # pixel_height (negative)
            )
            info['origin_x'] = transform.c
            info['origin_y'] = transform.f
            info['pixel_width'] = transform.a
            info['pixel_height'] = abs(transform.e)
        
        # Get CRS (projection)
        crs = dataset.crs
        if crs:
            info['projection'] = crs.to_wkt() if hasattr(crs, 'to_wkt') else str(crs)
            info['projection_name'] = crs.name if hasattr(crs, 'name') else None
            info['epsg_code'] = crs.to_epsg() if hasattr(crs, 'to_epsg') and crs.to_epsg() else None
        
        # Get bounds
        bounds = dataset.bounds
        if bounds:
            info['bounds'] = {
                'min_x': bounds.left,
                'max_x': bounds.right,
                'min_y': bounds.bottom,
                'max_y': bounds.top
            }
        
        # Get metadata
        info['metadata'] = dataset.meta.copy() if hasattr(dataset, 'meta') else {}
        info['tags'] = dataset.tags() if hasattr(dataset, 'tags') else {}
        info['description'] = dataset.name
        
        # Get driver information
        info['driver_long_name'] = dataset.driver
        
        # Get band information
        for i in range(1, dataset.count + 1):
            band_info = {
                'band_number': i,
                'data_type': str(dataset.dtypes[i-1]),
                'data_type_size': dataset.dtypes[i-1].itemsize * 8,
                'no_data_value': dataset.nodata,
                'color_interpretation': 'Unknown',  # Rasterio doesn't expose this easily
                'block_size_x': dataset.block_shapes[i-1][1] if hasattr(dataset, 'block_shapes') else 256,
                'block_size_y': dataset.block_shapes[i-1][0] if hasattr(dataset, 'block_shapes') else 256,
                'overview_count': 0,  # Rasterio handles overviews differently
                'unit_type': '',
                'scale': 1.0,
                'offset': 0.0,
                'description': '',
                'has_color_table': False,
            }
            
            # Read band to get statistics
            try:
                band_data = dataset.read(i)
                band_info['min'] = float(np.nanmin(band_data))
                band_info['max'] = float(np.nanmax(band_data))
                band_info['mean'] = float(np.nanmean(band_data))
                band_info['std_dev'] = float(np.nanstd(band_data))
                band_info['median'] = float(np.nanmedian(band_data))
                band_info['unique_values_count'] = len(np.unique(band_data[~np.isnan(band_data)]))
            except Exception:
                band_info['min'] = 0.0
                band_info['max'] = 255.0
                band_info['mean'] = 128.0
                band_info['std_dev'] = 64.0
            
            info['band_info'].append(band_info)
        
        return info
    
    def read_band_as_array(self, dataset: Any, band_number: int = 1) -> np.ndarray:
        """
        Read a specific band from the dataset as a NumPy array.
        
        Args:
            dataset: Rasterio DatasetReader object
            band_number: Band number to read (1-indexed)
            
        Returns:
            NumPy array containing band data
        """
        return dataset.read(band_number)
    
    def read_all_bands(self, dataset: Any) -> np.ndarray:
        """
        Read all bands from the dataset.
        
        Args:
            dataset: Rasterio DatasetReader object
            
        Returns:
            NumPy array with shape (bands, height, width)
        """
        return dataset.read()
    
    def get_image_preview(self, dataset: Any, max_size: int = 1000) -> np.ndarray:
        """
        Get a preview of the image for display purposes.
        
        Args:
            dataset: Rasterio DatasetReader object
            max_size: Maximum dimension for preview
            
        Returns:
            NumPy array suitable for display (RGB format)
        """
        width = dataset.width
        height = dataset.height
        
        # Calculate scaling factor
        scale = min(max_size / width, max_size / height, 1.0)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        if dataset.count >= 3:
            # RGB image - use first 3 bands
            r = dataset.read(1, out_shape=(new_height, new_width))
            g = dataset.read(2, out_shape=(new_height, new_width))
            b = dataset.read(3, out_shape=(new_height, new_width))
            
            # Normalize to 0-255 range
            def normalize(band):
                band_min = np.nanmin(band)
                band_max = np.nanmax(band)
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
            band = dataset.read(1, out_shape=(new_height, new_width))
            band_min = np.nanmin(band)
            band_max = np.nanmax(band)
            if band_max > band_min:
                normalized = ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
            else:
                normalized = band.astype(np.uint8)
            # Convert grayscale to RGB
            return np.dstack([normalized, normalized, normalized])
    
    def get_band_histogram(self, dataset: Any, band_number: int = 1, 
                          bins: int = 256, sample_size: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get histogram data for a band.
        
        Args:
            dataset: Rasterio DatasetReader object
            band_number: Band number (1-indexed)
            bins: Number of bins for histogram
            sample_size: If provided, sample this many pixels
            
        Returns:
            Tuple of (histogram values, bin edges)
        """
        array = dataset.read(band_number).flatten()
        
        # Sample if requested
        if sample_size and array.size > sample_size:
            array = np.random.choice(array, sample_size, replace=False)
        
        # Remove NaN and NoData values
        if dataset.nodata is not None:
            array = array[array != dataset.nodata]
        array = array[~np.isnan(array)]
        
        hist, bin_edges = np.histogram(array, bins=bins)
        return hist, bin_edges
    
    def create_histogram_plot(self, dataset: Any, band_number: int = 1, 
                              bins: int = 256, sample_size: Optional[int] = 100000) -> Any:
        """Create a histogram plot for a band."""
        hist, bin_edges = self.get_band_histogram(dataset, band_number, bins, sample_size)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Fit Gaussian curve
        array = dataset.read(band_number).flatten()
        if dataset.nodata is not None:
            array = array[array != dataset.nodata]
        array = array[~np.isnan(array)]
        
        if sample_size and array.size > sample_size:
            array = np.random.choice(array, sample_size, replace=False)
        
        mean = np.mean(array)
        std = np.std(array)
        
        # Create Gaussian curve
        x_gaussian = np.linspace(bin_edges[0], bin_edges[-1], 1000)
        gaussian = np.exp(-0.5 * ((x_gaussian - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
        gaussian = gaussian * len(array) * (bin_edges[1] - bin_edges[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=bin_centers,
            y=hist,
            name='Histogram',
            marker_color='rgba(55, 128, 191, 0.7)',
            opacity=0.7
        ))
        fig.add_trace(go.Scatter(
            x=x_gaussian,
            y=gaussian,
            mode='lines',
            name=f'Gaussian Fit (μ={mean:.2f}, σ={std:.2f})',
            line=dict(color='red', width=2)
        ))
        fig.update_layout(
            title=f'Band {band_number} Distribution with Gaussian Fit',
            xaxis_title='Pixel Value',
            yaxis_title='Frequency',
            hovermode='x unified',
            template='plotly_white'
        )
        return fig
    
    def create_band_comparison_plot(self, dataset: Any, band_numbers: List[int] = None, 
                                    sample_size: int = 10000) -> Any:
        """Create a comparison plot showing distributions of multiple bands."""
        if band_numbers is None:
            band_numbers = list(range(1, dataset.count + 1))
        
        fig = go.Figure()
        colors = px.colors.qualitative.Set3
        
        for idx, band_num in enumerate(band_numbers):
            if band_num > dataset.count:
                continue
            
            array = dataset.read(band_num).flatten()
            if array.size > sample_size:
                array = np.random.choice(array, sample_size, replace=False)
            
            if dataset.nodata is not None:
                array = array[array != dataset.nodata]
            array = array[~np.isnan(array)]
            
            hist, bin_edges = np.histogram(array, bins=100)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            
            fig.add_trace(go.Scatter(
                x=bin_centers,
                y=hist,
                mode='lines',
                name=f'Band {band_num}',
                line=dict(color=colors[idx % len(colors)], width=2),
                fill='tozeroy',
                opacity=0.6
            ))
        
        fig.update_layout(
            title='Band Distribution Comparison',
            xaxis_title='Pixel Value',
            yaxis_title='Frequency',
            hovermode='x unified',
            template='plotly_white',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        return fig
    
    def create_band_scatter_plot(self, dataset: Any, band_x: int = 1, band_y: int = 2, 
                                 sample_size: int = 10000) -> Any:
        """Create a scatter plot comparing two bands."""
        band_x_data = dataset.read(band_x).flatten()
        band_y_data = dataset.read(band_y).flatten()
        
        if band_x_data.size > sample_size:
            indices = np.random.choice(band_x_data.size, sample_size, replace=False)
            band_x_data = band_x_data[indices]
            band_y_data = band_y_data[indices]
        
        mask = np.ones(len(band_x_data), dtype=bool)
        if dataset.nodata is not None:
            mask = mask & (band_x_data != dataset.nodata) & (band_y_data != dataset.nodata)
        mask = mask & ~np.isnan(band_x_data) & ~np.isnan(band_y_data)
        
        band_x_data = band_x_data[mask]
        band_y_data = band_y_data[mask]
        
        correlation = np.corrcoef(band_x_data, band_y_data)[0, 1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=band_x_data,
            y=band_y_data,
            mode='markers',
            marker=dict(size=3, opacity=0.5, color=band_y_data, colorscale='Viridis', showscale=True),
            name='Pixel Values'
        ))
        
        z = np.polyfit(band_x_data, band_y_data, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(band_x_data.min(), band_x_data.max(), 100)
        y_trend = p(x_trend)
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=y_trend,
            mode='lines',
            name=f'Trend (r={correlation:.3f})',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=f'Band {band_x} vs Band {band_y} Scatter Plot (Correlation: {correlation:.3f})',
            xaxis_title=f'Band {band_x} Value',
            yaxis_title=f'Band {band_y} Value',
            template='plotly_white'
        )
        return fig
    
    def create_band_correlation_matrix(self, dataset: Any, sample_size: int = 10000) -> Any:
        """Create a correlation matrix heatmap for all bands."""
        num_bands = dataset.count
        correlation_matrix = np.zeros((num_bands, num_bands))
        
        band_arrays = []
        for i in range(1, num_bands + 1):
            array = dataset.read(i).flatten()
            if array.size > sample_size:
                array = np.random.choice(array, sample_size, replace=False)
            if dataset.nodata is not None:
                array = array[array != dataset.nodata]
            array = array[~np.isnan(array)]
            band_arrays.append(array)
        
        for i in range(num_bands):
            for j in range(num_bands):
                if i == j:
                    correlation_matrix[i, j] = 1.0
                else:
                    min_size = min(len(band_arrays[i]), len(band_arrays[j]))
                    arr_i = band_arrays[i][:min_size]
                    arr_j = band_arrays[j][:min_size]
                    correlation_matrix[i, j] = np.corrcoef(arr_i, arr_j)[0, 1]
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=[f'Band {i+1}' for i in range(num_bands)],
            y=[f'Band {i+1}' for i in range(num_bands)],
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.round(3),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        fig.update_layout(
            title='Band Correlation Matrix',
            template='plotly_white',
            width=600,
            height=600
        )
        return fig
    
    def create_statistics_comparison_chart(self, info: Dict[str, Any]) -> Any:
        """Create a bar chart comparing statistics across bands."""
        band_numbers = [b['band_number'] for b in info['band_info']]
        means = [b['mean'] for b in info['band_info']]
        stds = [b['std_dev'] for b in info['band_info']]
        mins = [b['min'] for b in info['band_info']]
        maxs = [b['max'] for b in info['band_info']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Mean', x=[f'Band {n}' for n in band_numbers], y=means, marker_color='lightblue'))
        fig.add_trace(go.Bar(name='Std Dev', x=[f'Band {n}' for n in band_numbers], y=stds, marker_color='lightcoral'))
        fig.add_trace(go.Bar(name='Min', x=[f'Band {n}' for n in band_numbers], y=mins, marker_color='lightgreen'))
        fig.add_trace(go.Bar(name='Max', x=[f'Band {n}' for n in band_numbers], y=maxs, marker_color='lightyellow'))
        
        fig.update_layout(
            title='Band Statistics Comparison',
            xaxis_title='Band',
            yaxis_title='Value',
            barmode='group',
            template='plotly_white',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        return fig
    
    def apply_colormap_to_band(self, dataset: Any, band_number: int = 1, 
                               colormap_name: str = 'viridis') -> np.ndarray:
        """Apply a colormap to a single-band image."""
        import matplotlib.cm as cm
        
        array = dataset.read(band_number)
        array_min = np.nanmin(array)
        array_max = np.nanmax(array)
        if array_max > array_min:
            normalized = (array - array_min) / (array_max - array_min)
        else:
            normalized = np.zeros_like(array)
        
        cmap = cm.get_cmap(colormap_name)
        colored = cmap(normalized)
        rgb = (colored[:, :, :3] * 255).astype(np.uint8)
        return rgb
    
    def calculate_ndvi(self, dataset: Any, red_band: int = 1, nir_band: int = 2) -> np.ndarray:
        """Calculate NDVI."""
        red = dataset.read(red_band).astype(np.float32)
        nir = dataset.read(nir_band).astype(np.float32)
        denominator = red + nir
        ndvi = np.where(denominator != 0, (nir - red) / denominator, 0)
        return ndvi
    
    def normalize_band(self, dataset: Any, band_number: int = 1, 
                      method: str = 'minmax', output_min: float = 0, 
                      output_max: float = 255) -> np.ndarray:
        """Normalize a band."""
        array = dataset.read(band_number).astype(np.float32)
        
        if method == 'minmax':
            array_min = np.nanmin(array)
            array_max = np.nanmax(array)
            if array_max > array_min:
                normalized = ((array - array_min) / (array_max - array_min)) * (output_max - output_min) + output_min
            else:
                normalized = np.zeros_like(array)
        elif method == 'zscore':
            mean = np.nanmean(array)
            std = np.nanstd(array)
            if std > 0:
                normalized = (array - mean) / std
            else:
                normalized = np.zeros_like(array)
        else:
            normalized = array
        
        return normalized
    
    def convert_image(self, input_file: str, output_file: str, output_format: str = 'GTiff') -> bool:
        """Convert an image from one format to another."""
        try:
            with rasterio.open(input_file) as src:
                profile = src.profile.copy()
                profile['driver'] = output_format
                
                with rasterio.open(output_file, 'w', **profile) as dst:
                    dst.write(src.read())
            return True
        except Exception:
            return False
