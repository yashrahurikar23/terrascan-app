"""
Streamlit App for GDAL Image Processing

This app allows users to upload images and view detailed information
about them using GDAL.
"""

import streamlit as st
from PIL import Image
import numpy as np
import tempfile
import os

# Try to import GDAL - handle gracefully if not installed
try:
    from gdal_utils import GDALImageProcessor
    from osgeo import gdal
    GDAL_AVAILABLE = True
except ImportError as e:
    GDAL_AVAILABLE = False
    GDAL_ERROR = str(e)


# Configure page
st.set_page_config(
    page_title="GDAL Image Processor",
    page_icon="🖼️",
    layout="wide"
)

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'image_info' not in st.session_state:
    st.session_state.image_info = None
if 'image_preview' not in st.session_state:
    st.session_state.image_preview = None
if 'dataset_path' not in st.session_state:
    st.session_state.dataset_path = None


def process_uploaded_image(uploaded_file):
    """Process the uploaded image and extract information."""
    try:
        # Read file bytes
        file_bytes = uploaded_file.read()
        
        # Get file extension for GDAL
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Create temporary file (GDAL works better with actual files)
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name
        
        # Open image with GDAL
        processor = GDALImageProcessor()
        dataset = processor.open_image(tmp_path)
        
        # Get image information
        info = processor.get_image_info(dataset)
        
        # Get preview for display
        preview = processor.get_image_preview(dataset, max_size=800)
        
        # Store dataset path for visualizations (we'll reopen it when needed)
        # Clean up dataset reference but keep temp file
        dataset = None
        
        return info, preview, tmp_path, None
                
    except Exception as e:
        # Clean up temp file on error
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return None, None, None, str(e)


