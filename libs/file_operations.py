"""
File operation utilities for moving and organizing ADNI MRI data.
Handles DICOM files, preprocessed files, and metadata-based file organization.
"""

import os
import shutil
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, List, Optional
from .metadata import createMetaCombinedString


def movePreprocessed(
    meta_df: pd.DataFrame,
    path: str,
    seq: str,
    cond: str,
    tesla: int = 3,
    divider: str = "raw_"
) -> Tuple[Dict, List[int]]:
    """
    Move preprocessed files from source to target directory and track unprocessed files.
    
    Args:
        meta_df: Metadata DataFrame
        path: Source path containing preprocessed files
        seq: Sequence type (T1 or T2)
        cond: Condition (AD, CN, or MCI)
        tesla: Tesla field strength (1.5 or 3)
        divider: Divider string in filename to parse IDs
        
    Returns:
        Tuple of (metadata_dict for unprocessed files, list of metadata indices)
    """
    target_path = "./preprocessed/"
    search_path = Path(path) / seq / cond
    
    print(f"Searching in: {search_path}")
    
    result = list(search_path.glob('**/wm*.nii'))
    unique = set(result)
    print(f"---------\n{seq}w-{cond}\nOriginal number of files: {len(result)}\nUnique result: {len(unique)}")
    
    sim = 0
    notsim = 0
    j = 0
    target_dir = Path(target_path) / seq / cond
    target_dir.mkdir(parents=True, exist_ok=True)
    
    meta_combined = createMetaCombinedString(meta_df)
    meta_dict = {
        "Image Data ID": [],
        "Subject": [],
        "Group": [],
        "Sex": [],
        "Age": [],
        "Visit": [],
        "Modality": [],
        "Description": [],
        "Type": [],
        "Acq Date": [],
        "Format": []
    }
    
    for j in range(len(meta_combined)):
        flag = 0
        for f in result[:]:
            pathToFile = str(f)
            fileName = Path(pathToFile).name
            fileNameNoExt = fileName.split(".nii")[0]
            
            try:
                part = fileNameNoExt.split('_MR')
                id_subject = part[0].split("ADNI_")[1]
                part = part[1].split(divider)[1]
                id_series = part.split("_S")[1].split("_I")[0]
                id_image = fileNameNoExt.split("_I")[1]
                
                combinedIDs = f"{id_subject}-I{id_image}"
                
                if combinedIDs in meta_combined[j]:
                    shutil.copy(f, target_dir / f"{j}-{fileName}")
                    flag = 1
            except IndexError:
                continue
        
        if flag == 1:
            sim += 1
        else:
            meta_dict["Image Data ID"].append(meta_df.loc[j, "Image Data ID"])
            meta_dict["Subject"].append(meta_df.loc[j, "Subject"])
            meta_dict["Group"].append(meta_df.loc[j, "Group"])
            meta_dict["Sex"].append(meta_df.loc[j, "Sex"])
            meta_dict["Age"].append(meta_df.loc[j, "Age"])
            meta_dict["Visit"].append(meta_df.loc[j, "Visit"])
            meta_dict["Modality"].append(meta_df.loc[j, "Modality"])
            meta_dict["Description"].append(meta_df.loc[j, "Description"])
            meta_dict["Type"].append(meta_df.loc[j, "Type"])
            meta_dict["Acq Date"].append(meta_df.loc[j, "Acq Date"])
            meta_dict["Format"].append(meta_df.loc[j, "Format"])
            notsim += 1
    
    print(f"Total {seq}w-{cond} data is {sim} and not preprocessed is {notsim}")
    return meta_dict, [i for i in range(len(meta_combined)) if i not in [j for j in range(len(meta_dict['Image Data ID']))]]


