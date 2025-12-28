# ADNI Data Processing - Complete Technical Structure

This document provides comprehensive technical reference for the refactored ADNI processing codebase. For user-facing documentation, see [README.md](README.md). For quick start instructions, see [QUICKSTART.md](QUICKSTART.md).

## 🗂️ Directory Structure

```
ADNI-processing/
├── src/                              # Core Python package
│   ├── __init__.py                  # Package initialization
│   ├── config.py                    # Global configuration & constants
│   ├── metadata.py                  # Metadata utilities & CSV handling
│   ├── file_operations.py           # Core file movement functions (6 functions)
│   ├── logging.py                   # Logging utilities
│   └── utils.py                     # Helper utilities
│
├── scripts/                          # Executable entry points
│   ├── run_pipeline.py              # Master orchestrator script
│   ├── move_preprocessed_files.py   # Move archived preprocessed data
│   ├── move_to_preprocess.py        # Queue files for preprocessing
│   ├── move_to_convert.py           # Queue DICOM for conversion
│   ├── move_final_files.py          # Move final processed files
│   └── check_status.py              # Pipeline status checker
│
├── outputs/                          # Runtime outputs
│   └── logs/                        # Timestamped execution logs
│
├── TempMeta/                        # Metadata CSVs (user-provided)
├── TempData/                        # Temporary organized files
├── preprocessed/                    # SPM-preprocessed files
├── final/                           # Final output files
│
└── Documentation Files
    ├── README.md                    # Main project documentation
    ├── QUICKSTART.md                # Getting started guide
    ├── STRUCTURE.md                 # This file
    ├── PIPELINE_ARCHITECTURE.md     # Visual diagrams
    ├── REFACTORING_SUMMARY.md       # What changed
    └── INDEX.md                     # Documentation index
```

---

## 📦 Core Modules (`src/`)

### `config.py` - Configuration & Constants

**Purpose**: Centralized configuration for all paths, patterns, and settings.

**Key Variables**:
```python
# Directory paths
INPUT_DIR = "./3T"                      # Raw NIfTI input directory
DICOM_DIR = "./DICOM"                  # Raw DICOM input directory
TEMP_META_DIR = "./TempMeta"            # Metadata CSV directory
TEMP_DATA_DIR = "./TempData"            # Intermediate organized files
PREPROCESSED_DIR = "./preprocessed"     # SPM-preprocessed output
FINAL_DIR = "./final"                   # Final output directory
CONVERT_DIR = "./2convert"              # DICOM conversion queue

# Sequences and conditions
SEQUENCES = ["T1", "T2"]                # MRI sequences
CONDITIONS = ["AD", "CN", "MCI"]        # Patient conditions
TESLA_STRENGTH = 3                      # Tesla strength (3T)

# File patterns & delimiters
FILE_DELIMITERS = {
    "raw_": "Raw files prefix",
    "br_": "Processed files prefix",
    "wm": "White matter segmented files"
}

# Metadata columns
META_COLUMNS = {
    "subject_id": str,
    "visit_id": str,
    "series_id": str,
    "image_id": str,
    "filename": str,
    ...
}

# Logging configuration
LOG_DIR = "./outputs/logs"
LOG_LEVEL = logging.INFO
LOG_FORMAT = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
```

**When to modify**: Adjust directory paths for your system, change file patterns, or update metadata column definitions.

---

### `metadata.py` - Metadata Utilities

**Purpose**: Handle CSV loading, validation, and manipulation.

**Key Functions**:

```python
def load_metadata(filepath: str) -> pd.DataFrame
    """Load and validate metadata CSV."""
    # Returns: DataFrame with metadata records
    # Validates required columns exist

def validate_metadata(df: pd.DataFrame) -> bool
    """Check metadata integrity."""
    # Ensures no missing critical values
    # Validates file references exist

def filter_by_condition(df: pd.DataFrame, condition: str) -> pd.DataFrame
    """Filter metadata by patient condition."""
    # Returns: Subset matching condition (AD, CN, MCI)

def filter_by_sequence(df: pd.DataFrame, seq: str) -> pd.DataFrame
    """Filter metadata by MRI sequence."""
    # Returns: Subset matching sequence (T1, T2)

def get_file_mapping(df: pd.DataFrame) -> dict
    """Create source→target file mapping."""
    # Returns: Dictionary of file paths for movement
```

