# Project Structure

This document describes the organization of the Terrascan project.

## Directory Structure

```
terrascan-app/
├── README.md                 # Main project README
├── LICENSE                   # License file
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── vercel.json               # Vercel deployment config
├── streamlit_app.py          # Entry point for Streamlit app
│
├── src/                      # Source code
│   ├── terrascan/           # Main package
│   │   ├── __init__.py       # Package initialization
│   │   ├── app.py            # Streamlit application
│   │   ├── processors/       # Image processing backends
│   │   │   ├── __init__.py
│   │   │   └── gdal_processor.py  # GDAL processor
│   │   ├── utils/            # Utility functions
│   │   │   └── __init__.py
│   │   └── visualizations/   # Visualization functions
│   │       └── __init__.py
│   └── examples/             # Example scripts
│       ├── __init__.py
│       ├── gdal_example.py
│       └── rasterio_example.py
│
├── docs/                     # Documentation
│   ├── learning/             # Learning resources
│   │   ├── README.md
│   │   ├── LEARNING_PLAN.md
│   │   ├── QUICK_START.md
│   │   └── 01_fundamentals/  # Phase-by-phase guides
│   │   └── ...
│   ├── deployment/           # Deployment guides
│   │   ├── DEPLOYMENT_OPTIONS.md
│   │   ├── STREAMLIT_CLOUD_DEPLOY.md
│   │   └── ...
│   ├── installation/        # Installation guides
│   │   ├── INSTALL_GDAL.md
│   │   └── QUICK_INSTALL.md
│   └── guides/               # Feature guides
│       ├── GDAL_TUTORIAL_FEATURES.md
│       └── LIBRARY_RECOMMENDATIONS.md
│
├── scripts/                  # Utility scripts
│   └── install_gdal.sh       # GDAL installation script
│
└── tests/                    # Test files (future)
```

## Package Structure

### `src/terrascan/`

The main package containing all application code.

- **`app.py`** - Main Streamlit application
- **`processors/`** - Image processing backends
  - `gdal_processor.py` - GDAL-based processor
  - Future: `rasterio_processor.py` - Rasterio-based processor
- **`utils/`** - Common utility functions
- **`visualizations/`** - Visualization helpers

### Import Structure

```python
# Main package
from terrascan import GDALImageProcessor

# Processors
from terrascan.processors import GDALImageProcessor, GDAL_AVAILABLE

# App
from terrascan.app import main
```

## Running the Application

### Development

```bash
# Using the entry point
streamlit run streamlit_app.py

# Or directly
streamlit run src/terrascan/app.py
```

### Docker

```bash
docker-compose up
```

## Adding New Features

### Adding a New Processor

1. Create file in `src/terrascan/processors/`
2. Implement processor class
3. Update `processors/__init__.py` to export it
4. Update main `__init__.py` if needed

### Adding New Utilities

1. Create file in `src/terrascan/utils/`
2. Add functions/classes
3. Update `utils/__init__.py` to export

### Adding Documentation

1. Place in appropriate `docs/` subdirectory
2. Update relevant README files
3. Link from main README if important

## Best Practices

1. **Keep code modular** - Separate concerns into different modules
2. **Use type hints** - Help with IDE support and documentation
3. **Document functions** - Docstrings for all public functions
4. **Follow PEP 8** - Python style guide
5. **Test your code** - Add tests in `tests/` directory (future)

## Future Improvements

- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Add CI/CD pipeline
- [ ] Add pre-commit hooks
- [ ] Add type checking (mypy)
- [ ] Add code formatting (black)
- [ ] Add linting (ruff/flake8)
