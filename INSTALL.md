# ChronoEEG Setup and Installation Guide

## Quick Start

### 1. Local Installation

```bash
# Navigate to the package directory
cd chronoeeg

# Install in development mode
pip install -e .

# Or install with all optional dependencies
pip install -e ".[dev,viz,docs]"
```

### 2. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chronoeeg --cov-report=html

# Run specific test file
pytest tests/test_preprocessing.py -v
```

### 3. Docker Usage

```bash
# Build the Docker image
docker-compose build

# Run tests in Docker
docker-compose run --rm chronoeeg-test

# Start Jupyter Lab server
docker-compose up jupyter
# Then open http://localhost:8888 in your browser

# Run interactive Python session
docker-compose run --rm chronoeeg python
```

## Package Structure

```
chronoeeg/
├── src/chronoeeg/          # Main package source
│   ├── io/                 # Data loading (WFDB, custom formats)
│   ├── preprocessing/      # Epoching, filtering, transforms
│   ├── quality/            # Signal quality assessment
│   ├── features/           # Classical & FMM feature extraction
│   ├── pipeline/           # End-to-end analysis pipelines
│   └── utils/              # Utilities
├── tests/                  # Unit and integration tests
├── notebooks/              # Example notebooks
├── docs/                   # Documentation (Sphinx)
├── docker/                 # Docker configuration
└── scripts/                # Utility scripts
```

## Basic Usage Examples

### Example 1: Load and Process Single Patient

```python
from chronoeeg.io import EEGDataLoader
from chronoeeg.preprocessing import EpochExtractor
from chronoeeg.quality import QualityAssessor

# Load data
loader = EEGDataLoader("path/to/data")
eeg_data, metadata = loader.load_patient("patient_001")

# Extract 5-minute epochs
extractor = EpochExtractor(epoch_length=300, sampling_rate=128)
epochs = extractor.extract(eeg_data, metadata)

# Assess quality
assessor = QualityAssessor(sampling_rate=128)
for epoch in epochs:
    quality = assessor.assess(epoch['data'])
    print(f"Epoch {epoch['epoch_number']}: {quality['overall_quality']:.2f}%")
```

### Example 2: Extract Features

```python
from chronoeeg.features import ClassicalFeatureExtractor, FMMFeatureExtractor

# Extract classical features
classical = ClassicalFeatureExtractor(sampling_rate=128)
classical_features = classical.extract(epochs[0]['data'])
print(f"Classical features: {classical_features.shape}")

# Extract FMM features
fmm = FMMFeatureExtractor(n_components=10, sampling_rate=128)
fmm_features = fmm.extract(epochs[0]['data'])
print(f"FMM components: {len(fmm_features)}")
```

### Example 3: Complete Pipeline

```python
from chronoeeg.pipeline import EEGAnalysisPipeline

# Create pipeline
pipeline = EEGAnalysisPipeline(
    epoch_length=300,
    sampling_rate=128,
    quality_threshold=70,
    feature_types=['classical', 'fmm'],
    n_fmm_components=10
)

# Process entire dataset
results = pipeline.fit_transform(
    data_folder="path/to/data",
    labels_file="path/to/labels.csv"
)

# Access results
X_train = results['features']
y_train = results['labels']
quality_scores = results['quality']
```

## Building for PyPI

### 1. Update Version

Edit `pyproject.toml` and update version number:

```toml
[project]
name = "chronoeeg"
version = "0.1.1"  # Increment version
```

### 2. Build Distribution

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check distribution
twine check dist/*
```

### 3. Upload to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Then upload to PyPI
twine upload dist/*
```

### 4. Install from PyPI

```bash
pip install chronoeeg
```

## Development Workflow

### 1. Code Style

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

### 2. Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### 3. Documentation

```bash
# Build docs
cd docs
make html

# View docs
open _build/html/index.html
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure package is installed: `pip install -e .`
2. **Missing dependencies**: Install all deps: `pip install -e ".[dev]"`
3. **Test failures**: Check Python version (requires 3.8+)

### Getting Help

- GitHub Issues: https://github.com/yourusername/chronoeeg/issues
- Documentation: https://chronoeeg.readthedocs.io
- Email: your.email@example.com

## Next Steps

1. Read the full documentation
2. Try the example notebooks in `notebooks/`
3. Run the test suite to verify installation
4. Start analyzing your own EEG data!
