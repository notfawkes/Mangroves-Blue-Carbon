"""
Configuration and constants for the Mangrove Research Paper Reproduction.
Reference: Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

CSV_PATH = RAW_DATA_DIR / "DataBase_Sentinel_2_Mangrove_LaMancha.csv"
XML_PATH = RAW_DATA_DIR / "Sentinel_2_satellite_reflectance_of_monospecific.xml"
PAPER_PDF_PATH = PROJECT_ROOT / "paper" / "mangrove_paper.pdf"

# Output directories
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_STATS_DIR = RESULTS_DIR / "statistics"
RESULTS_MODELS_DIR = RESULTS_DIR / "models"
RESULTS_FIGURES_DIR = RESULTS_DIR / "figures"
RESULTS_TABLES_DIR = RESULTS_DIR / "tables"
RESULTS_MAPS_DIR = RESULTS_DIR / "maps"
SAVED_MODELS_DIR = PROJECT_ROOT / "models"

# 10 Sentinel-2 Spectral Bands used in the paper (PAPER-SPECIFIED)
SPECTRAL_BANDS = [
    "Band_2",   # Blue (0.490 µm)
    "Band_3",   # Green (0.560 µm)
    "Band_4",   # Red (0.665 µm)
    "Band_5",   # Red Edge 1 (0.705 µm)
    "Band_6",   # Red Edge 2 (0.740 µm)
    "Band_7",   # Red Edge 3 (0.783 µm)
    "Band_8",   # NIR broad (0.842 µm)
    "Band_8A",  # NIR narrow (0.865 µm)
    "Band_11",  # SWIR 1 (1.610 µm)
    "Band_12",  # SWIR 2 (2.190 µm)
]

BAND_WAVELENGTHS = {
    "Band_2": 490,
    "Band_3": 560,
    "Band_4": 665,
    "Band_5": 705,
    "Band_6": 740,
    "Band_7": 783,
    "Band_8": 842,
    "Band_8A": 865,
    "Band_11": 1610,
    "Band_12": 2190,
}

BAND_NAMES = {
    "Band_2": "Blue (490 nm)",
    "Band_3": "Green (560 nm)",
    "Band_4": "Red (665 nm)",
    "Band_5": "Red Edge 1 (705 nm)",
    "Band_6": "Red Edge 2 (740 nm)",
    "Band_7": "Red Edge 3 (783 nm)",
    "Band_8": "NIR Broad (842 nm)",
    "Band_8A": "NIR Narrow (865 nm)",
    "Band_11": "SWIR 1 (1610 nm)",
    "Band_12": "SWIR 2 (2190 nm)",
}

# Species present in released CSV (DATA-DERIVED)
SPECIES_NAMES = [
    "Avicennia_germinans",
    "Rhizophora_mangle",
    "Laguncularia_racemosa",
]

# Paper's 4-Class Mapping (PAPER-SPECIFIED)
PAPER_4CLASS_MAPPING = {
    0: "Non-mangrove",
    1: "Rhizophora mangle",
    2: "Avicennia germinans",
    3: "Laguncularia racemosa",
}

# Data-derived 3-Species Mapping for monospecific experiment
SPECIES_TO_IDX_3CLASS = {
    "Rhizophora_mangle": 0,
    "Avicennia_germinans": 1,
    "Laguncularia_racemosa": 2,
}

IDX_TO_SPECIES_3CLASS = {v: k for k, v in SPECIES_TO_IDX_3CLASS.items()}

# Colors for figures matching paper style (Red for R. mangle, Black for A. germinans, Grey for L. racemosa)
SPECIES_COLORS = {
    "Rhizophora_mangle": "#d62728",    # Red
    "Avicennia_germinans": "#1f1f1f",  # Near Black
    "Laguncularia_racemosa": "#7f7f7f" # Grey
}

# Experimental configurations (PAPER-SPECIFIED)
HIDDEN_LAYERS = [1, 2, 3, 4, 5]
NEURONS_PER_LAYER = [5, 10, 20, 50, 100, 150, 300, 500]

# Train/Test Split (PAPER-SPECIFIED)
TRAIN_RATIO = 0.70
TEST_RATIO = 0.30

# Implementation Assumptions (NOT AVAILABLE in paper text)
RANDOM_SEED = 42
BATCH_SIZE = 64
EPOCHS = 100
DEFAULT_LEARNING_RATE = 0.001
PATIENCE = 15
