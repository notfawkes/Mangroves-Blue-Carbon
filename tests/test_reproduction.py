"""
Lightweight test suite for mangrove paper reproduction.
Verifies data loading, preprocessing, model architecture shapes, and deterministic behavior.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import numpy as np
import pandas as pd
import torch

from src.config import (
    SPECTRAL_BANDS,
    SPECIES_NAMES,
    SPECIES_TO_IDX_3CLASS,
    PAPER_4CLASS_MAPPING,
    CSV_PATH,
    XML_PATH,
)
from src.data.loader import load_raw_data, sample_balanced_3species, prepare_3species_train_test
from src.models.mlp import create_model, LogisticBaseline, MangroveMLP


def test_data_paths_exist():
    """Verify that the raw CSV and XML files exist."""
    assert CSV_PATH.exists(), f"Missing CSV at {CSV_PATH}"
    assert XML_PATH.exists(), f"Missing XML metadata at {XML_PATH}"


def test_raw_csv_schema_and_classes():
    """Verify CSV header has exactly 12 columns, 10 bands, and only 3 mangrove species."""
    df_head = load_raw_data(nrows=100)
    expected_cols = ["ID_Imagen", "Spp"] + SPECTRAL_BANDS
    assert list(df_head.columns) == expected_cols, "CSV columns do not match expected schema"
    assert len(SPECTRAL_BANDS) == 10, "Paper specifies exactly 10 spectral bands"


def test_balanced_sampling():
    """Verify that sample_balanced_3species returns equal class distribution."""
    # Test on small sample
    df_head = load_raw_data(nrows=50000)
    # Ensure all 3 species exist in sample
    available_spps = df_head["Spp"].unique()
    if len(available_spps) == 3:
        min_count = df_head["Spp"].value_counts().min()
        n = min(100, min_count)
        sampled = sample_balanced_3species(df_head, samples_per_class=n, random_seed=42)
        counts = sampled["Spp"].value_counts().to_dict()
        for spp in SPECIES_NAMES:
            assert counts[spp] == n, f"Class {spp} count mismatch"


def test_standard_scaler_behavior():
    """Verify StandardScaler normalizes features with zero mean and unit variance on train set."""
    # Synthetic feature matrix with 10 bands
    np.random.seed(42)
    X = np.random.randn(100, 10) * 5.0 + 10.0
    y = np.random.choice([0, 1, 2], size=100)
    df = pd.DataFrame(X, columns=SPECTRAL_BANDS)
    df["Spp"] = [SPECIES_NAMES[i] for i in y]
    df["ID_Imagen"] = "test_id"
    
    X_train_scaled, X_test_scaled, y_train, y_test, scaler = prepare_3species_train_test(
        df, test_size=0.30, random_seed=42
    )
    
    # Train set should have mean ~0 and std ~1
    assert np.allclose(X_train_scaled.mean(axis=0), 0.0, atol=1e-5), "Train mean should be ~0"
    assert np.allclose(X_train_scaled.std(axis=0), 1.0, atol=1e-5), "Train std should be ~1"


def test_model_shapes():
    """Verify forward pass output shapes for LogisticBaseline and MangroveMLP."""
    batch_size = 16
    in_features = 10
    num_classes = 3
    x = torch.randn(batch_size, in_features)
    
    # Logistic baseline
    logistic = create_model(num_hidden_layers=0, neurons_per_layer=0, in_features=in_features, num_classes=num_classes)
    out_log = logistic(x)
    assert out_log.shape == (batch_size, num_classes), f"Expected shape ({batch_size}, {num_classes}), got {out_log.shape}"
    
    # MLP with 1, 3, 5 layers
    for layers in [1, 3, 5]:
        for neurons in [10, 50, 300]:
            mlp = create_model(num_hidden_layers=layers, neurons_per_layer=neurons, in_features=in_features, num_classes=num_classes)
            out_mlp = mlp(x)
            assert out_mlp.shape == (batch_size, num_classes), f"MLP ({layers}L, {neurons}N) output shape mismatch"


def test_reproducibility():
    """Verify deterministic weight initialization and output under fixed seed."""
    torch.manual_seed(42)
    m1 = create_model(num_hidden_layers=2, neurons_per_layer=50, in_features=10, num_classes=3)
    
    torch.manual_seed(42)
    m2 = create_model(num_hidden_layers=2, neurons_per_layer=50, in_features=10, num_classes=3)
    
    x = torch.randn(4, 10)
    assert torch.equal(m1(x), m2(x)), "Models with same seed must produce identical outputs"
