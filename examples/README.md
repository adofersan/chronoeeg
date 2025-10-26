# ChronoEEG Examples

This directory contains example scripts demonstrating various features of ChronoEEG.

## Available Examples

### 1. complete_workflow.py

Comprehensive example showing:
- Synthetic EEG data generation
- Pipeline-based analysis
- Manual step-by-step analysis
- Configuration management
- Feature extraction

Run with:
```bash
python examples/complete_workflow.py
```

### 2. Quick Start Examples

#### Load and Epoch Data

```python
import chronoeeg as ceeg

# Load WFDB data
loader = ceeg.EEGDataLoader(sampling_rate=128)
data = loader.load_wfdb("path/to/record")

# Extract 5-minute epochs
epocher = ceeg.EpochExtractor(epoch_duration=300, sampling_rate=128)
epochs = epocher.fit_transform(data)
```

#### Quality Assessment

```python
# Assess quality
assessor = ceeg.QualityAssessor(
    nan_threshold=0.15,
    gap_threshold=0.10,
)
quality = assessor.assess(epochs, epoch_column='epoch_id')

# Filter good epochs
good_epochs = quality[quality['passes_threshold']]
print(f"Good epochs: {len(good_epochs)}/{len(quality)}")
```

#### Feature Extraction

```python
# Extract classical features
classical_extractor = ceeg.ClassicalFeatureExtractor(sampling_rate=128)
features = classical_extractor.extract(epoch_data)

# Extract FMM features
fmm_extractor = ceeg.FMMFeatureExtractor(n_components=10, sampling_rate=128)
fmm_features = fmm_extractor.extract(epoch_data)
```

#### Complete Pipeline

```python
# One-line analysis
pipeline = ceeg.EEGAnalysisPipeline(
    epoch_duration=300,
    sampling_rate=128,
    quality_threshold=0.7,
    extract_classical=True,
    extract_fmm=True,
)

results = pipeline.process(data)
```

## Coming Soon

- Real dataset examples
- Machine learning integration
- Visualization examples
- Advanced preprocessing
- Multi-file processing

## Need Help?

- Check the [documentation](https://chronoeeg.readthedocs.io)
- See [notebooks](../notebooks/) for interactive examples
- Open an [issue](https://github.com/yourusername/chronoeeg/issues)
