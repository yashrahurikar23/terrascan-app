# Terrascan Architecture: Multi-Library Image Processing

## 🎯 Design Goals

1. **Pluggable Processors** - Easy to add/remove image processing backends
2. **Unified Interface** - Same API regardless of underlying library
3. **Runtime Switching** - Switch between libraries without code changes
4. **Backward Compatible** - Existing code continues to work
5. **Extensible** - Easy to add new processors (Pillow, Xarray, etc.)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit App                        │
│                  (src/terrascan/app.py)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            Processor Manager (Factory)                  │
│         (src/terrascan/processors/manager.py)         │
│                                                         │
│  - get_processor(name) → Processor                      │
│  - list_available() → [names]                           │
│  - get_default() → Processor                           │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   GDAL       │ │  Rasterio    │ │   Pillow     │
│  Processor   │ │  Processor   │ │  Processor   │
│              │ │              │ │  (Future)    │
└──────────────┘ └──────────────┘ └──────────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Abstract Base      │
            │  Processor          │
            │  (Interface)        │
            └──────────────────────┘
```

---

## 📐 Component Design

### 1. Abstract Base Processor

**Location:** `src/terrascan/processors/base.py`

**Purpose:** Define the interface all processors must implement.

**Methods:**
```python
class BaseImageProcessor(ABC):
    @abstractmethod
    def open_image(file_path: str) -> Any
    
    @abstractmethod
    def get_image_info(dataset: Any) -> Dict[str, Any]
    
    @abstractmethod
    def read_band_as_array(dataset: Any, band: int) -> np.ndarray
    
    @abstractmethod
    def get_image_preview(dataset: Any, max_size: int) -> np.ndarray
    
    # ... all common methods
```

### 2. Concrete Processors

**GDAL Processor:** `src/terrascan/processors/gdal_processor.py`
- Implements BaseImageProcessor
- Wraps existing GDAL code
- Returns GDAL Dataset objects

**Rasterio Processor:** `src/terrascan/processors/rasterio_processor.py`
- Implements BaseImageProcessor
- Uses Rasterio library
- Returns Rasterio DatasetReader objects

**Future Processors:**
- Pillow Processor (basic image ops)
- Xarray Processor (scientific computing)

### 3. Processor Manager

**Location:** `src/terrascan/processors/manager.py`

**Purpose:** Factory pattern to get processors, handle availability.

**Methods:**
```python
class ProcessorManager:
    @staticmethod
    def get_processor(name: str = "auto") -> BaseImageProcessor
    
    @staticmethod
    def list_available() -> List[str]
    
    @staticmethod
    def get_default() -> BaseImageProcessor
```

### 4. Adapter Pattern

**Purpose:** Convert between different library's dataset objects to unified format.

**Location:** `src/terrascan/processors/adapters.py`

---

## 🔄 Data Flow

### Current Flow (GDAL only):
```
Upload → GDALImageProcessor → GDAL Dataset → Process → Display
```

### New Flow (Multi-library):
```
Upload → ProcessorManager → [GDAL|Rasterio|...] → Unified Interface → Process → Display
```

---

## 📋 Interface Specification

### BaseImageProcessor Interface

All processors must implement:

```python
class BaseImageProcessor(ABC):
    """Abstract base class for image processors."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return processor name."""
        pass
    
    @property
    @abstractmethod
    def available(self) -> bool:
        """Check if processor is available."""
        pass
    
    @abstractmethod
    def open_image(self, file_path: str) -> Any:
        """Open image file."""
        pass
    
    @abstractmethod
    def get_image_info(self, dataset: Any) -> Dict[str, Any]:
        """Extract image information."""
        pass
    
    @abstractmethod
    def read_band_as_array(self, dataset: Any, band_number: int) -> np.ndarray:
        """Read band as NumPy array."""
        pass
    
    @abstractmethod
    def get_image_preview(self, dataset: Any, max_size: int) -> np.ndarray:
        """Get preview image."""
        pass
    
    # ... all other methods
```

---

## 🔌 Plugin Registration

### Automatic Discovery

Processors are automatically discovered and registered:

```python
# In processors/__init__.py
PROCESSORS = {
    'gdal': GDALImageProcessor,
    'rasterio': RasterioImageProcessor,
    # Future: 'pillow': PillowImageProcessor,
}
```

### Priority Order

1. **Auto-detect** - Try processors in order of preference
2. **User selection** - Allow user to choose processor
3. **Fallback** - Use first available processor

---

## 🎛️ Configuration

### Environment Variables

```bash
TERRASCAN_PROCESSOR=gdal  # or rasterio, auto
TERRASCAN_PROCESSOR_PRIORITY=gdal,rasterio,pillow
```

### Runtime Selection

```python
# In Streamlit app
processor = ProcessorManager.get_processor("rasterio")
# or
processor = ProcessorManager.get_processor("auto")  # Auto-detect
```

---

## 🔄 Migration Strategy

### Phase 1: Add Architecture (No Breaking Changes)
1. Create BaseImageProcessor
2. Refactor GDAL processor to implement interface
3. Create ProcessorManager
4. Update app to use manager (backward compatible)

### Phase 2: Add Rasterio
1. Create RasterioImageProcessor
2. Register in manager
3. Test switching between processors

### Phase 3: Enhance
1. Add processor selection UI
2. Add performance comparison
3. Add fallback mechanisms

---

## 📊 Benefits

1. **Flexibility** - Switch libraries without code changes
2. **Extensibility** - Easy to add new processors
3. **Testing** - Test with different backends
4. **Performance** - Choose best library for task
5. **Reliability** - Fallback if one library fails

---

## 🔒 Backward Compatibility

- Existing code using `GDALImageProcessor` still works
- Manager provides `get_processor("gdal")` for explicit use
- Default behavior unchanged (uses GDAL if available)

---

## 🚀 Future Extensions

1. **Pillow Processor** - For basic image operations
2. **Xarray Processor** - For scientific computing
3. **Hybrid Processing** - Use multiple processors for different operations
4. **Performance Metrics** - Compare processor performance
5. **Caching Layer** - Cache results across processors

---

## 📝 Implementation Checklist

- [ ] Create BaseImageProcessor abstract class
- [ ] Refactor GDAL processor to implement interface
- [ ] Create Rasterio processor
- [ ] Create ProcessorManager
- [ ] Update app to use manager
- [ ] Add processor selection UI
- [ ] Add tests for each processor
- [ ] Update documentation

---

## 🎯 Success Criteria

1. ✅ Can switch between GDAL and Rasterio
2. ✅ No breaking changes to existing code
3. ✅ Easy to add new processors
4. ✅ Unified interface across processors
5. ✅ Graceful fallback if library unavailable