**Data Format**: Expected CSV with columns:
```
subject_id, visit_id, series_id, image_id, filename, [other columns]
002_S_0001, m00, S29096, I41124, ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii
```

---

### `file_operations.py` - Core File Movement Functions

**Purpose**: Implement the 6 main pipeline operations. This is the heart of the system.

**Function 1: `movePreprocessed()`**
```python
def movePreprocessed(meta_df, path, seq, cond, tesla=3, divider="raw_")
```
- Searches for preprocessed files (`**/wm*.nii`)
- Indexes with metadata ID
- Exports unprocessed list as CSV
- Returns: `(preprocessed_count, unprocessed_count)`

**Function 2: `move2preprocess()`**
```python
def move2preprocess(meta_df, seq, cond, tesla=3, divider="raw_")
```
- Organizes raw NIfTI files for preprocessing
- Creates subdirectories: `{subject-id}-{series-id}-{image-id}/`
- Moves from `./3T/{seq}/{cond}/` to `./TempData/{seq}/{cond}/`
- Returns: `file_count`

**Function 3: `move2convert()`**
```python
def move2convert(meta_df, seq, cond, tesla=3, divider="raw_")
```
- Organizes DICOM files for conversion
- Creates subdirectories: `{subject-id}-{series-id}_{image-id}/`
- Moves from `./DICOM/{seq}/{cond}/` to `./2convert/{seq}/{cond}/`
- Returns: `file_count`

**Function 4: `moveConverted()`**
```python
def moveConverted(meta_df, seq, cond, tesla=3, divider="br_")
```
- Moves converted NIfTI files from conversion folder
- Searches for white matter files: `**/wm*.nii`
- Indexes with metadata ID
- Moves to `./preprocessed/{seq}/{cond}/`
- Returns: `file_count`

**Function 5: `freemove()`**
```python
def freemove(source_path, target_path, seq, cond, tesla=3, file_format='**/*wm*.nii')
```
- Flexible file movement with custom glob patterns
- Default pattern: white matter (`*wm*.nii`)
- Creates indexed naming: `{index}-{filename}.nii`
- Moves to `./final/{seq}/{cond}/`
- Returns: `file_count`

**Function 6: `move2separate()`**
```python
def move2separate(meta_df, seq, tesla=3, ONLY_BASELINE=False, divider="Br_")
```
- Filters hold-out datasets by condition
- Excludes training set subjects (no duplicates)
- Organizes into `./DataSep/{seq}/{subject-id}-{series-id}/`
- Returns: `file_count`

**Common Parameters**:
- `meta_df` (DataFrame): Metadata with file references
- `seq` (str): Sequence type ("T1" or "T2")
- `cond` (str): Patient condition ("AD", "CN", or "MCI")
- `tesla` (int): Magnetic field strength (default: 3)
- `divider` (str): Filename delimiter to identify pattern

**Error Handling**:
```python
# All functions include:
- File existence validation before moving
- Directory creation with error recovery
- Detailed logging of operations and failures
- Return counts for verification
```

---

### `logging.py` - Logging Utilities

**Purpose**: Standardized logging across all modules.

**Key Functions**:
```python
def setup_logger(name: str, log_file: str = None) -> logging.Logger
    """Create and configure logger with timestamp."""
    # Auto-creates logs/ directory
    # Saves to: ./outputs/logs/{script_name}_{timestamp}.log
    # Logs to both file and console

def log_operation(logger, operation_name, status, details)
    """Log key operation with structured format."""
    # Format: [timestamp] - script - LEVEL - message

def log_file_count(logger, total, successful, failed)
    """Log file operation summary."""
```

**Log Format**:
```
2024-12-29 10:15:23,456 - move_preprocessed_files - INFO - Starting: Move Preprocessed Files
2024-12-29 10:15:24,123 - move_preprocessed_files - INFO - Loaded metadata with 150 records
2024-12-29 10:15:45,789 - move_preprocessed_files - INFO - Processed 145 files, 5 not found
2024-12-29 10:15:45,456 - move_preprocessed_files - INFO - Completed in 21.57 seconds
```

**Log Location**: `./outputs/logs/` with format `{script_name}_{YYYYMMDD_HHMMSS}.log`

---

### `utils.py` - Helper Utilities

**Purpose**: Common helper functions used across modules.

