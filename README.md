# ⏰ ChronoEEG: Advanced Multidimensional EEG Analysis Toolkit

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> A professional, modular Python library for comprehensive multidimensional EEG signal analysis, featuring advanced quality assessment, feature extraction, and machine learning capabilities.

---

## 🌟 Features

### 🔍 **Signal Quality Assessment**
- **Multi-metric Quality Evaluation**: NaN detection, gap analysis, outlier detection, flatline detection, sharpness analysis, and phase-locking cohesion
- **Automated Quality Scoring**: Per-segment quality metrics with customizable thresholds
- **Robustness**: Handles missing data, artifacts, and multi-channel inconsistencies

### 📊 **Feature Extraction**

#### Classical Features
- **Entropy Measures**: Permutation entropy, spectral entropy, SVD entropy
- **Fractal Dimensions**: Higuchi, Petrosian, and Katz fractal dimensions
- **Spectral Features**: Power spectral density across delta, theta, alpha, beta, and gamma bands
- **Statistical Aggregations**: Channel-wise and global statistics

#### Frequency Modulated Möbius (FMM)
- **Advanced Decomposition**: Phase-amplitude coupling analysis via Möbius transformations
- **Multi-component Extraction**: Automatic detection of oscillatory components in the complex plane
- **R² Quality Metrics**: Per-component variance explained
- **Frequency Analysis**: Time-frequency representation with adaptive resolution

### ⏱️ **Epoch Management**
- **Flexible Segmentation**: Configurable epoch lengths (default: 5-minute windows)
- **Time-aware Processing**: Handles multi-hour recordings with temporal metadata
- **Batch Processing**: Parallel processing support for large datasets

### 🤖 **Machine Learning Integration**
- **Scikit-learn Compatible**: Drop-in compatibility with sklearn pipelines
- **Custom Estimators**: Patient-level averaging, cross-validation strategies
- **Feature Selection**: Built-in feature importance and selection tools

---

## 📦 Installation

### From PyPI (recommended)
```bash
pip install chronoeeg
```

### From Source
```bash
git clone https://github.com/adofersan/chronoeeg.git
cd chronoeeg
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev]"
```

### Docker Installation
```bash
docker pull chronoeeg/chronoeeg:latest
docker run -it -v $(pwd)/data:/data chronoeeg/chronoeeg:latest
```

---

## 🚀 Quick Start

### Basic Usage

```python
from chronoeeg.io import EEGDataLoader
from chronoeeg.preprocessing import EpochExtractor
from chronoeeg.quality import QualityAssessor
from chronoeeg.features import ClassicalFeatureExtractor, FMMFeatureExtractor

# Load EEG data
loader = EEGDataLoader(data_folder="path/to/data")
eeg_data, metadata = loader.load_patient("patient_001")

# Extract 5-minute epochs
epoch_extractor = EpochExtractor(epoch_duration=300, sampling_rate=128)
epochs = epoch_extractor.extract(eeg_data, metadata)

# Assess signal quality
quality_assessor = QualityAssessor()
quality_scores = quality_assessor.assess_epochs(epochs)

# Extract classical features
classical_extractor = ClassicalFeatureExtractor(sampling_rate=128)
classical_features = classical_extractor.extract(epochs[0]['data'])

# Extract FMM features
fmm_extractor = FMMFeatureExtractor(n_components=10, sampling_rate=128)
fmm_features = fmm_extractor.extract(epochs[0]['data'])

print(f"Quality Score: {quality_scores[0]['overall_quality']:.2f}%")
print(f"Classical Features Shape: {classical_features.shape}")
print(f"FMM Components: {fmm_features.shape[0]}")
```

### Advanced Pipeline

```python
from chronoeeg.pipeline import EEGAnalysisPipeline
from sklearn.ensemble import RandomForestClassifier

# Create end-to-end pipeline
pipeline = EEGAnalysisPipeline(
    epoch_duration=300,
    sampling_rate=128,
    quality_threshold=70,  # Filter low-quality epochs
    feature_types=['classical', 'fmm'],
    n_fmm_components=10
)

# Process entire dataset
results = pipeline.fit_transform(
    data_folder="path/to/data",
    labels="path/to/labels.csv"
)

# Train classifier
X_train, y_train = results['features'], results['labels']
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
```

---

## 📊 Visualization Examples

### Quality Assessment Visualization
```python
from chronoeeg.visualization import plot_quality_metrics, plot_signal

# Plot quality metrics
plot_quality_metrics(quality_scores)

# Plot EEG signal
plot_signal(eeg_data, sampling_rate=128)
```

![Quality Dashboard Example](docs/images/quality_dashboard.png)

### Feature Visualization
```python
from chronoeeg.visualization import plot_feature_importance, plot_fmm_components

# Plot feature importance
plot_feature_importance(feature_importance, feature_names)

# Plot FMM components
plot_fmm_components(fmm_components, sampling_rate=128)
```

![Feature Importance Example](docs/images/feature_importance.png)

---

## 🧪 Testing

Run the full test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src/chronoeeg --cov-report=html
```

Run specific tests:
```bash
pytest tests/test_features.py -v
```

---

## 📚 Documentation

Full documentation is available at [https://chronoeeg.readthedocs.io](https://chronoeeg.readthedocs.io)

### Building Documentation Locally
```bash
cd docs
make html
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

#### Local Development
```bash
# Clone repository
git clone https://github.com/adofersan/chronoeeg.git
cd chronoeeg

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

#### Docker Development
```bash
# Build the Docker image
docker-compose build

# Run tests in Docker
docker-compose run --rm chronoeeg pytest

# Start Jupyter server
docker-compose up jupyter
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Based on research from the I-CARE challenge dataset
- Inspired by MNE-Python for EEG processing
- FMM implementation adapted from signal processing literature

---

## 📧 Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [@adofersan](https://github.com/adofersan)

---

## 🗺️ Roadmap

- [ ] Support for additional EEG file formats (EDF, BDF)
- [ ] Real-time streaming analysis capabilities
- [ ] GPU-accelerated feature extraction
- [ ] Pre-trained models for common EEG tasks
- [ ] Interactive web-based visualization dashboard
- [ ] Integration with deep learning frameworks (PyTorch, TensorFlow)

---

## 📊 Citation

If you use this library in your research, please cite:

```bibtex
@software{chronoeeg2025,
  author = {Adolfo Santamónica},
  title = {TODO},
  year = {2025},
  url = {https://github.com/adofersan/chronoeeg}
}
```

---

<div align="center">
  Made with ❤️ for the neuroscience community
</div>
