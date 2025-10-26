"""
Example: Complete EEG Analysis Workflow

This script demonstrates a complete end-to-end workflow for EEG analysis
using ChronoEEG.
"""

import chronoeeg as ceeg
import numpy as np
import pandas as pd

# Set up logging
logger = ceeg.setup_logger(level="INFO")

logger.info("="*60)
logger.info("ChronoEEG - Complete Workflow Example")
logger.info("="*60)


def create_synthetic_eeg(duration_minutes=20, sampling_rate=128, n_channels=6):
    """
    Create synthetic EEG data for demonstration.
    
    Parameters
    ----------
    duration_minutes : int
        Duration in minutes
    sampling_rate : int
        Sampling rate in Hz
    n_channels : int
        Number of EEG channels
        
    Returns
    -------
    pd.DataFrame
        Synthetic EEG data
    """
    logger.info(f"Generating {duration_minutes} min of synthetic EEG data...")
    
    np.random.seed(42)
    n_samples = sampling_rate * 60 * duration_minutes
    time = np.arange(n_samples) / sampling_rate
    
    data = np.zeros((n_samples, n_channels))
    
    for i in range(n_channels):
        # Delta (1-4 Hz) - deep sleep
        data[:, i] += 25 * np.sin(2 * np.pi * 2 * time)
        
        # Theta (4-8 Hz) - drowsiness
        data[:, i] += 20 * np.sin(2 * np.pi * 6 * time)
        
        # Alpha (8-13 Hz) - relaxed, eyes closed
        data[:, i] += 35 * np.sin(2 * np.pi * 10 * time)
        
        # Beta (13-30 Hz) - active thinking
        data[:, i] += 15 * np.sin(2 * np.pi * 18 * time)
        
        # Gamma (30-40 Hz) - high cognitive function
        data[:, i] += 8 * np.sin(2 * np.pi * 35 * time)
        
        # Add realistic noise
        data[:, i] += np.random.randn(n_samples) * 8
    
    # Standard 10-20 system channel names
    channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4'][:n_channels]
    df = pd.DataFrame(data, columns=channels)
    
    logger.info(f"✓ Created {df.shape[0]} samples × {df.shape[1]} channels")
    return df


def analyze_eeg_pipeline(data):
    """
    Run complete EEG analysis using pipeline.
    
    Parameters
    ----------
    data : pd.DataFrame
        Raw EEG data
        
    Returns
    -------
    dict
        Analysis results
    """
    logger.info("\n" + "="*60)
    logger.info("Running EEG Analysis Pipeline")
    logger.info("="*60)
    
    # Create pipeline with custom parameters
    pipeline = ceeg.EEGAnalysisPipeline(
        epoch_duration=300,  # 5-minute epochs
        sampling_rate=128,
        quality_threshold=0.7,
        extract_classical=True,
        extract_fmm=True,
        n_fmm_components=10,
    )
    
    # Process data
    logger.info("\nProcessing data through pipeline...")
    results = pipeline.process(data)
    
    # Summary statistics
    n_epochs = results['epochs']['epoch_id'].nunique()
    n_good = results['quality']['passes_threshold'].sum()
    avg_quality = results['quality']['overall_quality'].mean()
    n_features = results['features'].shape[1]
    
    logger.info("\n📊 Pipeline Results:")
    logger.info(f"  - Total epochs extracted: {n_epochs}")
    logger.info(f"  - Good quality epochs: {n_good} ({n_good/n_epochs*100:.1f}%)")
    logger.info(f"  - Average quality score: {avg_quality:.3f}")
    logger.info(f"  - Total features extracted: {n_features}")
    
    return results


