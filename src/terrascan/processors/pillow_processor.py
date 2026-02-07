"""
Pillow (PIL) Image Processor

Lightweight image processor using Pillow library.
Perfect for basic image operations when GDAL is not available.
No system dependencies required - pure Python!
"""

from typing import Dict, Optional, Tuple, Any, List
import numpy as np
from PIL import Image, ImageStat
import io

from terrascan.processors.base import BaseImageProcessor


class PillowImageProcessor(BaseImageProcessor):
    """
    Pillow-based image processor.
    
    Lightweight alternative to GDAL for basic image operations.
    Supports: JPEG, PNG, TIFF, BMP, GIF, and more.
    """
    
    @property
    def name(self) -> str:
        """Return processor name."""
        return "pillow"
    
    @property
    def available(self) -> bool:
        """Check if Pillow is available."""
        try:
            import PIL
            return True
        except ImportError:
            return False
    
    def open_image(self, file_path: str) -> Image.Image:
        """
        Open an image file using Pillow.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If the file cannot be opened
        """
        try:
            img = Image.open(file_path)
            # Load image to ensure it's fully read
            img.load()
            return img
        except Exception as e:
            raise ValueError(f"Could not open image: {str(e)}")
    
    def open_image_from_bytes(self, file_bytes: bytes, filename: str = "uploaded_image") -> Image.Image:
        """
        Open an image from bytes.
        
        Args:
            file_bytes: Image file as bytes
            filename: Original filename (for format detection)
            
        Returns:
            PIL Image object
        """
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.load()
            return img
        except Exception as e:
            raise ValueError(f"Could not open image from bytes: {str(e)}")
    
    def get_image_info(self, dataset: Image.Image) -> Dict[str, Any]:
        """
        Extract comprehensive information from an image.
        
        Args:
            dataset: PIL Image object
            
        Returns:
            Dictionary with image information
        """
        info = {
            'width': dataset.width,
            'height': dataset.height,
            'bands': len(dataset.getbands()) if hasattr(dataset, 'getbands') else 1,
            'format': dataset.format or 'UNKNOWN',
            'mode': dataset.mode,
            'driver': dataset.format or 'PIL',
            'driver_long_name': f'Pillow {dataset.format or "Image"}',
            'description': f'Image opened with Pillow',
            'metadata': {},
            'band_info': [],
            'geospatial': False,  # Pillow doesn't handle geospatial data
        }
        
        # Get image metadata (EXIF, etc.)
        if hasattr(dataset, '_getexif') and dataset._getexif():
            try:
                exif = dataset._getexif()
                info['metadata']['exif'] = dict(exif) if exif else {}
            except:
                pass
        
        # Get format-specific metadata
        if hasattr(dataset, 'info'):
            info['metadata'].update(dataset.info)
        
        # Get band information
        bands = dataset.getbands() if hasattr(dataset, 'getbands') else ['L']  # L = grayscale
        for i, band_name in enumerate(bands, 1):
            # Convert to numpy array for statistics
            if dataset.mode in ('RGB', 'RGBA', 'CMYK', 'LAB'):
                # Extract single band
                band_array = np.array(dataset)[:, :, i-1]
                # Create a single-band image for ImageStat
                band_img = Image.fromarray(band_array, mode='L')
            else:
                # Grayscale or single band
                band_array = np.array(dataset)
                band_img = dataset  # Use the original image for single band
            
            # Calculate statistics using ImageStat (more accurate for PIL)
            try:
                stats = ImageStat.Stat(band_img)
                # Use ImageStat results if available, otherwise use numpy
                band_mean = stats.mean[0] if stats.mean else float(band_array.mean())
                band_std = stats.stddev[0] if stats.stddev else float(band_array.std())
            except:
                # Fallback to numpy if ImageStat fails
                band_mean = float(band_array.mean())
                band_std = float(band_array.std())
            
            band_info = {
                'band_number': i,
                'band_name': band_name,
                'color_interpretation': band_name,  # R, G, B, L, etc.
                'data_type': str(band_array.dtype),
                'data_type_size': band_array.dtype.itemsize * 8,
                'min': float(band_array.min()),
                'max': float(band_array.max()),
                'mean': band_mean,
                'std_dev': band_std,
                'median': float(np.median(band_array)),
                'unique_values_count': len(np.unique(band_array)),
                'block_size_x': dataset.width,
                'block_size_y': dataset.height,
                'overview_count': 0,
                'no_data_value': None,
                'metadata': {},
            }
            
            info['band_info'].append(band_info)
        
        # Add mode-specific information
        info['color_mode'] = dataset.mode
        info['has_transparency'] = 'transparency' in dataset.info if hasattr(dataset, 'info') else False
        
        return info
    
    def read_band_as_array(self, dataset: Image.Image, band_number: int = 1) -> np.ndarray:
        """
        Read a specific band as a NumPy array.
        
        Args:
            dataset: PIL Image object
            band_number: Band number (1-indexed)
            
        Returns:
            NumPy array
        """
        arr = np.array(dataset)
        
        if len(arr.shape) == 3:
            # Multi-band image
            if band_number <= arr.shape[2]:
                return arr[:, :, band_number - 1]
            else:
                raise ValueError(f"Band {band_number} not available")
        else:
            # Single band (grayscale)
            if band_number == 1:
                return arr
            else:
                raise ValueError(f"Only one band available (grayscale image)")
    
    def read_all_bands(self, dataset: Image.Image) -> np.ndarray:
        """
        Read all bands as a NumPy array.
        
        Args:
            dataset: PIL Image object
            
        Returns:
            NumPy array with shape (bands, height, width) or (height, width)
        """
        arr = np.array(dataset)
        
        if len(arr.shape) == 3:
            # Multi-band: convert from (H, W, C) to (C, H, W)
            return np.transpose(arr, (2, 0, 1))
        else:
            # Single band: add dimension
            return arr[np.newaxis, :, :]
    
    def get_image_preview(self, dataset: Image.Image, max_size: int = 1000) -> np.ndarray:
        """
        Get a preview of the image for display.
        
        Args:
            dataset: PIL Image object
            max_size: Maximum dimension for preview
            
        Returns:
            NumPy array suitable for display (RGB format)
        """
        # Resize if needed
        width, height = dataset.size
        scale = min(max_size / width, max_size / height, 1.0)
        
        if scale < 1.0:
            new_size = (int(width * scale), int(height * scale))
            preview = dataset.resize(new_size, Image.Resampling.LANCZOS)
        else:
            preview = dataset
        
        # Convert to RGB if needed
        if preview.mode != 'RGB':
            preview = preview.convert('RGB')
        
        return np.array(preview)
    
    def convert_image(self, input_file: str, output_file: str, output_format: str = 'PNG') -> bool:
        """
        Convert an image from one format to another.
        
        Args:
            input_file: Path to input image
            output_file: Path to output image
            output_format: Output format (PNG, JPEG, etc.)
            
        Returns:
            True if conversion successful
        """
        try:
            img = Image.open(input_file)
            # Convert RGBA to RGB for JPEG
            if output_format.upper() == 'JPEG' and img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(output_file, format=output_format)
            return True
        except Exception:
            return False
    
    def get_band_histogram(self, dataset: Image.Image, band_number: int = 1, 
                          bins: int = 256, sample_size: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get histogram data for a band.
        
        Args:
            dataset: PIL Image object
            band_number: Band number
            bins: Number of bins
            sample_size: Sample size (for large images)
            
        Returns:
            Tuple of (histogram values, bin edges)
        """
        band_array = self.read_band_as_array(dataset, band_number)
        array = band_array.flatten()
        
        # Sample if requested
        if sample_size and array.size > sample_size:
            array = np.random.choice(array, sample_size, replace=False)
        
        hist, bin_edges = np.histogram(array, bins=bins)
        return hist, bin_edges
    
    def create_histogram_plot(self, dataset: Image.Image, band_number: int = 1, 
                             bins: int = 256, sample_size: Optional[int] = 100000):
        """
        Create a histogram plot (requires plotly).
        
        Args:
            dataset: PIL Image object
            band_number: Band number
            bins: Number of bins
            sample_size: Sample size
            
        Returns:
            Plotly figure
        """
        try:
            import plotly.graph_objects as go
        except ImportError:
            raise ImportError("Plotly is required for visualization")
        
        hist, bin_edges = self.get_band_histogram(dataset, band_number, bins, sample_size)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Calculate statistics
        band_array = self.read_band_as_array(dataset, band_number)
        array = band_array.flatten()
        if sample_size and array.size > sample_size:
            array = np.random.choice(array, sample_size, replace=False)
        
        mean = np.mean(array)
        std = np.std(array)
        
        # Create Gaussian fit
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
    
    def create_band_comparison_plot(self, dataset: Image.Image, band_numbers: List[int] = None, 
                                   sample_size: int = 10000):
        """Create band comparison plot."""
        try:
            import plotly.graph_objects as go
            import plotly.express as px
        except ImportError:
            raise ImportError("Plotly is required for visualization")
        
        if band_numbers is None:
            band_numbers = list(range(1, len(dataset.getbands()) + 1))
        
        fig = go.Figure()
        colors = px.colors.qualitative.Set3
        
        for idx, band_num in enumerate(band_numbers):
            band_array = self.read_band_as_array(dataset, band_num)
            array = band_array.flatten()
            
            if array.size > sample_size:
                array = np.random.choice(array, sample_size, replace=False)
            
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
    
    def create_band_scatter_plot(self, dataset: Image.Image, band_x: int = 1, band_y: int = 2, 
                                  sample_size: int = 10000):
        """Create scatter plot comparing two bands."""
        try:
            import plotly.graph_objects as go
        except ImportError:
            raise ImportError("Plotly is required for visualization")
        
        band_x_data = self.read_band_as_array(dataset, band_x).flatten()
        band_y_data = self.read_band_as_array(dataset, band_y).flatten()
        
        if band_x_data.size > sample_size:
            indices = np.random.choice(band_x_data.size, sample_size, replace=False)
            band_x_data = band_x_data[indices]
            band_y_data = band_y_data[indices]
        
        correlation = np.corrcoef(band_x_data, band_y_data)[0, 1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=band_x_data,
            y=band_y_data,
            mode='markers',
            marker=dict(size=3, opacity=0.5, color=band_y_data, colorscale='Viridis', showscale=True),
            name='Pixel Values'
        ))
        
        # Trend line
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
    
    def create_band_correlation_matrix(self, dataset: Image.Image, sample_size: int = 10000):
        """Create correlation matrix for all bands."""
        try:
            import plotly.graph_objects as go
        except ImportError:
            raise ImportError("Plotly is required for visualization")
        
        num_bands = len(dataset.getbands())
        correlation_matrix = np.zeros((num_bands, num_bands))
        
        band_arrays = []
        for i in range(1, num_bands + 1):
            array = self.read_band_as_array(dataset, i).flatten()
            if array.size > sample_size:
                array = np.random.choice(array, sample_size, replace=False)
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
    
    def create_statistics_comparison_chart(self, info: Dict[str, Any]):
        """Create statistics comparison chart."""
        try:
            import plotly.graph_objects as go
        except ImportError:
            raise ImportError("Plotly is required for visualization")
        
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
    
    def apply_colormap_to_band(self, dataset: Image.Image, band_number: int = 1, 
                              colormap_name: str = 'viridis') -> np.ndarray:
        """Apply colormap to a single band."""
        import matplotlib.cm as cm
        
        band_array = self.read_band_as_array(dataset, band_number)
        array_min = band_array.min()
        array_max = band_array.max()
        
        if array_max > array_min:
            normalized = (band_array - array_min) / (array_max - array_min)
        else:
            normalized = np.zeros_like(band_array)
        
        cmap = cm.get_cmap(colormap_name)
        colored = cmap(normalized)
        rgb = (colored[:, :, :3] * 255).astype(np.uint8)
        return rgb
    
    def calculate_ndvi(self, dataset: Image.Image, red_band: int = 1, nir_band: int = 2) -> np.ndarray:
        """
        Calculate NDVI (requires at least 2 bands).
        
        Note: This assumes bands are in RGB order. For actual NDVI,
        you need proper red and NIR bands from multispectral imagery.
        """
        red = self.read_band_as_array(dataset, red_band).astype(np.float32)
        nir = self.read_band_as_array(dataset, nir_band).astype(np.float32)
        
        denominator = red + nir
        ndvi = np.where(denominator != 0, (nir - red) / denominator, 0)
        return ndvi
    
    def normalize_band(self, dataset: Image.Image, band_number: int = 1, 
                      method: str = 'minmax', output_min: float = 0, 
                      output_max: float = 255) -> np.ndarray:
        """Normalize a band using different methods."""
        band_array = self.read_band_as_array(dataset, band_number).astype(np.float32)
        
        if method == 'minmax':
            array_min = band_array.min()
            array_max = band_array.max()
            if array_max > array_min:
                normalized = ((band_array - array_min) / (array_max - array_min)) * (output_max - output_min) + output_min
            else:
                normalized = np.zeros_like(band_array)
        elif method == 'zscore':
            mean = band_array.mean()
            std = band_array.std()
            if std > 0:
                normalized = (band_array - mean) / std
            else:
                normalized = np.zeros_like(band_array)
        else:
            normalized = band_array
        
        return normalized
    
    def format_info_for_display(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Format image information for display."""
        return info
