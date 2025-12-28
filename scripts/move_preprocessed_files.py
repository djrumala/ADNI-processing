"""
Move already preprocessed files from old location to preprocessed folder.
Handles previously processed data from preprocessed_old directory.

Usage:
    python move_preprocessed_files.py --seq T1 --cond AD --path ./preprocessed_old
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.file_operations import movePreprocessed
from libs.metadata import exportCSV
from libs.config import TEMP_META_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Move preprocessed files to target directory"
    )
    parser.add_argument("--seq", type=str, required=True, choices=["T1", "T2"],
                        help="MRI sequence (T1 or T2)")
    parser.add_argument("--cond", type=str, required=True, choices=["AD", "CN", "MCI"],
                        help="Condition (AD, CN, or MCI)")
    parser.add_argument("--path", type=str, default="./preprocessed_old",
                        help="Source path containing preprocessed files")
    parser.add_argument("--tesla", type=int, default=3, choices=[1, 2, 3],
                        help="Tesla field strength")
    parser.add_argument("--divider", type=str, default="raw_",
                        help="Divider string in filename")
    
    args = parser.parse_args()
    
    # Load metadata
    meta_csv = TEMP_META_DIR / f"Balanced_Meta_{args.seq}w_{args.cond}.csv"
    if not meta_csv.exists():
        print(f"Error: Metadata file not found at {meta_csv}")
        return 1
    
    meta_df = pd.read_csv(meta_csv)
    print(f"Loaded metadata with {len(meta_df)} records")
    
    # Move files
    print(f"\nMoving preprocessed {args.seq}w-{args.cond} files...")
    meta_dict, meta_nums = movePreprocessed(
        meta_df=meta_df,
        path=args.path,
        seq=args.seq,
        cond=args.cond,
        tesla=args.tesla,
        divider=args.divider
    )
    
    # Export unprocessed files list
    if meta_dict["Image Data ID"]:
        unprocessed_df = exportCSV(
            meta_dict,
            title=f"To-Be-Preprocessed_{args.seq}w_{args.cond}",
            output_dir=str(TEMP_META_DIR)
        )
        print(f"\nExported {len(unprocessed_df)} unprocessed files to metadata")
    
    print("\n✓ Task completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
