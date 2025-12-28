"""
Move raw NIFTI files that need preprocessing to TempData folder.
Organizes files with proper subdirectory structure for Windows preprocessing.

Usage:
    python move_to_preprocess.py --seq T1 --cond AD
    python move_to_preprocess.py --seq T2 --cond MCI --path ./3T
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.file_operations import move2preprocess
from libs.config import TEMP_META_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Move unprocessed files to preprocessing queue"
    )
    parser.add_argument("--seq", type=str, required=True, choices=["T1", "T2"],
                        help="MRI sequence")
    parser.add_argument("--cond", type=str, required=True, choices=["AD", "CN", "MCI"],
                        help="Condition")
    parser.add_argument("--path", type=str, default="./3T",
                        help="Source path with unprocessed files")
    parser.add_argument("--tesla", type=int, default=3,
                        help="Tesla field strength")
    
    args = parser.parse_args()
    
    # Load metadata for unprocessed files
    meta_csv = TEMP_META_DIR / f"To-Be-Preprocessed_{args.seq}w_{args.cond}.csv"
    if not meta_csv.exists():
        print(f"Error: Metadata file not found at {meta_csv}")
        print(f"Make sure to run move_preprocessed_files.py first")
        return 1
    
    meta_df = pd.read_csv(meta_csv)
    print(f"Loaded metadata with {len(meta_df)} records to preprocess")
    
    # Move files
    print(f"\nMoving {args.seq}w-{args.cond} files to preprocessing queue...")
    count = move2preprocess(
        meta_df=meta_df,
        seq=args.seq,
        cond=args.cond,
        tesla=args.tesla
    )
    
    print(f"\n✓ Moved {count} files to ./TempData/{args.seq}/{args.cond}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
