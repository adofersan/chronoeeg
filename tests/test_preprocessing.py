"""
Tests for Epoch Extraction

Ensures correct segmentation of continuous EEG data into fixed-length epochs.
"""

import pytest
import numpy as np
import pandas as pd
from datetime import time
from chronoeeg.preprocessing import EpochExtractor, EpochValidator


class TestEpochExtractor:
    """Tests for EpochExtractor class."""
    
    def test_initialization(self):
        """Test epoch extractor initialization."""
        extractor = EpochExtractor(epoch_length=300, sampling_rate=128)
        
        assert extractor.epoch_length == 300
        assert extractor.sampling_rate == 128
        assert extractor.samples_per_epoch == 300 * 128
    
    def test_extract_basic(self, sample_eeg_data, sample_metadata):
        """Test basic epoch extraction."""
        extractor = EpochExtractor(epoch_length=60, sampling_rate=128)  # 1-minute epochs
        
        epochs = extractor.extract(sample_eeg_data, sample_metadata)
        
        assert len(epochs) >= 1
        assert all('data' in epoch for epoch in epochs)
        assert all('start_time' in epoch for epoch in epochs)
        assert all('end_time' in epoch for epoch in epochs)
    
    def test_extract_no_metadata(self, sample_eeg_data):
        """Test epoch extraction without metadata."""
        extractor = EpochExtractor(epoch_length=60, sampling_rate=128)
        
        epochs = extractor.extract(sample_eeg_data, metadata=None)
        
        assert len(epochs) >= 1
    
    def test_epoch_data_shape(self, sample_eeg_data, sample_metadata):
        """Test that extracted epochs have correct shape."""
        extractor = EpochExtractor(epoch_length=10, sampling_rate=128)  # 10-second epochs
        
        epochs = extractor.extract(sample_eeg_data, sample_metadata)
        
        if epochs:
            expected_samples = 10 * 128
            # Allow some tolerance for the last epoch
            assert all(
                abs(len(epoch['data']) - expected_samples) <= 1
                for epoch in epochs
            )
    
    def test_time_parsing(self):
        """Test time string parsing."""
        extractor = EpochExtractor()
        
        parsed = extractor._parse_time("10:30:45")
        assert parsed == time(10, 30, 45)
        
        parsed_none = extractor._parse_time(None)
        assert parsed_none is None


class TestEpochValidator:
    """Tests for EpochValidator class."""
    
    def test_validate_valid_epoch(self, sample_epoch):
        """Test validation of valid epoch."""
        validator = EpochValidator(min_valid_ratio=0.5)
        
        is_valid, message = validator.validate_epoch(sample_epoch)
        
        assert is_valid
        assert "Valid" in message
    
    def test_validate_empty_epoch(self):
        """Test validation of empty epoch."""
        validator = EpochValidator()
        
        empty_epoch = {
            'data': pd.DataFrame(),
            'start_time': time(10, 0, 0),
            'end_time': time(10, 0, 10)
        }
        
        is_valid, message = validator.validate_epoch(empty_epoch)
        
        assert not is_valid
        assert "empty" in message.lower()
    
    def test_validate_low_quality_epoch(self, sample_epoch):
        """Test validation of epoch with too many NaNs."""
        validator = EpochValidator(min_valid_ratio=0.9)
        
        # Add many NaNs
        epoch = sample_epoch.copy()
        data = epoch['data'].copy()
        mask = np.random.rand(*data.shape) < 0.5
        epoch['data'] = data.mask(mask)
        
        is_valid, message = validator.validate_epoch(epoch)
        
        assert not is_valid
        assert "Insufficient" in message
