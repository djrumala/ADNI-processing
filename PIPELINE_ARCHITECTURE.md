# ADNI Processing Pipeline Architecture

## Overall Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ADNI Data Processing Pipeline                    │
└─────────────────────────────────────────────────────────────────────┘

Step 1: Move Preprocessed Files
────────────────────────────────────────────────────────────────────────
INPUT:  ./preprocessed_old/{seq}/{cond}/*.nii
        TempMeta/Balanced_Meta_{seq}w_{cond}.csv
        
    movePreprocessed()
        ↓
        • Match metadata with filenames
        • Move wm*.nii files to target
        • Index with metadata ID
        • Generate list of unprocessed files
        
OUTPUT: ./preprocessed/{seq}/{cond}/{meta-id}-{filename}.nii
        TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv

Step 2: Move Files to Preprocessing Queue
────────────────────────────────────────────────────────────────────────
INPUT:  ./3T/{seq}/{cond}/*.nii
        TempMeta/To-Be-Preprocessed_{seq}w_{cond}.csv
        
    move2preprocess()
        ↓
        • Find unpreprocessed files
        • Organize by subject-series-image
        • Create subdirectories for each file
        • Ready for transfer to Windows
        
OUTPUT: ./TempData/{seq}/{cond}/{subject}-{series}-{image}/*.nii

Step 3: Move DICOM Files for Conversion
────────────────────────────────────────────────────────────────────────
INPUT:  ./DICOM/{seq}/{cond}/*.dcm
        TempMeta/Balanced_Meta_{seq}w_{cond}.csv
        
    move2convert()
        ↓
        • Match DICOM files with metadata
        • Create conversion-ready structure
        • Group related files together
        
OUTPUT: ./2convert/{seq}/{cond}/{subject}-{series}_{image}/*.dcm

Step 4: Move Final Processed Files
────────────────────────────────────────────────────────────────────────
INPUT:  ./processed/{seq}/{cond}/{patterns}
        Pattern: **/*wm*.nii (default)
        
    freemove()
        ↓
        • Find files matching pattern
        • Copy to final location
        • Index with sequential numbers
        
OUTPUT: ./final/{seq}/{cond}/{index}-{filename}.nii

ALL STEPS ORCHESTRATED BY: run_pipeline.py
────────────────────────────────────────────────────────────────────────
python scripts/run_pipeline.py --seq T1 --cond AD --step all
```

## Data Organization Hierarchy

```
ADNI-processing/                          ← Base directory
│
├── Raw Data Sources
│   ├── 3T/                               ← Raw NIFTI files
│   │   ├── T1/
│   │   │   ├── AD/
│   │   │   ├── CN/
│   │   │   └── MCI/
│   │   └── T2/
│   │       ├── AD/
│   │       ├── CN/
│   │       └── MCI/
│   │
│   └── DICOM/                            ← Raw DICOM files
│       ├── T1/
│       │   ├── AD/
│       │   ├── CN/
│       │   └── MCI/
│       └── T2/
│           ├── AD/
│           ├── CN/
│           └── MCI/
│
├── Archive & Processing
│   ├── preprocessed_old/                 ← Previously preprocessed
│   ├── preprocessed_addition/            ← Additional preprocessed files
│   │
│   └── Processing Outputs
│       ├── TempMeta/                     ← Metadata CSVs
│       │   ├── Balanced_Meta_T1w_AD.csv
│       │   ├── To-Be-Preprocessed_T1w_AD.csv
│       │   └── ...
│       │
│       ├── TempData/                     ← Staged for preprocessing
│       │   ├── T1/
│       │   │   ├── AD/
│       │   │   │   ├── 002_S_0001-S29096-I41124/
│       │   │   │   ├── 002_S_0456-S29097-I41125/
│       │   │   │   └── ...
│       │   │   └── ...
│       │   └── T2/
│       │       └── ...
│       │
│       ├── 2convert/                     ← Ready for conversion
│       │   ├── T1/
│       │   │   ├── AD/
│       │   │   │   ├── 002_S_0001-S29096_I41124/
│       │   │   │   ├── 002_S_0456-S29097_I41125/
│       │   │   │   └── ...
│       │   │   └── ...
│       │   └── T2/
│       │       └── ...
│       │
│       ├── Converted/                    ← Converted NIfTI
│       │   ├── T1/
│       │   │   ├── AD/
│       │   │   ├── CN/
│       │   │   └── MCI/
│       │   └── T2/
│       │       └── ...
│       │
│       └── preprocessed/                 ← Final preprocessed
│           ├── T1/
│           │   ├── AD/
│           │   │   ├── 0-wm{filename}.nii
│           │   │   ├── 1-wm{filename}.nii
│           │   │   └── ...
│           │   ├── CN/
│           │   └── MCI/
│           └── T2/
│               └── ...
│
├── Final Output
│   └── final/                            ← Final organized output
│       ├── T1/
│       │   ├── AD/
│       │   │   ├── 0-wm{filename}.nii
│       │   │   ├── 1-wm{filename}.nii
│       │   │   └── ...
│       │   ├── CN/
│       │   └── MCI/
│       └── T2/
│           └── ...
│
└── Code & Documentation
    ├── src/                              ← Python package
    │   ├── config.py
    │   ├── metadata.py
    │   ├── file_operations.py
    │   ├── logging.py
    │   ├── utils.py
    │   └── __init__.py
    │
    ├── scripts/                          ← Executable scripts
    │   ├── move_preprocessed_files.py
    │   ├── move_to_preprocess.py
    │   ├── move_to_convert.py
    │   ├── move_final_files.py
    │   ├── run_pipeline.py
    │   └── check_status.py
    │
    ├── outputs/                          ← Results & logs
    │   └── logs/
    │       ├── move_preprocessed_files_20241229_101523.log
    │       ├── move_to_preprocess_20241229_101545.log
    │       ├── move_to_convert_20241229_101612.log
    │       └── move_final_files_20241229_101634.log
    │
    ├── README.md                         ← Main documentation
    ├── STRUCTURE.md                      ← Detailed structure
    ├── QUICKSTART.md                     ← Getting started
    ├── REFACTORING_SUMMARY.md            ← What changed
    └── requirements.txt                  ← Dependencies