def freemove(
    source_path: str,
    target_path: str,
    seq: str,
    cond: str,
    tesla: int = 3,
    file_format: str = '**/*wm*.nii'
) -> int:
    """
    Move files based on filename pattern matching.
    Flexible function for moving preprocessed or other processed files.
    
    Args:
        source_path: Source directory path
        target_path: Target directory path
        seq: Sequence type (T1 or T2)
        cond: Condition (AD, CN, or MCI)
        tesla: Tesla field strength
        file_format: Glob pattern for file matching (default: white matter segmented files)
        
    Returns:
        Count of files moved
    """
    target_dir = Path(target_path) / seq / cond
    target_dir.mkdir(parents=True, exist_ok=True)
    
    search_path = Path(source_path) / seq / cond
    print(f"Source path: {search_path}")
    print(f"Exists: {search_path.exists()}")
    
    result = sorted(list(search_path.glob(file_format)))
    unique = set(result)
    print(f"----\n{seq}-{cond}\nOriginal number of files: {len(result)}\nUnique result: {len(unique)}")
    
    j = 0
    for f in result:
        pathToFile = str(f)
        fileName = Path(pathToFile).name
        
        if "ADNI" in fileName:
            print(f"Moving: {fileName}")
            shutil.copy(f, target_dir / f"{j}-{fileName}")
            j += 1
    
    print(f"Total files moved: {j}")
    return j


def move2preprocess(
    meta_df: pd.DataFrame,
    seq: str,
    cond: str,
    tesla: int = 3,
    divider: str = "raw_"
) -> int:
    """
    Move files that need preprocessing to designated folder with proper organization.
    Creates subdirectories for each subject-series-image combination.
    
    Args:
        meta_df: Metadata DataFrame
        seq: Sequence type (T1 or T2)
        cond: Condition (AD, CN, or MCI)
        tesla: Tesla field strength
        divider: Divider string in filename to parse IDs
        
    Returns:
        Count of files moved
    """
    nii_path = f"./3T/{seq}/"
    target_path = "./TempData/"
    
    print(f"Source path: {nii_path}{cond}/")
    
    result = list(Path(nii_path).glob(f'**/*{cond}/**/*.nii'))
    unique = set(result)
    print(f"---------\n{seq}w-{cond}\nOriginal number: {len(result)}\nUnique result: {len(unique)}")
    
    sim = 0
    ctr = 0
    
    for ctr in range(len(meta_df)):
        flag = 0
        for f in result[:]:
            pathToFile = str(f)
            fileName = Path(pathToFile).name
            fileNameNoExt = fileName.split(".nii")[0]
            
            try:
                part = fileNameNoExt.split('_MR')
                id_subject = part[0].split("ADNI_")[1]
                part = part[1].split(divider)[1]
                id_series = part.split("_S")[1].split("_I")[0]
                id_image = fileNameNoExt.split("_I")[1]
                
                subdirName = f"{id_subject}-{id_series}-{id_image}"
                meta_combined = f"{id_subject}-I{id_image}"
                
                meta_combined_list = createMetaCombinedString(meta_df)
                
                if meta_combined in meta_combined_list[ctr]:
                    target_dir = Path(target_path) / seq / cond / subdirName
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f, target_dir / fileName)
                    flag = 1
                    sim += 1
            except (IndexError, ValueError):
                continue
    
    print(f"Total {seq}w - {cond} data is {sim}")
    return sim


def move2convert(
    meta_df: pd.DataFrame,
    seq: str,
    cond: str,
    tesla: int = 3,
    divider: str = "raw_"
) -> int:
    """
    Move DICOM files to conversion folder with proper directory structure.
    Organizes files by series and image ID for DICOM to NIfTI conversion.
    
    Args:
        meta_df: Metadata DataFrame
        seq: Sequence type (T1 or T2)
        cond: Condition (AD, CN, or MCI)
        tesla: Tesla field strength
        divider: Divider string in filename to parse IDs
        
    Returns:
        Count of files moved
    """
    dicom_path = f"./DICOM/{seq}/{cond}/"
    target_path = "./2convert/"
    
    print(f"Source DICOM path: {dicom_path}")
    
    result = list(Path(dicom_path).glob('**/*.dcm'))
    unique = set(result)
    print(f"---------\n{seq}w-{cond}\nOriginal number: {len(result)}\nUnique result: {len(unique)}")
    
    sim = 0
    ctr = 0
    
    for ctr in range(len(meta_df)):
        flag = 0
        for f in result[:]:
            pathToFile = str(f)
            fileName = Path(pathToFile).name
            
            try:
                # Extract IDs from path structure (assuming nested folder structure)
                parts = Path(pathToFile).parts
                # Adjust indexing based on your actual folder structure
                if len(parts) > 3:
                    id_subject = meta_df.loc[ctr, "Subject"]
                    id_series = meta_df.loc[ctr, "Image Data ID"]
                    id_image = meta_df.loc[ctr, "Image Data ID"]
                    
                    subdirName = f"{id_subject}-{id_series}_{id_image}"
                    target_dir = Path(target_path) / seq / cond / subdirName
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f, target_dir / fileName)
                    flag = 1
                    sim += 1
            except (IndexError, ValueError):
                continue
    
    print(f"Total {seq}w - {cond} data is {sim}")
    return sim


