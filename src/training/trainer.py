"""
Model training and evaluation pipeline for 3-species mangrove classification.
Reference: Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961.
"""

import time
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List, Optional
from pathlib import Path

from src.config import (
    RANDOM_SEED,
    BATCH_SIZE,
    EPOCHS,
    DEFAULT_LEARNING_RATE,
    HIDDEN_LAYERS,
    NEURONS_PER_LAYER,
    RESULTS_MODELS_DIR,
    SAVED_MODELS_DIR,
)
from src.models.mlp import create_model


def set_seed(seed: int = RANDOM_SEED):
    """Ensure deterministic execution across PyTorch and NumPy."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_single_model(
    model: nn.Module,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    epochs: int = EPOCHS,
    batch_size: int = BATCH_SIZE,
    learning_rate: float = DEFAULT_LEARNING_RATE,
    device: Optional[torch.device] = None,
) -> Dict:
    """
    Train a single model (MLP or Logistic) using Adam optimizer and Cross-Entropy loss.
    Tracks training duration, train accuracy, and test accuracy.
    """
    if device is None:
        device = torch.device("cpu")
        
    model.to(device)
    set_seed(RANDOM_SEED)
    
    train_dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long).to(device)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    history = {"train_loss": [], "train_acc": [], "test_acc": []}
    start_time = time.time()
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * batch_x.size(0)
            
        epoch_loss = running_loss / len(X_train)
        history["train_loss"].append(epoch_loss)
        
        # Periodic evaluation
        if (epoch + 1) % 10 == 0 or epoch == epochs - 1:
            model.eval()
            with torch.no_grad():
                train_preds = model(X_train_tensor).argmax(dim=1)
                test_preds = model(X_test_tensor).argmax(dim=1)
                train_acc = (train_preds == y_train_tensor).float().mean().item()
                test_acc = (test_preds == y_test_tensor).float().mean().item()
                history["train_acc"].append(train_acc)
                history["test_acc"].append(test_acc)
                
    elapsed_time = time.time() - start_time
    
    # Final evaluation
    model.eval()
    with torch.no_grad():
        final_train_preds = model(X_train_tensor).argmax(dim=1)
        final_test_preds = model(X_test_tensor).argmax(dim=1)
        final_train_acc = (final_train_preds == y_train_tensor).float().mean().item()
        final_test_acc = (final_test_preds == y_test_tensor).float().mean().item()
        
    return {
        "train_accuracy": final_train_acc,
        "test_accuracy": final_test_acc,
        "training_time_seconds": elapsed_time,
        "epochs": epochs,
        "history": history,
        "test_predictions": final_test_preds.cpu().numpy(),
    }


def evaluate_architecture_grid(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    epochs: int = 30,
    batch_size: int = 256,
    learning_rate: float = DEFAULT_LEARNING_RATE,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Evaluate the full grid of model configurations:
    - 1 Logistic Regression baseline
    - 5 Hidden Layer depths x 8 Neuron counts = 40 MLP configurations
    Total = 41 models on the 3-species dataset.
    """
    records = []
    
    # 1. Logistic Baseline
    if verbose:
        print("Training Model 1/41: Logistic Regression Baseline...")
    logistic_model = create_model(num_hidden_layers=0, neurons_per_layer=0, num_classes=3)
    res = train_single_model(
        logistic_model, X_train, y_train, X_test, y_test,
        epochs=epochs, batch_size=batch_size, learning_rate=learning_rate
    )
    records.append({
        "Model_ID": "Logistic_Baseline",
        "Architecture_Type": "Logistic",
        "Hidden_Layers": 0,
        "Neurons_Per_Layer": 0,
        "Total_Parameters": sum(p.numel() for p in logistic_model.parameters()),
        "Train_Accuracy": res["train_accuracy"],
        "Test_Accuracy": res["test_accuracy"],
        "Training_Time_Sec": res["training_time_seconds"],
    })
    
    # 2. MLP Grid
    model_count = 1
    for layers in HIDDEN_LAYERS:
        for neurons in NEURONS_PER_LAYER:
            model_count += 1
            model_id = f"MLP_{layers}L_{neurons}N"
            if verbose:
                print(f"Training Model {model_count}/41: {model_id}...")
            mlp_model = create_model(num_hidden_layers=layers, neurons_per_layer=neurons, num_classes=3)
            res = train_single_model(
                mlp_model, X_train, y_train, X_test, y_test,
                epochs=epochs, batch_size=batch_size, learning_rate=learning_rate
            )
            records.append({
                "Model_ID": model_id,
                "Architecture_Type": "MLP",
                "Hidden_Layers": layers,
                "Neurons_Per_Layer": neurons,
                "Total_Parameters": sum(p.numel() for p in mlp_model.parameters()),
                "Train_Accuracy": res["train_accuracy"],
                "Test_Accuracy": res["test_accuracy"],
                "Training_Time_Sec": res["training_time_seconds"],
            })
            
    df_results = pd.DataFrame(records)
    return df_results