```

## Function Call Dependency Graph

```
                      run_pipeline.py
                    (Master Orchestrator)
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
    Script 1          Script 2             Script 3          Script 4
        │               │                   │                   │
        ▼               ▼                   ▼                   ▼
movePreprocessed()  move2preprocess()   move2convert()    freemove()
        │               │                   │                   │
        ├──────────────┬─┴──────────────────┤                   │
        │              │                    │                   │
        ▼              ▼                    ▼                   ▼
   createMetaCombinedString()           Path operations     pathlib
   exportCSV()                          metadata matching   glob patterns
   
        │              │                    │                   │
        └──────────────┴────────────────────┴───────────────────┘
                                │
                                ▼
                          config.py
                      (Global Settings)
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
            Directories    File Patterns   Delimiters
            Sequences       Constants      Defaults
            Conditions
```

## File Naming Convention

```
Original DICOM/NIfTI:
┌─────────────────────────────────────────────────────┐
│ ADNI_002_S_0001_MR_MPRAGE_br_raw_20070329...nii    │
├──────────────┬────────────────────────────────────┤
│ Subject ID   │ Date & Acquisition Info             │
│ 002_S_0001   │ MPRAGE, br_raw, timestamp...       │
└──────────────┴────────────────────────────────────┘

After movePreprocessed():
┌──────────────────────────────────────────────────┐
│ 42-wm{original_filename}.nii                    │
├──────────────┬────────────────────────────────┤
│ Metadata ID  │ Preprocessed marker + original │
│ 42           │ wm = white matter segment       │
└──────────────┴────────────────────────────────┘

Directory Structure:
┌────────────────────────────────────────────────────┐
│ {subject-id}-{series-id}-{image-id}              │
├────────────────┬──────────────┬──────────────────┤
│ Subject        │ Series ID    │ Image ID         │
│ 002_S_0001     │ S29096       │ I41124           │
└────────────────┴──────────────┴──────────────────┘
```

## Script Execution Flow

```
User Input
    │
    ▼
