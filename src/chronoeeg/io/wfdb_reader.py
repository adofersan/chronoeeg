"""
WFDB Format Reader

This module contains functions for reading EEG data in WFDB format,
adapted from the I-CARE challenge helper code.
"""

import os
import numpy as np
from typing import Dict


def load_recording_data(record_name: str, check_values: bool = False) -> Dict:
    """
    Load WFDB recording data.
    
    Parameters
    ----------
    record_name : str
        Path to the record (with or without .hea extension)
    check_values : bool, optional
        Whether to verify checksums. Default is False
    
    Returns
    -------
    Dict
        Dictionary containing:
        - 'record_name': str
        - 'num_signals': int
        - 'sampling_frequency': float
        - 'num_samples': int
        - 'signals': np.ndarray (num_samples x num_signals)
        - 'channels': List[str]
        - 'gains': List[float]
        - 'baselines': List[float]
    
    Raises
    ------
    FileNotFoundError
        If the header file is not found
    ValueError
        If multiple signal files are referenced or format is invalid
    """
    # Allow either the record name or the header filename
    _root, ext = os.path.splitext(record_name)
    if ext == '':
        header_file = record_name + '.hea'
    else:
        header_file = record_name
    
    # Load the header file
    if not os.path.isfile(header_file):
        raise FileNotFoundError(f'{record_name} recording not found.')
    
    with open(header_file, 'r', encoding='utf-8') as f:
        header = [l.strip() for l in f.readlines() if l.strip()]
    
    # Parse the header file
    record_name = None
    num_signals = None
    sampling_frequency = None
    num_samples = None
    signal_files = []
    gains = []
    baselines = []
    adc_zeros = []
    channels = []
    initial_values = []
    checksums = []
    
    for i, l in enumerate(header):
        arrs = [arr.strip() for arr in l.split(' ')]
        # Parse the record line
        if i == 0:
            record_name = arrs[0]
            num_signals = int(arrs[1])
            sampling_frequency = float(arrs[2])
            num_samples = int(arrs[3])
        # Parse the signal specification lines
        elif not l.startswith('#') and len(l.strip()) > 0:
            signal_file = arrs[0]
            if '(' in arrs[2] and ')' in arrs[2]:
                gain = float(arrs[2].split('/')[0].split('(')[0])
                baseline = float(arrs[2].split('/')[0].split('(')[1].split(')')[0])
            else:
                gain = float(arrs[2].split('/')[0])
                baseline = 0.0
            adc_zero = int(arrs[4])
            initial_value = int(arrs[5])
            checksum = int(arrs[6])
            channel = arrs[8]
            signal_files.append(signal_file)
            gains.append(gain)
            baselines.append(baseline)
            adc_zeros.append(adc_zero)
            initial_values.append(initial_value)
            checksums.append(checksum)
            channels.append(channel)
    
    # Check that the header file only references one signal file
    num_signal_files = len(set(signal_files))
    if num_signal_files != 1:
        raise ValueError(
            f'The header file {header_file} references {num_signal_files} '
            'signal files; one signal file expected.'
        )
    
    # Load the signal file
    head, _tail = os.path.split(header_file)
    signal_file = os.path.join(head, list(set(signal_files))[0])
    
    signals = np.fromfile(signal_file, dtype=np.int16).reshape(-1, num_signals)
    
    # Convert to physical units
    for i in range(num_signals):
        signals[:, i] = (signals[:, i] - baselines[i] - adc_zeros[i]) / gains[i]
    
    # Verify checksums if requested
    if check_values:
        for i in range(num_signals):
            if np.sum(signals[:, i]) != checksums[i]:
                raise ValueError(f'Checksum failed for channel {channels[i]}')
    
    return {
        'record_name': os.path.splitext(os.path.basename(header_file))[0],
        'num_signals': num_signals,
        'sampling_frequency': sampling_frequency,
        'num_samples': num_samples,
        'signals': signals,
        'channels': channels,
        'gains': gains,
        'baselines': baselines,
    }


def get_variable(string: str, variable_name: str, variable_type):
    """
    Extract a variable from metadata string.
    
    Parameters
    ----------
    string : str
        Full metadata text
    variable_name : str
        Name of the variable to extract (e.g., '#Age')
    variable_type : type
        Type to convert the value to
    
    Returns
    -------
    variable_type
        Extracted and converted value
    """
    for line in string.split('\n'):
        if line.startswith(variable_name):
            value = line.split(':')[1].strip()
            if variable_type == bool:
                return value == 'True'
            else:
                return variable_type(value)
    return None
