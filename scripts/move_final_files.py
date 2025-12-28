"""
Move converted NIfTI files to final preprocessed folder.
Flexible function that moves any files based on pattern matching.

Usage:
    python move_final_files.py --seq T1 --cond AD --source ./processed --target ./final
    python move_final_files.py --seq T2 --cond MCI --pattern '**/*wm*.nii'
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.file_operations import freemove


def main():
    parser = argparse.ArgumentParser(
        description="Move final preprocessed files using pattern matching"
    )
    parser.add_argument("--seq", type=str, required=True, choices=["T1", "T2"],
                        help="MRI sequence")
    parser.add_argument("--cond", type=str, required=True, choices=["AD", "CN", "MCI"],
                        help="Condition")
    parser.add_argument("--source", type=str, default="./processed",
                        help="Source directory")
    parser.add_argument("--target", type=str, default="./final",
                        help="Target directory")
    parser.add_argument("--pattern", type=str, default="**/*wm*.nii",
                        help="File glob pattern to match")
    parser.add_argument("--tesla", type=int, default=3,
                        help="Tesla field strength")
    
    args = parser.parse_args()
    
    # Move files
    print(f"Moving {args.seq}w-{args.cond} files from {args.source} to {args.target}")
    print(f"Using pattern: {args.pattern}")
    
    count = freemove(
        source_path=args.source,
        target_path=args.target,
        seq=args.seq,
        cond=args.cond,
        tesla=args.tesla,
        file_format=args.pattern
    )
    
    print(f"\n✓ Successfully moved {count} files to {args.target}/{args.seq}/{args.cond}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
