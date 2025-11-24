"""
EEG Data Loaders

This module provides loaders for various EEG data formats, with primary support
for WFDB format used in the I-CARE challenge dataset.
"""

import os
from typing import Dict, List, Optional, Tuple

import pandas as pd


class EEGDataLoader:
    """
    Loader for EEG data in various formats.

    Primary support for WFDB format with extensibility for other formats.

    Parameters
    ----------
    data_folder : str
        Path to the root folder containing EEG data
    format : str, optional
        Data format ('wfdb', 'edf', 'bdf'). Default is 'wfdb'

    Examples
    --------
    >>> loader = EEGDataLoader(data_folder="path/to/data")
    >>> eeg_data, metadata = loader.load_patient("patient_001")
    >>> print(f"Loaded {eeg_data.shape[0]} samples from {eeg_data.shape[1]} channels")
    """

    def __init__(self, data_folder: str, file_format: str = "wfdb"):
        """Initialize the EEG data loader."""
        self.data_folder = data_folder
        self.file_format = file_format

        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"Data folder not found: {data_folder}")

    def find_patients(self) -> List[str]:
        """
        Find all patient IDs in the data folder.

        Returns
        -------
        List[str]
            List of patient identifiers
        """
        patient_ids = []
        for item in sorted(os.listdir(self.data_folder)):
            patient_folder = os.path.join(self.data_folder, item)
            if os.path.isdir(patient_folder):
                metadata_file = os.path.join(patient_folder, f"{item}.txt")
                if os.path.isfile(metadata_file):
                    patient_ids.append(item)
        return patient_ids

    def load_patient(self, patient_id: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Load EEG data and metadata for a specific patient.

        Parameters
        ----------
        patient_id : str
            Patient identifier

        Returns
        -------
        eeg_data : pd.DataFrame
            EEG signal data with channels as columns
        metadata : Dict
            Patient metadata including demographics and recording info

        Raises
        ------
        FileNotFoundError
            If patient data is not found
        """
        patient_folder = os.path.join(self.data_folder, patient_id)

        if not os.path.exists(patient_folder):
            raise FileNotFoundError(f"Patient folder not found: {patient_folder}")

        # Load metadata
        metadata = self._load_metadata(patient_folder, patient_id)

        # Load recording data
        recording_files = self._find_recording_files(patient_folder)
        eeg_data = self._load_recordings(recording_files)

        return eeg_data, metadata

    def load_recording(self, record_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Load a specific EEG recording file.

        Parameters
        ----------
        record_path : str
            Path to the recording file (without extension)

        Returns
        -------
        data : pd.DataFrame
            EEG signal data
        recording_metadata : Dict
            Recording-specific metadata (sampling rate, channels, etc.)
        """
        from chronoeeg.io.wfdb_reader import load_recording_data

        # Load WFDB data
        recording_data = load_recording_data(record_path)

        # Convert to DataFrame
        signals = recording_data["signals"]
        channels = recording_data["channels"]

        df = pd.DataFrame(signals, columns=channels)

        metadata = {
            "sampling_frequency": recording_data["sampling_frequency"],
            "num_samples": recording_data["num_samples"],
            "channels": channels,
            "record_name": recording_data["record_name"],
        }

        return df, metadata

    def _load_metadata(self, patient_folder: str, patient_id: str) -> Dict:
        """Load patient metadata from text file."""
        metadata_file = os.path.join(patient_folder, f"{patient_id}.txt")

        metadata = {}
        with open(metadata_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if ":" in line and line.startswith("#"):
                    key, value = line.split(":", 1)
                    key = key.strip("#").strip()
                    metadata[key] = value.strip()

        return metadata

    def _find_recording_files(self, patient_folder: str) -> List[str]:
        """Find all recording files for a patient."""
        record_names = set()

        for file_name in os.listdir(patient_folder):
            if file_name.endswith(".hea"):
                root, _ = os.path.splitext(file_name)
                # Extract record name from filename (e.g., 'patient_01_0001' from 'patient_01_0001_001.hea')
                record_name = "_".join(root.split("_")[:-1]) if "_" in root else root
                record_path = os.path.join(patient_folder, record_name)
                record_names.add(record_path)

        return sorted(list(record_names))

    def _load_recordings(self, recording_files: List[str]) -> pd.DataFrame:
        """Load multiple recording files and concatenate."""
        all_data = []

        for record_file in recording_files:
            data, _ = self.load_recording(record_file)
            all_data.append(data)

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()


class MultiDatasetLoader:
    """
    Loader that can handle multiple EEG datasets with different formats.

    This loader provides a unified interface for loading from different
    EEG databases (I-CARE, TUH, CHBMIT, etc.)

    Parameters
    ----------
    dataset_type : str
        Type of dataset ('icare', 'tuh', 'chbmit', 'custom')
    config : Dict, optional
        Dataset-specific configuration

    Examples
    --------
    >>> loader = MultiDatasetLoader(dataset_type='icare', config={'data_path': 'data/'})
    >>> patients = loader.get_patient_list()
    """

    def __init__(self, dataset_type: str, config: Optional[Dict] = None):
        """Initialize multi-dataset loader."""
        self.dataset_type = dataset_type
        self.config = config or {}

        # Initialize appropriate loader based on dataset type
        if dataset_type == "icare":
            self.loader = EEGDataLoader(
                data_folder=self.config.get("data_path", "./data"), file_format="wfdb"
            )
        else:
            raise NotImplementedError(f"Dataset type '{dataset_type}' not yet supported")

    def load(self, identifier: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Load data using dataset-specific identifier.

        Parameters
        ----------
        identifier : str
            Dataset-specific identifier (patient ID, record ID, etc.)

        Returns
        -------
        data : pd.DataFrame
            EEG signal data
        metadata : Dict
            Associated metadata
        """
        return self.loader.load_patient(identifier)

    def get_patient_list(self) -> List[str]:
        """Get list of all available patients/records."""
        return self.loader.find_patients()
