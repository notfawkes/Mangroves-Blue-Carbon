# Paper Reported Results: Multilayer Perceptron for Mangrove Identification

Reference: **Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961**  
DOI: [10.1016/j.ecoinf.2024.102961](https://doi.org/10.1016/j.ecoinf.2024.102961)

---

## 1. Scientific Category & Status
- **Classification**: `PAPER REPORTED RESULTS`
- **Scope**: Published findings and numerical accuracy scores transcribed directly from the paper text (Section 3.2, 3.3) and figures (Fig. 5, Fig. 6, Fig. 9).
- **Important Note**: These numbers represent the authors' experiments on their balanced 60,000-pixel binary dataset and 40,000-pixel four-class dataset. Because the non-mangrove background class was not included in the public repository, these reported values serve as scientific reference benchmarks, **not** target values to be manufactured.

---

## 2. Binary Model Results (60,000 Pixels: Mangrove vs Non-Mangrove)

### Experimental Context:
- **Dataset**: Balanced 60,000 TOA Sentinel-2 pixels (30,000 Mangrove, 30,000 Non-mangrove).
- **Split**: 70% Training (42,000 pixels) / 30% Test (18,000 pixels).
- **Features**: 10 Sentinel-2 bands (B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12).
- **Architecture**: Feed-forward MLP with 1 to 5 hidden layers, ReLU activations, Sigmoid output, Binary Cross-Entropy loss, Adam optimizer.
- **Baseline**: Logistic regression (single input-to-output layer with sigmoid).

### Exact Published Accuracies:

| Model Architecture | Hidden Layers | Neurons per Layer | Train Accuracy | Test Accuracy | Status in Paper |
|---|:---:|:---:|:---:|:---:|---|
| **Logistic Regression** | 0 | - | **0.9916** | **0.9910** | Baseline model (lowest accuracy) |
| **1 Hidden Layer** | 1 | 300 | **0.9995** | **0.9988** | Highest score for 1 layer |
| **2 Hidden Layers** | 2 | 100 | **0.9994** | **0.9987** | Highest score for 2 layers |
| **3 Hidden Layers** | 3 | 50 | **0.9996** | **0.9987** | **Optimal score overall** (Section 3.2) |
| **4 Hidden Layers** | 4 | 150 | **0.9993** | **0.9986** | Shared highest for 4 layers |
| **4 Hidden Layers** | 4 | 300 | **0.9993** | **0.9986** | Most reliable spatial test (Section 3.3) |
| **5 Hidden Layers** | 5 | 50 | **0.9995** | **0.9988** | Shared highest for 5 layers |
| **5 Hidden Layers** | 5 | 300 | **0.9995** | **0.9988** | Shared highest for 5 layers |

### Summary of Binary Findings:
- All evaluated MLP configurations exceeded **0.990** accuracy.
- Even the logistic baseline achieved >99.1% accuracy, demonstrating that the spectral separation between mangrove forest and general non-mangrove land covers (water, dunes, urban, crops) is exceptionally high.
- The 3-layer, 50-neuron model demonstrated the highest training accuracy (0.9996) and near-peak test accuracy (0.9987).
- In spatial verification (Fig. 7), the 4-layer model with 300 neurons was selected by the authors as the most visually reliable.

---

## 3. Multiclass Model Results (40,000 Pixels: 4 Classes)

### Experimental Context:
- **Dataset**: Balanced 40,000 TOA Sentinel-2 pixels (10,000 per class):
  - Class 0: Non-mangrove
  - Class 1: *Rhizophora mangle* (Red mangrove)
  - Class 2: *Avicennia germinans* (Black mangrove)
  - Class 3: *Laguncularia racemosa* (White mangrove)
- **Split**: 70% Training (28,000 pixels) / 30% Test (12,000 pixels).
- **Features**: 10 Sentinel-2 bands, `StandardScaler`.
- **Architecture**: 1 to 5 hidden layers, ReLU activations, Softmax output, Multiclass Cross-Entropy loss, Adam optimizer.
- **Baseline**: Multiclass logistic regression.

### Exact Published Accuracies:

| Model Architecture | Hidden Layers | Neurons per Layer | Train Accuracy | Test Accuracy | Status in Paper |
|---|:---:|:---:|:---:|:---:|---|
| **Logistic Regression** | 0 | - | **0.7670** | **0.7684** | Baseline model (lowest accuracy) |
| **1 Hidden Layer** | 1 | 500 | **0.9110** | **0.9065** | Highest score for 1 layer |
| **2 Hidden Layers** | 2 | 300 | **0.9575** | **0.9436** | Highest score for 2 layers |
| **3 Hidden Layers** | 3 | 500 | **0.9863** | **0.9654** | Highest accuracy among reported models |
| **4 Hidden Layers** | 4 | 100 | **0.9662** | **0.9528** | Reported in Section 3.3 / Fig. 9 |
| **4 Hidden Layers** | 4 | 150 | **0.9775** | **0.9607** | Reported in Section 3.3 / Fig. 9 |
| **4 Hidden Layers** | 4 | 300 | **0.9795** | **0.9602** | Selected in Section 3.2 & Fig. 8 |
| **5 Hidden Layers** | 5 | 50 | **0.9550** | **0.9454** | **Most reliable for spatial mapping** (Section 3.3, Fig. 9, 10) |
| **5 Hidden Layers** | 5 | 150 | **0.9810** | **0.9632** | Reported in Section 3.3 / Fig. 9 |
| **5 Hidden Layers** | 5 | 300 | **0.9873** | **0.9684** | Peak test accuracy among reported models |

### Summary of Multiclass Findings:
- Multiclass accuracy was substantially lower for the logistic baseline (76.7%), proving that discriminating among individual mangrove species requires non-linear decision boundaries.
- MLP models with 2 or more hidden layers consistently achieved $>94\%$ accuracy.
- The 5-layer model with 50 neurons was explicitly identified as the **most reliable model overall for spatial generalizability** (Figs. 9 and 10), even though its test accuracy (0.9454) was slightly below the peak model (0.9684). This reflects the authors' insight that simpler models with fewer neurons per layer avoid overfitting to spectral noise.

---

## 4. Architecture Inventory & Evaluation Matrix

The paper describes exploring hidden layers 1 to 5 across 8 neuron widths: $\{5, 10, 20, 50, 100, 150, 300, 500\}$:

```
Total Potential Model Configurations per Problem:
1 Logistic Baseline + 5 Hidden Layer depths × 8 Neuron widths = 41 Architectures
```

The authors chose to report specific representative best-performing models in the main body text and highlight their spatial predictions in Figs 7–10.