**Key Functions**:
```python
def get_file_paths(directory: str, pattern: str) -> list
    """Find files matching glob pattern."""
    # Returns: List of absolute file paths

def parse_filename(filename: str) -> dict
    """Extract metadata from filename."""
    # Returns: {subject_id, series_id, image_id, sequence, ...}

def ensure_directory(path: str) -> bool
    """Create directory if not exists."""
    # Returns: True if created/exists

def move_file(source: str, target: str, overwrite: bool = False) -> bool
    """Safely move file with validation."""
    # Returns: True if successful

def get_relative_path(abs_path: str) -> str
    """Convert absolute path to relative."""
    # For logging clarity

def validate_csv_structure(filepath: str, required_cols: list) -> bool
    """Verify CSV has required columns."""
```

---

## 🚀 Script Modules (`scripts/`)

### `run_pipeline.py` - Master Orchestrator

**Purpose**: Execute complete pipeline or specific steps.

**Entry Point**:
```bash
python scripts/run_pipeline.py --seq T1 --cond AD --step all
```

**Arguments**:
```
--seq {T1, T2}              # MRI sequence (required)
--cond {AD, CN, MCI}        # Condition (required)
--step {all, step_name}     # Pipeline step (default: all)
--old-path PATH             # Path to old preprocessed files
--source-path PATH          # Path to processed files
--target-path PATH          # Output path
```

**Execution Flow**:
```python
1. Parse arguments and validate
2. Load configuration and metadata
3. Initialize logger
4. Execute steps in sequence:
   - Step 1: movePreprocessed()
   - Step 2: move2preprocess()
   - Step 3: move2convert()
   - Step 4: freemove()
5. Generate summary report
6. Save logs
```

**Return Code**:
```
0 = Success
1 = Metadata not found
2 = Directory creation failed
3 = File operation failed
```

---

### `move_preprocessed_files.py` - Preprocessed Files Handler

**Function**: Wrapper for `movePreprocessed()`

**Entry**:
```bash
python scripts/move_preprocessed_files.py --seq T1 --cond AD --path ./preprocessed_old
```

**Workflow**:
1. Load balanced metadata from `TempMeta/Balanced_Meta_{seq}w_{cond}.csv`
2. Search for preprocessed files in `--path`
3. Match files with metadata
4. Move to `./preprocessed/{seq}/{cond}/`
5. Export unprocessed list to `TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv`
6. Log results

---

### `move_to_preprocess.py` - Preprocessing Queue

**Function**: Wrapper for `move2preprocess()`

**Entry**:
```bash
python scripts/move_to_preprocess.py --seq T1 --cond AD
```

**Workflow**:
1. Load metadata from `TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv` (or balanced if not exists)
2. Find raw files in `./3T/{seq}/{cond}/`
3. Create subdirectories with metadata IDs
4. Move to `./TempData/{seq}/{cond}/` for Windows transfer
5. Log file count and success rate

---

### `move_to_convert.py` - DICOM Conversion Queue

**Function**: Wrapper for `move2convert()`

**Entry**:
```bash
python scripts/move_to_convert.py --seq T1 --cond AD
```

**Workflow**:
1. Load balanced metadata
2. Find DICOM files in `./DICOM/{seq}/{cond}/`
3. Create subdirectories with metadata IDs
4. Move to `./2convert/{seq}/{cond}/`
5. Organize for DICOM→NIfTI conversion tools
6. Log organization summary

---

### `move_final_files.py` - Final File Movement

**Function**: Wrapper for `freemove()`

**Entry**:
```bash
python scripts/move_final_files.py --seq T1 --cond AD \
    --source ./processed --target ./final \
    --pattern "**/*wm*.nii"
```

**Workflow**:
1. Validate source and target paths
2. Search for files matching pattern
3. Create index-based filenames
4. Move to `./final/{seq}/{cond}/`
5. Log indexed file mapping

**Common Patterns**:
```
**/*wm*.nii        # White matter segmented
**/*n*.nii         # Normalized files
**/*wn*.nii        # Warped normalized
**/*y_*.nii        # Tissue classes
```

---

### `check_status.py` - Pipeline Status

**Function**: Diagnostic tool to check pipeline progress.

**Entry**:
```bash
python scripts/check_status.py --seq T1 --cond AD
```

**Checks**:
- Metadata file existence
- Input directory structure
- File counts at each stage
- Log files and timestamps
- Missing subjects or files
- Data integrity

---

## 📊 Data Organization Strategy

### File Naming Conventions

**Raw Files** (Input):
```
ADNI_{subject_id}_MR_{sequence}_br_raw_{timestamp}_{series}_{image}.nii
Example: ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii
```

