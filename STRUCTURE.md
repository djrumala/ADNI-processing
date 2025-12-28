# ADNI Data Processing Python Package"""














































































































































































































































































































































































- Documented workflow pipeline- Comprehensive logging and configuration- Modular architecture with 5 main scripts- Converted from Jupyter notebooks**v1.0.0** - Initial Python package structure## Version History---```pip install pandas```bashInstall dependencies:- shutil (included in Python standard library)- pathlib (included in Python 3.4+)- pandas- Python 3.6+## Requirements---4. Access organized data in structured directories3. Check logs in `outputs/logs/`2. Run scripts from `scripts/` directory1. Keep original notebooks as referenceTo use this new structure:- Logging integrated throughout- Configuration centralized in `config.py`- Workflow orchestrated through command-line scripts- Functions extracted into modular Python files- Original notebooks in root directory (reference)This codebase was extracted from Jupyter notebooks:## Converting from Notebook to Python Module---✅ **Tracked**: Metadata tracking throughout pipeline✅ **Logged**: Comprehensive logging of all operations✅ **Documented**: Docstrings and inline comments✅ **Testable**: Individual functions can be unit tested✅ **Maintainable**: Clean separation of concerns✅ **Scalable**: Easy to add new processing steps✅ **Modular**: Reusable functions across different scripts## Advantages of This Structure---- Logging settings- Metadata column names- Default Tesla field strength- File patterns and delimiters- Input/output directoriesEdit `src/config.py` to customize:## Configuration---```2024-12-29 10:15:45,456 - move_preprocessed_files - INFO - Completed Move Preprocessed Files in 21.57s2024-12-29 10:15:45,123 - move_preprocessed_files - INFO - Total T1w-AD data is 145 and not preprocessed is 52024-12-29 10:15:23,789 - move_preprocessed_files - INFO - Loaded metadata with 150 records2024-12-29 10:15:23,456 - move_preprocessed_files - INFO - Starting: Move Preprocessed Files```Example log:- Both file and console output- Includes timestamps, operation details, and error messages- File format: `{step_name}_{timestamp}.log`**Log files** are automatically generated in `outputs/logs/`:## Logging---```    └── ...└── T2/│   └── ...│   │   └── ...│   │   ├── 0-wm{filename}.nii│   ├── AD/├── T1/final/    └── ...└── T2/│   └── ...│   │   └── 002_S_0456-S29097-I41125/{dicom_files}│   │   ├── 002_S_0001-S29096-I41124/{dicom_files}│   ├── AD/├── T1/TempData/    └── MCI/    ├── CN/    ├── AD/└── T2/│   └── MCI/│   ├── CN/│   │   └── 1-wm{filename}.nii│   │   ├── 0-wm{filename}.nii│   ├── AD/├── T1/preprocessed/```### Organized File Structure- `TempMeta/HoldOut_Balanced_T1w_AD_3T.csv` - Hold-out dataset metadata- `TempMeta/To-Be-Preprocessed_T1w_AD.csv` - Unprocessed files list- `TempMeta/Balanced_Meta_T1w_AD.csv` - Balanced T1 AD metadata### Metadata CSVs Generated## Output Files & Logs---```    --pattern "**/*wm*.nii"    --target ./final \    --source ./processed \    --seq T1 --cond AD \python scripts/move_final_files.py \# Move T1 files using custom pattern```bash### Example 3: Custom File Movement```done    python scripts/run_pipeline.py --seq T2 --cond $cond --step allfor cond in AD CN MCI; do# Process all T2 groupsdone    python scripts/run_pipeline.py --seq T1 --cond $cond --step allfor cond in AD CN MCI; do# Process all T1 groups```bash### Example 2: Complete Pipeline for All Groups```python scripts/move_to_convert.py --seq T1 --cond AD# Step 3: Move DICOM for conversionpython scripts/move_to_preprocess.py --seq T1 --cond AD# Step 2: Move unprocessed files to preprocessing queue  python scripts/move_preprocessed_files.py --seq T1 --cond AD# Step 1: Move old preprocessed filescd ADNI-processing# Process T1 Alzheimer's Disease group```bash### Example 1: Process Single Sequence & Condition## Usage Examples---- **Output**: `{metadata-index}-{original_filename}.nii`- **Preprocessed**: `wm{original_filename}.nii` (white matter segmented)- **Original**: `ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii`**File Naming Conventions**:```Example: 002_S_0001-S29096-I41124{subject-id}-{series-id}-{image-id}```**Subject-Series-Image Directory**:### Directory Naming Conventions## Data Organization Strategy---- `ProcessingLogger`: Context manager for step logging- `setup_logging()`: Initialize logging configurationLogging utilities:### `src/logging.py`- `freemove()`: Flexible file movement with pattern matching- `move2separate()`: Separate data for robustness evaluation- `moveConverted()`: Move converted NIfTI files- `move2convert()`: Move DICOM files for conversion- `move2preprocess()`: Move raw files to preprocessing queue- `movePreprocessed()`: Move preprocessed files & track unprocessedFile organization functions:### `src/file_operations.py`- `mergeMetadata()`: Combine multiple metadata DataFrames- `filterMetadata()`: Filter metadata by criteria- `exportCSV()`: Export metadata dictionaries to CSV- `createMetaCombinedString()`: Generate combined ID strings for matchingMetadata utilities:### `src/metadata.py`- Default parameters- File patterns and delimiters- Sequences and conditions- Directory paths (inputs, outputs, temporary)Global configuration and constants:### `src/config.py`## Module Reference---```--target-path PATH          # Output path for final files--source-path PATH          # Path to processed files--old-path PATH             # Path to old preprocessed files--step {all|step_name}      # Which step to run--cond {AD, CN, MCI}        # Condition (required)--seq {T1, T2}              # MRI sequence (required)```**Options**:```python scripts/run_pipeline.py --seq T1 --cond AD --step move_preprocessed```bash**Run specific step**:```python scripts/run_pipeline.py --seq T1 --cond AD --step all```bash**Run all steps at once**:## Master Pipeline Orchestrator---- Final files: `./final/{seq}/{cond}/{index}-{filename}.nii`**Outputs**:- Pattern: `**/*wm*.nii` (default: white matter segmented files)- Processed files: `./processed/{seq}/{cond}/`**Inputs**:- Organizes files by sequence and condition- Customizable glob patterns for file selection- `freemove()`: Flexible file movement based on pattern matching**Functions**:```    --source ./processed --target ./final --pattern "**/*wm*.nii"python scripts/move_final_files.py --seq T1 --cond AD \```bash**Purpose**: Move converted/preprocessed files to final output location### Step 4: Move Final Preprocessed Files---- Organized DICOM: `./2convert/{seq}/{cond}/{subject}-{series}_{image}/`**Outputs**:- DICOM files: `./DICOM/{seq}/{cond}/`- Balanced metadata CSV: `TempMeta/Balanced_Meta_{seq}w_{cond}.csv`**Inputs**:- Handles metadata-based file matching- Creates structure: `./2convert/{seq}/{cond}/{subject}-{series}_{image}/`- `move2convert()`: Organizes DICOM files for conversion**Functions**:```python scripts/move_to_convert.py --seq T1 --cond AD```bash**Purpose**: Prepare DICOM files for DICOM-to-NIfTI conversion### Step 3: Move DICOM Files for Conversion---- Organized files: `./TempData/{seq}/{cond}/{subject}-{series}-{image}/`**Outputs**:- Raw files: `./3T/{seq}/`- Unprocessed metadata: `TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv`**Inputs**:- Matches files using metadata- Creates organized subdirectories: `{subject-id}-{series-id}-{image-id}`- `move2preprocess()`: Moves raw NIFTI files to preprocessing queue**Functions**:```python scripts/move_to_preprocess.py --seq T1 --cond AD```bash**Purpose**: Organize raw files for Windows-based preprocessing (SPM/MATLAB)### Step 2: Move Files to Preprocessing Queue---- Unprocessed list: `TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv`- Preprocessed files: `./preprocessed/{seq}/{cond}/`**Outputs**:- Source files: `./preprocessed_old/{seq}/{cond}/`- Balanced metadata CSV: `TempMeta/Balanced_Meta_{seq}w_{cond}.csv`**Inputs**:- Exports to-be-preprocessed list as CSV- Generates metadata for unprocessed files- `movePreprocessed()`: Moves preprocessed files (`wm*.nii`) from source to target**Functions**:```python scripts/move_preprocessed_files.py --seq T1 --cond AD --path ./preprocessed_old```bash**Purpose**: Collect and organize previously preprocessed files from archive folders### Step 1: Move Preprocessed Files## Processing Pipeline Steps```└── STRUCTURE.md                     # This file├── README.md                        # Project documentation├── data_matching.ipynb              # Original notebook (reference)├── data_clean.ipynb                 # Original notebook (reference)├── data_final_move.ipynb            # Original notebook (reference)│├── final/                           # Final organized output├── preprocessed/                    # Final preprocessed NIfTI files├── TempData/                        # Temporary data storage├── TempMeta/                        # Metadata CSVs││   └── logs/                        # Processing execution logs├── outputs/                         # Output & results││   └── run_pipeline.py              # Master pipeline orchestrator│   ├── move_final_files.py          # Step 4: Move final processed files│   ├── move_to_convert.py           # Step 3: Move DICOM for conversion│   ├── move_to_preprocess.py        # Step 2: Move files to preprocessing queue│   ├── move_preprocessed_files.py   # Step 1: Move old preprocessed files├── scripts/                         # Executable workflows││   └── utils.py                     # General utilities│   ├── logging.py                   # Logging utilities│   ├── file_operations.py           # File operations & moving│   ├── metadata.py                  # Metadata utilities│   ├── config.py                    # Configuration & constants│   ├── __init__.py                  # Package initialization├── src/                              # Core package modulesADNI-processing/```This repository has been converted from Jupyter Notebook format to a clean, modular Python codebase.## Project Structure OverviewADNI Data Processing Project

