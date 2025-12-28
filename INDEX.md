# ADNI Data Processing - Complete Documentation Index

Welcome to the refactored ADNI data processing codebase! This document serves as the starting point for navigating all documentation and code.

## 📚 Documentation Files

### 1. **README.md** (Main Project Documentation)
**Start here if you want to understand the project overview.**
- Project status and features
- Complete data pipeline steps
- Detailed function documentation (6 functions)
- All three key functions documented:
  - `move2convert()` - Move DICOM files
  - `move2preprocess()` - Move files to preprocessing queue
  - `freemove()` - Flexible file movement
- Usage examples and command-line reference

**File size**: ~470 lines
**Key sections**:
- Project Structure
- File Operations Functions (1-6)
- Master Pipeline Orchestrator
- Logging and Output
- Configuration

---

### 2. **QUICKSTART.md** (Getting Started)
**Start here if you want to run the code immediately.**
- Installation instructions
- Step-by-step workflow
- Basic commands for each step
- Batch processing for all groups
- Directory structure expectations
- Troubleshooting guide
- Example: Complete processing session

**File size**: ~300 lines
**Key sections**:
- Installation
- Basic Workflow (Option 1 & 2)
- Processing Multiple Groups
- Output Directories
- Monitoring Progress

---

### 3. **STRUCTURE.md** (Complete Architecture Reference)
**Start here if you want to understand the technical structure.**
- Detailed directory structure
- Module reference for all Python files
- Complete function API documentation
- Data organization strategy
- File naming conventions
- Logging system
- Configuration management

**File size**: ~420 lines
**Key sections**:
- Processing Pipeline Steps (Step 1-4)
- Module Reference
- Usage Examples
- Advantages of This Structure

---

### 4. **PIPELINE_ARCHITECTURE.md** (Visual Guides)
**Start here if you prefer visual/diagram-based documentation.**
- Overall pipeline flow diagrams
- Data organization hierarchy
- Function dependency graphs
- File naming conventions
- Script execution flow
- Configuration hierarchy
- Event logging architecture
- Complete example walkthrough

**File size**: ~300 lines
**Key sections**:
- Pipeline Flow
- Data Organization Hierarchy
- Function Call Dependency Graph
- File Naming Convention

---

### 5. **REFACTORING_SUMMARY.md** (What Changed)
**Start here if you're wondering what happened to the notebooks.**
- Before/after comparison
- New project structure
- Six key functions organized
- How to use the new system
- Documentation locations
- Benefits of refactoring

**File size**: ~300 lines
**Key sections**:
- What Was Changed
- New Project Structure
- Six Key Functions
- How to Use
- Benefits

---

## 🗂️ Code Structure

### `src/` - Core Python Package
| Module | Purpose | Lines |
|--------|---------|-------|
| `__init__.py` | Package initialization | 28 |
| `config.py` | Global configuration | 75 |
| `metadata.py` | Metadata utilities | 100 |
| `file_operations.py` | File movement functions | 410 |
| `logging.py` | Logging utilities | 65 |
| `utils.py` | Helper functions | 165 |

**Total**: ~840 lines of production code

---

### `scripts/` - Executable Workflows
| Script | Function | Lines |
|--------|----------|-------|
| `move_preprocessed_files.py` | Move archived preprocessed files | 65 |
| `move_to_preprocess.py` | Move files to preprocessing queue | 60 |
| `move_to_convert.py` | Move DICOM for conversion | 60 |
| `move_final_files.py` | Move final processed files | 65 |
| `run_pipeline.py` | Master orchestrator | 130 |
| `check_status.py` | Pipeline diagnostics | 50 |

**Total**: ~430 lines of scripts

---

## 🚀 Quick Navigation Guide

### If you want to...

**...understand what this project does:**
→ Read [README.md](README.md) - Project Overview section

**...run the code right now:**
→ Go to [QUICKSTART.md](QUICKSTART.md) - Installation & Usage

**...understand the complete architecture:**
→ Check [STRUCTURE.md](STRUCTURE.md) - Processing Pipeline Steps

**...see visual diagrams:**
→ Look at [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md)

**...know what changed from notebooks:**
→ Read [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)

**...check your setup status:**
→ Run `python scripts/check_status.py`

---

## 📋 Function Documentation Map

### The Three Main Functions

