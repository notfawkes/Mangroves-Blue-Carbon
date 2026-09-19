# Spatial Validation Audit and Reproducibility Status

Reference: **Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961**  
Section 3.3 ("Models test") & Figures 7, 8, 9, 10

---

## 1. Executive Summary & Scientific Status

- **Status**: `DATA-LIMITED / NOT REPRODUCIBLE AT NUMERICAL / RASTER LEVEL`
- **Audit Conclusion**: The authors' spatial evaluation methodology is thoroughly described and conceptualized in the paper text, but the raw satellite GeoTIFF raster scenes, UAV orthophoto GeoTIFF, and QGIS ground-truth polygon shapefiles were **not released** in the public data repository.
- **Scientific Integrity Mandate**: In strict adherence to reproduction guidelines:
  1. We do **not** download unrelated external satellite images and claim they represent the paper's original scenes.
  2. We do **not** fabricate missing spatial masks.
  3. We conduct a rigorous audit of what the paper did, document why the spatial rasters cannot be directly reproduced from the CSV, and preserve the qualitative and spatial findings reported by the authors.

---

## 2. Spatial Data Used in the Paper

The paper's spatial testing methodology utilized three categories of spatial assets:

### A. Study Sites
1. **La Mancha, Veracruz, Mexico** ($19^\circ 35' 12''\text{ N}, 96^\circ 23' 09''\text{ W}$):
   - Priority mangrove conservation area ($9,050\text{ km}^2$).
   - Used for training and primary spatial testing (Figs. 7, 8, 9).
2. **Arroyo Moreno, Veracruz, Mexico** ($19^\circ 00' 59''\text{ N}, 96^\circ 03' 43''\text{ W}$):
   - Natural protected area near the port of Veracruz.
   - Used as an independent out-of-domain site to test spatial scalability and generalization (Fig. 10).

### B. Spatial Imagery & Photogrammetry
1. **UAV High-Resolution Orthophoto**:
   - Acquired July 2021 via DJI Mavic Mini 2 drone at 100 m altitude.
   - 5,435 zenithal aerial photographs processed in Agisoft Metashape Pro v1.8.5.
   - Ground spatial resolution: **3.5 cm**.
   - Ground control points: 100 field verification locations surveyed with Garmin GPSMAP 527.
2. **Recent Sentinel-2 L1C Full-Scene Satellite Imagery**:
   - Cloud-free Level-1C MSI scenes covering the entire La Mancha lagoon and Arroyo Moreno estuary.
   - 10 spectral bands processed to surface reflectance at 10 m pixel resolution.
3. **QGIS Species Polygons**:
   - Digitized vector masks of monospecific stands of *A. germinans*, *R. mangle*, *L. racemosa*, and mixed flooded freshwater wetlands.

---

## 3. Local Data Availability Audit

| Spatial Asset | Described in Paper | Present in Local Repository | Local Path / Status |
|---|:---:|:---:|---|
| Sentinel-2 Monospecific Mangrove CSV | Yes | **YES** | `data/raw/DataBase_Sentinel_2_Mangrove_LaMancha.csv` (191 MB) |
| EML XML Dataset Metadata | Yes | **YES** | `data/raw/Sentinel_2_satellite_reflectance_of_monospecific.xml` |
| Non-Mangrove Background Pixels | Yes | **NO** | Not included in released files |
| Sentinel-2 L1C Scene GeoTIFFs | Yes | **NO** | Not deposited in repository |
| UAV Orthophoto GeoTIFF (3.5 cm) | Yes | **NO** | Not deposited in repository |
| QGIS Vector Masks / Polygons | Yes | **NO** | Not deposited in repository |
| Arroyo Moreno Validation GeoTIFFs | Yes | **NO** | Not deposited in repository |

---

## 4. Analysis of Paper's Spatial Findings

Although the raw rasters are unavailable, the paper's spatial experiments yielded crucial ecological and architectural insights that are documented here:

### 1. Binary Spatial Performance (Fig. 7)
- **Layer Depth vs Spatial Coherence**: While binary accuracy across all models was $>99\%$, spatial map performance varied substantially. The logistic regression baseline exhibited extensive salt-and-pepper noise and false positives in water bodies.
- **Top Binary Model**: The **4-hidden-layer model with 300 neurons** was identified as the most reliable binary spatial model, cleanly delineating mangrove boundaries with minimal water confusion.

### 2. Multiclass Spatial Performance & Species Dominance (Fig. 8 & 9)
- **High Accuracy $\neq$ High Spatial Quality**: The model with the highest test accuracy (3 layers, 500 neurons: 0.9654) suffered from spectral confusion between *R. mangle* (red mangrove) and surrounding water bodies due to high canopy moisture reflectance.
- **White Mangrove Overestimation**: Simpler models (including logistic) severely overestimated *L. racemosa* (white mangrove).
- **The Optimal Ecological Model**: The authors concluded that the **5-hidden-layer model with 50 neurons** was the most reliable for real-world mapping (Fig. 9E). Even with a slightly lower test accuracy (0.9454), its lower neuron count acted as a regularizer, preventing overfitting to spectral edge effects.

### 3. Arroyo Moreno Generalization (Fig. 10)
- Testing in Arroyo Moreno validated that the model trained on La Mancha could generalize across geographic regions without retraining.
- *R. mangle* exhibited slight spatial overestimation in permanently flooded zones, but *A. germinans* and *L. racemosa* boundaries matched historical field surveys (López-Portillo et al., 2002).

---

## 5. What Can and Cannot Be Reproduced

- **CANNOT BE REPRODUCED**:
  - Direct raster-level pixel inference generating Figs 7, 8, 9, 10 without the original satellite GeoTIFF files.
  - Pixel-by-pixel spatial intersection with the 3.5 cm UAV orthophoto.
- **CAN BE REPRODUCED / AUDITED**:
  - The architectural tradeoffs identified by the authors (simplicity vs overfitting).
  - The spectral distribution analysis explaining why water and *R. mangle* exhibit spectral overlap.
  - Complete documentation of the spatial methodology within `notebooks/07_spatial_validation.ipynb`.