def analyze_eeg_manual(data):
    """
    Run EEG analysis step-by-step manually.
    
    Parameters
    ----------
    data : pd.DataFrame
        Raw EEG data
        
    Returns
    -------
    dict
        Analysis results
    """
    logger.info("\n" + "="*60)
    logger.info("Running Manual Step-by-Step Analysis")
    logger.info("="*60)
    
    # Step 1: Epoch extraction
    logger.info("\n1️⃣  Extracting epochs...")
    epocher = ceeg.EpochExtractor(
        epoch_duration=300,
        sampling_rate=128,
        overlap=0.0
    )
    epochs = epocher.fit_transform(data)
    logger.info(f"   ✓ Extracted {epochs['epoch_id'].nunique()} epochs")
    
    # Step 2: Quality assessment
    logger.info("\n2️⃣  Assessing quality...")
    assessor = ceeg.QualityAssessor(
        nan_threshold=0.15,
        gap_threshold=0.10,
        outlier_threshold=0.05,
    )
    quality = assessor.assess(epochs, epoch_column='epoch_id')
    
    good_epochs = quality[quality['passes_threshold']]
    logger.info(f"   ✓ {len(good_epochs)}/{len(quality)} epochs passed quality checks")
    
    # Step 3: Feature extraction on first good epoch
    logger.info("\n3️⃣  Extracting features from first good epoch...")
    
    first_good_id = good_epochs.iloc[0]['epoch_id']
    epoch_data = epochs[epochs['epoch_id'] == first_good_id].drop('epoch_id', axis=1)
    
    # Classical features
    classical_extractor = ceeg.ClassicalFeatureExtractor(sampling_rate=128)
    classical_features = classical_extractor.extract(epoch_data)
    logger.info(f"   ✓ Extracted {len(classical_features.columns)} classical features")
    
    # FMM features
    fmm_extractor = ceeg.FMMFeatureExtractor(n_components=10, sampling_rate=128)
    fmm_features = fmm_extractor.extract(epoch_data)
    logger.info(f"   ✓ Extracted {len(fmm_features)} FMM components")
    
    # Combine features
    combined_features = pd.concat([classical_features, fmm_features], axis=1)
    
    return {
        'epochs': epochs,
        'quality': quality,
        'classical_features': classical_features,
        'fmm_features': fmm_features,
        'combined_features': combined_features,
    }


def demonstrate_configuration():
    """Demonstrate configuration management."""
    logger.info("\n" + "="*60)
    logger.info("Configuration Management Demo")
    logger.info("="*60)
    
    # Get default config
    config = ceeg.get_config()
    logger.info("\n📋 Default Configuration:")
    logger.info(f"  - Sampling rate: {config.preprocessing.sampling_rate} Hz")
    logger.info(f"  - Epoch duration: {config.preprocessing.epoch_duration} s")
    logger.info(f"  - Quality NaN threshold: {config.quality.nan_threshold}")
    logger.info(f"  - FMM components: {config.features.n_components}")
    
    # Create custom config
    custom_config = ceeg.ChronoEEGConfig()
    custom_config.preprocessing.sampling_rate = 256
    custom_config.quality.nan_threshold = 0.20
    custom_config.features.n_components = 15
    
    logger.info("\n⚙️  Custom Configuration:")
    logger.info(f"  - Sampling rate: {custom_config.preprocessing.sampling_rate} Hz")
    logger.info(f"  - Quality NaN threshold: {custom_config.quality.nan_threshold}")
    logger.info(f"  - FMM components: {custom_config.features.n_components}")


def main():
    """Run complete example workflow."""
    
    # 1. Create synthetic data
    data = create_synthetic_eeg(duration_minutes=20)
    
    # 2. Run pipeline analysis
    pipeline_results = analyze_eeg_pipeline(data)
    
    # 3. Run manual analysis
    manual_results = analyze_eeg_manual(data)
    
    # 4. Demonstrate configuration
    demonstrate_configuration()
    
    # 5. Summary
    logger.info("\n" + "="*60)
    logger.info("✅ Workflow Complete!")
    logger.info("="*60)
    logger.info("\nNext steps:")
    logger.info("  1. Try with your own EEG data")
    logger.info("  2. Customize quality thresholds")
    logger.info("  3. Experiment with FMM components")
    logger.info("  4. Build ML models with extracted features")
    logger.info("\n📚 Documentation: https://chronoeeg.readthedocs.io")
    logger.info("🐛 Issues: https://github.com/yourusername/chronoeeg/issues")
    

if __name__ == "__main__":
    main()
