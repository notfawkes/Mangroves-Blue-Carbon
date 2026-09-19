# REPRODUCTION SPECIFICATION

## Research Paper Reference
- **Title**: An approach for accurate identification and monitoring of species in mangrove forests based on multi-source spectral data and deep learning
- **Authors**: Erandi Monterrubio-Martínez, Rubicel Trujillo-Acatitla, José Tuxpan-Vargas, Patricia Moreno-Casasola
- **Journal**: *Ecological Informatics*, Volume 85, March 2025, Article 102961
- **DOI**: [10.1016/j.ecoinf.2024.102961](https://doi.org/10.1016/j.ecoinf.2024.102961)

---

## Strict Scientific Classification Taxonomy
Every parameter, methodology step, and experimental choice is classified into one of the following official categories:
- **`PAPER-SPECIFIED`**: Explicitly stated in the paper text, tables, figures, or equations.
- **`DATA-DERIVED`**: Directly computed or derived from the authors' released dataset or metadata file.
- **`IMPLEMENTATION ASSUMPTION`**: Not stated in the paper, chosen based on standard scientific best practices, and explicitly documented.
- **`DATA-LIMITED`**: Described in the paper methodology but omitted by the authors from their publicly deposited dataset.
- **`NOT AVAILABLE`**: Completely absent from both the paper text and the released public artifacts.

---

## Comprehensive 33-Point Specification Matrix

### 1. Research Objective
- **Description**: Accurate identification and monitoring of mangrove species (*Rhizophora mangle*, *Avicennia germinans*, *Laguncularia racemosa*) using multi-source spectral data (Sentinel-2 L1C surface reflectance) and deep learning Multilayer Perceptrons (MLPs), demonstrating sub-pixel and species-level mapping without requiring handcrafted vegetation indices.
- **Classification**: `PAPER-SPECIFIED` (Abstract, Section 1, Section 2)

### 2. Study Area
- **Primary Site**: La Mancha, Actopan, Veracruz, Mexico ($19^\circ 35' 12''\text{ N}, 96^\circ 23' 09''\text{ W}$), Gulf of Mexico, Ramsar site 1336 ($9,050\text{ km}^2$ region of influence). Chosen for well-defined monospecific mangrove forests.
- **Secondary Generalization Site**: Arroyo Moreno, Boca del Río, Veracruz, Mexico ($19^\circ 00' 59''\text{ N}, 96^\circ 03' 43''\text{ W}$).
- **Classification**: `PAPER-SPECIFIED` (Section 2.1, Fig. 2)

### 3. Dataset Source
- **Satellite Sensor**: European Space Agency (ESA) Sentinel-2 MultiSpectral Instrument (MSI), Level-1C (L1C) Top-of-Atmosphere (TOA) data obtained from Copernicus Browser.
- **UAV Photogrammetry**: DJI Mavic Mini 2 zenithal drone flight at 100 m altitude (July 2021), 5,435 photos processed in Agisoft Metashape Pro v1.8.5 producing a 3.5 cm resolution orthophoto.
- **Ground Truth Verification**: 100 ground control points collected using Garmin GPSMAP 527 via walking and boat surveys. Monospecific and mixed mangrove polygons digitized in QGIS v3.22.14.
- **Classification**: `PAPER-SPECIFIED` (Section 2.1, Fig. 1)

### 4. Dataset Files
- **Locally Available Files**:
  - `data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv` (191.04 MB; 1,605,681 rows, 12 columns)
  - `data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml` (Ecological Metadata Language - EML v2.2.0 metadata)
- **Unavailable / Unreleased Files**:
  - Non-mangrove background pixel reflectance table
  - Subsampled 60,000-row binary dataset CSV
  - Subsampled 40,000-row 4-class dataset CSV
  - Raw UAV orthophoto GeoTIFF and QGIS polygon shapefiles
  - Raw Sentinel-2 GeoTIFF scenes for La Mancha and Arroyo Moreno spatial testing
- **Classification**: `DATA-DERIVED` (Available CSV/XML) / `DATA-LIMITED` (Unreleased files)

### 5. Number of Samples
- **Released CSV Total Rows**: 1,605,681 pixels (10,923 pixels per image across 147 cloud-free Sentinel-2 acquisitions).
- **Paper Binary Database**: 60,000 pixels (30,000 mangrove + 30,000 non-mangrove).
- **Paper Multiclass Database**: 40,000 pixels (10,000 per class $\times$ 4 classes).
- **Classification**: `DATA-DERIVED` (1,605,681 in CSV) / `PAPER-SPECIFIED` (60k and 40k in Section 2.1)

### 6. Classes
- **Released CSV Classes (3 Monospecific Mangrove Species)**:
  - `Avicennia_germinans` (Black mangrove): 1,441,482 pixels (89.77%)
  - `Rhizophora_mangle` (Red mangrove): 125,832 pixels (7.84%)
  - `Laguncularia_racemosa` (White mangrove): 38,367 pixels (2.39%)
- **Paper Binary Classes**:
  - `0`: Non-mangrove
  - `1`: Mangrove (mask of the three species considered as one)
- **Paper Multiclass Classes (4 Classes)**:
  - `0`: Non-mangrove (randomly sampled from rainforest, crops, water, urban, dunes, other wetlands)
  - `1`: Red mangrove (*Rhizophora mangle*)
  - `2`: Black mangrove (*Avicennia germinans*)
  - `3`: White mangrove (*Laguncularia racemosa*)
- **Classification**: `DATA-DERIVED` (3 classes in CSV) / `PAPER-SPECIFIED` (4 classes in paper)

### 7. Sentinel-2 Spectral Bands
- Exactly 10 spectral bands:
  - RGB: Band 2, Band 3, Band 4
  - Vegetation Red Edge (VRE): Band 5, Band 6, Band 7, Band 8A
  - Near-Infrared (NIR): Band 8
  - Short-Wave Infrared (SWIR): Band 11, Band 12
- Cirrus (Band 10), Coastal aerosol (Band 1), and Water vapor (Band 9) were excluded.
- **Classification**: `PAPER-SPECIFIED` (Section 2.1, Section 2.3)

### 8. Band Central Wavelengths
- Band 2 (Blue): 0.490 µm (490 nm)
- Band 3 (Green): 0.560 µm (560 nm)
- Band 4 (Red): 0.665 µm (665 nm)
- Band 5 (Red Edge 1): 0.705 µm (705 nm)
- Band 6 (Red Edge 2): 0.740 µm (740 nm)
- Band 7 (Red Edge 3): 0.783 µm (783 nm)
- Band 8 (NIR Broad): 0.842 µm (842 nm)
- Band 8A (NIR Narrow): 0.865 µm (865 nm)
- Band 11 (SWIR 1): 1.610 µm (1610 nm)
- Band 12 (SWIR 2): 2.190 µm (2190 nm)
- **Classification**: `PAPER-SPECIFIED` (Section 2.1, Section 2.3)

### 9. Spatial Resolution
- Native 10 m: Band 2, Band 3, Band 4, Band 8
- Native 20 m resampled to 10 m: Band 5, Band 6, Band 7, Band 8A, Band 11, Band 12
- All analysis conducted at uniform 10 m pixel scale.
- **Classification**: `PAPER-SPECIFIED` (Section 2.1)

### 10. Data Acquisition Period
- Sentinel-2 satellite time-series: 2015 to 2021 (147 cloud-free L1C acquisitions).
- UAV drone mapping: July 2021.
- Field ground control surveys: July 2021.
- **Classification**: `PAPER-SPECIFIED` (Section 2.1, XML metadata)

### 11. Reflectance Preprocessing
- Digital numbers converted to surface reflectance (values scaled roughly between 0.005 and 0.68).
- The authors explicitly state that multispectral reflectance bands alone are used without calculating vegetation indices (e.g. NDVI, NDWI, MVI, CMRI).
- **Classification**: `PAPER-SPECIFIED` (Section 2.1, Section 4)

### 12. Resampling Methodology
- Bilinear interpolation using the `rasterio` package in Python 3.8.13 applied to the 20 m bands (B5, B6, B7, B8A, B11, B12) to match 10 m resolution.
- Already applied in the released CSV `DataBase_Sentinel_2_Mangrove_LaMancha.csv`.
- **Classification**: `PAPER-SPECIFIED` (Section 2.1) / `DATA-DERIVED` (present in CSV)

### 13. Standardization / Normalization
- Scikit-learn v1.2.1 `StandardScaler` ($\mu = 0, \sigma = 1$).
- Standard formula: $z = \frac{x - \mu}{\sigma}$ fit on training features and applied to test features.
- **Classification**: `PAPER-SPECIFIED` (Section 2.1)

### 14. Dataset Construction
- Polygons of monospecific forest areas used to extract pixel vectors from 147 scenes.
- 10,923 pixels per scene ($9,806$ *A. germinans*, $856$ *R. mangle*, $261$ *L. racemosa$).
- 147 scenes $\times$ 10,923 pixels = 1,605,681 total rows.
- **Classification**: `PAPER-SPECIFIED` & `DATA-DERIVED`

### 15. Binary Dataset Definition
- Class-balanced database containing 60,000 pixels:
  - Class 1 (Mangrove): 30,000 pixels (mask of the 3 species combined as one)
  - Class 0 (Non-mangrove): 30,000 pixels (randomly sampled from rainforest, crops, water, urban, dunes, other wetlands)
- Status in released CSV: Non-mangrove pixels were **not released**.
- **Classification**: `PAPER-SPECIFIED` (Concept) / `DATA-LIMITED` (Data availability)

### 16. Multiclass Dataset Definition
- Class-balanced database containing 40,000 pixels (10,000 pixels per class):
  - Class 0: Non-mangrove (10,000 pixels)
  - Class 1: *Rhizophora mangle* (10,000 pixels)
  - Class 2: *Avicennia germinans* (10,000 pixels)
  - Class 3: *Laguncularia racemosa* (10,000 pixels)
- Status in released CSV: Non-mangrove pixels were **not released**. The three mangrove species have sufficient real samples ($125\text{k}, 1.44\text{M}, 38\text{k}$ respectively) to sample 10,000 each.
- **Classification**: `PAPER-SPECIFIED` (Concept) / `DATA-LIMITED` (Data availability)

### 17. Train / Test Split
- 70% Training / 30% Testing.
- Implemented using Scikit-learn v1.2.1 `train_test_split`.
- For 60,000 binary: 42,000 train / 18,000 test.
- For 40,000 multiclass: 28,000 train / 12,000 test.
- For our data-derived 30,000 3-species experiment: 21,000 train / 9,000 test.
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 18. ANOVA Methodology
- One-Way Analysis of Variance (One-Way ANOVA) performed independently on each of the 10 spectral bands.
- Tests whether mean reflectance differs significantly among species.
- Implemented in paper using `bioinfokit` v1 in Python 3.8.13.
- **Classification**: `PAPER-SPECIFIED` (Section 2.2)

### 19. Tukey Post-Hoc Methodology
- Tukey's Honestly Significant Difference (Tukey HSD) test with 95% confidence interval ($\alpha = 0.05$).
- Pairwise comparisons between species pairs (*A. germinans* vs *R. mangle*, *A. germinans* vs *L. racemosa*, *R. mangle* vs *L. racemosa*).
- Paper reported $p < 0.05$ across all bands.
- **Classification**: `PAPER-SPECIFIED` (Section 2.2, Section 3.1)

### 20. MLP Architecture Family
- Feed-forward Multilayer Perceptron (MLP) for sub-pixel / pixel-wise classification.
- Baseline: Single input-to-output linear layer (logistic regression).
- Hidden layer architectures: 1 to 5 hidden layers.
- Fully connected linear layers with non-linear activation.
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 21. Number of Hidden Layers
- Explored systematically from 1 to 5 hidden layers ($L \in \{1, 2, 3, 4, 5\}$).
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 22. Number of Neurons per Hidden Layer
- Hidden layer widths evaluated: 5, 10, 20, 50, 100, 150, 300, 500 neurons per layer.
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 23. Activation Functions
- Hidden layers: Rectified Linear Unit (`ReLU`).
- Binary output layer: `Sigmoid` ($\sigma(z) = \frac{1}{1 + e^{-z}}$), output range $[0, 1]$.
- Multiclass output layer: `Softmax` ($\text{Softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$).
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 24. Optimizer
- Algorithm: `Adam` (Adaptive Moment Estimation).
- Learning rate $\alpha$: `NOT AVAILABLE` in paper text. Default standard $\alpha = 0.001$ used as `IMPLEMENTATION ASSUMPTION`.
- Adam parameters $\beta_1, \beta_2, \epsilon$: `NOT AVAILABLE` (defaults: $0.9, 0.999, 10^{-8}$).
- **Classification**: Optimizer algorithm is `PAPER-SPECIFIED`; learning rate and hyperparams are `IMPLEMENTATION ASSUMPTION` / `NOT AVAILABLE`.

### 25. Loss Functions
- Binary models: Binary Cross-Entropy (`BCE`):
  $$\mathcal{L}_{BCE} = - \frac{1}{N} \sum [y \log \hat{y} + (1-y) \log (1-\hat{y})]$$
- Multiclass models: Multiclass Categorical Cross-Entropy (`CCE`):
  $$\mathcal{L}_{CCE} = - \frac{1}{N} \sum \sum y_{i,k} \log \hat{y}_{i,k}$$
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 26. Output Classes
- Binary: 1 scalar neuron predicting $P(y = 1 \mid \mathbf{x})$.
- Multiclass (Paper): 4 output neurons for classes 0, 1, 2, 3.
- Multiclass (Data-Derived 3-Species): 3 output neurons for classes 0, 1, 2 (*R. mangle*, *A. germinans*, *L. racemosa*).
- **Classification**: `PAPER-SPECIFIED` (Paper 4-class) / `DATA-DERIVED` (Our 3-class)

### 27. Experimental Configurations
- Model configurations explored:
  - Logistic baseline (0 hidden layers)
  - 1 Hidden Layer: 5, 10, 20, 50, 100, 150, 300, 500
  - 2 Hidden Layers: 5, 10, 20, 50, 100, 150, 300, 500
  - 3 Hidden Layers: 5, 10, 20, 50, 100, 150, 300, 500
  - 4 Hidden Layers: 5, 10, 20, 50, 100, 150, 300, 500
  - 5 Hidden Layers: 5, 10, 20, 50, 100, 150, 300, 500
- Total potential grid per task: 1 logistic + (5 layers $\times$ 8 widths) = 41 architectures.
- **Classification**: `PAPER-SPECIFIED` (Section 2.3)

### 28. Evaluation Metrics
- Primary metric: Overall Accuracy ($\frac{TP + TN}{Total}$) on Training (70%) and Testing (30%) splits.
- Secondary spatial evaluation: Visual inspection of spatial distribution and comparison with UAV orthophoto ground truth.
- **Classification**: `PAPER-SPECIFIED` (Section 3.2, 3.3)

### 29. Published Results
- **Binary Key Reported Accuracies (Section 3.2, Fig. 5)**:
  - Logistic: Train $\approx 0.9916$, Test $\approx 0.9910$
  - 1 Layer / 300 Neurons: Train $\approx 0.9995$, Test $\approx 0.9988$
  - 2 Layers / 100 Neurons: Train $\approx 0.9994$, Test $\approx 0.9987$
  - 3 Layers / 50 Neurons: Train $\approx 0.9996$, Test $\approx 0.9987$ (Selected optimal model)
  - 4 Layers / 150 & 300 Neurons: Train $\approx 0.9993$, Test $\approx 0.9986$
  - 5 Layers / 50 & 300 Neurons: Train $\approx 0.9995$, Test $\approx 0.9988$
- **Multiclass Key Reported Accuracies (Section 3.2, Fig. 6, Fig. 9)**:
  - Logistic: Train $\approx 0.7670$, Test $\approx 0.7684$
  - 1 Layer / 500 Neurons: Train $\approx 0.9110$, Test $\approx 0.9065$
  - 2 Layers / 300 Neurons: Train $\approx 0.9575$, Test $\approx 0.9436$
  - 3 Layers / 500 Neurons: Train $\approx 0.9863$, Test $\approx 0.9654$ (Highest accuracy)
  - 4 Layers / 300 Neurons: Train $\approx 0.9795$, Test $\approx 0.9602$
  - 5 Layers / 300 Neurons: Train $\approx 0.9873$, Test $\approx 0.9684$
  - 4 Layers / 100 Neurons: Train $\approx 0.9662$, Test $\approx 0.9528$
  - 4 Layers / 150 Neurons: Train $\approx 0.9775$, Test $\approx 0.9607$
  - 5 Layers / 50 Neurons: Train $\approx 0.9550$, Test $\approx 0.9454$ (Selected as most reliable for spatial distribution)
  - 5 Layers / 150 Neurons: Train $\approx 0.9810$, Test $\approx 0.9632$
- **Classification**: `PAPER-SPECIFIED` (Transcribed exactly from published paper)

### 30. Spatial Validation Methodology
- Models applied to full scene Sentinel-2 images over La Mancha and Arroyo Moreno.
- Pixel-by-pixel prediction compared visually against orthophoto ground-truth masks.
- Analysis of spatial confusion (water vs *R. mangle*, mixed mangrove overestimation).
- Status: Scene GeoTIFFs, UAV orthophotos, and vector masks are **not provided**.
- **Classification**: `PAPER-SPECIFIED` (Method) / `DATA-LIMITED` (Data availability)

### 31. Unspecified Parameters Audit
- **Batch size**: `NOT AVAILABLE` in paper. Implementation Assumption: 64.
- **Epochs / Stopping criteria**: `NOT AVAILABLE` in paper. Implementation Assumption: 100 epochs with training loss tracking.
- **Learning rate**: `NOT AVAILABLE` in paper. Implementation Assumption: 0.001 (standard Adam default).
- **Random seed**: `NOT AVAILABLE` in paper. Implementation Assumption: seed 42.
- **Weight initialization**: `NOT AVAILABLE` in paper. Implementation Assumption: PyTorch default (Kaiming uniform for linear layers with ReLU).
- **Train/test random_state**: `NOT AVAILABLE` in paper. Implementation Assumption: seed 42.
- **Deep learning framework**: PyTorch / Keras (Chollet 2021 referenced). Implementation Assumption: PyTorch with MPS / CPU backend.
- **Classification**: `NOT AVAILABLE` / `IMPLEMENTATION ASSUMPTION`

### 32. Ambiguities or Inconsistencies in the Paper
1. **Missing Non-Mangrove in Repository**: While the paper states non-mangrove samples were collected from rainforest, crops, water, dunes, urban, and wetlands, the published repository dataset contains strictly the monospecific mangrove reflectance CSV.
2. **Textual Typo in Section 3.3**: The text states: *"whereas the one hidden layer with 150 neurons attained a training score of 0.9775 and a test score of 0.9607"*, but Fig. 9 legend describes this as *"Model of Four Hidden Layer with 150 neurons"*. The figure caption and context confirm this was the 4-layer model.
3. **Absence of Tabular Numerical Outputs**: All results in the paper are presented via bar charts (Figs 5 & 6) and spatial maps (Figs 7–10), with only selected models mentioned numerically in the text.
- **Classification**: `PAPER-SPECIFIED` (Textual analysis)

### 33. Reproducibility Status of Project Components
| Component | Status | Classification |
|---|---|---|
| XML Metadata Audit | Complete | `REPRODUCED` |
| CSV Schema & Distribution Audit | Complete | `REPRODUCED` |
| Spectral Band Reflectance Profiles | Complete | `REPRODUCED` |
| One-Way ANOVA across 10 Bands | Complete | `REPRODUCED` |
| Tukey HSD Pairwise Species Tests | Complete | `REPRODUCED` |
| Boxplot Generation (Fig. 4 reproduction) | Complete | `REPRODUCED` |
| StandardScaler Pipeline | Complete | `REPRODUCED` |
| Paper Binary 60k Numerical Reproduction | Impossible (Data unreleased) | `DATA-LIMITED / NOT-REPRODUCIBLE` |
| Paper Multiclass 40k Numerical Reproduction | Impossible (Data unreleased) | `DATA-LIMITED / NOT-REPRODUCIBLE` |
| Paper Results Transcription & Analysis | Complete | `PAPER REPORTED RESULTS` |
| Monospecific 3-Class Mangrove MLP Experiments | Executed on released data | `DATA-DERIVED EXPERIMENT` |
| Spatial Raster Mapping Reproduction | Impossible (Rasters unreleased) | `DATA-LIMITED / NOT-REPRODUCIBLE` |
| Spatial Validation Analysis & Audit | Complete | `PAPER-SPECIFIED AUDIT` |