def moveConverted(
    meta_df: pd.DataFrame,
    seq: str,
    cond: str,
    tesla: int = 3,
    divider: str = "br_"
) -> int:
    """
    Move converted NIfTI files from conversion folder to preprocessed folder.
    
    Args:
        meta_df: Metadata DataFrame
        seq: Sequence type (T1 or T2)
        cond: Condition (AD, CN, or MCI)
        tesla: Tesla field strength
        divider: Divider string in filename to parse IDs
        
    Returns:
        Count of files moved
    """
    nii_path = f"./Converted/{seq}/{cond}/"
    target_path = "./preprocessed/"
    
    print(f"Source NIfTI path: {nii_path}")
    
    result = list(Path(nii_path).glob('**/wm*.nii'))
    unique = set(result)
    print(f"---------\n{seq}w-{cond}\nOriginal number: {len(result)}\nUnique result: {len(unique)}")
    
    sim = 0
    j = 0
    target_dir = Path(target_path) / seq / cond
    target_dir.mkdir(parents=True, exist_ok=True)
    
    meta_combined = createMetaCombinedString(meta_df)
    
    for j in range(len(meta_combined)):
        flag = 0
        for f in result[:]:
            pathToFile = str(f)
            fileName = Path(pathToFile).name
            fileNameNoExt = fileName.split(".nii")[0]
            
            try:
                part = fileNameNoExt.split('_MR')
                id_subject = part[0].split("ADNI_")[1]
                part = part[1].split(divider)[1]
                id_series = part.split("_S")[1].split("_I")[0]
                id_image = fileNameNoExt.split("_I")[1]
                
                combinedIDs = f"{id_subject}-I{id_image}"
                
                if combinedIDs in meta_combined[j]:
                    shutil.copy(f, target_dir / f"{j}-{fileName}")
                    flag = 1
                    sim += 1
            except IndexError:
                continue
    
    print(f"Total {seq}w - {cond} data is {sim}")
    return sim


def move2separate(
    meta_df: pd.DataFrame,
    seq: str,
    tesla: int = 3,
    ONLY_BASELINE: bool = False,
    divider: str = "Br_"
) -> int:
    """
    Move and separate data into organized folder structure for robustness evaluation.
    
    Args:
        meta_df: Metadata DataFrame
        seq: Sequence type (T1 or T2)
        tesla: Tesla field strength
        ONLY_BASELINE: Filter only baseline visits
        divider: Divider string in filename to parse IDs
        
    Returns:
        Count of files processed
    """
    nii_path = f"./DataOri/{tesla}T/{seq}/"
    target_path = "./DataSep/"
    
    print(f"Source path: {nii_path}")
    
    result = sorted(list(Path(nii_path).glob('**/*.nii')))
    unique = set(result)
    print(f"---------\n{seq}w\nOriginal number: {len(result)}\nUnique result: {len(unique)}")
    
    sim = 0
    ctr = 0
    
    meta_combined = createMetaCombinedString(meta_df)
    
    for ctr in range(len(meta_combined)):
        flag = 0
        for f in result[:]:
            pathToFile = str(f)
            fileName = Path(pathToFile).name
            
            try:
                # Match metadata
                for meta_id, meta_str in enumerate(meta_combined):
                    if str(ctr) in str(meta_id):
                        id_subject = meta_df.loc[ctr, "Subject"]
                        id_series = meta_df.loc[ctr, "Image Data ID"]
                        subdirName = f"{id_subject}-{id_series}"
                        
                        target_dir = Path(target_path) / seq / subdirName
                        target_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy(f, target_dir / fileName)
                        flag = 1
                        sim += 1
                        break
            except (IndexError, ValueError):
                continue
    
    print(f"Total {seq} data is {sim}")
    return sim
