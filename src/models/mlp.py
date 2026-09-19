"""
Multilayer Perceptron (MLP) and Logistic Regression model definitions.
Reference: Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961.
"""

import torch
import torch.nn as nn
from typing import List, Optional


class LogisticBaseline(nn.Module):
    """
    Logistic Regression baseline model as described in Section 2.3:
    'In this study, the initial model consisted of a single input and one output layer,
     with the sigmoid as the activation function, so that it could be interpreted
     as a logistic regression.'
    For multiclass, it maps directly from input features to class logits.
    """
    def __init__(self, in_features: int = 10, num_classes: int = 3):
        super().__init__()
        self.linear = nn.Linear(in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)


class MangroveMLP(nn.Module):
    """
    Multilayer Perceptron architecture evaluated in the paper:
    - Hidden layers: 1 to 5 layers
    - Neurons per hidden layer: 5, 10, 20, 50, 100, 150, 300, 500
    - Activation: ReLU in all hidden layers
    - Output layer: Linear logits (passed to CrossEntropyLoss or BCEWithLogitsLoss)
    """
    def __init__(
        self,
        in_features: int = 10,
        num_classes: int = 3,
        num_hidden_layers: int = 1,
        neurons_per_layer: int = 50,
    ):
        super().__init__()
        if num_hidden_layers < 1:
            raise ValueError("num_hidden_layers must be >= 1 for MangroveMLP. Use LogisticBaseline for 0 layers.")

        layers: List[nn.Module] = []
        
        # First hidden layer
        layers.append(nn.Linear(in_features, neurons_per_layer))
        layers.append(nn.ReLU())
        
        # Additional hidden layers
        for _ in range(num_hidden_layers - 1):
            layers.append(nn.Linear(neurons_per_layer, neurons_per_layer))
            layers.append(nn.ReLU())
        
        # Output layer
        layers.append(nn.Linear(neurons_per_layer, num_classes))
        
        self.network = nn.Sequential(*layers)
        self.num_hidden_layers = num_hidden_layers
        self.neurons_per_layer = neurons_per_layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def create_model(
    num_hidden_layers: int,
    neurons_per_layer: int,
    in_features: int = 10,
    num_classes: int = 3
) -> nn.Module:
    """
    Factory function to instantiate models matching paper configurations.
    - If num_hidden_layers == 0: returns LogisticBaseline.
    - If num_hidden_layers >= 1: returns MangroveMLP.
    """
    if num_hidden_layers == 0:
        return LogisticBaseline(in_features=in_features, num_classes=num_classes)
    return MangroveMLP(
        in_features=in_features,
        num_classes=num_classes,
        num_hidden_layers=num_hidden_layers,
        neurons_per_layer=neurons_per_layer
    )
