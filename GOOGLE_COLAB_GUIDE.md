# Google Colab Execution Guide

**Project:** Strict Scientific Reproduction & Audit of Sentinel-2 Mangrove Species Classification  
**Reference Paper:** *Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961*  
**Paper DOI:** [10.1016/j.ecoinf.2024.102961](https://doi.org/10.1016/j.ecoinf.2024.102961)  
**Dataset DOI:** [10.5063/F1FN14P1](https://doi.org/10.5063/F1FN14P1)  

---

## 1. Overview & Executive Summary

This guide provides step-by-step instructions for running the complete 8-notebook reproduction suite in **Google Colab** (Free or Pro tiers).

The repository is structured to be **100% executable in Google Colab**. Because the raw Sentinel-2 reflectance dataset is 191 MB (exceeding standard Git LFS / GitHub upload thresholds without external storage), this guide includes automated `wget` commands that fetch the official dataset directly from the DataONE / Knowledge Network for Biocomplexity (KNB) repository.

---

## 2. Quick Start: The 1-Cell Master Runner (Recommended)

If you want to clone the repository, install dependencies, fetch the dataset, and execute all 8 notebooks sequentially in a single automated run, open a **New Google Colab Notebook** and run this single cell:

```python
# ==============================================================================
# COMPLETE REPRODUCTION FAST TRACK (Google Colab 1-Cell Execution)
# ==============================================================================

# 1. Clone the repository
!git clone https://github.com/notfawkes/Mangroves-Blue-Carbon.git
%cd /content/Mangroves-Blue-Carbon

# 2. Install required packages
!pip install -q -r requirements.txt

# 3. Create raw data directory and download official KNB dataset (191 MB CSV + EML XML)
!mkdir -p data/raw
print("Downloading official Sentinel-2 dataset from KNB repository (doi:10.5063/F1FN14P1)...")
!wget -q --show-progress -O data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv \
  "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/urn:uuid:dea9b281-1f49-485c-bab8-65fc7eca6685"
!wget -q -O data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml \
  "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/doi:10.5063/F1FN14P1"
print("Data download complete.")

# 4. Run automated test suite
!pytest tests/test_reproduction.py -v

# 5. Execute all 8 notebooks sequentially and render outputs
!python run_notebooks.py
```

*Estimated Execution Time: ~8–12 minutes on Colab standard CPU, ~4–6 minutes on T4 GPU.*

---

## 3. Step-by-Step Interactive Workflow

If you prefer to run the notebooks interactively one by one, follow these steps.

### Step 1: Open Google Colab & Select Runtime
1. Navigate to [Google Colab](https://colab.research.google.com/).
2. Create a new notebook (or open an existing one).
3. Select your desired runtime accelerator:
   - Menu: **Runtime** $\rightarrow$ **Change runtime type**
   - **Hardware accelerator**: Select **T4 GPU** (faster MLP grid training) or **CPU** (fully supported; total training takes under 10 minutes).
   - Click **Save**.

### Step 2: Clone Repository & Navigate to Workspace
In a new code cell, run:
```python
!git clone https://github.com/notfawkes/Mangroves-Blue-Carbon.git
%cd /content/Mangroves-Blue-Carbon
```

### Step 3: Install Required Dependencies
Colab comes with PyTorch, NumPy, and Pandas pre-installed. Run this cell to ensure all version requirements (including `statsmodels` for Tukey HSD) match:
```python
!pip install -q -r requirements.txt
```

### Step 4: Download Official Raw Datasets
Because the 191 MB CSV (`DataBase_Sentinel_2_Mangrove_LaMancha.csv`) is excluded from GitHub via `.gitignore`, download the official files directly from the KNB DataONE repository into `data/raw/`:

```python
!mkdir -p data/raw

# Download Sentinel-2 Reflectance Database (191 MB, 1,605,681 rows)
!wget -q --show-progress -O data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv \
  "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/urn:uuid:dea9b281-1f49-485c-bab8-65fc7eca6685"

# Download EML XML Metadata
!wget -q -O data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml \
  "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/doi:10.5063/F1FN14P1"

# Verify file sizes
!ls -lh data/raw/
```
You should see:
- `DataBase_Sentinel_2_Mangrove_LaMancha.csv`: ~191 MB
- `Sentinel_2_satellite_reflectance_of_monospecific.xml`: ~16 KB

### Step 5: Verify Setup with Unit Tests
Execute the unit test suite to verify data schemas, sampling logic, `StandardScaler` behavior, model dimensions, and seed determinism:
```python
!pytest tests/test_reproduction.py -v
```
*Expected result: 6 passed in ~1.5 seconds.*

---

## 4. Notebook Execution Sequence & Details

The 8 notebooks are designed to be executed sequentially. Here is the purpose, dependencies, and outputs of each:

| # | Notebook | Purpose & Method | Prerequisite | Est. Runtime | Key Outputs |
|:---:|---|---|---|:---:|---|
| **01** | `01_dataset_audit.ipynb` | Audits EML XML schema, row count (1,605,681), 10 spectral bands, null check, and 147 scene IDs. | `data/raw/` | ~2s | `results/dataset_audit.json` |
| **02** | `02_exploratory_analysis.ipynb` | Extracts mean reflectance signatures (490–2190 nm), 10-band correlation matrix, and Red/NIR/SWIR density distributions. | `data/raw/` | ~4s | `spectral_signatures.png`, `band_correlation_matrix.png` |
| **03** | `03_anova_tukey.ipynb` | One-Way ANOVA across 10 bands ($p < 10^{-10}$) and 30 pairwise Tukey HSD tests ($p < 0.001$). Replicates Figure 4 boxplots. | `data/raw/` | ~6s | `reproduced_figure4_boxplots.png`, `anova_results.csv`, `tukey_results.csv` |
| **04** | `04_three_class_mangrove_mlp.ipynb` | Trains 41 model architectures (Logistic Baseline + 40 MLPs: 1–5 hidden layers, 5–500 neurons) on 30k balanced pixels (10k/species) with 70/30 split. | `data/raw/` | ~4–8 min | `three_class_mangrove_results.csv`, `three_class_confusion_matrix.png` |
| **05** | `05_paper_models_transcription_and_analysis.ipynb` | Transcribes the paper's published binary (60k) and 4-class (40k) results from Sections 3.2 & 3.3. | None | ~2s | `paper_reported_binary.csv`, `paper_reported_multiclass.csv` |
| **06** | `06_architecture_comparison.ipynb` | Compares published 4-class results with our 3-species results across identical architectures. Analyzes scaling laws. | Output of 04 & 05 | ~2s | `architecture_comparison.csv`, `depth_width_scaling_3species.png` |
| **07** | `07_spatial_validation.ipynb` | Audits spatial reproduction feasibility; documents why raw satellite raster inference is `DATA-LIMITED` (GeoTIFFs unreleased). | None | ~1s | `spatial_audit_summary.json` |
| **08** | `08_paper_vs_reproduction.ipynb` | Dedicated 13-section research-grade accuracy comparison & discrepancy analysis. Renders 7 publication plots and final CEP summary. | Output of 04, 05, 06 | ~3s | `paper_vs_our_accuracy_comparison.png`, `training_vs_test_accuracy_gap.png`, etc. |

---

## 5. Universal Colab Setup Snippet for Individual Notebooks

If you open any individual notebook directly in Colab (via **File** $\rightarrow$ **Open notebook** $\rightarrow$ **GitHub** or by uploading the `.ipynb` file), insert this **universal setup cell** at the very top of the notebook before executing Cell 1:

```python
# --- UNIVERSAL GOOGLE COLAB INITIALIZATION CELL ---
import os, sys
from pathlib import Path

# Detect if running in Google Colab
if 'google.colab' in str(get_ipython()):
    # 1. Clone repository if not present
    if not os.path.exists('/content/Mangroves-Blue-Carbon'):
        !git clone https://github.com/notfawkes/Mangroves-Blue-Carbon.git /content/Mangroves-Blue-Carbon

    # 2. Change working directory to notebooks/ (ensures relative paths resolve identically to local execution)
    %cd /content/Mangroves-Blue-Carbon/notebooks

    # 3. Add repo root to sys.path so 'import src' works seamlessly
    repo_root = '/content/Mangroves-Blue-Carbon'
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    # 4. Download raw dataset if missing
    !mkdir -p /content/Mangroves-Blue-Carbon/data/raw
    csv_file = '/content/Mangroves-Blue-Carbon/data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv'
    if not os.path.exists(csv_file):
        print("Fetching Sentinel-2 raw dataset (191 MB) from KNB repository...")
        !wget -q --show-progress -O {csv_file} "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/urn:uuid:dea9b281-1f49-485c-bab8-65fc7eca6685"
        !wget -q -O /content/Mangroves-Blue-Carbon/data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/doi:10.5063/F1FN14P1"
        print("Dataset ready.")
```

> **Why is this necessary in Colab?**  
> In local execution, launching Jupyter from the `notebooks/` directory sets the current working directory to `notebooks/`, and `Path("..").resolve()` resolves to the project root. In Colab, the default working directory is `/content`. Running `%cd /content/Mangroves-Blue-Carbon/notebooks` and inserting the repository root into `sys.path` guarantees that all module imports (`from src.config import ...`) and file paths resolve seamlessly without modifying any notebook code.

---

## 6. Running Headless from Terminal/Code Cell

You can run individual notebooks headless via Python in Colab:

```python
%cd /content/Mangroves-Blue-Carbon

# Run a single notebook and populate its outputs:
!python run_notebooks.py 01_dataset_audit.ipynb

# Or run multiple specific notebooks:
!python run_notebooks.py 02_exploratory_analysis.ipynb 03_anova_tukey.ipynb

# Or run the entire suite:
!python run_notebooks.py
```

---

## 7. Saving and Exporting Generated Results

All generated tables, models, and high-resolution figures are saved in the `results/` directory.

### Option A: Download All Results as a Zip File
Run this code cell in Colab to download all generated artifacts directly to your local computer:

```python
%cd /content/Mangroves-Blue-Carbon

# Archive results and figures
!zip -q -r reproduction_results.zip results/

# Trigger browser download
from google.colab import files
files.download("reproduction_results.zip")
```

### Option B: Mount Google Drive (Persistent Storage)
If you want generated models and figures to persist across Colab session restarts, mount your Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')

# Copy results directory to your Google Drive
!cp -r /content/Mangroves-Blue-Carbon/results /content/drive/MyDrive/Mangrove_Reproduction_Results/
print("Results successfully copied to Google Drive!")
```

---

## 8. Troubleshooting & Common Pitfalls

| Issue | Root Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Colab working directory is `/content` instead of `/content/Mangroves-Blue-Carbon`. | Run `%cd /content/Mangroves-Blue-Carbon` and `sys.path.insert(0, '/content/Mangroves-Blue-Carbon')`. |
| `FileNotFoundError: Raw CSV not found at data/raw/...` | The 191 MB CSV was not downloaded (Git clones exclude raw data). | Run the `wget` commands in Section 3, Step 4. |
| Notebook 04 takes too long to run | Running on a slow single-core CPU. | In Colab, change runtime to **T4 GPU** (`Runtime -> Change runtime type -> T4 GPU`). |
| Session Disconnect / Timeout during training | Colab free tier times out after idle periods. | Keep the browser tab active, or run `python run_notebooks.py` as a single background job. |
| Plot text formatting looks misaligned | Missing default fonts in Linux Colab environment. | Seaborn fallback is automatically handled by the config; `plt.style.use('seaborn-v0_8-whitegrid')` functions natively. |

---

## 9. Verification Checklist for Evaluators

When evaluating on Google Colab, verify these key scientific milestones:

- [ ] **Figure 4 Replication (`03_anova_tukey.ipynb`)**: Confirm all 10 Sentinel-2 bands reject $H_0$ ($p < 10^{-10}$) and all 30 pairwise Tukey HSD tests reject $H_0$ ($p < 0.001$).
- [ ] **41-Model Grid (`04_three_class_mangrove_mlp.ipynb`)**: Verify training of all 41 architectures, reaching peak test accuracy of **94.98%** (`MLP_4L_300N`) and **90.22%** on the paper's preferred spatial architecture (`MLP_5L_50N`).
- [ ] **Train-Test Gap Audit (`08_paper_vs_reproduction.ipynb`)**: Confirm that `MLP_5L_50N` exhibits the lowest train-test gap (**+2.14 pp**), demonstrating the implicit regularization of narrow deep networks.
- [ ] **Comparability Demarcation (`08_paper_vs_reproduction.ipynb`)**: Verify that the 4-class paper benchmark and 3-species data-derived results are explicitly identified as non-equivalent tasks (average $-3.09$ pp offset due to absent non-mangrove background class).