#### 1. `move2convert()` - Move DICOM Files for Conversion
**Location**: [README.md - Move DICOM Files for Conversion](README.md#3-move-dicom-files-for-conversion-move2convert)
**Purpose**: Prepare DICOM files for DICOM-to-NIfTI conversion
**Usage**: 
```bash
python scripts/move_to_convert.py --seq T1 --cond AD
```
**Key Details**:
- Input: DICOM files + balanced metadata
- Output: Organized DICOM in `2convert/`
- Creates structure: `{subject-id}-{series-id}_{image-id}`

---

#### 2. `move2preprocess()` - Move Files to Preprocessing Queue
**Location**: [README.md - Move Files to Preprocessing Queue](README.md#2-move-files-to-preprocessing-queue-move2preprocess)
**Purpose**: Organize raw files for Windows-based preprocessing
**Usage**:
```bash
python scripts/move_to_preprocess.py --seq T1 --cond AD
```
**Key Details**:
- Input: Raw NIFTI files + unprocessed metadata
- Output: Organized files in `TempData/`
- Creates structure: `{subject-id}-{series-id}-{image-id}`

---

#### 3. `freemove()` - Move Final Processed Files
**Location**: [README.md - Move Final Processed Files](README.md#5-move-final-processed-files-freemove)
**Purpose**: Flexible file movement with pattern matching
**Usage**:
```bash
python scripts/move_final_files.py --seq T1 --cond AD \
    --source ./processed --target ./final --pattern "**/*wm*.nii"
```
**Key Details**:
- Input: Any processed files matching pattern
- Output: Final files in organized structure
- Customizable glob patterns

---

### Additional Functions (Context & Utilities)

#### `movePreprocessed()` - Archive Preprocessed Files
**Location**: [README.md - Move Preprocessed Files](README.md#1-move-preprocessed-files-movepreprocessed)
**Purpose**: Collect previously preprocessed files
**Key**: Also generates metadata for unprocessed files

---

#### `moveConverted()` - Archive Converted Files
**Purpose**: Move converted NIfTI files to preprocessed folder
**Location**: [STRUCTURE.md - API Reference](STRUCTURE.md#moveconverted)

---

#### `move2separate()` - Organize Hold-Out Data
**Purpose**: Separate robustness evaluation datasets
**Location**: [STRUCTURE.md - API Reference](STRUCTURE.md#move2separate)

---

## 📊 Data Flow Diagram

```
Raw Data (3T, DICOM)
    ↓
[Step 1] Move Preprocessed Files
    ↓
[Step 2] Move to Preprocessing Queue ← move2preprocess()
    ↓
    (PREPROCESSING HAPPENS ON WINDOWS)
    ↓
[Step 3] Move DICOM for Conversion ← move2convert()
    ↓
    (CONVERSION HAPPENS EXTERNALLY)
    ↓
[Step 4] Move Final Files ← freemove()
    ↓
Final Output
```

---

## 🎯 Common Tasks

### Task 1: Process All T1 Groups
```bash
for cond in AD CN MCI; do
    python scripts/run_pipeline.py --seq T1 --cond $cond --step all
done
```
→ See [QUICKSTART.md - Processing Multiple Groups](QUICKSTART.md#processing-multiple-groups)

---

### Task 2: Process Specific Step Only
```bash
python scripts/run_pipeline.py --seq T1 --cond AD --step move_to_preprocess
```
→ See [README.md - Master Pipeline Orchestrator](README.md#master-pipeline-orchestrator)

---

### Task 3: Move Custom File Types
```bash
python scripts/move_final_files.py --seq T1 --cond AD \
    --pattern "**/*n*.nii"  # normalized files
```
→ See [README.md - freemove() usage](README.md#5-move-final-processed-files-freemove)

---

### Task 4: Check Pipeline Status
```bash
python scripts/check_status.py
```
→ Shows file counts and available metadata

---

### Task 5: View Processing Logs
```bash
tail -f outputs/logs/*.log
```
→ Real-time monitoring of operations

---

## 🔧 Configuration & Customization

**Global Settings**: [src/config.py](src/config.py)

**Key Configuration Points**:
1. **Directory Paths**: Define input/output locations
2. **File Patterns**: Change which files to match
3. **Sequences & Conditions**: Default values
4. **Metadata Columns**: Expected CSV format
5. **Logging**: Log directory and format

→ See [README.md - Configuration](README.md#configuration)

---

## ❓ FAQ & Troubleshooting

### "Where do I start?"
1. Read [QUICKSTART.md](QUICKSTART.md) (5 min read)
2. Run `python scripts/check_status.py` (1 min setup)
3. Execute first script (varies)

### "What are the three main functions?"
1. **move2convert()** - DICOM organization
2. **move2preprocess()** - Raw file organization
3. **freemove()** - Flexible movement

All documented in [README.md](README.md)

### "How do I process all my data?"
See [QUICKSTART.md - Processing Multiple Groups](QUICKSTART.md#processing-multiple-groups)

### "How do I check if things are working?"
Run `python scripts/check_status.py`

### "How do I see what's happening?"
Check `outputs/logs/*.log` files

### "How do I customize behavior?"
Edit [src/config.py](src/config.py) or use command-line arguments

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Python Modules | 6 |
| Executable Scripts | 6 |
| Documentation Files | 5 |
| Total Code Lines | ~1,270 |
| Total Documentation Lines | ~1,600 |
| Functions Documented | 6 |
| Example Commands | 20+ |

---

## 🎓 Learning Path

**For Quick Start** (30 minutes):
1. [QUICKSTART.md](QUICKSTART.md) - Installation
2. Run first example
3. Check logs

**For Complete Understanding** (2-3 hours):
1. [README.md](README.md) - Overview & functions
2. [STRUCTURE.md](STRUCTURE.md) - Detailed architecture
3. [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md) - Diagrams

**For Advanced Usage** (1+ hours):
1. Read all .py files in `src/` and `scripts/`
2. Modify [src/config.py](src/config.py)
3. Create custom scripts using imported functions

**For Maintenance** (as needed):
1. Check [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for context
2. Reference function docstrings in code
3. Review logs in `outputs/logs/`

---

## 📝 File Locations Quick Reference

```
Documentation:
  • README.md                    ← Start here
  • QUICKSTART.md               ← Run commands
  • STRUCTURE.md                ← Technical details
  • PIPELINE_ARCHITECTURE.md    ← Visual guides
  • REFACTORING_SUMMARY.md      ← What changed
  
Code:
  • src/config.py               ← Global settings
  • src/metadata.py             ← Utilities
  • src/file_operations.py      ← Main functions
  • scripts/run_pipeline.py     ← Master script
  
Dependencies:
  • requirements.txt            ← Install these
```

---

## 🔗 Cross-References

### By Topic

**Understanding Functions**:
- [README.md - File Operations Functions](README.md#file-operations-functions)
- [STRUCTURE.md - Module Reference](STRUCTURE.md#module-reference)

**Running Commands**:
- [QUICKSTART.md - Basic Workflow](QUICKSTART.md#basic-workflow)
- [README.md - Master Pipeline](README.md#master-pipeline-orchestrator)

**Directory Structure**:
- [STRUCTURE.md - Processing Pipeline](STRUCTURE.md#processing-pipeline-steps)
- [PIPELINE_ARCHITECTURE.md - Data Organization](PIPELINE_ARCHITECTURE.md#data-organization-hierarchy)

**Configuration**:
- [src/config.py](src/config.py) (actual settings)
- [README.md - Configuration](README.md#configuration)

---

## ✅ Verification Checklist

Before running the pipeline:

- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python scripts/check_status.py`
- [ ] Verify directory structure exists
- [ ] Check `TempMeta/` has metadata CSVs
- [ ] Ensure write permissions for output

---

## 🆘 Getting Help

1. **"Where is function X documented?"**
   → Check [README.md](README.md) for main functions
   → Check [STRUCTURE.md](STRUCTURE.md) for complete API
   → Check function docstrings in code

2. **"How do I do X?"**
   → Check [QUICKSTART.md](QUICKSTART.md) for common tasks
   → Check [README.md](README.md) for examples

3. **"What went wrong?"**
   → Check logs in `outputs/logs/`
   → Run `python scripts/check_status.py`
   → Check [QUICKSTART.md - Troubleshooting](QUICKSTART.md#troubleshooting)

4. **"I want to customize behavior"**
   → Edit [src/config.py](src/config.py)
   → Use command-line arguments
   → See [README.md - Configuration](README.md#configuration)

---

## 📚 Document Sizes

| Document | Lines | Purpose |
|----------|-------|---------|
| README.md | ~470 | Main documentation |
| QUICKSTART.md | ~300 | Getting started |
| STRUCTURE.md | ~420 | Technical details |
| PIPELINE_ARCHITECTURE.md | ~300 | Visual guides |
| REFACTORING_SUMMARY.md | ~300 | What changed |
| This file | ~450 | Navigation guide |

**Total**: ~2,240 lines of documentation

---

## 🎯 One-Minute Overview

**ADNI Data Processing** is a Python package for organizing brain MRI data:

**Three Main Functions**:
1. `move2convert()` - Organize DICOM for conversion
2. `move2preprocess()` - Organize files for preprocessing  
3. `freemove()` - Flexible file movement

**To Use It**:
```bash
python scripts/run_pipeline.py --seq T1 --cond AD --step all
```

**To Learn More**:
- [QUICKSTART.md](QUICKSTART.md) - 5 minute quick start
- [README.md](README.md) - Complete documentation
- [STRUCTURE.md](STRUCTURE.md) - Technical details

---

**Last Updated**: December 29, 2025
**Version**: 1.0.0
**Status**: Production Ready ✓
