"""
Metadata utilities for handling and processing ADNI dataset metadata.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List


def createMetaCombinedString(meta_df: pd.DataFrame) -> List[str]:
    """
    Create combined metadata strings from dataframe for matching operations.
    
    Args:
        meta_df: Pandas DataFrame containing metadata
        
    Returns:
        List of combined ID strings (format: "subject_id-Iimage_id")
    """
    meta_combined = []
    for i in range(len(meta_df)):
        subject_id = meta_df.loc[i, "Subject"]
        image_id = meta_df.loc[i, "Image Data ID"]
        combined = f"{subject_id}-I{image_id}"
        meta_combined.append(combined)
    return meta_combined


def exportCSV(meta_dict: Dict, title: str, output_dir: str = "./TempMeta/") -> pd.DataFrame:
    """
    Export metadata dictionary to CSV file.
    
    Args:
        meta_dict: Dictionary containing metadata
        title: Title for the CSV file (will be saved as TempMeta/{title}.csv)
        output_dir: Output directory path
        
    Returns:
        Pandas DataFrame that was saved
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    temp_meta_df = pd.DataFrame(meta_dict)
    csv_file = output_path / f"{title}.csv"
    
    with open(csv_file, mode='w') as f:
        temp_meta_df.to_csv(f)
    
    print(f"Metadata exported to: {csv_file}")
    return temp_meta_df


def filterMetadata(meta_df: pd.DataFrame, **filters) -> pd.DataFrame:
    """
    Filter metadata based on specified criteria.
    
    Args:
        meta_df: Input metadata DataFrame
        **filters: Column name and value pairs for filtering
        
    Returns:
        Filtered DataFrame
    """
    result = meta_df.copy()
    for col, value in filters.items():
        if col in result.columns:
            result = result[result[col] == value]
    return result


def mergeMetadata(meta_list: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge multiple metadata DataFrames.
    
    Args:
        meta_list: List of DataFrames to merge
        
    Returns:
        Merged DataFrame
    """
    return pd.concat(meta_list, ignore_index=True)
