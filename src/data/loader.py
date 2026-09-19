"""
Data loader and dataset utilities for Sentinel-2 mangrove reflectance.
Reference: Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional, Dict

from src.config import (
    CSV_PATH,
    SPECTRAL_BANDS,
    SPECIES_TO_IDX_3CLASS,
    RANDOM_SEED,
    TRAIN_RATIO,
    TEST_RATIO,
)


def load_raw_data(nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Load the raw Sentinel-2 monospecific mangrove reflectance CSV.
    The file contains 1,605,681 rows and 12 columns.
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Raw CSV not found at {CSV_PATH}")
    
    df = pd.read_csv(CSV_PATH, nrows=nrows)
    return df


def sample_balanced_3species(
    df: pd.DataFrame,
    samples_per_class: int = 10000,
    random_seed: int = RANDOM_SEED
) -> pd.DataFrame:
    """
    Create a class-balanced 3-species dataset from the available mangrove data.
    Samples exactly `samples_per_class` rows from each of:
      - Rhizophora mangle (available: 125,832)
      - Avicennia germinans (available: 1,441,482)
      - Laguncularia racemosa (available: 38,367)
    
    Total samples = 3 * samples_per_class (default 30,000).
    """
    sampled_dfs = []
    for spp in ["Rhizophora_mangle", "Avicennia_germinans", "Laguncularia_racemosa"]:
        spp_df = df[df["Spp"] == spp]
        if len(spp_df) < samples_per_class:
            raise ValueError(f"Not enough samples for {spp}: requested {samples_per_class}, found {len(spp_df)}")
        sampled = spp_df.sample(n=samples_per_class, random_state=random_seed)
        sampled_dfs.append(sampled)
    
    balanced_df = pd.concat(sampled_dfs, ignore_index=True)
    # Shuffle the combined dataset
    balanced_df = balanced_df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    return balanced_df


def prepare_3species_train_test(
    df: pd.DataFrame,
    test_size: float = TEST_RATIO,
    random_seed: int = RANDOM_SEED
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """
    Prepares train and test arrays with StandardScaler:
    - X: 10 Sentinel-2 bands
    - y: Integer encoded classes (0: R. mangle, 1: A. germinans, 2: L. racemosa)
    - 70% train / 30% test split
    - StandardScaler fit ONLY on training data, then transforming both train and test.
    """
    X = df[SPECTRAL_BANDS].values.astype(np.float32)
    y = df["Spp"].map(SPECIES_TO_IDX_3CLASS).values.astype(np.int64)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_seed,
        stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
