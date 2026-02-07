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

# Import processor manager and processors
try:
    from terrascan.processors import (
        ProcessorManager,
        get_processor,
        get_default_processor,
        list_available_processors,
        GDALImageProcessor,
        GDAL_AVAILABLE,
        RASTERIO_AVAILABLE,
        PILLOW_AVAILABLE,
        PillowImageProcessor
    )
    PROCESSOR_MANAGER_AVAILABLE = True
except ImportError as e:
    PROCESSOR_MANAGER_AVAILABLE = False
    ProcessorManager = None
    GDAL_AVAILABLE = False
    RASTERIO_AVAILABLE = False
    GDALImageProcessor = None
    GDAL_ERROR = str(e)
    
    # Try to import Pillow directly as fallback (it's lightweight and should work)
    PILLOW_AVAILABLE = False
    PillowImageProcessor = None
    try:
        # Try relative import first (if we're in the package)
        try:
            from .processors.pillow_processor import PillowImageProcessor
        except (ImportError, ValueError):
            # Try absolute import
            from terrascan.processors.pillow_processor import PillowImageProcessor
        
        if PillowImageProcessor:
            pillow_instance = PillowImageProcessor()
            PILLOW_AVAILABLE = pillow_instance.available
    except (ImportError, AttributeError, Exception):
        PILLOW_AVAILABLE = False
        PillowImageProcessor = None


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
if 'selected_processor' not in st.session_state:
    st.session_state.selected_processor = None
if 'current_processor' not in st.session_state:
    st.session_state.current_processor = None


def get_current_processor():
    """Get the current processor instance."""
    if not PROCESSOR_MANAGER_AVAILABLE:
        # Fallback: try processors directly
        # Try Pillow first (lightweight, always available)
        if PILLOW_AVAILABLE and PillowImageProcessor:
            try:
                pillow_instance = PillowImageProcessor()
                if pillow_instance.available:
                    return pillow_instance
            except:
                pass
        
        # Fallback to GDAL if available
        if GDAL_AVAILABLE and GDALImageProcessor:
            try:
                return GDALImageProcessor()
            except:
                pass
        
        return None
    
    # Use selected processor or default
    processor_name = st.session_state.get('selected_processor', 'auto')
    processor = get_processor(processor_name)
    
    if processor is None:
        # Fallback to default
        processor = get_default_processor()
    
    return processor


