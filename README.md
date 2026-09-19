# Strict Scientific Reproduction: Mangrove Species Identification via Multi-Source Spectral Data and Deep Learning

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Reproducibility Status](https://img.shields.io/badge/Scientific%20Reproduction-Audited-brightgreen.svg)](FINAL_REPRODUCTION_CHECKLIST.md)

This repository provides a **strict scientific reproduction and methodological audit** for the Complex Engineering Problem (CEP) Machine Learning examination, replicating the research paper:

> **"An approach for accurate identification and monitoring of species in mangrove forests based on multi-source spectral data and deep learning"**  
> **Authors**: Erandi Monterrubio-Martínez, Rubicel Trujillo-Acatitla, José Tuxpan-Vargas, Patricia Moreno-Casasola  
> **Journal**: *Ecological Informatics*, Volume 85, March 2025, Article 102961  
> **DOI**: [10.1016/j.ecoinf.2024.102961](https://doi.org/10.1016/j.ecoinf.2024.102961)  
> **Local PDF**: [`paper/mangrove_paper.pdf`](paper/mangrove_paper.pdf)

---

## 1. Research Problem & Objective

Mangrove ecosystems provide vital ecosystem services including coastal stabilization, storm buffering, high-density blue carbon sequestration, and nursery habitats for marine species. Monitoring species-level distribution in Latin America has historically been limited by mixed canopy patches, labor-intensive fieldwork, and reliance on drone imagery.

The authors propose using Sentinel-2 MultiSpectral Instrument (MSI) Top-of-Atmosphere (TOA) surface reflectance directly with Multilayer Perceptrons (MLPs) to achieve sub-pixel, species-level classification across monospecific mangrove stands (*Rhizophora mangle*, *Avicennia germinans*, *Laguncularia racemosa*) without handcrafted vegetation indices (such as NDVI, NDWI, MVI, or CMRI).

---

## 2. Dataset & Audit Findings

The authors released a public repository dataset on the Knowledge Network for Biocomplexity (KNB):
- **File**: `data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv` (191.04 MB)
- **Metadata**: `data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml` (EML v2.2.0)
- **Total Rows**: 1,605,681 pixels across 147 cloud-free Sentinel-2 scenes (2015–2021).
- **Footprint**: Exactly 10,923 digitized pixels per scene.

### Key Finding from the Dataset Audit:
- **Available Data**: The released CSV strictly contains **monospecific mangrove forest reflectance**:
  - *Avicennia germinans* (Black mangrove): 1,441,482 pixels (89.77%)
  - *Rhizophora mangle* (Red mangrove): 125,832 pixels (7.84%)
  - *Laguncularia racemosa* (White mangrove): 38,367 pixels (2.39%)
- **Missing Classes & Files**: The authors did **not** publish their non-mangrove class (rainforest, crops, water, urban, dunes, wetlands), their subsampled 60,000 binary or 40,000 4-class splits, nor the raw satellite GeoTIFF rasters or 3.5 cm drone orthophoto.
- **Scientific Integrity Stance**: In strict adherence to scientific reproduction rules:
  1. We **do not fabricate substitute non-mangrove data**.
  2. The paper's published binary and 4-class numbers are transcribed and analyzed as **`PAPER REPORTED RESULTS`**.
  3. We conduct a **`DATA-DERIVED EXPERIMENT`** on the released 3-species monospecific dataset, explicitly labeled:  
     `DATA-DERIVED EXPERIMENT — NOT DIRECTLY COMPARABLE TO THE PAPER'S REPORTED 4-CLASS RESULTS`.

---

## 3. Three-Tier Scientific Architecture

To maintain strict scientific clarity, all findings are categorized into three non-overlapping tiers:

| Tier | Category Name | Description | Datasets / Methodology |
|:---:|---|---|---|
| **A** | **Paper Reported Results** | Published results transcribed from the publication for reference. | 60k Binary (Mangrove vs Non-mangrove), 40k 4-Class (3 Species + Non-mangrove). |
| **B** | **Faithfully Reproduced Results** | Experiments 100% reproducible with released data and specified methods. | One-Way ANOVA across 10 bands, Tukey HSD ($\alpha=0.05$), Figure 4 boxplots replication, `StandardScaler`. |
| **C** | **Data-Derived Experiments** | New experiments executed on available data due to unreleased paper datasets. | 3-Species Monospecific MLP Grid (1–5 layers, 5–500 neurons) on 30,000 balanced samples. |

---

## 4. Repository Structure

```
Mangroves-Blue-Carbon/
├── paper/
│   └── mangrove_paper.pdf
│
├── data/
│   ├── raw/
│   │   ├── DataBase_Sentinel_2_Mangrove_LaMancha.csv
│   │   └── Sentinel_2_satellite_reflectance_of_monospecific.xml
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01_dataset_audit.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_anova_tukey.ipynb
│   ├── 04_three_class_mangrove_mlp.ipynb
│   ├── 05_paper_models_transcription_and_analysis.ipynb
│   ├── 06_architecture_comparison.ipynb
│   └── 07_spatial_validation.ipynb
│
├── src/
│   ├── config.py
│   ├── data/
│   │   └── loader.py
│   ├── models/
│   │   └── mlp.py
│   ├── statistics/
│   │   └── anova_tukey.py
│   └── training/
│       └── trainer.py
│
├── results/
│   ├── dataset_audit.md
│   ├── dataset_audit.json
│   ├── paper_reported_results.md
│   ├── PAPER_VS_REPRODUCTION.md
│   ├── SPATIAL_REPRODUCTION_STATUS.md
│   ├── spatial_audit_summary.json
│   ├── statistics/
│   │   ├── anova_results.csv
│   │   └── tukey_results.csv
│   ├── models/
│   │   ├── architecture_comparison.csv
│   │   ├── architecture_inventory.csv
│   │   ├── paper_reported_binary.csv
│   │   ├── paper_reported_multiclass.csv
│   │   └── three_class_mangrove_results.csv
│   ├── figures/
│   │   ├── reproduced_figure4_boxplots.png
│   │   ├── spectral_signatures.png
│   │   ├── band_correlation_matrix.png
│   │   ├── diagnostic_band_distributions.png
│   │   ├── depth_width_scaling_3species.png
│   │   ├── paper_reported_accuracies_summary.png
│   │   └── three_class_confusion_matrix.png
│   └── tables/
│       └── spectral_summary_stats.csv
│
├── tests/
│   └── test_reproduction.py
│
├── requirements.txt
├── pytest.ini
├── run_notebooks.py
├── REPRODUCTION_SPECIFICATION.md
├── FINAL_REPRODUCTION_CHECKLIST.md
└── README.md
```

---

## 5. Quickstart & Installation

### Step 1: Clone and Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 2: Run Unit & Integrity Tests
```bash
pytest tests/test_reproduction.py -v
```

### Step 3: Launch Jupyter Notebooks
```bash
jupyter notebook
```
All notebooks are self-contained, sequential, and pre-populated with executed outputs, tables, and figures.

### Step 4 (Optional): Execute All Notebooks Headless
To re-execute all 7 notebooks from top to bottom in a single command:
```bash
python run_notebooks.py
```

---

## 6. Key Scientific Results

### A. Statistical Analysis Reproduction (Fig. 4 Replication)
- **One-Way ANOVA**: All 10 Sentinel-2 bands reject $H_0$ ($p < 10^{-10}$).
- **Tukey HSD**: All 30 pairwise species comparisons reject $H_0$ at $\alpha = 0.05$ ($p < 0.001$), confirming the authors' finding that spectral variations across Sentinel-2 bands are statistically significant across all species.
- Generated plot: [`results/figures/reproduced_figure4_boxplots.png`](results/figures/reproduced_figure4_boxplots.png).

### B. Published Benchmark Summary (Transcribed from Paper)
- **Binary Classification (60k samples)**:
  - Logistic Baseline: Train $0.9916$, Test $0.9910$
  - 3 Layers / 50 Neurons: Train **$0.9996$**, Test **$0.9987$** (Optimal binary model)
- **Multiclass Classification (40k samples, 4 classes)**:
  - Logistic Baseline: Train $0.7670$, Test $0.7684$
  - 3 Layers / 500 Neurons: Train $0.9863$, Test **$0.9654$** (Highest test score)
  - 5 Layers / 50 Neurons: Train $0.9550$, Test $0.9454$ (Most reliable spatial model)

### C. Data-Derived Monospecific MLP Experiments (30k samples, 3 species)
- Logistic Baseline: Train $0.8448$, Test $0.8423$
- 3 Layers / 500 Neurons: Train $0.9752$, Test $0.9620$
- 5 Layers / 50 Neurons: Train $0.9560$, Test $0.9490$
- Full 41-model grid recorded in [`results/models/three_class_mangrove_results.csv`](results/models/three_class_mangrove_results.csv).

---

## 7. Evidence-Grounded Discrepancy Analysis

All differences between the published benchmarks and our data-derived experiments are strictly classified in [`results/PAPER_VS_REPRODUCTION.md`](results/PAPER_VS_REPRODUCTION.md):
- **`CONFIRMED`**: 4 classes in paper (including Non-mangrove) vs 3 monospecific mangrove classes in released data. Separating vegetation from water/soil yields different decision boundaries than separating taxonomically related mangrove species.
- **`LIKELY`**: Unspecified Adam hyperparameters (learning rate, weight decay, epochs, batch size, PyTorch vs Keras framework differences).
- **`POSSIBLE`**: Pixel subsampling selection variance from the 1.6-million-row pool.
- **`UNKNOWN`**: Hardware floating-point rounding and non-deterministic CUDA/MPS kernel operations.

---

## 8. Spatial Validation & Reproducibility Status

As documented in [`results/SPATIAL_REPRODUCTION_STATUS.md`](results/SPATIAL_REPRODUCTION_STATUS.md), the satellite GeoTIFF scenes for La Mancha and Arroyo Moreno, the 3.5 cm drone orthophoto, and the QGIS species boundary shapefiles were **not released** by the authors. This component is classified as **`DATA-LIMITED / NOT REPRODUCIBLE AT RASTER LEVEL`**.

---

## 9. Compliance Checklist

See [`FINAL_REPRODUCTION_CHECKLIST.md`](FINAL_REPRODUCTION_CHECKLIST.md) for the complete 37-point audit mapping every requirement to `IMPLEMENTED`, `REPRODUCED`, `DATA-LIMITED`, `PAPER-UNSPECIFIED`, or `NOT-REPRODUCIBLE`.