def main():
    """Main Streamlit application."""
    st.title("🖼️ GDAL Image Processor")
    
    # Check if GDAL is available
    if not GDAL_AVAILABLE:
        st.error("❌ GDAL is not installed!")
        st.markdown("""
        ### Installation Required
        
        GDAL (Geospatial Data Abstraction Library) is required to process images.
        
        **To install GDAL on Fedora/RHEL:**
        ```bash
        sudo dnf install gdal gdal-devel python3-gdal
        ```
        
        **Then install the Python package:**
        ```bash
        cd /home/metheus/projects/image_processing
        uv pip install gdal
        ```
        
        **Or use the setup script:**
        ```bash
        ./setup.sh
        ```
        
        After installation, restart this Streamlit app.
        """)
        st.code(f"Error: {GDAL_ERROR}", language="python")
        return
    
    st.markdown("Upload an image to view detailed information extracted using GDAL")
    
    # Create two columns: left for upload/image, right for details
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Image Upload & Preview")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['tif', 'tiff', 'jpg', 'jpeg', 'png', 'jp2', 'img', 'hdf', 'nc'],
            help="Supported formats: GeoTIFF, JPEG, PNG, JPEG2000, and more"
        )
        
        if uploaded_file is not None:
            # Process button
            if st.button("Process Image", type="primary"):
                with st.spinner("Processing image..."):
                    result = process_uploaded_image(uploaded_file)
                    
                    if len(result) == 4:
                        info, preview, dataset_path, error = result
                    else:
                        # Fallback for old return format
                        info, preview, error = result
                        dataset_path = None
                    
                    if error:
                        st.error(f"Error processing image: {error}")
                        st.session_state.image_info = None
                        st.session_state.image_preview = None
                        st.session_state.dataset_path = None
                    else:
                        st.session_state.image_info = info
                        st.session_state.image_preview = preview
                        st.session_state.uploaded_file = uploaded_file.name
                        st.session_state.dataset_path = dataset_path
                        st.success("Image processed successfully!")
            
            # Display image preview if available
            if st.session_state.image_preview is not None:
                st.markdown("### Image Preview")
                # Convert numpy array to PIL Image for display
                preview_image = Image.fromarray(st.session_state.image_preview)
                st.image(preview_image, use_container_width=True, caption=st.session_state.uploaded_file)
        
        else:
            st.info("👆 Please upload an image file to get started")
            st.session_state.image_info = None
            st.session_state.image_preview = None
    
    with col2:
        st.subheader("Image Details")
        
        if st.session_state.image_info is not None:
            info = st.session_state.image_info
            
            # Create tabs for organized display
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "📊 Overview", 
                "🌍 Geospatial", 
                "🎨 Bands", 
                "📋 Metadata",
                "📈 Visualizations",
                "🔧 Operations",
                "⚙️ Advanced"
            ])
            
            # Tab 1: Overview
            with tab1:
                st.markdown("### Basic Information")
                
                # Display key metrics in columns
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Width", f"{info['width']:,} px")
                    st.metric("Height", f"{info['height']:,} px")
                with col_b:
                    st.metric("Bands", info['bands'])
                    st.metric("Total Pixels", f"{info['width'] * info['height']:,}")
                
                st.divider()
                
                # Driver information
                st.markdown("#### Driver Information")
                st.write(f"**Driver:** {info['driver']}")
                if 'driver_long_name' in info and info['driver_long_name']:
                    st.write(f"**Full Name:** {info['driver_long_name']}")
                
                # File size estimate (if available)
                if st.session_state.uploaded_file:
                    st.divider()
                    st.markdown("#### File Information")
                    st.write(f"**Filename:** {st.session_state.uploaded_file}")
            
            # Tab 2: Geospatial Information
            with tab2:
                if info.get('geotransform'):
                    st.markdown("### Coordinate System")
                    
                    # Geotransform parameters
                    st.markdown("#### Geotransform Parameters")
                    col_c, col_d = st.columns(2)
                    with col_c:
                        st.write(f"**Origin X:** `{info['origin_x']:.6f}`")
                        st.write(f"**Origin Y:** `{info['origin_y']:.6f}`")
                    with col_d:
                        st.write(f"**Pixel Width:** `{info['pixel_width']:.6f}`")
                        st.write(f"**Pixel Height:** `{info['pixel_height']:.6f}`")
                    
                    # Bounds
                    if 'bounds' in info:
                        st.divider()
                        st.markdown("#### Spatial Bounds")
                        bounds = info['bounds']
                        st.write(f"**Min X:** `{bounds['min_x']:.6f}`")
                        st.write(f"**Max X:** `{bounds['max_x']:.6f}`")
                        st.write(f"**Min Y:** `{bounds['min_y']:.6f}`")
                        st.write(f"**Max Y:** `{bounds['max_y']:.6f}`")
                    
                    # Projection
                    if info.get('projection_name'):
                        st.divider()
                        st.markdown("#### Projection")
                        st.write(f"**Name:** {info['projection_name']}")
                        if 'epsg_code' in info and info['epsg_code']:
                            st.write(f"**EPSG Code:** EPSG:{info['epsg_code']}")
                        if 'proj4_string' in info and info['proj4_string']:
                            with st.expander("Proj4 String"):
                                st.code(info['proj4_string'])
                        if 'srs_wkt' in info:
                            with st.expander("WKT (Well-Known Text)"):
                                st.code(info['srs_wkt'], language='text')
                else:
                    st.info("No geospatial information available for this image.")
            
            # Tab 3: Band Details
            with tab3:
                st.markdown("### Band Information")
                
                for band_info in info['band_info']:
                    band_num = band_info['band_number']
                    
                    with st.expander(f"Band {band_num} - {band_info.get('color_interpretation', 'Unknown')}", expanded=True):
                        # Statistics in columns
                        col_e, col_f, col_g, col_h = st.columns(4)
                        with col_e:
                            st.metric("Min", f"{band_info['min']:.2f}")
                        with col_f:
                            st.metric("Max", f"{band_info['max']:.2f}")
                        with col_g:
                            st.metric("Mean", f"{band_info['mean']:.2f}")
                        with col_h:
                            st.metric("Std Dev", f"{band_info['std_dev']:.2f}")
                        
                        st.divider()
                        
                        # Band properties
                        col_i, col_j = st.columns(2)
                        with col_i:
                            st.write(f"**Data Type:** {band_info['data_type']}")
                            if 'data_type_size' in band_info:
                                st.write(f"**Data Size:** {band_info['data_type_size']} bits")
                            st.write(f"**Color Interpretation:** {band_info['color_interpretation']}")
                            if 'unit_type' in band_info and band_info['unit_type']:
                                st.write(f"**Unit Type:** {band_info['unit_type']}")
                        with col_j:
                            st.write(f"**Block Size:** {band_info['block_size_x']} × {band_info['block_size_y']}")
                            st.write(f"**Overview Count:** {band_info['overview_count']}")
                            if 'no_data_value' in band_info and band_info['no_data_value'] is not None:
                                st.write(f"**No Data Value:** `{band_info['no_data_value']}`")
                            else:
                                st.write("**No Data Value:** None")
                        
                        # Additional properties
                        if 'scale' in band_info and band_info['scale'] != 1.0:
                            st.write(f"**Scale:** {band_info['scale']}")
                        if 'offset' in band_info and band_info['offset'] != 0.0:
                            st.write(f"**Offset:** {band_info['offset']}")
                        if 'description' in band_info and band_info['description']:
                            st.write(f"**Description:** {band_info['description']}")
                        if 'median' in band_info:
                            st.write(f"**Median:** {band_info['median']:.2f}")
                        if 'unique_values_count' in band_info:
                            st.write(f"**Unique Values:** {band_info['unique_values_count']:,}")
                        if 'has_color_table' in band_info and band_info['has_color_table']:
                            st.write(f"**Color Table:** {band_info.get('color_table_count', 'N/A')} entries")
            
            # Tab 4: Metadata
            with tab4:
                st.markdown("### Dataset Metadata")
                
                if info.get('metadata'):
                    for key, value in info['metadata'].items():
                        st.write(f"**{key}:** {value}")
                else:
                    st.info("No dataset metadata available.")
                
                # Band metadata
                if info.get('band_info'):
                    st.divider()
                    st.markdown("### Band Metadata")
                    for band_info in info['band_info']:
                        band_num = band_info['band_number']
                        if band_info.get('metadata'):
                            with st.expander(f"Band {band_num} Metadata"):
                                for key, value in band_info['metadata'].items():
                                    st.write(f"**{key}:** {value}")
            
            # Tab 5: Visualizations
            with tab5:
                st.markdown("### Data Visualizations")
                st.markdown("Generate graphs and charts to analyze band distributions and relationships.")
                
                if st.session_state.dataset_path and os.path.exists(st.session_state.dataset_path):
                    processor = GDALImageProcessor()
                    dataset = processor.open_image(st.session_state.dataset_path)
                    
                    try:
                        # Histogram with Gaussian fit
                        st.markdown("#### Band Histogram with Gaussian Fit")
                        band_select = st.selectbox(
                            "Select Band for Histogram",
                            options=list(range(1, info['bands'] + 1)),
                            index=0,
                            key="hist_band"
                        )
                        
                        bins_select = st.slider("Number of Bins", 50, 500, 256, key="hist_bins")
                        
                        if st.button("Generate Histogram", key="gen_hist"):
                            with st.spinner("Generating histogram..."):
                                fig_hist = processor.create_histogram_plot(dataset, band_select, bins_select)
                                st.plotly_chart(fig_hist, use_container_width=True)
                        
                        st.divider()
                        
                        # Band comparison
                        if info['bands'] > 1:
                            st.markdown("#### Band Distribution Comparison")
                            selected_bands = st.multiselect(
                                "Select Bands to Compare",
                                options=list(range(1, info['bands'] + 1)),
                                default=list(range(1, min(4, info['bands'] + 1))),
                                key="compare_bands"
                            )
                            
                            if selected_bands and st.button("Generate Comparison", key="gen_compare"):
                                with st.spinner("Generating comparison..."):
                                    fig_compare = processor.create_band_comparison_plot(dataset, selected_bands)
                                    st.plotly_chart(fig_compare, use_container_width=True)
                            
                            st.divider()
                            
                            # Scatter plot
                            st.markdown("#### Band Scatter Plot")
                            col_x, col_y = st.columns(2)
                            with col_x:
                                band_x = st.selectbox("X-axis Band", options=list(range(1, info['bands'] + 1)), index=0, key="scatter_x")
                            with col_y:
                                band_y = st.selectbox("Y-axis Band", options=list(range(1, info['bands'] + 1)), index=min(1, info['bands'] - 1), key="scatter_y")
                            
                            if st.button("Generate Scatter Plot", key="gen_scatter"):
                                with st.spinner("Generating scatter plot..."):
                                    fig_scatter = processor.create_band_scatter_plot(dataset, band_x, band_y)
                                    st.plotly_chart(fig_scatter, use_container_width=True)
                            
                            st.divider()
                            
                            # Correlation matrix
                            st.markdown("#### Band Correlation Matrix")
                            if st.button("Generate Correlation Matrix", key="gen_corr"):
                                with st.spinner("Calculating correlations..."):
                                    fig_corr = processor.create_band_correlation_matrix(dataset)
                                    st.plotly_chart(fig_corr, use_container_width=True)
                            
                            st.divider()
                        
                        # Statistics comparison chart
                        st.markdown("#### Statistics Comparison")
                        if st.button("Generate Statistics Chart", key="gen_stats"):
                            with st.spinner("Generating statistics chart..."):
                                fig_stats = processor.create_statistics_comparison_chart(info)
                                st.plotly_chart(fig_stats, use_container_width=True)
                        
                    finally:
                        dataset = None
                else:
                    st.info("Dataset not available for visualizations. Please process the image first.")
            
            # Tab 6: Operations (inspired by GDAL tutorials)
            with tab6:
                st.markdown("### Image Operations")
                st.markdown("Common GDAL operations for image processing and transformation.")
                
                if st.session_state.dataset_path and os.path.exists(st.session_state.dataset_path):
                    processor = GDALImageProcessor()
                    dataset = processor.open_image(st.session_state.dataset_path)
                    
                    try:
                        # Format Conversion
                        st.markdown("#### 🔄 Format Conversion")
                        with st.expander("Convert Image Format", expanded=False):
                            output_format = st.selectbox(
                                "Output Format",
                                options=['GTiff', 'JPEG', 'PNG', 'JPEG2000', 'HFA', 'ENVI'],
                                key="convert_format"
                            )
                            if st.button("Convert Format", key="btn_convert"):
                                st.info("Format conversion feature - save functionality coming soon!")
                        
                        st.divider()
                        
                        # Colormap Application
                        if info['bands'] == 1:
                            st.markdown("#### 🎨 Apply Colormap")
                            st.markdown("Apply a colormap to single-band images for better visualization.")
                            
                            colormap_options = ['viridis', 'plasma', 'inferno', 'magma', 'jet', 
                                               'hot', 'cool', 'spring', 'summer', 'autumn', 'winter']
                            selected_colormap = st.selectbox(
                                "Select Colormap",
                                options=colormap_options,
                                index=0,
                                key="colormap_select"
                            )
                            
                            if st.button("Apply Colormap", key="btn_colormap"):
                                with st.spinner("Applying colormap..."):
                                    colored = processor.apply_colormap_to_band(dataset, 1, selected_colormap)
                                    st.image(colored, use_container_width=True, 
                                           caption=f"Band 1 with {selected_colormap} colormap")
                        
                        st.divider()
                        
                        # NDVI Calculation
                        if info['bands'] >= 2:
                            st.markdown("#### 🌱 Spectral Indices")
                            
                            st.markdown("**NDVI (Normalized Difference Vegetation Index)**")
                            st.markdown("Formula: `(NIR - Red) / (NIR + Red)`")
                            
                            col_red, col_nir = st.columns(2)
                            with col_red:
                                red_band = st.selectbox(
                                    "Red Band",
                                    options=list(range(1, info['bands'] + 1)),
                                    index=0,
                                    key="ndvi_red"
                                )
                            with col_nir:
                                nir_band = st.selectbox(
                                    "NIR Band",
                                    options=list(range(1, info['bands'] + 1)),
                                    index=min(1, info['bands'] - 1),
                                    key="ndvi_nir"
                                )
                            
                            if st.button("Calculate NDVI", key="btn_ndvi"):
                                with st.spinner("Calculating NDVI..."):
                                    ndvi = processor.calculate_ndvi(dataset, red_band, nir_band)
                                    
                                    # Display NDVI statistics
                                    st.metric("NDVI Min", f"{ndvi.min():.3f}")
                                    st.metric("NDVI Max", f"{ndvi.max():.3f}")
                                    st.metric("NDVI Mean", f"{ndvi.mean():.3f}")
                                    
                                    # Apply colormap for visualization
                                    # Normalize NDVI to 0-1 for colormap
                                    ndvi_normalized = (ndvi + 1) / 2  # NDVI ranges from -1 to 1
                                    import matplotlib.cm as cm
                                    cmap = cm.get_cmap('RdYlGn')
                                    colored_ndvi = (cmap(ndvi_normalized)[:, :, :3] * 255).astype(np.uint8)
                                    
                                    st.image(colored_ndvi, use_container_width=True, 
                                           caption="NDVI Visualization (Red=Low, Yellow=Medium, Green=High)")
                        
                        st.divider()
                        
                        # Band Normalization
                        st.markdown("#### 📊 Band Normalization")
                        st.markdown("Normalize band values using different methods.")
                        
                        norm_band = st.selectbox(
                            "Select Band to Normalize",
                            options=list(range(1, info['bands'] + 1)),
                            index=0,
                            key="norm_band"
                        )
                        
                        norm_method = st.selectbox(
                            "Normalization Method",
                            options=['minmax', 'zscore'],
                            key="norm_method"
                        )
                        
                        if norm_method == 'minmax':
                            col_min, col_max = st.columns(2)
                            with col_min:
                                output_min = st.number_input("Output Min", value=0.0, key="norm_min")
                            with col_max:
                                output_max = st.number_input("Output Max", value=255.0, key="norm_max")
                        else:
                            output_min = 0.0
                            output_max = 255.0
                        
                        if st.button("Normalize Band", key="btn_normalize"):
                            with st.spinner("Normalizing band..."):
                                normalized = processor.normalize_band(
                                    dataset, norm_band, norm_method, output_min, output_max
                                )
                                
                                st.metric("Normalized Min", f"{normalized.min():.2f}")
                                st.metric("Normalized Max", f"{normalized.max():.2f}")
                                st.metric("Normalized Mean", f"{normalized.mean():.2f}")
                                
                                # Display normalized band
                                if norm_method == 'minmax':
                                    display_array = normalized.astype(np.uint8)
                                else:
                                    # For z-score, normalize to 0-255 for display
                                    display_array = ((normalized - normalized.min()) / 
                                                   (normalized.max() - normalized.min()) * 255).astype(np.uint8)
                                
                                st.image(display_array, use_container_width=True, 
                                       caption=f"Normalized Band {norm_band} ({norm_method})")
                        
                    finally:
                        dataset = None
                else:
                    st.info("Dataset not available for operations. Please process the image first.")
            
            # Tab 7: Advanced
            with tab7:
                st.markdown("### Technical Details")
                
                st.markdown("#### Driver Information")
                st.write(f"**Short Name:** {info['driver']}")
                if 'driver_long_name' in info:
                    st.write(f"**Long Name:** {info.get('driver_long_name', 'N/A')}")
                
                if info.get('description'):
                    st.divider()
                    st.markdown("#### Dataset Description")
                    st.write(info['description'])
                
                st.divider()
                st.markdown("#### Memory Information")
                total_size = info['width'] * info['height'] * info['bands']
                if 'band_info' in info and len(info['band_info']) > 0:
                    data_type_size = info['band_info'][0].get('data_type_size', 8)
                    estimated_size = (total_size * data_type_size) / (8 * 1024 * 1024)  # MB
                    st.write(f"**Estimated Size:** {estimated_size:.2f} MB")
                
        else:
            st.info("Upload and process an image to see details here")
            
            # Show example of what information will be displayed
            with st.expander("ℹ️ What information will be shown?"):
                st.markdown("""
                Once you upload and process an image, you'll see organized information in tabs:
                
                - **📊 Overview**: Basic dimensions, driver information
                - **🌍 Geospatial**: Coordinates, bounds, projection details
                - **🎨 Bands**: Detailed statistics and properties for each band
                - **📋 Metadata**: Dataset and band metadata
                - **📈 Visualizations**: Histograms, scatter plots, correlation matrices, and more
                - **🔧 Operations**: Format conversion, colormaps, NDVI, normalization (inspired by GDAL tutorials)
                - **⚙️ Advanced**: Technical details and memory information
                """)


if __name__ == "__main__":
    main()
