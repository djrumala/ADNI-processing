"""
Configuration and constants for ADNI data processing.
"""

from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
TEMP_META_DIR = BASE_DIR / "TempMeta"
TEMP_DATA_DIR = BASE_DIR / "TempData"

# Source directories
DICOM_DIR = BASE_DIR / "DICOM"
RAW_DATA_DIR = BASE_DIR / "3T"
PREPROCESSED_OLD_DIR = BASE_DIR / "preprocessed_old"
PREPROCESSED_ADDITION_DIR = BASE_DIR / "preprocessed_addition"

# Target directories
PREPROCESSED_DIR = BASE_DIR / "preprocessed"
CONVERT_DIR = BASE_DIR / "2convert"
CONVERTED_DIR = BASE_DIR / "Converted"
FINAL_DIR = BASE_DIR / "final"

# MRI sequences and conditions
SEQUENCES = ["T1", "T2"]
CONDITIONS = ["AD", "CN", "MCI"]
TESLA_STRENGTHS = [1.5, 3]

# File patterns
DICOM_PATTERN = "**/*.dcm"
NIFTI_PATTERN = "**/*.nii"
NIFTI_GZ_PATTERN = "**/*.nii.gz"
PREPROCESSED_PATTERN = "**/wm*.nii"

# Filename delimiters
FILENAME_DIVIDERS = {
    "raw": "raw_",
    "br": "br_",
    "Br": "Br_"
}

# Metadata column names
METADATA_COLUMNS = [
    "Image Data ID",
    "Subject",
    "Group",
    "Sex",
    "Age",
    "Visit",
    "Modality",
    "Description",
    "Type",
    "Acq Date",
    "Format"
]

# Default parameters
DEFAULT_TESLA = 3
DEFAULT_DIVIDER = "raw_"
DEFAULT_FORMAT = "Br_"

# Logging
LOG_DIR = OUTPUT_DIR / "logs"
LOG_FILE = LOG_DIR / "processing.log"
