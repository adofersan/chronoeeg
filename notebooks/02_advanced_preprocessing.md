# Advanced Preprocessing with ChronoEEG

This notebook covers advanced preprocessing techniques including filtering, montage transformation, and artifact removal.

## Filtering

### Bandpass Filtering

```python
import chronoeeg as ceeg
import numpy as np
import pandas as pd

# Create sample data
np.random.seed(42)
data = pd.DataFrame(
    np.random.randn(12800, 6) * 50,  # 100 seconds at 128 Hz
    columns=['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4']
)

# Apply bandpass filter (0.5-40 Hz)
from chronoeeg.preprocessing.filters import SignalFilter

filter_obj = SignalFilter(
    lowcut=0.5,
    highcut=40.0,
    sampling_rate=128,
    filter_order=5
)

filtered_data = filter_obj.bandpass(data)
print(f"Filtered data shape: {filtered_data.shape}")
```

### Notch Filtering (Remove Power Line Noise)

```python
# Remove 50 Hz power line noise
filtered_data = filter_obj.notch(filtered_data, notch_freq=50.0)
print("Power line noise removed")
```

## Montage Transformation

### Bipolar Montage

```python
from chronoeeg.preprocessing.transforms import BipolarMontage

# Define bipolar pairs
montage = BipolarMontage(pairs=[
    ('Fp1', 'F3'),
    ('Fp2', 'F4'),
    ('F3', 'C3'),
    ('F4', 'C4'),
])

bipolar_data = montage.transform(data)
print(f"Bipolar montage shape: {bipolar_data.shape}")
print(f"Bipolar channels: {list(bipolar_data.columns)}")
```

## Advanced Epoching

### Overlapping Epochs

```python
# Create overlapping epochs (50% overlap)
epocher = ceeg.EpochExtractor(
    epoch_duration=300,  # 5 minutes
    sampling_rate=128,
    overlap=0.5  # 50% overlap
)

epochs = epocher.fit_transform(filtered_data)
print(f"Number of epochs with overlap: {epochs['epoch_id'].nunique()}")
```

### Custom Epoch Alignment

```python
from datetime import datetime

# Align epochs to specific times
start_time = datetime(2024, 1, 1, 0, 0, 0)

epocher_aligned = ceeg.EpochExtractor(
    epoch_duration=300,
    sampling_rate=128,
    start_time=start_time,
    align_to_clock=True  # Align to 00:00, 00:05, 00:10, etc.
)
```

## Quality-Based Filtering

```python
# Advanced quality assessment with custom thresholds
from chronoeeg.config import QualityConfig

quality_config = QualityConfig(
    nan_threshold=0.10,  # Stricter
    gap_threshold=0.05,
    outlier_threshold=0.03,
    flatline_threshold=0.02,
    sharpness_threshold=0.08,
    cohesion_threshold=0.75
)

# Create assessor with custom config
quality_assessor = ceeg.QualityAssessor(
    nan_threshold=quality_config.nan_threshold,
    gap_threshold=quality_config.gap_threshold,
)

quality_scores = quality_assessor.assess(epochs, epoch_column='epoch_id')

# Multi-level quality filtering
high_quality = quality_scores[quality_scores['overall_quality'] > 0.9]
medium_quality = quality_scores[
    (quality_scores['overall_quality'] > 0.7) & 
    (quality_scores['overall_quality'] <= 0.9)
]

print(f"High quality epochs: {len(high_quality)}")
print(f"Medium quality epochs: {len(medium_quality)}")
```

## Parallel Processing

```python
from chronoeeg.utils.parallel import ParallelProcessor

# Process multiple files in parallel
processor = ParallelProcessor(n_jobs=4, verbose=1)

def process_file(filepath):
    loader = ceeg.EEGDataLoader()
    data = loader.load_wfdb(filepath)
    epocher = ceeg.EpochExtractor(epoch_duration=300, sampling_rate=128)
    return epocher.fit_transform(data)

# Process multiple files
file_list = ['file1.hea', 'file2.hea', 'file3.hea']
results = processor.process_parallel(process_file, file_list)
```

## Saving Preprocessed Data

```python
# Save with metadata
metadata = {
    'sampling_rate': 128,
    'epoch_duration': 300,
    'filter_lowcut': 0.5,
    'filter_highcut': 40.0,
    'quality_threshold': 0.7,
}

# Save epochs
epochs.to_parquet('epochs_preprocessed.parquet')

# Save quality scores
quality_scores.to_csv('quality_scores.csv', index=False)

# Save metadata
import json
with open('metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

## Next Steps

- Feature extraction: `03_feature_engineering.ipynb`
- Machine learning: `04_machine_learning.ipynb`