def process_uploaded_image(uploaded_file):
    """Process the uploaded image and extract information."""
    try:
        # Get processor
        processor = get_current_processor()
        if processor is None:
            raise ImportError("No image processor available")
        
        # Read file bytes
        file_bytes = uploaded_file.read()
        
        # Get file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Create temporary file (processors work better with actual files)
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name
        
        # Open image with processor
        dataset = processor.open_image(tmp_path)
        
        # Get image information
        info = processor.get_image_info(dataset)
        
        # Get preview for display
        preview = processor.get_image_preview(dataset, max_size=800)
        
        # Store processor name and dataset path for later use
        st.session_state.current_processor = processor.name
        st.session_state.dataset_path = tmp_path
        
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
    st.title("🖼️ Geospatial Image Processor")
    
    # Get available processors
    if PROCESSOR_MANAGER_AVAILABLE:
        available_processors = list_available_processors()
        processor_info = ProcessorManager.get_processor_info()
    else:
        # Fallback: check processors directly
        available_processors = []
        processor_info = {}
        
        # Check Pillow first (lightweight, always available)
        # Try multiple ways to import/check Pillow
        pillow_found = False
        
        # Method 1: Check if PIL is installed (most reliable check)
        try:
            import PIL
            # PIL is installed, now try to import our processor
            # Note: Image is already imported at module level
            try:
                # Try different import paths
                pillow_proc = None
                try:
                    # Try relative import (if we're in the package)
                    from .processors.pillow_processor import PillowImageProcessor
                    pillow_proc = PillowImageProcessor
                except (ImportError, ValueError, AttributeError):
                    try:
                        # Try absolute import with src path
                        import sys
                        from pathlib import Path
                        src_path = Path(__file__).parent.parent.parent / "src"
                        if str(src_path) not in sys.path:
                            sys.path.insert(0, str(src_path))
                        from terrascan.processors.pillow_processor import PillowImageProcessor
                        pillow_proc = PillowImageProcessor
                    except:
                        # Last resort: try direct import
                        import importlib.util
                        pillow_path = Path(__file__).parent.parent / "processors" / "pillow_processor.py"
                        if pillow_path.exists():
                            spec = importlib.util.spec_from_file_location("pillow_processor", pillow_path)
                            pillow_module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(pillow_module)
                            pillow_proc = pillow_module.PillowImageProcessor
                
                if pillow_proc:
                    pillow_instance = pillow_proc()
                    if pillow_instance.available:
                        available_processors.append('pillow')
                        processor_info['pillow'] = {'name': 'pillow', 'available': True, 'description': 'Lightweight image processing'}
                        pillow_found = True
            except Exception as e:
                # If processor class fails, but PIL is installed, create a simple wrapper
                pass
        except ImportError:
            pass
        
        # Method 2: Use imported PillowImageProcessor if available
        if not pillow_found and PILLOW_AVAILABLE and PillowImageProcessor:
            try:
                pillow_instance = PillowImageProcessor()
                if pillow_instance.available:
                    available_processors.append('pillow')
                    processor_info['pillow'] = {'name': 'pillow', 'available': True}
                    pillow_found = True
            except:
                pass
        
        # Check GDAL
        if GDAL_AVAILABLE and GDALImageProcessor:
            try:
                gdal_instance = GDALImageProcessor()
                if gdal_instance.available:
                    available_processors.append('gdal')
                    processor_info['gdal'] = {'name': 'gdal', 'available': True}
            except:
                pass
    
    # Check if any processor is available
    if not available_processors:
        # Last resort: Check if PIL is installed and try to use it directly
        try:
            import PIL
            # PIL is definitely installed, so Pillow should work
            # Note: Image is already imported at module level
            # Try one more time with a simpler approach
            try:
                import sys
                from pathlib import Path
                # Find the pillow_processor.py file
                current_file = Path(__file__)
                pillow_file = current_file.parent / "processors" / "pillow_processor.py"
                if pillow_file.exists():
                    # Add parent to path
                    parent_path = str(pillow_file.parent.parent)
                    if parent_path not in sys.path:
                        sys.path.insert(0, parent_path)
                    # Try import
                    from terrascan.processors.pillow_processor import PillowImageProcessor
                    pillow_instance = PillowImageProcessor()
                    if pillow_instance.available:
                        available_processors.append('pillow')
                        processor_info['pillow'] = {'name': 'pillow', 'available': True}
            except Exception:
                # Even if import fails, PIL is installed, so we can show a helpful message
                pass
        except ImportError:
            pass
    
    # Check if any processor is available (after last resort check)
    if not available_processors:
        st.error("❌ No image processors are available on this platform")
        
        # Check if Pillow can be installed
        try:
            import PIL
            pillow_available = True
        except ImportError:
            pillow_available = False
        
        if not pillow_available:
            st.warning("""
            ### 💡 Quick Fix: Install Pillow
            
            **Pillow is a lightweight image processing library** that works without system dependencies!
            
            Install it now:
            ```bash
            pip install pillow
            ```
            
            Then refresh this page. Pillow will work immediately for basic image processing.
            """)
        
        # Detect if we're on Streamlit Cloud
        is_streamlit_cloud = os.environ.get('STREAMLIT_SERVER_PORT') is not None or 'streamlit.app' in str(os.environ)
        
        if is_streamlit_cloud:
            st.info("""
            ### 🌐 Streamlit Cloud
            
            **Good news:** Pillow should work on Streamlit Cloud! It's already in `requirements.txt`.
            
            If Pillow isn't working, check that `pillow>=10.0.0` is in your `requirements.txt`.
            """)
        
        st.markdown("""
        ### 📚 Available Processors
        
        **Pillow (Recommended for Learning)** ⭐
        - ✅ Easy installation: `pip install pillow`
        - ✅ No system dependencies
        - ✅ Works immediately
        - ✅ Perfect for basic image operations
        - ⚠️ No geospatial data support
        
        **GDAL (Advanced Geospatial)**
        - ⚠️ Complex installation (system dependencies)
        - ✅ Full geospatial support
        - ✅ Professional workflows
        - ✅ 200+ format support
        """)
        
        with st.expander("📋 GDAL Installation (Optional - for geospatial features)", expanded=False):
            st.markdown("""
            **GDAL is optional!** You can use Pillow for basic operations.
            
            Only install GDAL if you need:
            - Geospatial coordinates
            - Projections
            - Advanced format support
            
            **For Local Installation (Fedora/RHEL):**
            ```bash
            sudo dnf install -y gcc-c++ make python3-devel gdal gdal-devel python3-gdal
            pip install gdal
            ```
            
            **For Local Installation (Ubuntu/Debian):**
            ```bash
            sudo apt-get update
            sudo apt-get install -y libgdal-dev gdal-bin python3-gdal
            pip install gdal
            ```
            
            **For macOS:**
            ```bash
            brew install gdal
            pip install gdal
            ```
            
            **For Docker Deployment:**
            See `Dockerfile` in the repository for a complete setup.
            """)
        
        # Show technical error if present
        if 'GDAL_ERROR' in locals() and GDAL_ERROR:
            st.divider()
            st.markdown("### 🔧 Technical Details")
            
            # Check if it's a module import error
            if "No module named 'terrascan'" in str(GDAL_ERROR):
                st.error("""
                **Module Import Error Detected**
                
                This usually means the Python path isn't set correctly. 
                
                **Quick Fix:**
                1. Make sure you're running from the project root directory
                2. Use one of these commands:
                
                ```bash
                # Option 1 (Easiest):
                streamlit run streamlit_app.py
                
                # Option 2:
                ./run_app.sh
                
                # Option 3:
                python run_app.py
                ```
                
                See `QUICK_FIX.md` or `TROUBLESHOOTING.md` for more details.
                """)
            else:
                st.code(f"Technical Error: {GDAL_ERROR}", language="python")
        
        # Show what the app can do
        st.divider()
        st.markdown("### ℹ️ App Status")
        
        # Check if Pillow is actually installed
        try:
            import PIL
            pillow_installed = True
        except ImportError:
            pillow_installed = False
        
        if pillow_installed and not pillow_available:
            st.warning("""
            ⚠️ **Pillow is installed but not detected!**
            
            This usually means there's a Python path issue. Try:
            1. Restart the app using: `streamlit run streamlit_app.py`
            2. Or check `TROUBLESHOOTING.md` for solutions
            """)
        elif pillow_installed:
            st.success("✅ Pillow is installed! The app should detect it automatically.")
            st.info("💡 If you still see this message, try restarting with: `streamlit run streamlit_app.py`")
        else:
            st.warning("⚠️ Install Pillow to enable image processing: `pip install pillow`")
            st.info("💡 Once Pillow is installed, refresh this page and you can start processing images!")
        
        return
    
    # Processor selection sidebar
    with st.sidebar:
        st.header("⚙️ Processor Settings")
        
        # Always show processor selection if multiple are available
        if PROCESSOR_MANAGER_AVAILABLE and len(available_processors) > 1:
            selected = st.selectbox(
                "Image Processor",
                options=['auto'] + available_processors,
                index=0,
                help="Select which library to use for image processing. 'auto' selects the best available."
            )
            st.session_state.selected_processor = selected
            
            # Show processor info
            if selected != 'auto':
                info = processor_info.get(selected, {})
                st.caption(f"**{selected.upper()}** - {'✅ Available' if info.get('available') else '❌ Not Available'}")
            else:
                default_proc = get_default_processor()
                if default_proc:
                    st.caption(f"**Auto-selected:** {default_proc.name.upper()}")
        elif len(available_processors) == 1:
            proc_name = available_processors[0].upper()
            st.info(f"✅ Using: **{proc_name}**")
            if proc_name.lower() == 'pillow':
                st.caption("💡 Pillow is perfect for basic image operations! Upload an image below to get started.")
            elif proc_name.lower() == 'gdal':
                st.caption("🌍 GDAL provides full geospatial capabilities including coordinates and projections!")
            st.session_state.selected_processor = available_processors[0]
        else:
            st.warning("No processors available")
        
        # Always show processor status section
        st.divider()
        st.markdown("### 📋 Processor Status")
        
        # Check all processors and show their status
        processor_status = {}
        
        # Check GDAL
        if PROCESSOR_MANAGER_AVAILABLE:
            processor_status['gdal'] = ProcessorManager.is_available('gdal')
            processor_status['rasterio'] = ProcessorManager.is_available('rasterio')
            processor_status['pillow'] = ProcessorManager.is_available('pillow')
        else:
            # Fallback check
            processor_status['gdal'] = GDAL_AVAILABLE and GDALImageProcessor is not None
            processor_status['rasterio'] = RASTERIO_AVAILABLE
            processor_status['pillow'] = PILLOW_AVAILABLE and PillowImageProcessor is not None
        
        # Display processor status
        for proc_name in ['gdal', 'rasterio', 'pillow']:
            is_available = processor_status.get(proc_name, False)
            status_icon = "✅" if is_available else "❌"
            status_text = "Available" if is_available else "Not Available"
            
            # Add descriptions
            descriptions = {
                'gdal': 'Full geospatial support, 200+ formats',
                'rasterio': 'Pythonic GDAL wrapper',
                'pillow': 'Lightweight, basic image operations'
            }
            
            with st.expander(f"{status_icon} **{proc_name.upper()}** - {status_text}", expanded=False):
                st.caption(descriptions.get(proc_name, ''))
                if proc_name == 'gdal' and not is_available:
                    st.info("💡 Install GDAL for geospatial features:\n```bash\n# macOS:\nbrew install gdal\npip install gdal\n\n# Ubuntu/Debian:\nsudo apt-get install libgdal-dev gdal-bin\npip install gdal\n```")
                elif proc_name == 'pillow' and not is_available:
                    st.info("💡 Install Pillow:\n```bash\npip install pillow\n```")
        
        # Show current selection
        if st.session_state.selected_processor:
            st.divider()
            current = st.session_state.selected_processor.upper()
            if current == 'AUTO':
                default_proc = get_default_processor() if PROCESSOR_MANAGER_AVAILABLE else None
                if default_proc:
                    st.caption(f"**Current:** Auto → {default_proc.name.upper()}")
                else:
                    st.caption(f"**Current:** Auto")
            else:
                st.caption(f"**Current:** {current}")
    
    # Show helpful message based on processor
    current_proc_name = available_processors[0] if available_processors else None
    if current_proc_name == 'pillow':
        st.success("🎉 **Pillow is ready!** Upload an image below to process it. All features work with Pillow!")
    else:
        st.markdown("Upload an image to view detailed information extracted using geospatial libraries")
    
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
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                "📊 Overview", 
                "🌍 Geospatial", 
                "🎨 Bands", 
                "📋 Metadata",
                "📈 Visualizations",
                "🔧 Operations",
                "💡 Use Cases",
                "⚙️ Advanced"
            ])
            
            # Tab 1: Overview
            with tab1:
                st.markdown("### Basic Information")
                
                # Display key metrics in columns
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(
                        "Width", 
                        f"{info['width']:,} px",
                        help="The number of pixels in the horizontal (X) direction. This represents the image width in pixels."
                    )
                    st.metric(
                        "Height", 
                        f"{info['height']:,} px",
                        help="The number of pixels in the vertical (Y) direction. This represents the image height in pixels."
                    )
                with col_b:
                    st.metric(
                        "Bands", 
                        info['bands'],
                        help="The number of spectral bands (channels) in the image. Common examples: 1 (grayscale), 3 (RGB), 4 (RGBA), or more for multispectral/hyperspectral imagery."
                    )
                    st.metric(
                        "Total Pixels", 
                        f"{info['width'] * info['height']:,}",
                        help="Total number of pixels in the image (Width × Height). This is the total data points in a single band."
                    )
                
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
                        st.metric(
                            "Origin X", 
                            f"{info['origin_x']:.6f}",
                            help="The X coordinate (longitude or easting) of the top-left corner of the image in the coordinate system. This is the geospatial reference point."
                        )
                        st.metric(
                            "Origin Y", 
                            f"{info['origin_y']:.6f}",
                            help="The Y coordinate (latitude or northing) of the top-left corner of the image in the coordinate system. This is the geospatial reference point."
                        )
                    with col_d:
                        st.metric(
                            "Pixel Width", 
                            f"{info['pixel_width']:.6f}",
                            help="The ground distance (in coordinate system units) that one pixel represents in the X direction. Positive values indicate eastward, negative indicates westward."
                        )
                        st.metric(
                            "Pixel Height", 
                            f"{info['pixel_height']:.6f}",
                            help="The ground distance (in coordinate system units) that one pixel represents in the Y direction. Usually negative (northward) in most coordinate systems."
                        )
                    
                    # Bounds
                    if 'bounds' in info:
                        st.divider()
                        st.markdown("#### Spatial Bounds")
                        bounds = info['bounds']
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            st.metric(
                                "Min X", 
                                f"{bounds['min_x']:.6f}",
                                help="The minimum (westernmost) X coordinate of the image extent. The left boundary of the image in the coordinate system."
                            )
                            st.metric(
                                "Min Y", 
                                f"{bounds['min_y']:.6f}",
                                help="The minimum (southernmost) Y coordinate of the image extent. The bottom boundary of the image in the coordinate system."
                            )
                        with col_b2:
                            st.metric(
                                "Max X", 
                                f"{bounds['max_x']:.6f}",
                                help="The maximum (easternmost) X coordinate of the image extent. The right boundary of the image in the coordinate system."
                            )
                            st.metric(
                                "Max Y", 
                                f"{bounds['max_y']:.6f}",
                                help="The maximum (northernmost) Y coordinate of the image extent. The top boundary of the image in the coordinate system."
                            )
                    
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
                            st.metric(
                                "Min", 
                                f"{band_info['min']:.2f}",
                                help="The minimum pixel value in this band. Represents the darkest/lowest value in the image data."
                            )
                        with col_f:
                            st.metric(
                                "Max", 
                                f"{band_info['max']:.2f}",
                                help="The maximum pixel value in this band. Represents the brightest/highest value in the image data."
                            )
                        with col_g:
                            st.metric(
                                "Mean", 
                                f"{band_info['mean']:.2f}",
                                help="The average (arithmetic mean) of all pixel values in this band. Indicates the overall brightness level of the image."
                            )
                        with col_h:
                            st.metric(
                                "Std Dev", 
                                f"{band_info['std_dev']:.2f}",
                                help="Standard deviation of pixel values. Measures the spread/variability of pixel values. Higher values indicate more contrast and variation in the image."
                            )
                        
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
                    processor = get_current_processor()
                    if processor is None:
                        st.error("No image processor available")
                    else:
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
                    processor = get_current_processor()
                    if processor is None:
                        st.error("No image processor available")
                    else:
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
                                        col_ndvi1, col_ndvi2, col_ndvi3 = st.columns(3)
                                        with col_ndvi1:
                                            st.metric(
                                                "NDVI Min", 
                                                f"{ndvi.min():.3f}",
                                                help="Minimum NDVI value. NDVI ranges from -1 to +1. Values near -1 indicate water or non-vegetated areas, values near +1 indicate dense healthy vegetation."
                                            )
                                        with col_ndvi2:
                                            st.metric(
                                                "NDVI Max", 
                                                f"{ndvi.max():.3f}",
                                                help="Maximum NDVI value. Higher values (closer to +1) indicate areas with the most healthy, dense vegetation in the image."
                                            )
                                        with col_ndvi3:
                                            st.metric(
                                                "NDVI Mean", 
                                                f"{ndvi.mean():.3f}",
                                                help="Average NDVI value across the entire image. Values > 0.3 typically indicate vegetation presence, > 0.6 indicates dense vegetation."
                                            )
                                        
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
                                    
                                    col_norm1, col_norm2, col_norm3 = st.columns(3)
                                    with col_norm1:
                                        st.metric(
                                            "Normalized Min", 
                                            f"{normalized.min():.2f}",
                                            help="Minimum value after normalization. For minmax: matches output_min. For zscore: may be negative (standard deviations below mean)."
                                        )
                                    with col_norm2:
                                        st.metric(
                                            "Normalized Max", 
                                            f"{normalized.max():.2f}",
                                            help="Maximum value after normalization. For minmax: matches output_max. For zscore: may be positive (standard deviations above mean)."
                                        )
                                    with col_norm3:
                                        st.metric(
                                            "Normalized Mean", 
                                            f"{normalized.mean():.2f}",
                                            help="Average value after normalization. For minmax: typically near the middle of output range. For zscore: should be near 0 (mean of standardized data)."
                                        )
                                    
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
            
            # Tab 7: Use Cases
            with tab7:
                st.markdown("### Common Use Cases & Examples")
                st.markdown("Explore practical applications and examples of image processing.")
                
                use_case_tabs = st.tabs([
                    "🌱 Agriculture & Vegetation",
                    "🏙️ Urban Planning",
                    "🌊 Water & Hydrology",
                    "🔥 Disaster Monitoring",
                    "📊 Scientific Analysis",
                    "🎨 Image Enhancement"
                ])
                
                with use_case_tabs[0]:
                    st.markdown("#### Agriculture & Vegetation Analysis")
                    st.markdown("""
                    **NDVI (Normalized Difference Vegetation Index)**
                    - Monitor crop health and growth
                    - Detect vegetation stress
                    - Estimate biomass
                    - Plan irrigation
                    
                    **How to use:**
                    1. Upload a multispectral image with Red and NIR bands
                    2. Go to Operations tab
                    3. Calculate NDVI
                    4. Values > 0.3 indicate vegetation, > 0.6 indicates healthy dense vegetation
                    """)
                    
                    if info['bands'] >= 2:
                        st.info("✅ This image has multiple bands - you can calculate NDVI in the Operations tab!")
                    else:
                        st.warning("⚠️ This image has only one band. NDVI requires at least Red and NIR bands.")
                
                with use_case_tabs[1]:
                    st.markdown("#### Urban Planning & Development")
                    st.markdown("""
                    **Applications:**
                    - Land use classification
                    - Building footprint detection
                    - Urban heat island analysis
                    - Infrastructure planning
                    - Population density estimation
                    
                    **Techniques:**
                    - Band combination for false-color visualization
                    - Normalization for comparison across time
                    - Statistical analysis of urban features
                    """)
                
                with use_case_tabs[2]:
                    st.markdown("#### Water & Hydrology")
                    st.markdown("""
                    **Applications:**
                    - Water body detection and mapping
                    - Flood monitoring
                    - Water quality assessment
                    - Wetland identification
                    - Coastal zone monitoring
                    
                    **Techniques:**
                    - Use NIR band for water detection (water absorbs NIR)
                    - Calculate water indices (NDWI)
                    - Monitor changes over time
                    """)
                
                with use_case_tabs[3]:
                    st.markdown("#### Disaster Monitoring")
                    st.markdown("""
                    **Applications:**
                    - Wildfire detection and monitoring
                    - Flood extent mapping
                    - Earthquake damage assessment
                    - Drought monitoring
                    - Landslide detection
                    
                    **Techniques:**
                    - Before/after comparison
                    - Change detection algorithms
                    - Rapid damage assessment
                    """)
                
                with use_case_tabs[4]:
                    st.markdown("#### Scientific Analysis")
                    st.markdown("""
                    **Applications:**
                    - Climate research
                    - Environmental monitoring
                    - Geological mapping
                    - Oceanography
                    - Atmospheric studies
                    
                    **Techniques:**
                    - Spectral analysis
                    - Time series analysis
                    - Statistical modeling
                    - Correlation analysis between bands
                    """)
                
                with use_case_tabs[5]:
                    st.markdown("#### Image Enhancement")
                    st.markdown("""
                    **Applications:**
                    - Improve image contrast
                    - Normalize for comparison
                    - Apply colormaps for visualization
                    - Format conversion
                    - Quality enhancement
                    
                    **Available Tools:**
                    - Band normalization (min-max, z-score)
                    - Colormap application
                    - Format conversion
                    - Histogram equalization (via visualizations)
                    """)
            
            # Tab 8: Advanced
            with tab8:
                st.markdown("### Technical Details")
                
                st.markdown("#### Driver Information")
                st.write(f"**Short Name:** {info['driver']}")
                if 'driver_long_name' in info:
                    st.write(f"**Long Name:** {info.get('driver_long_name', 'N/A')}")
                
                if info.get('description'):
                    st.divider()
                    st.markdown("#### Dataset Description")
                    st.write(info['description'])
                
                # Show processor information
                if st.session_state.current_processor:
                    st.divider()
                    st.markdown("#### Processor Information")
                    st.write(f"**Processor Used:** {st.session_state.current_processor.upper()}")
                    if PROCESSOR_MANAGER_AVAILABLE:
                        available = list_available_processors()
                        st.write(f"**Available Processors:** {', '.join([p.upper() for p in available])}")
                
                st.divider()
                st.markdown("#### Memory Information")
                total_size = info['width'] * info['height'] * info['bands']
                if 'band_info' in info and len(info['band_info']) > 0:
                    data_type_size = info['band_info'][0].get('data_type_size', 8)
                    estimated_size = (total_size * data_type_size) / (8 * 1024 * 1024)  # MB
                    st.metric(
                        "Estimated Size", 
                        f"{estimated_size:.2f} MB",
                        help="Estimated memory size required to load the entire image into memory. Calculated as: (Width × Height × Bands × DataTypeSize) / 8. This is the uncompressed size in memory."
                    )
                
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
                - **🔧 Operations**: Format conversion, colormaps, NDVI, normalization
                - **💡 Use Cases**: Practical applications and examples
                - **⚙️ Advanced**: Technical details and memory information
                """)


if __name__ == "__main__":
    main()
