# Q2: Iris Species Classification using Decision Tree

## Overview
Multi-class classification of Iris species using Decision Tree Classifier to handle non-linear decision boundaries.

## Problem Statement
Develop a decision tree model to classify species in the Iris dataset. Evaluate using:
- **Accuracy**: Percentage of correctly classified species
- **Classification Report**: Precision, Recall, F1-score for each species
- **Decision Tree Visualization**: Visual representation of tree structure and splits

## Dataset
- **Source**: Scikit-learn Iris dataset (built-in)
- **Samples**: 150 total (50 per species)
- **Features**: 4 continuous features
  - Sepal length (cm)
  - Sepal width (cm)
  - Petal length (cm)
  - Petal width (cm)
- **Classes**: 3 species
  - Setosa
  - Versicolor
  - Virginica

## Model
- **Algorithm**: Decision Tree Classifier
- **Criterion**: Gini impurity
- **Max Depth**: 4 (prevents overfitting)
- **Train-Test Split**: 70-30 with stratification

## Project Structure
```
q2/
├── main.py                       # Main execution script
├── model/
│   └── decision_tree_model.py   # Iris classifier class
├── output/                       # Results and visualizations
├── README.md                     # This file
└── requirements.txt              # Dependencies
```

## Installation

```bash
cd "C:\C programing\ADlab\day3\q2"
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Output

### 1. Console Output
- Dataset statistics (samples, features, class distribution)
- Tree structure (depth, number of leaves)
- **Accuracy score**
- **Confusion matrix**
- **Classification report** (Precision, Recall, F1-score for each species)
- **Feature importance** rankings

### 2. Files Generated
- `output/predictions.csv` - Predictions for each test sample
- `output/metrics.txt` - Detailed performance metrics
- `output/iris_classification_results.png` - 4-panel visualization
- `output/decision_tree_structure.png` - Full decision tree visualization

### 3. Visualizations

#### iris_classification_results.png (4 panels):
1. **Confusion Matrix Heatmap** - Shows classification accuracy per species
2. **Class Distribution** - Actual vs Predicted counts
3. **Feature Importance** - Which features matter most
4. **Petal Dimensions Scatter** - Shows separability with misclassifications marked

#### decision_tree_structure.png:
- **Full tree structure** showing all decision nodes
- **Feature splits** at each node
- **Gini impurity** values
- **Sample counts** per node
- **Class predictions** at leaf nodes
- **Color-coded** by majority class

## Key Metrics

| Metric | Description |
|--------|-------------|
| **Accuracy** | Overall correct classifications across all species |
| **Precision** | Of predicted species X, how many are actually X |
| **Recall** | Of actual species X, how many were identified |
| **F1-Score** | Harmonic mean of precision and recall |

## Algorithm

### Decision Tree Learning Process

```
1. Start with all training samples at root
2. For each node:
   a. Calculate Gini impurity for all possible splits
   b. Choose split that maximizes information gain
   c. Split node into child nodes
3. Repeat until:
   - Max depth reached (4)
   - Node is pure (all same class)
   - Insufficient samples to split
4. Assign majority class to each leaf
```

### Prediction Process

```
1. Start at root node
2. Follow decision path based on feature values
3. At each node:
   - If feature[i] <= threshold: go left
   - Else: go right
4. Return class at leaf node
```

## Decision Tree Structure

Example split logic:
```
Root Node
├─ Petal length <= 2.45?
│  ├─ YES → Setosa (pure)
│  └─ NO → Continue...
│     ├─ Petal width <= 1.75?
│     │  ├─ YES → Versicolor (mostly)
│     │  └─ NO → Virginica (mostly)
```

## Expected Results

**Typical Performance:**
- Accuracy: ~95-100%
- Precision per class: ~0.95-1.00
- Recall per class: ~0.95-1.00
- F1-Score per class: ~0.95-1.00

**Feature Importance (typical):**
1. Petal width: ~0.45
2. Petal length: ~0.42
3. Sepal length: ~0.10
4. Sepal width: ~0.03

## Advantages of Decision Trees

✓ **Handles non-linear boundaries** - Can model complex relationships  
✓ **Interpretable** - Easy to understand decision rules  
✓ **No feature scaling needed** - Works with raw features  
✓ **Handles mixed data types** - Numerical and categorical  
✓ **Visual representation** - Can plot the entire tree

## Requirements
```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

---

**Date:** December 16, 2025  
**Status:** Complete ✓
