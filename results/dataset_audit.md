# Dataset Audit & Metadata Verification Report

Reference: **Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961**  
Dataset File: `data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv`  
Metadata File: `data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml`

---

## 1. Executive Summary & Provenance

- **Primary Repository Dataset**: `DataBase_Sentinel_2_Mangrove_LaMancha.csv` (191.04 MB).
- **Format**: Comma-Separated Values (CSV), UTF-8 text encoding.
- **Data Source**: Sentinel-2 Level-1C (L1C) MultiSpectral Instrument (MSI) Top-of-Atmosphere (TOA) reflectance data acquired via the Copernicus Browser (2015–2021).
- **Sensor Bands**: 10 spectral bands processed to surface reflectance at uniform 10 m resolution.
- **Ground Truth Reference**: Drone orthophoto (3.5 cm resolution) acquired with a DJI Mavic Mini 2 in July 2021 at 100 m altitude (5,435 photographs processed in Agisoft Metashape Pro v1.8.5) coupled with 100 field GPS control points (GPSMAP 527). Polygons digitized in QGIS v3.22.14.

---

## 2. Dataset Schema & Column Definitions

| Column Name | Data Type | Physical Meaning | Sentinel-2 Band Reference | Central Wavelength | Spatial Resolution |
|---|:---:|---|---|:---:|:---:|
| `ID_Imagen` | `object` (string) | Sentinel-2 L1C Granule Identifier | Scene Metadata | N/A | Full scene footprint |
| `Spp` | `object` (string) | Biological species label | Ground Truth Mask | N/A | Stand-level polygon |
| `Band_2` | `float64` | Surface Reflectance | Blue | 490 nm | 10 m (native) |
| `Band_3` | `float64` | Surface Reflectance | Green | 560 nm | 10 m (native) |
| `Band_4` | `float64` | Surface Reflectance | Red | 665 nm | 10 m (native) |
| `Band_5` | `float64` | Surface Reflectance | Vegetation Red Edge 1 | 705 nm | 10 m (resampled from 20 m) |
| `Band_6` | `float64` | Surface Reflectance | Vegetation Red Edge 2 | 740 nm | 10 m (resampled from 20 m) |
| `Band_7` | `float64` | Surface Reflectance | Vegetation Red Edge 3 | 783 nm | 10 m (resampled from 20 m) |
| `Band_8` | `float64` | Surface Reflectance | Near-Infrared (NIR broad) | 842 nm | 10 m (native) |
| `Band_8A` | `float64` | Surface Reflectance | Near-Infrared (NIR narrow) | 865 nm | 10 m (resampled from 20 m) |
| `Band_11` | `float64` | Surface Reflectance | Short-Wave Infrared 1 | 1610 nm | 10 m (resampled from 20 m) |
| `Band_12` | `float64` | Surface Reflectance | Short-Wave Infrared 2 | 2190 nm | 10 m (resampled from 20 m) |

---

## 3. Statistical Inventory & Data Integrity

- **Total Rows**: **1,605,681**
- **Total Columns**: **12**
- **Missing / Null Values**: **0** across all 12 columns (100% complete data).
- **Duplicate Rows**: None (temporal time-series of pixel coordinates).
- **Unique Sentinel-2 Granules (`ID_Imagen`)**: **147** cloud-free acquisitions between 2015 and 2021.
- **Pixels per Scene**: Exactly **10,923 pixels** in every single image acquisition, proving a constant spatial mask footprint across the entire time series:
  $$\frac{1,605,681\text{ rows}}{147\text{ scenes}} = 10,923\text{ pixels/scene}$$

---

## 4. Species Distribution in Released CSV

| Species Scientific Name | Common Name | Class Code | Row Count | Percentage of Total | Footprint per Scene |
|---|---|:---:|:---:|:---:|:---:|
| *Avicennia germinans* | Black mangrove | `Avicennia_germinans` | **1,441,482** | 89.77% | 9,806 pixels |
| *Rhizophora mangle* | Red mangrove | `Rhizophora_mangle` | **125,832** | 7.84% | 856 pixels |
| *Laguncularia racemosa* | White mangrove | `Laguncularia_racemosa` | **38,367** | 2.39% | 261 pixels |
| **Total** | | | **1,605,681** | **100.00%** | **10,923 pixels** |

---

## 5. Spectral Reflectance Ranges

| Band | Minimum Value | Maximum Value | Mean | Standard Deviation |
|---|:---:|:---:|:---:|:---:|
| `Band_2` (Blue) | 0.0802 | 0.1254 | 0.0963 | 0.0064 |
| `Band_3` (Green) | 0.0601 | 0.1147 | 0.0858 | 0.0076 |
| `Band_4` (Red) | 0.0400 | 0.0936 | 0.0619 | 0.0078 |
| `Band_5` (VRE 1) | 0.0369 | 0.6682 | 0.0768 | 0.0210 |
| `Band_6` (VRE 2) | 0.0551 | 0.6722 | 0.1492 | 0.0252 |
| `Band_7` (VRE 3) | 0.0615 | 0.6805 | 0.1873 | 0.0289 |
| `Band_8` (NIR Broad) | 0.0608 | 0.3681 | 0.2291 | 0.0335 |
| `Band_8A` (NIR Narrow)| 0.0236 | 0.6878 | 0.1062 | 0.0315 |
| `Band_11` (SWIR 1) | 0.0149 | 0.6184 | 0.0934 | 0.0242 |
| `Band_12` (SWIR 2) | 0.0049 | 0.4603 | 0.0441 | 0.0177 |

---

## 6. Critical Audit Verdict: Database Identity vs Paper Experiments

> ### [!IMPORTANT]
> **AUDIT CONCLUSION:**
> 1. **Released File Identity**: The CSV contains exclusively monospecific mangrove forest reflectance for the three species (*A. germinans*, *R. mangle*, *L. racemosa*).
> 2. **Absence of Non-Mangrove Background**: The paper states that its experiments used:
>    - A balanced **60,000-pixel binary dataset** (30,000 mangrove + 30,000 non-mangrove).
>    - A balanced **40,000-pixel multiclass dataset** (10,000 each of *R. mangle*, *A. germinans*, *L. racemosa*, and non-mangrove).
>    The non-mangrove class (comprising rainforest, crops, water, urban, dunes, and wetlands) was **not deposited by the authors in their public repository**.
> 3. **Absence of Pre-Sampled Splits**: The authors did not release the exact random subsample indices for the 60,000 and 40,000 records.
> 4. **Scientific Position**: Under strict reproduction ethics, we:
>    - Categorize the original binary and 4-class experiments as `DATA-LIMITED / NOT AVAILABLE`.
>    - Do **not** fabricate substitute non-mangrove data.
>    - Transcribe the published results as scientific benchmarks.
>    - Perform data-derived experiments on the released monospecific 3-species dataset (30,000 samples: 10,000 per species).
