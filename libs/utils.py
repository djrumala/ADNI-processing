"""
Utility functions for ADNI data processing.
"""

import os
from pathlib import Path
from typing import List, Dict
import pandas as pd


def validate_directory_structure(base_path: str) -> Dict[str, bool]:
    """
    Validate required directory structure exists.
    
    Args:
        base_path: Base directory path
        
    Returns:
        Dictionary showing which directories exist
    """
    base = Path(base_path)
    required_dirs = {
        "3T": base / "3T",
        "DICOM": base / "DICOM",
        "preprocessed_old": base / "preprocessed_old",
        "TempMeta": base / "TempMeta",
    }
    
    validation = {}
    for name, path in required_dirs.items():
        validation[name] = path.exists()
    
    return validation


def ensure_output_directories(base_path: str) -> None:
    """
    Create output directories if they don't exist.
    
    Args:
        base_path: Base directory path
    """
    output_dirs = [
        "preprocessed",
        "TempData",
        "2convert",
        "Converted",
        "final",
        "outputs/logs",
    ]
    
    base = Path(base_path)
    for dir_name in output_dirs:
        dir_path = base / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Ensured directory: {dir_path}")


def count_files_in_directory(path: str, pattern: str = "**/*") -> int:
    """
    Count files in directory matching pattern.
    
    Args:
        path: Directory path
        pattern: Glob pattern (default: all files)
        
    Returns:
        Count of matching files
    """
    dir_path = Path(path)
    if not dir_path.exists():
        return 0
    return len(list(dir_path.glob(pattern)))


def get_directory_summary(base_path: str) -> Dict[str, int]:
    """
    Get summary of file counts in key directories.
    
    Args:
        base_path: Base directory path
        
    Returns:
        Dictionary with directory names and file counts
    """
    base = Path(base_path)
    
    directories = {
        "3T (Raw)": count_files_in_directory(base / "3T", "**/*.nii"),
        "DICOM": count_files_in_directory(base / "DICOM", "**/*.dcm"),
        "Preprocessed Old": count_files_in_directory(base / "preprocessed_old", "**/*.nii"),
        "Preprocessed": count_files_in_directory(base / "preprocessed", "**/*.nii"),
        "TempData": count_files_in_directory(base / "TempData", "**/*.nii"),
        "2Convert": count_files_in_directory(base / "2convert", "**/*.dcm"),
        "Final": count_files_in_directory(base / "final", "**/*.nii"),
    }
    
    return directories


def list_available_metadata(meta_dir: str) -> List[str]:
    """
    List available metadata CSV files.
    
    Args:
        meta_dir: Metadata directory path
        
    Returns:
        List of metadata CSV filenames
    """
    meta_path = Path(meta_dir)
    if not meta_path.exists():
        return []
    
    csv_files = [f.name for f in meta_path.glob("*.csv")]
    return sorted(csv_files)


def validate_metadata_csv(csv_path: str, required_columns: List[str] = None) -> bool:
    """
    Validate metadata CSV file structure.
    
    Args:
        csv_path: Path to CSV file
        required_columns: List of required column names
        
    Returns:
        True if valid, False otherwise
    """
    if required_columns is None:
        required_columns = [
            "Image Data ID", "Subject", "Group", "Sex", "Age",
            "Visit", "Modality", "Description", "Type", "Acq Date", "Format"
        ]
    
    try:
        df = pd.read_csv(csv_path)
        missing = set(required_columns) - set(df.columns)
        if missing:
            print(f"Missing columns: {missing}")
            return False
        return True
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False


def print_pipeline_status(base_path: str) -> None:
    """
    Print pipeline status and statistics.
    
    Args:
        base_path: Base directory path
    """
    print("\n" + "="*70)
    print("ADNI Data Processing Pipeline Status")
    print("="*70)
    
    # Check directories
    validation = validate_directory_structure(base_path)
    print("\nRequired Directories:")
    for name, exists in validation.items():
        status = "✓" if exists else "✗"
        print(f"  {status} {name}")
    
    # File counts
    print("\nFile Counts:")
    summary = get_directory_summary(base_path)
    for name, count in summary.items():
        print(f"  {name}: {count}")
    
    # Available metadata
    print("\nAvailable Metadata CSVs:")
    meta_files = list_available_metadata(Path(base_path) / "TempMeta")
    if meta_files:
        for meta_file in meta_files:
            print(f"  • {meta_file}")
    else:
        print("  (No metadata files found)")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent
    
    # Ensure output directories exist
    print("Creating output directories...")
    ensure_output_directories(str(base_path))
    
    # Print status
    print_pipeline_status(str(base_path))
