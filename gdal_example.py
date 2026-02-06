"""
GDAL Python Example - Basic Image Processing Operations

This script demonstrates common GDAL operations using Python bindings.
"""

from osgeo import gdal
from osgeo import osr
import numpy as np


def open_image(filename):
    """Open a raster image file using GDAL."""
    dataset = gdal.Open(filename)
    if dataset is None:
        raise ValueError(f"Could not open file: {filename}")
    return dataset


def get_image_info(dataset):
    """Extract basic information from a GDAL dataset."""
    print("Image Information:")
    print(f"  Driver: {dataset.GetDriver().ShortName}")
    print(f"  Size: {dataset.RasterXSize} x {dataset.RasterYSize}")
    print(f"  Number of bands: {dataset.RasterCount}")
    
    # Get geospatial information
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        print(f"  Origin: ({geotransform[0]}, {geotransform[3]})")
        print(f"  Pixel size: ({geotransform[1]}, {geotransform[5]})")
    
    # Get projection
    projection = dataset.GetProjection()
    if projection:
        srs = osr.SpatialReference()
        srs.ImportFromWkt(projection)
        print(f"  Projection: {srs.GetAttrValue('PROJCS') or srs.GetAttrValue('GEOGCS')}")
    
    return {
        'width': dataset.RasterXSize,
        'height': dataset.RasterYSize,
        'bands': dataset.RasterCount,
        'geotransform': geotransform,
        'projection': projection
    }


def read_band_as_array(dataset, band_number=1):
    """Read a specific band from the dataset as a NumPy array."""
    band = dataset.GetRasterBand(band_number)
    array = band.ReadAsArray()
    print(f"\nBand {band_number} Statistics:")
    print(f"  Min: {array.min()}")
    print(f"  Max: {array.max()}")
    print(f"  Mean: {array.mean():.2f}")
    print(f"  Data type: {gdal.GetDataTypeName(band.DataType)}")
    return array


def create_output_image(output_filename, template_dataset, data_array, driver_name='GTiff'):
    """Create a new image file based on a template dataset."""
    driver = gdal.GetDriverByName(driver_name)
    
    # Get template information
    xsize = template_dataset.RasterXSize
    ysize = template_dataset.RasterYSize
    
    # Create output dataset
    out_dataset = driver.Create(output_filename, xsize, ysize, 1, gdal.GDT_Float32)
    
    # Copy geotransform and projection from template
    out_dataset.SetGeoTransform(template_dataset.GetGeoTransform())
    out_dataset.SetProjection(template_dataset.GetProjection())
    
    # Write data to band
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(data_array)
    out_band.FlushCache()
    
    print(f"\nOutput image created: {output_filename}")
    return out_dataset


def convert_image(input_file, output_file, output_format='GTiff'):
    """Convert an image from one format to another."""
    input_ds = gdal.Open(input_file)
    if input_ds is None:
        raise ValueError(f"Could not open input file: {input_file}")
    
    driver = gdal.GetDriverByName(output_format)
    output_ds = driver.CreateCopy(output_file, input_ds, 0)
    
    if output_ds is None:
        raise ValueError(f"Could not create output file: {output_file}")
    
    print(f"Converted {input_file} to {output_file}")
    return output_ds


def main():
    """Example usage of GDAL functions."""
    print("GDAL Python Example")
    print("=" * 50)
    
    # Example: Open and read an image
    # Replace 'your_image.tif' with your actual image file
    example_file = 'example.tif'
    
    try:
        # Open the dataset
        dataset = open_image(example_file)
        
        # Get image information
        info = get_image_info(dataset)
        
        # Read first band as array
        if dataset.RasterCount > 0:
            band_array = read_band_as_array(dataset, 1)
            
            # Example: Create a processed version (e.g., normalize)
            normalized = (band_array - band_array.min()) / (band_array.max() - band_array.min())
            
            # Save processed image
            create_output_image('output_normalized.tif', dataset, normalized)
        
        # Close dataset
        dataset = None
        print("\nProcessing complete!")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Make sure you have a valid image file to process.")
        print("GDAL supports many formats: GeoTIFF, JPEG, PNG, NetCDF, HDF, etc.")


if __name__ == "__main__":
    main()
