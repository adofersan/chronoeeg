# Notebooks Directory

## Overview

This directory contains **exploratory notebooks and prototype code** that served as inspiration for the main ChronoEEG library. These files represent the original research and development work.

## ⚠️ Important Notice

**These notebooks are NOT part of the distributed package.** They are kept in the repository for reference and development purposes only.

The production-ready, cleaned, and refactored code is located in:
- `src/chronoeeg/` - Main package code
- `examples/` - Working examples using the package

## Contents

### Jupyter Notebooks
- `01_epoch_calculation_TODOFIX.ipynb` - Early epoch calculation experiments
- `02_epoch_quality_extraction.ipynb` - Quality metric development
- `03_feature_extraction.ipynb` - Feature extraction prototypes
- `04_epoch_quality_analysis.ipynb` - Quality analysis research
- `05_modelling.ipynb` - ML modeling experiments

### Python Files (Prototype Code)
- `helper_code.py` - Helper functions from I-CARE challenge
- `team_code.py` - Original challenge submission code
- `ClassicalFeatureExtractor.py` - Prototype classical features
- `FMMFeatureExtractor.py` - Prototype FMM features
- `segment_quality_evaluation.py` - Quality evaluation prototypes
- `utils.py` - Miscellaneous utilities

### Configuration & Data
- `sweep.yaml` - Hyperparameter sweep configuration
- `scores_24h.csv` - Sample scoring data

## Usage

### To Use the Production Package

Instead of using these notebooks directly, use the cleaned package:

```python
# Install the package
pip install -e .

# Use the production code
import chronoeeg as ceeg

# Load data
loader = ceeg.EEGDataLoader(data_folder="path/to/data")

# Extract features
extractor = ceeg.ClassicalFeatureExtractor(sampling_rate=128)
features = extractor.extract(eeg_data)
```

### For Development Reference

These notebooks can be used to:
1. Understand the original research process
2. Compare prototype implementations with production code
3. Extract ideas for new features
4. Reference original data analysis workflows

## Migration Notes

The code in these notebooks has been refactored and incorporated into the main package with the following improvements:

1. ✅ **Proper modular structure** - Separated concerns into io, preprocessing, features, quality, etc.
2. ✅ **Type hints and documentation** - Added comprehensive docstrings and type annotations
3. ✅ **Error handling** - Robust exception handling throughout
4. ✅ **Testing** - Unit tests in `tests/` directory
5. ✅ **Configuration** - Centralized configuration system
6. ✅ **Logging** - Professional logging infrastructure
7. ✅ **Code quality** - Linted, formatted, and follows best practices

## Not Included in Package Distribution

As specified in `MANIFEST.in`, these notebooks are excluded from the package distribution to keep the installed package clean and focused on production code.
