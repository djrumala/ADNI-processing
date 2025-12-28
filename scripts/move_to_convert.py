"""
Move DICOM files to conversion folder with proper organization.
Prepares files for DICOM to NIfTI conversion.

Usage:
    python move_to_convert.py --seq T1 --cond AD
    python move_to_convert.py --seq T2 --cond CN --path ./DICOM
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.file_operations import move2convert
from libs.config import TEMP_META_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Move DICOM files to conversion queue"
    )
    parser.add_argument("--seq", type=str, required=True, choices=["T1", "T2"],
                        help="MRI sequence")
    parser.add_argument("--cond", type=str, required=True, choices=["AD", "CN", "MCI"],
                        help="Condition")
    parser.add_argument("--path", type=str, default="./DICOM",
                        help="Source path with DICOM files")
    parser.add_argument("--tesla", type=int, default=3,
                        help="Tesla field strength")
    
    args = parser.parse_args()
    
    # Load metadata
    meta_csv = TEMP_META_DIR / f"Balanced_Meta_{args.seq}w_{args.cond}.csv"
    if not meta_csv.exists():
        print(f"Error: Metadata file not found at {meta_csv}")
        return 1
    
    meta_df = pd.read_csv(meta_csv)
    print(f"Loaded metadata with {len(meta_df)} records")
    
    # Move DICOM files
    print(f"\nMoving {args.seq}w-{args.cond} DICOM files to conversion queue...")
    count = move2convert(
        meta_df=meta_df,
        seq=args.seq,
        cond=args.cond,
        tesla=args.tesla
    )
    
    print(f"\n✓ Moved {count} files to ./2convert/{args.seq}/{args.cond}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
