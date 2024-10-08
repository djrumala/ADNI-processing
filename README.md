# About Repository
This repo includes technical documentation for data preparation for 3D brain MR image classification using ADNI dataset.

We have used this data preprocessing and processing of ADNI dataset for several publications (see: [About Citation](https://github.com/djrumala/ADNI-processing#about-citation))

# Steps 
The whole data preparation process is started out by:
1. [Data Collecting](https://github.com/djrumala/ADNI-processing#data-collecting)
2. [Data Cleaning](https://github.com/djrumala/ADNI-processingp#data-cleaning)
3. [Data Preprocessing](https://github.com/djrumala/ADNI-processing#data-preprocessing)
4. [Data Augmentation](https://github.com/djrumala/ADNI-processing#data-augmentation)
5. [Data Loading](https://github.com/djrumala/ADNI-processing#data-loading)

# Data Collecting
The datasets are taken and downloaded from ADNI dataset here: `https://ida.loni.usc.edu/login.jsp`

Multispectral MRI datasets with 3 Tesla (3T) field strength of T1-weighted and T2-weighted are collected from ADNI1.

The original metadata of the downloaded files are saved inside the folder `/Metadata/` as `{seq}w_{group}_ADNI1_3T_{data download}.csv`


# Data Cleaning
Data cleaning follows several steps:
### 1. Generating list of relevant weighted MRI data 
The first data cleaning is to generate metadata of relevant MRI sequences from the original metadata.

As we know, MRI can generate more than one sequence (multi-spectral images) during a scan. In this case, according to [ADNI 1 Technical Procedures Manual](https://adni.loni.usc.edu/wp-content/uploads/2010/09/ADNI_MRI_Tech_Proc_Manual.pdf), when visitting for a scan, a subject will be asked for scans with the approved ADNI sequences. Two of the sequences include T1 (MP-RAGE) and T2 Dual Echo.

Relevant metadata of T1 is obtained by including only `MP-RAGE` from the `Description` column, and only `TSE/FSE` for T2. There is no use for filterring out certain visit times on `visit` column (in which such filter was used the first time to easily balance the data size for each group. And doing so will be hard to get pair of matched T1 and T2 that will be performed in Step 2. More details see the first but unused source code: `data_clean.ipynb`). 

Generated output from this process is saved inside the folder `/TempMeta/` with the file name `Cleaned_Ori_Nolimit_{seq}w_{group}_ADNI1_{tesla}T.csv.csv`

Source code: `data_cleaning_nolimit.ipynb`

### 2. Listing the pair of matched T1 and T2

We want to list the pair of matched T1 and T2 MRI data, meaning they are scans that come from one subject on a certain visit. 

In this step, coarse list of matched data is generated by comparing the values of several attributes (subject id, visit, and acquisition date) from the metadata of T1 and T2 data. Generated metadata is saved inside the folder `/TempMeta/` with the filename `Matched_Nolimit_{seq}w_{group}_ADNI1_3T_12_05_2022.csv`

However, generated metadata from this process still contains duplicated values. The counting of number of subjects and images generated from this list is performed in excel `Metadata_Matched_Nolimit.xlsx` on section `NotUnique_Count`

Source code: `data_matching.ipynb` (1st section)

### 3. Generate unique and balanced list of matched data

There are two generated list from this process:

1. Unique version of matched metadata in T1 and T2 (there are some missing data from T1, creating unbalanced list of matched data in T1 and T2)
2. Balanced version of matched metadata between T1 and T2 

More details are noted in the code.

Source code: `data_matching.ipynb` (2nd section)

### 4. Balancing data size of all groups
The process is performed manually in Excel. The intention is we want to balance the number of data of all groups both in T1 and T2. The result of this process is a metadata saved inside the folder of `/TempMeta/` with the filename `Balanced_Meta_{seq}w_{group}.csv`

The analysis of this process is available in Excel file: `Metadata_Balanced.xlsx`

### 5. Collecting and moving the to-be-preprocessed MRI data

There are three major steps in here:
1. Find and move the already preprocessed files and create list of not yet preprocessed files.
    - Compare the availability of the preprocessed files in folder `/preprocessed_old` with the generated final metadata in Step 4
    - The preprocessed files are moved to folder `/preprocessed/` with the filename `{meta id}-{original filename}.nii.gz.`
    - List of not yet preprocessed files is saved as metadata inside the folder `/TempMeta/` with the filename `To-Be-Preprocessed_{seq}w_{group}.csv`
    - Note: This step can be skipped if there is not yet preprocessed data, but might be useful later when there are missed preprocessed data during the preprocessing step.
2. Move the not yet preprocessed files
    - Path of the source files refers to the raw original directory. In this work, raw directory is `/3T/`
    - Comparing files available in the original directory with the generated metadata in step 5.1. 
    - The files will be moved to folder `/TempData/` and put inside a decent sub-directory that contains `{subject id}-{series id}-{image id}`
    - The files will be kept as its original filename
3. Move the new preprocessed files
    - Compare the availability of the additional preprocessed files in folder `/preprocessed_addition` with the generated final metadata in Step 4
    - The preprocessed files are moved to folder `/preprocessed/` with the filename `{meta id}-{original filename}.nii.gz.`
    - Note: do not move manually since we need the filename to be changed into the standard `{meta id}-{original filename}.nii.gz.`. This is important to notice the pair of matched T1 and T2

Source code: `data_final_move.ipynb`

# Data Cleaning of Hold-Out Datasets For Robustness Evaluation
We need new data (hold-out data) that has never been used before during training the models. It is necessary for robustness evaluation.
1. Filtering new data as hold-out dataset
    - Compare the metadata of the training datasets `Balanced_Meta_{seq}w_{group}.csv` with the metadata of the new collected datasets
    - Exclude data that comes from the same subjects / patients (no duplicate of `subject-id`)
    - Copy the data to the folder `/DataPrep`
    - Note: This step can be skipped if the data comes from different repository or database
2. Generate the metadata for the hold-out datasets and separate the data by group/class
    - Move the balanced hold-out data files to the folder `/DataSep/` and put inside a decent sub-directory that contains `{subject id}-{series id}-{image id}`
    - Save the generated metadata inside the folder `/TempMeta/` with the name `HoldOut_Cleaned_T1w_{group}_{Tesla}T.csv`
3. Balance the number of data per class
    - Balancing data per class is done manually by making sure that there is no duplicate subject
    - Move the balanced hold-out data files to the folder `/TempData/` and put inside a decent sub-directory that contains `{subject id}-{series id}-{image id}`
    - The metadata for the balanced hold-out datasets are saved inside the folder `/TempMeta/` with the name `HoldOut_Balanced_T1w_{group}_{Tesla}T.csv`

Source code: `data_final_move.ipynb` -in section Data Separation for Robustness Evaluation

# Data Preprocessing
Data preprocessing is performed using SPM, which includes the following process:
1. Data normalization / Intensity normalization
2. Skull-stripping
3. Data registration (matching to one template and put the brain in the standardized space)
4. Data scaling

# Data Augmentation
Due to unstable performance of the Deep Learning model, we have implemented data augmentation techniques to AD and other classes too in order to increase number of training and testing data. In this case, we added more images up to 300 data. 
The implemented data augmentation techniques include flipping and rotation. Flipping is applied to all 150 volume images of non AD group in T1 and T2 as well as to the volume images in AD group. All augmented images by flipping technique have been saved with the name `flip_filename`. Meanwhile, we also applied rotation only to AD group. 5 degree rotation is applied to the first half (25) dataset and -5 degree rotation is applied to the rest half dataset of AD group in T1 and T2. As we still need more data, we applied more rotation and flipping techniques to the AD group in T1 and T2. Thus, there are 5 kinds of data additions in AD group, which are `flip`, `rotP`, `rotM`, `rotP_flip`, `rotM_flip`. Therefore, eventually we obtained 300 volume images in AD group.

# Data Loading

Data loading is another important step in this experiment. During the data loading, we also need to make sure that the pairs of T1 and T2 data are fed together to the same model for the joint training technique. Besides, as we have all known, in order to prevent data leakage, data augmentation should be done after data splitting. However, in this experiment, we have first executed data augmentation. Since we want to do 5-fold cross validation and our data splitting is based on 70/10/20 separation for train/valid/test, we must build data loader that will load the data as if we performed proper data splitting (split the data before augmentation). To do that, we can make use of the `meta-id` in the file name. 

In this case, we have created the data loading algorithm for proper data splitting as presented in section `Load Dataset` in the codes. The codes are available in the main repository.

# About Citation
For more detail please refer to the publication: 

[1] Rumala, D.J. (2023). How You Split Matters: Data Leakage and Subject Characteristics Studies in Longitudinal Brain MRI Analysis. In: Wesarg, S., et al. Clinical Image-Based Procedures, Fairness of AI in Medical Imaging, and Ethical and Philosophical Issues in Medical Imaging . CLIP EPIMI FAIMI 2023 2023 2023. Lecture Notes in Computer Science, vol 14242. Springer, Cham. [https://doi.org/10.1007/978-3-031-45249-9_23](https://doi.org/10.1007/978-3-031-45249-9_23).

More information and comprehensive summary about this publication can be freely accessed here: [https://djrumala.github.io/publications/how-you-split-matters](https://djrumala.github.io/publications/how-you-split-matters)
