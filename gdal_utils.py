"""
GDAL Utility Functions

This module provides reusable functions for common GDAL image processing operations.
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


class GDALImageProcessor:
    """Utility class for GDAL image processing operations."""
    
    @staticmethod
    def open_image(file_path: str) -> gdal.Dataset:
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
    
    @staticmethod
    def open_image_from_bytes(file_bytes: bytes, filename: str = "uploaded_image") -> gdal.Dataset:
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
    
    @staticmethod
    def get_image_info(dataset: gdal.Dataset) -> Dict[str, Any]:
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
    
    @staticmethod
    def read_band_as_array(dataset: gdal.Dataset, band_number: int = 1) -> np.ndarray:
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
    
    @staticmethod
    def read_all_bands(dataset: gdal.Dataset) -> np.ndarray:
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
    
    @staticmethod
    def get_image_preview(dataset: gdal.Dataset, max_size: int = 1000) -> np.ndarray:
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
    
    @staticmethod
    def format_info_for_display(info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format image information for display in UI.
        Returns the raw info dictionary for better organization in tabs.
        """
        return info
    
    @staticmethod
    def convert_image(input_file: str, output_file: str, output_format: str = 'GTiff') -> bool:
        """
        Convert an image from one format to another.
        
        Args:
            input_file: Path to input image
            output_file: Path to output image
            output_format: Output format driver name (e.g., 'GTiff', 'JPEG', 'PNG')
            
        Returns:
            True if conversion successful, False otherwise
        """
        input_ds = gdal.Open(input_file)
        if input_ds is None:
            return False
        
        driver = gdal.GetDriverByName(output_format)
        if driver is None:
            return False
        
        output_ds = driver.CreateCopy(output_file, input_ds, 0)
        if output_ds is None:
            return False
        
        output_ds = None
        input_ds = None
        return True
    
    @staticmethod
    def get_band_histogram(dataset: gdal.Dataset, band_number: int = 1, bins: int = 256, sample_size: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get histogram data for a band.
        
        Args:
            dataset: GDAL Dataset object
            band_number: Band number (1-indexed)
            bins: Number of bins for histogram
            sample_size: If provided, sample this many pixels (for large images)
            
        Returns:
            Tuple of (histogram values, bin edges)
        """
        band = dataset.GetRasterBand(band_number)
        array = band.ReadAsArray()
        
        # Sample if requested
        if sample_size and array.size > sample_size:
            flat_array = array.flatten()
            indices = np.random.choice(flat_array.size, sample_size, replace=False)
            array = flat_array[indices]
        else:
            array = array.flatten()
        
        # Remove NaN and NoData values
        no_data = band.GetNoDataValue()
        if no_data is not None:
            array = array[array != no_data]
        array = array[~np.isnan(array)]
        
        hist, bins = np.histogram(array, bins=bins)
        return hist, bins
    
    @staticmethod
    def create_histogram_plot(dataset: gdal.Dataset, band_number: int = 1, bins: int = 256, 
                              sample_size: Optional[int] = 100000) -> go.Figure:
        """
        Create a histogram plot for a band using Plotly.
        
        Args:
            dataset: GDAL Dataset object
            band_number: Band number (1-indexed)
            bins: Number of bins
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        band = dataset.GetRasterBand(band_number)
        hist, bin_edges = GDALImageProcessor.get_band_histogram(dataset, band_number, bins, sample_size)
        
        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Fit Gaussian curve
        array = band.ReadAsArray().flatten()
        no_data = band.GetNoDataValue()
        if no_data is not None:
            array = array[array != no_data]
        array = array[~np.isnan(array)]
        
        if sample_size and array.size > sample_size:
            array = np.random.choice(array, sample_size, replace=False)
        
        mean = np.mean(array)
        std = np.std(array)
        
        # Create Gaussian curve
        x_gaussian = np.linspace(bin_edges[0], bin_edges[-1], 1000)
        gaussian = np.exp(-0.5 * ((x_gaussian - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
        gaussian = gaussian * len(array) * (bin_edges[1] - bin_edges[0])  # Scale to match histogram
        
        fig = go.Figure()
        
        # Add histogram
        fig.add_trace(go.Bar(
            x=bin_centers,
            y=hist,
            name='Histogram',
            marker_color='rgba(55, 128, 191, 0.7)',
            opacity=0.7
        ))
        
        # Add Gaussian fit
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
    
    @staticmethod
    def create_band_comparison_plot(dataset: gdal.Dataset, band_numbers: List[int] = None, 
                                    sample_size: int = 10000) -> go.Figure:
        """
        Create a comparison plot showing distributions of multiple bands.
        
        Args:
            dataset: GDAL Dataset object
            band_numbers: List of band numbers to compare (default: all bands)
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        if band_numbers is None:
            band_numbers = list(range(1, dataset.RasterCount + 1))
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set3
        
        for idx, band_num in enumerate(band_numbers):
            if band_num > dataset.RasterCount:
                continue
                
            band = dataset.GetRasterBand(band_num)
            array = band.ReadAsArray().flatten()
            
            # Sample if needed
            if array.size > sample_size:
                array = np.random.choice(array, sample_size, replace=False)
            
            # Remove NoData
            no_data = band.GetNoDataValue()
            if no_data is not None:
                array = array[array != no_data]
            array = array[~np.isnan(array)]
            
            # Create histogram
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
    
    @staticmethod
    def create_band_scatter_plot(dataset: gdal.Dataset, band_x: int = 1, band_y: int = 2, 
                                  sample_size: int = 10000) -> go.Figure:
        """
        Create a scatter plot comparing two bands.
        
        Args:
            dataset: GDAL Dataset object
            band_x: X-axis band number
            band_y: Y-axis band number
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        band_x_data = dataset.GetRasterBand(band_x).ReadAsArray().flatten()
        band_y_data = dataset.GetRasterBand(band_y).ReadAsArray().flatten()
        
        # Sample if needed
        if band_x_data.size > sample_size:
            indices = np.random.choice(band_x_data.size, sample_size, replace=False)
            band_x_data = band_x_data[indices]
            band_y_data = band_y_data[indices]
        
        # Remove NoData
        no_data_x = dataset.GetRasterBand(band_x).GetNoDataValue()
        no_data_y = dataset.GetRasterBand(band_y).GetNoDataValue()
        
        mask = np.ones(len(band_x_data), dtype=bool)
        if no_data_x is not None:
            mask = mask & (band_x_data != no_data_x)
        if no_data_y is not None:
            mask = mask & (band_y_data != no_data_y)
        mask = mask & ~np.isnan(band_x_data) & ~np.isnan(band_y_data)
        
        band_x_data = band_x_data[mask]
        band_y_data = band_y_data[mask]
        
        # Calculate correlation
        correlation = np.corrcoef(band_x_data, band_y_data)[0, 1]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=band_x_data,
            y=band_y_data,
            mode='markers',
            marker=dict(
                size=3,
                opacity=0.5,
                color=band_y_data,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title=f'Band {band_y} Value')
            ),
            name='Pixel Values',
            hovertemplate=f'Band {band_x}: %{{x}}<br>Band {band_y}: %{{y}}<extra></extra>'
        ))
        
        # Add trend line
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
            template='plotly_white',
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def create_band_correlation_matrix(dataset: gdal.Dataset, sample_size: int = 10000) -> go.Figure:
        """
        Create a correlation matrix heatmap for all bands.
        
        Args:
            dataset: GDAL Dataset object
            sample_size: Sample size for large images
            
        Returns:
            Plotly figure object
        """
        num_bands = dataset.RasterCount
        correlation_matrix = np.zeros((num_bands, num_bands))
        
        # Read all bands
        band_arrays = []
        for i in range(1, num_bands + 1):
            band = dataset.GetRasterBand(i)
            array = band.ReadAsArray().flatten()
            
            # Sample if needed
            if array.size > sample_size:
                array = np.random.choice(array, sample_size, replace=False)
            
            # Remove NoData
            no_data = band.GetNoDataValue()
            if no_data is not None:
                array = array[array != no_data]
            array = array[~np.isnan(array)]
            
            band_arrays.append(array)
        
        # Calculate correlation matrix
        for i in range(num_bands):
            for j in range(num_bands):
                if i == j:
                    correlation_matrix[i, j] = 1.0
                else:
                    # Align arrays by sampling to same size
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
    
    @staticmethod
    def create_statistics_comparison_chart(info: Dict[str, Any]) -> go.Figure:
        """
        Create a bar chart comparing statistics across bands.
        
        Args:
            info: Image information dictionary from get_image_info
            
        Returns:
            Plotly figure object
        """
        band_numbers = [b['band_number'] for b in info['band_info']]
        means = [b['mean'] for b in info['band_info']]
        stds = [b['std_dev'] for b in info['band_info']]
        mins = [b['min'] for b in info['band_info']]
        maxs = [b['max'] for b in info['band_info']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Mean',
            x=[f'Band {n}' for n in band_numbers],
            y=means,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Std Dev',
            x=[f'Band {n}' for n in band_numbers],
            y=stds,
            marker_color='lightcoral'
        ))
        
        fig.add_trace(go.Bar(
            name='Min',
            x=[f'Band {n}' for n in band_numbers],
            y=mins,
            marker_color='lightgreen'
        ))
        
        fig.add_trace(go.Bar(
            name='Max',
            x=[f'Band {n}' for n in band_numbers],
            y=maxs,
            marker_color='lightyellow'
        ))
        
        fig.update_layout(
            title='Band Statistics Comparison',
            xaxis_title='Band',
            yaxis_title='Value',
            barmode='group',
            template='plotly_white',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        return fig
    
    @staticmethod
    def apply_colormap_to_band(dataset: gdal.Dataset, band_number: int = 1, 
                                colormap_name: str = 'viridis') -> np.ndarray:
        """
        Apply a colormap to a single-band image for visualization.
        
        Args:
            dataset: GDAL Dataset object
            band_number: Band number to apply colormap to
            colormap_name: Name of colormap (viridis, plasma, inferno, magma, jet, etc.)
            
        Returns:
            RGB array with colormap applied
        """
        import matplotlib.cm as cm
        
        band = dataset.GetRasterBand(band_number)
        array = band.ReadAsArray()
        
        # Normalize to 0-1 range
        array_min = array.min()
        array_max = array.max()
        if array_max > array_min:
            normalized = (array - array_min) / (array_max - array_min)
        else:
            normalized = np.zeros_like(array)
        
        # Get colormap
        cmap = cm.get_cmap(colormap_name)
        colored = cmap(normalized)
        
        # Convert to 0-255 RGB
        rgb = (colored[:, :, :3] * 255).astype(np.uint8)
        return rgb
    
    @staticmethod
    def calculate_ndvi(dataset: gdal.Dataset, red_band: int = 1, nir_band: int = 2) -> np.ndarray:
        """
        Calculate NDVI (Normalized Difference Vegetation Index).
        
        Args:
            dataset: GDAL Dataset object
            red_band: Red band number (1-indexed)
            nir_band: Near-infrared band number (1-indexed)
            
        Returns:
            NDVI array (values from -1 to 1)
        """
        red = dataset.GetRasterBand(red_band).ReadAsArray().astype(np.float32)
        nir = dataset.GetRasterBand(nir_band).ReadAsArray().astype(np.float32)
        
        # Avoid division by zero
        denominator = red + nir
        ndvi = np.where(denominator != 0, (nir - red) / denominator, 0)
        
        return ndvi
    
    @staticmethod
    def normalize_band(dataset: gdal.Dataset, band_number: int = 1, 
                      method: str = 'minmax', output_min: float = 0, 
                      output_max: float = 255) -> np.ndarray:
        """
        Normalize a band using different methods.
        
        Args:
            dataset: GDAL Dataset object
            band_number: Band number to normalize
            method: 'minmax' or 'zscore'
            output_min: Minimum output value (for minmax)
            output_max: Maximum output value (for minmax)
            
        Returns:
            Normalized array
        """
        band = dataset.GetRasterBand(band_number)
        array = band.ReadAsArray().astype(np.float32)
        
        if method == 'minmax':
            array_min = array.min()
            array_max = array.max()
            if array_max > array_min:
                normalized = ((array - array_min) / (array_max - array_min)) * (output_max - output_min) + output_min
            else:
                normalized = np.zeros_like(array)
        elif method == 'zscore':
            mean = array.mean()
            std = array.std()
            if std > 0:
                normalized = (array - mean) / std
            else:
                normalized = np.zeros_like(array)
        else:
            normalized = array
        
        return normalized
