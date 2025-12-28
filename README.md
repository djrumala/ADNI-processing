# About Repository
This repo includes technical documentation and Python codebase for data preparation for 3D brain MR image classification using ADNI dataset.

We have used this data preprocessing and processing of ADNI dataset for several publications (see: [About Citation](https://github.com/djrumala/ADNI-processing#about-citation))

## Project Status
✅ **REFACTORED**: Converted from Jupyter Notebooks to modular Python codebase
- Clean package structure with reusable modules
- Executable scripts for each pipeline step
- Comprehensive logging and configuration
- Full documentation in [STRUCTURE.md](STRUCTURE.md)

# Quick Start
Execute the complete data processing pipeline:
```bash
python scripts/run_pipeline.py --seq T1 --cond AD --step all
```

See [Usage Examples](QUICKSTART.md) for detailed instructions.

# Project Structure
```
ADNI-processing/
├── src/                      # Core Python package
│   ├── config.py            # Configuration & constants
│   ├── metadata.py          # Metadata utilities
│   ├── file_operations.py   # File moving functions
│   └── logging.py           # Logging utilities
│
├── scripts/                 # Executable workflows
│   ├── move_preprocessed_files.py
│   ├── move_to_preprocess.py
│   ├── move_to_convert.py
│   ├── move_final_files.py
│   └── run_pipeline.py      # Master orchestrator
│
├── outputs/                 # Results & logs
│   └── logs/
│
├── TempMeta/                # Metadata CSVs
├── TempData/                # Temporary data
├── preprocessed/            # Final preprocessed files
├── final/                   # Final output
│
└── STRUCTURE.md             # Detailed structure documentation
```

See [STRUCTURE.md](STRUCTURE.md) for complete details on the Python codebase structure, module reference, and usage examples.

# Data Pipeline Overview

The ADNI data processing pipeline follows these high-level steps:

1. **Data Collection**: Download raw DICOM and NIfTI files from [ADNI](https://ida.loni.usc.edu/login.jsp)
2. **Data Cleaning**: Filter relevant sequences (T1-weighted MP-RAGE, T2-weighted TSE/FSE) and create matched T1/T2 pairs
3. **Data Organizing**: Move files to preprocessing queue with proper directory structure  
4. **Preprocessing**: Apply SPM normalization, skull-stripping, registration, and scaling
5. **Augmentation**: Apply data augmentation (flipping, rotation) to balance dataset
6. **Final Output**: Move processed files to final output directory

The refactored Python codebase automates steps 3-6 with reusable, configurable modules. Steps 1-2 (collection and cleaning) involve manual data acquisition and metadata preparation.

# Data Organization

Input data structure expected:
```
./DICOM/{seq}/{cond}/          # Raw DICOM files
./3T/{seq}/{cond}/             # Raw NIfTI files  
./TempMeta/                    # Metadata CSVs
```

Required metadata file:
- `Balanced_Meta_{seq}w_{cond}.csv` - Finalized balanced dataset list

# Python Codebase for Automated Processing

The original Jupyter notebooks have been converted into a modular Python package that automates the data processing pipeline.

## File Operations Functions

The core file movement and organization operations are implemented as reusable Python functions in `src/file_operations.py`. Each function handles a specific step in the data processing pipeline.

### 1. Move Preprocessed Files (`movePreprocessed`)
Collects already-preprocessed files from archive folders and moves them to the target preprocessed directory.

**Purpose**: Handle previously processed data to avoid reprocessing

**Function**:
```python
movePreprocessed(meta_df, path, seq, cond, tesla=3, divider="raw_")
```

**What it does**:
- Searches for preprocessed files matching pattern `**/wm*.nii`
- Compares metadata with available files
- Moves matching files to `/preprocessed/{seq}/{cond}/`
- Exports list of not-yet-preprocessed files as CSV for next step
- Indexes files with metadata ID: `/preprocessed/{seq}/{cond}/{meta-id}-{filename}.nii`

**Inputs**:
- Balanced metadata CSV: `TempMeta/Balanced_Meta_{seq}w_{cond}.csv`
- Source preprocessed files: `./preprocessed_old/{seq}/{cond}/`

**Outputs**:
- Organized preprocessed files: `./preprocessed/{seq}/{cond}/`
- Unprocessed list: `TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv`

**Usage**:
```bash
python scripts/move_preprocessed_files.py --seq T1 --cond AD --path ./preprocessed_old
```

### 2. Move Files to Preprocessing Queue (`move2preprocess`)
Organizes raw NIFTI files that need preprocessing with proper directory structure for Windows-based processing.

**Purpose**: Prepare files for SPM/MATLAB preprocessing on Windows machines

**Function**:
```python
move2preprocess(meta_df, seq, cond, tesla=3, divider="raw_")
```

**What it does**:
- Identifies files to be preprocessed from metadata
- Organizes each file in a subdirectory: `{subject-id}-{series-id}-{image-id}`
- Moves to `/TempData/{seq}/{cond}/` for transfer to Windows
- Maintains filename integrity for later matching

**File Organization**:
```
TempData/T1/AD/
├── 002_S_0001-S29096-I41124/
│   └── ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329110738780_1_S29096_I41124.nii
├── 002_S_0456-S29097-I41125/
│   └── ADNI_002_S_0456_MR_MPRAGE_br_raw_20070330120442156_2_S29097_I41125.nii
└── ...
```

**Inputs**:
- Unprocessed metadata: `TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv`
- Raw files: `./3T/{seq}/`

**Outputs**:
- Organized files: `./TempData/{seq}/{cond}/{subject}-{series}-{image}/`

**Usage**:
```bash
python scripts/move_to_preprocess.py --seq T1 --cond AD
```

### 3. Move DICOM Files for Conversion (`move2convert`)
Prepares DICOM files for DICOM-to-NIfTI conversion by organizing them with proper metadata-based directory structure.

**Purpose**: Organize raw DICOM files before conversion process

**Function**:
```python
move2convert(meta_df, seq, cond, tesla=3, divider="raw_")
```

**What it does**:
- Matches DICOM files with metadata
- Creates subdirectories: `{subject-id}-{series-id}_{image-id}`
- Moves to `/2convert/{seq}/{cond}/` for conversion process
- Preserves original DICOM filenames for conversion tools

**File Organization**:
```
2convert/T1/AD/
├── 002_S_0001-S29096_I41124/
│   ├── DICOM_file_001.dcm
│   ├── DICOM_file_002.dcm
│   └── ...
├── 002_S_0456-S29097_I41125/
│   └── ...
└── ...
```

**Notes**:
- DICOM files must be in: `./DICOM/{seq}/{cond}/`
- Directory naming helps conversion tools process related images together
- This step is crucial before DICOM to NIfTI conversion

**Inputs**:
- Balanced metadata CSV: `TempMeta/Balanced_Meta_{seq}w_{cond}.csv`
- DICOM files: `./DICOM/{seq}/{cond}/`

**Outputs**:
- Organized DICOM: `./2convert/{seq}/{cond}/{subject}-{series}_{image}/`

**Usage**:
```bash
python scripts/move_to_convert.py --seq T1 --cond AD
```

### 4. Move Converted Files (`moveConverted`)
Moves converted NIfTI files from conversion folder to preprocessed folder with metadata indexing.

**Purpose**: Archive converted files in preprocessed folder

**Function**:
```python
moveConverted(meta_df, seq, cond, tesla=3, divider="br_")
```

**What it does**:
- Searches for white matter segmented files: `**/wm*.nii`
- Matches metadata with filenames
- Moves to `/preprocessed/{seq}/{cond}/`
- Indexes with metadata ID for later pairing of T1 and T2

**Inputs**:
- Balanced metadata CSV: `TempMeta/Balanced_Meta_{seq}w_{cond}.csv`
- Converted files: `./Converted/{seq}/{cond}/`

**Outputs**:
- Preprocessed files: `./preprocessed/{seq}/{cond}/{meta-id}-{filename}.nii`

### 5. Move Final Processed Files (`freemove`)
Flexible function that moves any files based on filename pattern matching.

**Purpose**: Move final preprocessed/processed files to output directory

**Function**:
```python
freemove(source_path, target_path, seq, cond, tesla=3, file_format='**/*wm*.nii')
```

**What it does**:
- Uses customizable glob pattern to find files
- Default pattern matches white matter segmented files: `**/wm*.nii`
- Moves to `/final/{seq}/{cond}/` with indexed naming
- Flexible for different file types and patterns

**File Organization**:
```
final/T1/AD/
├── 0-wm{filename}.nii
├── 1-wm{filename}.nii
├── 2-wm{filename}.nii
└── ...
```

**Parameters**:
- `file_format`: Glob pattern (e.g., `**/*wm*.nii`, `**/*y_*.nii`, `**/*p*.nii`)
- Can move different file types: segmented, normalized, warped, etc.

**Inputs**:
- Processed files: `./processed/{seq}/{cond}/`

**Outputs**:
- Final files: `./final/{seq}/{cond}/{index}-{filename}.nii`

**Usage**:
```bash
# Move white matter segmented files (default)
python scripts/move_final_files.py --seq T1 --cond AD \
    --source ./processed --target ./final

# Move normalized files
python scripts/move_final_files.py --seq T1 --cond AD \
    --source ./processed --target ./final --pattern "**/*n*.nii"

# Move warped files
python scripts/move_final_files.py --seq T1 --cond AD \
    --source ./processed --target ./final --pattern "**/*wn*.nii"
```

### 6. Separate Data for Robustness Evaluation (`move2separate`)
Organizes hold-out datasets for robustness evaluation with proper grouping.

**Purpose**: Prepare new/hold-out data that has never been used in training

**Function**:
```python
move2separate(meta_df, seq, tesla=3, ONLY_BASELINE=False, divider="Br_")
```

**What it does**:
- Filters new datasets from different sources
- Excludes data from subjects already in training set
- Organizes into `/DataSep/` for manual verification
- Enables robustness testing with completely new data

**Inputs**:
- New dataset metadata: `HoldOut_Cleaned_{seq}w_{cond}_{tesla}T.csv`
- New data files: source directory

**Outputs**:
- Separated data: `./DataSep/{seq}/{subject-id}-{series-id}/`

## Master Pipeline Orchestrator

Run the complete workflow automatically:

```bash
python scripts/run_pipeline.py --seq T1 --cond AD --step all
```

**Pipeline Steps**:
1. Move preprocessed files
2. Move files to preprocessing queue
3. Move DICOM files for conversion
4. Move final processed files

**Options**:
```
--seq {T1, T2}              # MRI sequence (required)
--cond {AD, CN, MCI}        # Condition (required)
--step {all|step_name}      # Which step to run (default: all)
--old-path PATH             # Path to old preprocessed files
--source-path PATH          # Path to processed files
--target-path PATH          # Output path for final files
```

**Examples**:
```bash
# Process single group
python scripts/run_pipeline.py --seq T1 --cond AD --step all

# Run only preprocessing step
python scripts/run_pipeline.py --seq T1 --cond AD --step move_to_preprocess

# Process multiple groups (T1)
for cond in AD CN MCI; do
    python scripts/run_pipeline.py --seq T1 --cond $cond --step all
done

# Process all groups (T1 and T2)
for seq in T1 T2; do
    for cond in AD CN MCI; do
        python scripts/run_pipeline.py --seq $seq --cond $cond --step all
    done
done
```

## Logging and Output

All operations are logged to `outputs/logs/` with timestamps and details:

```
outputs/logs/
├── move_preprocessed_files_20241229_101523.log
├── move_to_preprocess_20241229_101545.log
├── move_to_convert_20241229_101612.log
└── move_final_files_20241229_101634.log
```

Log example:
```
2024-12-29 10:15:23,456 - move_preprocessed_files - INFO - Starting: Move Preprocessed Files
2024-12-29 10:15:24,123 - move_preprocessed_files - INFO - Loaded metadata with 150 records
2024-12-29 10:15:45,789 - move_preprocessed_files - INFO - Total T1w-AD data is 145 and not preprocessed is 5
2024-12-29 10:15:45,456 - move_preprocessed_files - INFO - Completed Move Preprocessed Files in 21.57s
```

## Configuration

Global configuration in `src/config.py`:
- Directory paths (inputs, outputs, temporary)
- Sequences, conditions, Tesla strengths
- File patterns and delimiters
- Metadata column definitions
- Logging settings

Customize these settings for different project configurations.

# Data Processing Steps

Data preprocessing is performed using SPM and includes:
- Normalization / Intensity normalization
- Skull-stripping
- Registration to standard template
- Scaling

Data augmentation (flipping and rotation) is applied post-preprocessing to balance dataset sizes.

For model training, data loading ensures:
- Proper split-before-augmentation to prevent data leakage
- Paired T1/T2 images fed together for joint training
- Metadata ID-based grouping for cross-validation

# About Citation
For more detail please refer to the publication: 

[1] Rumala, D.J. (2023). How You Split Matters: Data Leakage and Subject Characteristics Studies in Longitudinal Brain MRI Analysis. In: Wesarg, S., et al. Clinical Image-Based Procedures, Fairness of AI in Medical Imaging, and Ethical and Philosophical Issues in Medical Imaging . CLIP EPIMI FAIMI 2023 2023 2023. Lecture Notes in Computer Science, vol 14242. Springer, Cham. [https://doi.org/10.1007/978-3-031-45249-9_23](https://doi.org/10.1007/978-3-031-45249-9_23).

More information and comprehensive summary about this publication can be freely accessed here: [https://djrumala.github.io/publications/how-you-split-matters](https://djrumala.github.io/publications/how-you-split-matters)
