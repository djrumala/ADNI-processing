#!/usr/bin/env python3
"""
Pipeline status and diagnostics utility.
Shows current state of data directories and metadata.

Usage:
    python check_status.py
    python check_status.py --path ./path/to/ADNI-processing
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from libs.utils import (
    validate_directory_structure,
    ensure_output_directories,
    print_pipeline_status,
    list_available_metadata,
)


def main():
    parser = argparse.ArgumentParser(
        description="Check ADNI pipeline status"
    )
    parser.add_argument(
        "--path", type=str, default=".",
        help="Base path to ADNI-processing directory"
    )
    
    args = parser.parse_args()
    base_path = Path(args.path)
    
    if not base_path.exists():
        print(f"Error: Path does not exist: {base_path}")
        return 1
    
    # Ensure output directories
    print("Creating output directories...")
    ensure_output_directories(str(base_path))
    
    # Print status
    print_pipeline_status(str(base_path))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
