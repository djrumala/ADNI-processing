# Quick Start Guide - ADNI Data Processing

## Installation

1. **Clone/Navigate to repository**:
   ```bash
   cd ADNI-processing
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Basic Workflow

### Option 1: Run Individual Steps

**Step 1: Move Preprocessed Files**
```bash
python scripts/move_preprocessed_files.py --seq T1 --cond AD
```
- Moves old preprocessed files from `./preprocessed_old/`
- Creates list of files needing preprocessing

**Step 2: Move Files to Preprocessing**
```bash
python scripts/move_to_preprocess.py --seq T1 --cond AD
```
- Organizes unpreprocessed files for Windows-based preprocessing
- Creates subdirectories for each subject-series-image combination

**Step 3: Move DICOM Files for Conversion**
```bash
python scripts/move_to_convert.py --seq T1 --cond AD
```
- Prepares DICOM files for conversion to NIfTI format
- Organizes with metadata-based directory structure

**Step 4: Move Final Processed Files**
```bash
python scripts/move_final_files.py --seq T1 --cond AD
```
- Moves final preprocessed files to output directory
- Uses customizable pattern matching

### Option 2: Run Complete Pipeline

```bash
python scripts/run_pipeline.py --seq T1 --cond AD --step all
```

Processes all 4 steps automatically for the specified sequence and condition.

## Processing Multiple Groups

### Process all T1 groups:
```bash
for cond in AD CN MCI; do
    python scripts/run_pipeline.py --seq T1 --cond $cond --step all
done
```

### Process all groups (T1 and T2):
```bash
for seq in T1 T2; do
    for cond in AD CN MCI; do
        python scripts/run_pipeline.py --seq $seq --cond $cond --step all
    done
done
```

## Directory Structure

Before running, ensure you have:

```
ADNI-processing/
├── 3T/                      # Raw NIFTI files
│   ├── T1/
│   │   ├── AD/
│   │   ├── CN/
│   │   └── MCI/
│   └── T2/
│       ├── AD/
│       ├── CN/
│       └── MCI/
│
├── DICOM/                   # Raw DICOM files
│   ├── T1/
│   │   ├── AD/
│   │   ├── CN/
│   │   └── MCI/
│   └── T2/
│       ├── AD/
│       ├── CN/
│       └── MCI/
│
├── preprocessed_old/        # Previously preprocessed files
│   ├── T1/
│   │   ├── AD/
│   │   ├── CN/
│   │   └── MCI/
│   └── T2/
│       ├── AD/
│       ├── CN/
│       └── MCI/
│
└── TempMeta/                # Metadata CSVs
    ├── Balanced_Meta_T1w_AD.csv
    ├── Balanced_Meta_T1w_CN.csv
    ├── Balanced_Meta_T1w_MCI.csv
    ├── Balanced_Meta_T2w_AD.csv
    ├── Balanced_Meta_T2w_CN.csv
    └── Balanced_Meta_T2w_MCI.csv
```

## Output Directories Created

The scripts will automatically create:

```
preprocessed/               # Final preprocessed files
├── T1/
│   ├── AD/
│   ├── CN/
│   └── MCI/
└── T2/
    ├── AD/
    ├── CN/
    └── MCI/

TempData/                   # Files staged for preprocessing
├── T1/
│   ├── AD/
│   ├── CN/
│   └── MCI/
└── T2/
    ├── AD/
    ├── CN/
    └── MCI/

2convert/                   # DICOM files for conversion
├── T1/
│   ├── AD/
│   ├── CN/
│   └── MCI/
└── T2/
    ├── AD/
    ├── CN/
    └── MCI/

final/                      # Final output files
├── T1/
│   ├── AD/
│   ├── CN/
│   └── MCI/
└── T2/
    ├── AD/
    ├── CN/
    └── MCI/

outputs/logs/               # Processing logs
├── move_preprocessed_files_*.log
├── move_to_preprocess_*.log
├── move_to_convert_*.log
└── move_final_files_*.log
```

## Monitoring Progress

Check logs in `outputs/logs/`:

```bash
# View latest log
tail -f outputs/logs/*.log

# Check specific step
cat outputs/logs/move_preprocessed_files_*.log
```

## Customization

### Change default paths in `src/config.py`:

```python
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "your_data_folder"
PREPROCESSED_DIR = BASE_DIR / "your_preprocessed_folder"
# ... etc
```

### Custom file patterns in `move_final_files.py`:

```bash
# Move normalized files
python scripts/move_final_files.py --seq T1 --cond AD --pattern "**/*n*.nii"

# Move warped files
python scripts/move_final_files.py --seq T1 --cond AD --pattern "**/*wn*.nii"

# Move all nifti files
python scripts/move_final_files.py --seq T1 --cond AD --pattern "**/*.nii"
```

## Troubleshooting

### File not found errors
- Verify source directory exists
- Check metadata CSV is in `TempMeta/` folder
- Ensure correct sequence/condition names (T1/T2, AD/CN/MCI)

### Permission errors
- Check write permissions for output directories
- Ensure you have read access to source files

### Metadata mismatches
- Verify metadata CSV column names match expected format
- Check subject IDs and image IDs in metadata

## More Information

For detailed documentation, see:
- [STRUCTURE.md](STRUCTURE.md) - Complete project structure and API reference
- [README.md](README.md) - Full project documentation
- Function docstrings in `src/` modules

## Example: Complete Processing Session

```bash
#!/bin/bash
# Process all T1 groups for Robustness Evaluation

echo "Starting ADNI Data Processing Pipeline"
echo "======================================="

cd ADNI-processing

# Define groups
SEQUENCES="T1 T2"
CONDITIONS="AD CN MCI"

# Process each combination
for seq in $SEQUENCES; do
    for cond in $CONDITIONS; do
        echo ""
        echo "Processing $seq - $cond..."
        python scripts/run_pipeline.py \
            --seq $seq \
            --cond $cond \
            --step all \
            --old-path ./preprocessed_old \
            --source-path ./processed \
            --target-path ./final
        
        if [ $? -eq 0 ]; then
            echo "✓ $seq - $cond completed successfully"
        else
            echo "✗ $seq - $cond failed - check logs"
        fi
    done
done

echo ""
echo "Pipeline Complete!"
echo "Check outputs/logs/ for detailed logs"
```

Save as `process_all.sh`, make executable with `chmod +x process_all.sh`, then run:
```bash
./process_all.sh
```
