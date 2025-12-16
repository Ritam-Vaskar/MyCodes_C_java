# ADLab Day 3: Machine Learning Classification Models

## Overview
Two classification projects demonstrating different ML algorithms for different problem types.

---

## Q1: Binary Classification - Spam Email Detection 🔍

**Algorithm:** Logistic Regression  
**Problem:** Binary classification (Spam vs Non-Spam)  
**Dataset:** 5,572 real SMS messages from UCI repository

### Key Results
- **Accuracy:** 97.40%
- **Spam Detection Rate:** 80.54% (120/149 spam caught)
- **False Positives:** 0 (perfect precision)
- **Dataset:** Real SMS Spam Collection (auto-downloaded)

### Output Files
- `q1/output/spam_classification_results.png` - 4-panel visualization
- `q1/output/predictions.csv` - Individual predictions
- `q1/output/metrics.txt` - Detailed metrics

### Metrics Evaluated
✓ Accuracy  
✓ Confusion Matrix  
✓ Precision, Recall, F1-Score for both classes  
✓ Top spam/non-spam indicator words

---

## Q2: Multi-Class Classification - Iris Species Detection 🌸

**Algorithm:** Decision Tree Classifier  
**Problem:** Multi-class classification (3 species)  
**Dataset:** 150 iris samples (built-in scikit-learn)

### Key Results
- **Accuracy:** 88.89%
- **Tree depth:** 4 levels
- **Number of leaves:** 7
- **Most important features:** Petal length (54.9%), Petal width (43.7%)

### Output Files
- `q2/output/iris_classification_results.png` - 4-panel visualization
- `q2/output/decision_tree_structure.png` - **Full tree visualization**
- `q2/output/predictions.csv` - Individual predictions
- `q2/output/metrics.txt` - Detailed metrics

### Metrics Evaluated
✓ Accuracy  
✓ Confusion Matrix  
✓ Precision, Recall, F1-Score for each species  
✓ Feature importance rankings  
✓ **Decision tree visualization using plot_tree()**

---

## Quick Start

### Run Both Projects
```bash
# Q1: Spam Classification
cd "C:\C programing\ADlab\day3\q1"
python main.py

# Q2: Iris Classification
cd "C:\C programing\ADlab\day3\q2"
python main.py
```

### Install Dependencies
```bash
pip install numpy pandas scikit-learn matplotlib seaborn
```

---

## Project Structure

```
day3/
├── README.md                    # This file
│
├── q1/                          # Binary Classification
│   ├── main.py                  # Spam classifier
│   ├── model/
│   │   └── logistic_regression_model.py
│   ├── utils/
│   │   └── data_loader.py
│   ├── output/
│   │   ├── spam_classification_results.png
│   │   ├── predictions.csv
│   │   └── metrics.txt
│   ├── README.md
│   └── requirements.txt
│
└── q2/                          # Multi-Class Classification
    ├── main.py                  # Iris classifier
    ├── model/
    │   └── decision_tree_model.py
    ├── output/
    │   ├── iris_classification_results.png
    │   ├── decision_tree_structure.png
    │   ├── predictions.csv
    │   └── metrics.txt
    ├── README.md
    └── requirements.txt
```

---

## Key Differences

| Aspect | Q1: Logistic Regression | Q2: Decision Tree |
|--------|------------------------|-------------------|
| **Problem Type** | Binary classification | Multi-class classification |
| **Data Type** | Text (SMS messages) | Numerical (measurements) |
| **Dataset Size** | 5,572 real messages | 150 samples |
| **Features** | 1000 TF-IDF features | 4 physical measurements |
| **Decision Boundary** | Linear | Non-linear |
| **Interpretability** | Feature coefficients | Tree structure visualization |
| **Accuracy** | 97.40% | 88.89% |
| **Classes** | 2 (Spam, Non-Spam) | 3 (Setosa, Versicolor, Virginica) |
| **Data Source** | UCI/GitHub (auto-download) | Scikit-learn built-in |

---

## Algorithm Highlights

### Logistic Regression (Q1)
- **Linear model** for binary classification
- Uses **sigmoid function** to output probabilities
- **TF-IDF vectorization** converts text to numbers
- **Coefficient weights** show word importance
- Perfect for linearly separable problems

### Decision Tree (Q2)
- **Non-linear model** for complex boundaries
- Uses **recursive splitting** based on features
- **Gini impurity** to measure split quality
- **Fully interpretable** - can visualize entire tree
- Handles non-linear relationships naturally

---

## Performance Summary

### Q1: Spam Classification
```
              precision    recall  f1-score   support
Non-Spam        0.9709    1.0000    0.9852       966
Spam            1.0000    0.8054    0.8922       149
accuracy                            0.9740      1115
```

**Note**: Imbalanced dataset (13% spam). Model achieves perfect precision (no false positives) but misses ~20% of spam messages.

### Q2: Iris Classification
```
              precision    recall  f1-score   support
setosa          1.0000    1.0000    1.0000        15
versicolor      0.8571    0.8000    0.8276        15
virginica       0.8125    0.8667    0.8387        15
accuracy                            0.8889        45
```

---

## Visualizations Included

### Q1 Visualizations:
1. Confusion matrix heatmap
2. Class distribution (actual vs predicted)
3. Top 10 spam indicator words
4. Top 10 non-spam indicator words

### Q2 Visualizations:
1. Confusion matrix heatmap
2. Class distribution (actual vs predicted)
3. Feature importance bar chart
4. Petal dimensions scatter plot (with misclassifications marked)
5. **Full decision tree structure** (showing all splits)

---

## Learning Objectives Achieved

✅ Binary classification using Logistic Regression  
✅ Multi-class classification using Decision Trees  
✅ Model evaluation with accuracy, confusion matrix, classification report  
✅ Precision, Recall, F1-Score calculation for all classes  
✅ Decision tree visualization using `plot_tree()`  
✅ Understanding linear vs non-linear decision boundaries  
✅ Feature importance analysis  
✅ Text preprocessing with TF-IDF  

---

**Date:** December 16, 2025  
**Status:** Complete ✓  
**Total Projects:** 2  
**Total Samples Analyzed:** Q1=5,572 (real SMS), Q2=150 (Iris)  
**Overall Accuracy:** Q1=97.40%, Q2=88.89%