A Python-based pipeline for processing ADNI MRI datasets.
Handles data cleaning, organization, and preprocessing workflows.

Project Structure:
    src/                      # Core package modules
        __init__.py           # Package initialization
        config.py             # Configuration and constants
        metadata.py           # Metadata utilities
        file_operations.py    # File moving/organization functions
        logging.py            # Logging utilities
    
    scripts/                  # Executable scripts
        move_preprocessed_files.py    # Move already preprocessed files
        move_to_preprocess.py         # Move files to preprocessing queue
        move_to_convert.py            # Move DICOM files for conversion
        move_final_files.py           # Move final processed files
        run_pipeline.py               # Master workflow orchestrator
    
    outputs/                  # Output directory for results and logs
        logs/                 # Processing logs
    
    TempMeta/                 # Temporary metadata CSVs
    TempData/                 # Temporary data storage
    preprocessed/             # Final preprocessed files
    final/                    # Final organized output

Quick Start:
    1. Move preprocessed files:
       python scripts/move_preprocessed_files.py --seq T1 --cond AD
    
    2. Move files to preprocessing queue:
       python scripts/move_to_preprocess.py --seq T1 --cond AD
    
    3. Move final processed files:
       python scripts/move_final_files.py --seq T1 --cond AD --source ./processed --target ./final
    
    4. Run complete pipeline:
       python scripts/run_pipeline.py --seq T1 --cond AD --step all

Functions:
    - movePreprocessed()    : Move preprocessed files from source to target
    - move2preprocess()     : Move raw files to preprocessing queue
    - move2convert()        : Move DICOM files for conversion
    - moveConverted()       : Move converted NIfTI files
    - move2separate()       : Separate and organize data
    - freemove()            : Flexible file movement with pattern matching
    - exportCSV()           : Export metadata to CSV
    - createMetaCombinedString() : Generate combined ID strings

Author: DEWINDA
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "DEWINDA"
