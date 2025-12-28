"""
Master workflow script for entire ADNI data processing pipeline.
Orchestrates all steps from preprocessing to final file organization.

Usage:
    python run_pipeline.py --config config.yaml
    python run_pipeline.py --seq T1 --cond AD --step all
    python run_pipeline.py --seq T1 --cond AD --step move_preprocessed
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from libs.config import OUTPUT_DIR, LOG_DIR
import subprocess


def run_step(step_name, script_path, args_dict):
    """Run a pipeline step."""
    print(f"\n{'='*70}")
    print(f"Step: {step_name}")
    print(f"{'='*70}")
    
    cmd = ["python", str(script_path)]
    for key, value in args_dict.items():
        if value:
            cmd.extend([f"--{key}", str(value)])
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {step_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="ADNI Data Processing Pipeline"
    )
    parser.add_argument("--seq", type=str, choices=["T1", "T2"],
                        help="MRI sequence to process")
    parser.add_argument("--cond", type=str, choices=["AD", "CN", "MCI"],
                        help="Condition to process")
    parser.add_argument("--step", type=str, 
                        choices=["all", "move_preprocessed", "move_to_preprocess", 
                                 "move_to_convert", "move_final"],
                        default="all",
                        help="Which step(s) to run")
    parser.add_argument("--old-path", type=str, default="./preprocessed_old",
                        help="Path to old preprocessed files")
    parser.add_argument("--source-path", type=str, default="./processed",
                        help="Path to processed files")
    parser.add_argument("--target-path", type=str, default="./final",
                        help="Path for final output")
    
    args = parser.parse_args()
    
    if not args.seq or not args.cond:
        print("Error: --seq and --cond are required")
        return 1
    
    # Create output and log directories
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Log file
    log_file = LOG_DIR / f"pipeline_{args.seq}_{args.cond}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    print(f"\n{'='*70}")
    print(f"ADNI Data Processing Pipeline")
    print(f"Sequence: {args.seq}, Condition: {args.cond}")
    print(f"Log file: {log_file}")
    print(f"{'='*70}")
    
    base_args = {"seq": args.seq, "cond": args.cond}
    scripts_dir = Path(__file__).parent
    
    # Define pipeline steps
    steps = []
    
    if args.step == "all" or args.step == "move_preprocessed":
        steps.append((
            "Move Preprocessed Files",
            scripts_dir / "move_preprocessed_files.py",
            {**base_args, "path": args.old_path}
        ))
    
    if args.step == "all" or args.step == "move_to_preprocess":
        steps.append((
            "Move Files to Preprocessing Queue",
            scripts_dir / "move_to_preprocess.py",
            base_args
        ))
    
    if args.step == "all" or args.step == "move_to_convert":
        steps.append((
            "Move DICOM Files to Conversion Queue",
            scripts_dir / "move_to_convert.py",
            base_args
        ))
    
    if args.step == "all" or args.step == "move_final":
        steps.append((
            "Move Final Preprocessed Files",
            scripts_dir / "move_final_files.py",
            {**base_args, "source": args.source_path, "target": args.target_path}
        ))
    
    # Execute steps
    completed = 0
    failed = 0
    
    for step_name, script_path, step_args in steps:
        if run_step(step_name, script_path, step_args):
            completed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Pipeline Summary")
    print(f"{'='*70}")
    print(f"Completed: {completed}")
    print(f"Failed: {failed}")
    print(f"Log file: {log_file}")
    print(f"{'='*70}\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
