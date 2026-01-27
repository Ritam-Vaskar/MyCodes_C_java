# Q3: PCA for Fraud Detection with Imbalanced Dataset

## Objective
Evaluate if PCA can reduce dimensionality while preserving fraud detection accuracy using KNN and SVM classifiers on a highly imbalanced dataset.

## Dataset
- **Synthetic Fraud Detection** dataset
- **Features**: 30 numerical features
- **Samples**: 10,000 transactions
- **Imbalance**: 97% legitimate, 3% fraudulent (32:1 ratio)

## Implementation
1. Generate highly imbalanced fraud detection dataset
2. Train KNN and SVM without PCA (baseline)
3. Apply PCA with varying components {5, 10, 15, 20}
4. Compare ROC-AUC scores before and after PCA
5. Generate ROC curves for visualization

## Outputs
- `roc_auc_comparison.csv` - ROC-AUC scores for all configurations
- `roc_auc_comparison.png` - Performance comparison plots
- `roc_curves.png` - ROC curves for best configuration
- `summary.txt` - Analysis summary

## How to Run
```bash
cd q3
python main.py
```

## Expected Results
- High ROC-AUC scores (>0.90) even with severe class imbalance
- PCA maintains fraud detection capability with 50-67% dimensionality reduction
- Both KNN and SVM show robustness to PCA transformation
