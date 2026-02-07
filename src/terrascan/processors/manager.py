"""
Processor Manager

Factory pattern for managing and selecting image processors.
Allows switching between different image processing libraries (GDAL, Rasterio, etc.)
without changing application code.
"""

from typing import Optional, List, Dict
import os

from terrascan.processors.base import BaseImageProcessor

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


class ProcessorManager:
    """
    Manager for image processors.
    
    Handles processor registration, availability checking, and selection.
    Supports automatic processor selection based on availability and priority.
    """
    
    # Processor registry
    _PROCESSORS: Dict[str, type] = {}
    _AVAILABILITY: Dict[str, bool] = {}
    
    # Default priority order (first available will be used)
    # Pillow is lightweight and always available, so it's a good fallback
    DEFAULT_PRIORITY = ['gdal', 'rasterio', 'pillow']
    
    @classmethod
    def _register_processors(cls):
        """Register all available processors."""
        if GDAL_AVAILABLE and GDALImageProcessor:
            cls._PROCESSORS['gdal'] = GDALImageProcessor
            instance = GDALImageProcessor()
            cls._AVAILABILITY['gdal'] = instance.available
        
        if RASTERIO_AVAILABLE and RasterioImageProcessor:
            cls._PROCESSORS['rasterio'] = RasterioImageProcessor
            instance = RasterioImageProcessor()
            cls._AVAILABILITY['rasterio'] = instance.available
        
        if PILLOW_AVAILABLE and PillowImageProcessor:
            cls._PROCESSORS['pillow'] = PillowImageProcessor
            instance = PillowImageProcessor()
            cls._AVAILABILITY['pillow'] = instance.available
    
    @classmethod
    def list_available(cls) -> List[str]:
        """
        List all available processors.
        
        Returns:
            List of processor names that are available
        """
        cls._register_processors()
        return [name for name, available in cls._AVAILABILITY.items() if available]
    
    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all registered processors (regardless of availability).
        
        Returns:
            List of all processor names
        """
        cls._register_processors()
        return list(cls._PROCESSORS.keys())
    
    @classmethod
    def is_available(cls, name: str) -> bool:
        """
        Check if a specific processor is available.
        
        Args:
            name: Processor name (e.g., 'gdal', 'rasterio')
            
        Returns:
            True if processor is available, False otherwise
        """
        cls._register_processors()
        return cls._AVAILABILITY.get(name, False)
    
    @classmethod
    def get_processor(cls, name: Optional[str] = None) -> Optional[BaseImageProcessor]:
        """
        Get a processor instance.
        
        Args:
            name: Processor name ('gdal', 'rasterio', 'auto', or None)
                 - 'auto' or None: Automatically select first available processor
                 - Specific name: Get that specific processor
        
        Returns:
            Processor instance or None if not available
        """
        cls._register_processors()
        
        # Auto-select if not specified
        if name is None or name == 'auto':
            return cls.get_default()
        
        # Get specific processor
        name_lower = name.lower()
        if name_lower not in cls._PROCESSORS:
            return None
        
        processor_class = cls._PROCESSORS[name_lower]
        instance = processor_class()
        
        if not instance.available:
            return None
        
        return instance
    
    @classmethod
    def get_default(cls) -> Optional[BaseImageProcessor]:
        """
        Get the default processor (first available in priority order).
        
        Returns:
            Default processor instance or None if none available
        """
        cls._register_processors()
        
        # Check environment variable for priority
        priority = os.environ.get('TERRASCAN_PROCESSOR_PRIORITY', ','.join(cls.DEFAULT_PRIORITY))
        priority_list = [p.strip() for p in priority.split(',')]
        
        # Try processors in priority order
        for processor_name in priority_list:
            if cls.is_available(processor_name):
                processor_class = cls._PROCESSORS[processor_name]
                return processor_class()
        
        # Fallback: try any available processor
        for processor_name in cls._PROCESSORS.keys():
            if cls.is_available(processor_name):
                processor_class = cls._PROCESSORS[processor_name]
                return processor_class()
        
        return None
    
    @classmethod
    def get_processor_info(cls) -> Dict[str, Dict[str, any]]:
        """
        Get information about all processors.
        
        Returns:
            Dictionary mapping processor names to their info
        """
        cls._register_processors()
        
        info = {}
        for name, processor_class in cls._PROCESSORS.items():
            instance = processor_class()
            info[name] = {
                'name': instance.name,
                'available': instance.available,
                'class': processor_class.__name__
            }
        
        return info


# Convenience functions
def get_processor(name: Optional[str] = None) -> Optional[BaseImageProcessor]:
    """Get a processor instance (convenience function)."""
    return ProcessorManager.get_processor(name)


def get_default_processor() -> Optional[BaseImageProcessor]:
    """Get the default processor (convenience function)."""
    return ProcessorManager.get_default()


def list_available_processors() -> List[str]:
    """List available processors (convenience function)."""
    return ProcessorManager.list_available()