**Organized Files** (TempData):
```
Directory: {subject_id}-{series_id}-{image_id}/
  └── [original filename unchanged]
Example: 002_S_0001-S29096-I41124/
  └── ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii
```

**Preprocessed Files** (After SPM):
```
{meta_id}-{original_filename}
Example: 145-ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii
```

**Final Files** (Output):
```
{index}-{filename}
Example: 0-wm ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii
```

### Directory Hierarchy

```
Sequence Level (T1, T2)
  └── Condition Level (AD, CN, MCI)
      └── Subject Level ({subject_id}-{series_id}-{image_id})
          └── File Level (nii.gz)
```

**Advantage**: Easy to batch process by sequence/condition or transfer to Windows machines.

---

## 🔧 Configuration Management

### Override Configuration in Scripts

```python
from src import config

# Override defaults
config.INPUT_DIR = "/path/to/custom/3T"
config.SEQUENCES = ["T1"]
config.CONDITIONS = ["AD", "CN"]
```

### Environment-Specific Paths

For Windows preprocessing transfer:
```python
config.TEMP_DATA_DIR = "Z:\\shared_drive\\TempData"  # Network drive
```

For cluster processing:
```python
config.PREPROCESSED_DIR = "/scratch/user/preprocessed"
config.FINAL_DIR = "/output/final"
```

---

## 📈 Processing Pipeline Workflow

### Step 1: Move Preprocessed Files
```
Input:  Balanced metadata + existing preprocessed files
        ./preprocessed_old/{seq}/{cond}/wm*.nii
Output: ./preprocessed/{seq}/{cond}/{meta-id}-{filename}.nii
        ./TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv
```

### Step 2: Queue for Preprocessing
```
Input:  To-Be-Preprocessed metadata + raw files
        ./3T/{seq}/{cond}/*.nii
Output: ./TempData/{seq}/{cond}/{subject-id}-{series-id}-{image-id}/
        Ready for Windows SPM transfer
```

### Step 3: Queue DICOM for Conversion
```
Input:  Balanced metadata + raw DICOM files
        ./DICOM/{seq}/{cond}/*.dcm
Output: ./2convert/{seq}/{cond}/{subject-id}-{series-id}_{image-id}/
        Ready for DICOM→NIfTI conversion
```

### Step 4: Move Final Processed Files
```
Input:  Processed files matching pattern
        ./processed/{seq}/{cond}/*wm*.nii
Output: ./final/{seq}/{cond}/{index}-{filename}.nii
        Ready for machine learning
```

---

## 🧪 Testing & Validation

### Validate Input Structure
```bash
# Check if directories exist and have expected structure
python scripts/check_status.py --seq T1 --cond AD
```

### Test with Single Subject
```bash
# Run on subset for testing
python scripts/move_to_preprocess.py --seq T1 --cond AD --limit 1
```

### Verify Output
```bash
# Count files at each stage
ls -R ./TempData/T1/AD/ | grep -c ".nii"
ls -R ./preprocessed/T1/AD/ | grep -c ".nii"
ls -R ./final/T1/AD/ | grep -c ".nii"
```

---

## 🔐 Error Handling Strategy

### File Not Found
```python
# All functions check existence before moving
if not os.path.exists(source):
    logger.warning(f"File not found: {source}")
    # Skips and continues with others
```

### Directory Creation Failure
```python
# Auto-create directories recursively
os.makedirs(target_dir, exist_ok=True)
# Falls back to error logging if permission denied
```

### Metadata Mismatch
```python
# Validates metadata structure before processing
if not validate_metadata(df):
    logger.error("Invalid metadata structure")
    # Halts execution with clear error message
```

---

## 📚 Advantages of This Structure

1. **Modularity**: Each function handles one pipeline step
2. **Reusability**: Functions can be imported and used independently
3. **Testability**: Isolated functions easier to unit test
4. **Logging**: Comprehensive logging at each step for debugging
5. **Scalability**: Easy to process multiple sequences/conditions in batch
6. **Portability**: Can move `./TempData/` to Windows for SPM processing
7. **Traceability**: Metadata ID tracking enables reproducibility
8. **Flexibility**: `freemove()` pattern allows custom file types

---

## 🔗 Related Documentation

- [README.md](README.md) - User-facing project overview
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md) - Visual diagrams
- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - What changed from notebooks
- [INDEX.md](INDEX.md) - Documentation index