┌─────────────────────────────────────────┐
│  python scripts/run_pipeline.py         │
│  --seq T1 --cond AD --step all          │
└─────────────────────────────────────────┘
    │
    ├─→ Parse arguments
    │
    ├─→ Create output directories
    │
    ├─→ Initialize logging
    │
    ├─→ Step 1: move_preprocessed_files.py
    │   ├─ Load metadata
    │   ├─ Call movePreprocessed()
    │   ├─ Export unprocessed list
    │   └─ Log results
    │
    ├─→ Step 2: move_to_preprocess.py
    │   ├─ Load metadata
    │   ├─ Call move2preprocess()
    │   └─ Log results
    │
    ├─→ Step 3: move_to_convert.py
    │   ├─ Load metadata
    │   ├─ Call move2convert()
    │   └─ Log results
    │
    ├─→ Step 4: move_final_files.py
    │   ├─ Load metadata (optional)
    │   ├─ Call freemove()
    │   └─ Log results
    │
    └─→ Print summary
        • Files processed
        • Success/failure count
        • Log file location
        
    ▼
✓ Pipeline Complete
  Logs available in: outputs/logs/
```

## Configuration Hierarchy

```
Global Configuration (src/config.py)
    │
    ├─ Directories (BASE_DIR, DATA_DIR, OUTPUT_DIR, etc.)
    │
    ├─ Processing Modes
    │   ├─ SEQUENCES: T1, T2
    │   ├─ CONDITIONS: AD, CN, MCI
    │   └─ TESLA: 1.5, 3
    │
    ├─ File Patterns
    │   ├─ DICOM_PATTERN: **/*.dcm
    │   ├─ NIFTI_PATTERN: **/*.nii
    │   └─ PREPROCESSED_PATTERN: **/wm*.nii
    │
    ├─ Metadata Columns
    │   ├─ Image Data ID
    │   ├─ Subject
    │   ├─ Group
    │   ├─ Sex
    │   ├─ Age
    │   └─ ...
    │
    └─ Logging Settings
        ├─ Log Directory
        └─ Log Format
        
        │
        ▼
Individual Script Configuration
    │
    ├─ Command-line arguments override defaults
    ├─ Environment-specific paths
    └─ Custom patterns for file matching
```

## Event Logging Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Processing Operation Starts               │
└─────────────────────────────────────────────────────────┘
            │
            ├─→ ProcessingLogger.__enter__()
            │   └─→ Initialize logger
            │   └─→ Record start time
            │
            ├─→ Execute Core Logic
            │   ├─→ Load metadata (INFO)
            │   ├─→ Find files (INFO)
            │   ├─→ Move files (DEBUG)
            │   └─→ Export results (INFO)
            │
            └─→ ProcessingLogger.__exit__()
                ├─→ Calculate duration
                ├─→ Log completion (INFO)
                ├─→ If error: log error (ERROR)
                └─→ Write to file & console

Output:
├─ Console: Real-time updates
├─ Log File: Timestamped history
│   Location: outputs/logs/{step_name}_{timestamp}.log
└─ Return Value: Success/Failure status
```

## Complete Pipeline Example: T1 AD Processing

```
Input State:
  3T/T1/AD/*.nii (100 files)
  DICOM/T1/AD/*.dcm (10,000 files)
  preprocessed_old/T1/AD/*.nii (50 files)
  TempMeta/Balanced_Meta_T1w_AD.csv (150 records)

Command:
  python scripts/run_pipeline.py --seq T1 --cond AD --step all

Execution:
  
  1️⃣ Step 1: Move Preprocessed Files
     Moved: 50 files → ./preprocessed/T1/AD/
     Not Yet: 100 files → To-Be-Preprocessed_T1w_AD.csv
  
  2️⃣ Step 2: Move to Preprocessing Queue
     Organized: 100 files → ./TempData/T1/AD/{subdirs}/
  
  3️⃣ Step 3: Move DICOM for Conversion
     Organized: 10,000 files → ./2convert/T1/AD/{subdirs}/
  
  4️⃣ Step 4: Move Final Files
     Copied: 50+ files → ./final/T1/AD/

Output State:
  ./preprocessed/T1/AD/ ............ 50 indexed files
  ./TempData/T1/AD/ ................ 100 files in subdirs
  ./2convert/T1/AD/ ................ 10,000 files in subdirs
  ./final/T1/AD/ ................... 50+ indexed files
  ./outputs/logs/ .................. 4 log files (timestamped)
  TempMeta/ ........................ Updated metadata CSVs

Status:
  ✓ Preprocessing queue ready (TempData/)
  ✓ Conversion queue ready (2convert/)
  ✓ All operations logged
  ✓ Ready for next stage
```
