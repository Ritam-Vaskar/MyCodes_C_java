# Q2: SVM Classification with PCA on Breast Cancer Dataset

## Objective
Analyze how SVM classification accuracy changes when reducing 30 original features to k principal components.

## Dataset
- **Breast Cancer Wisconsin** dataset from sklearn
- **Features**: 30 numerical features
- **Samples**: 569 samples
- **Classes**: Malignant, Benign

## Implementation
1. Load and preprocess Breast Cancer dataset
2. Train SVM with original 30 features (baseline)
3. Apply PCA with k = {2, 5, 10, 15} components
4. Train SVM for each k value
5. Compare accuracy, precision, recall metrics

## Outputs
- `results_comparison.csv` - Metrics for all configurations
- `metrics_comparison.png` - Visual comparison of metrics
- `accuracy_vs_variance.png` - Tradeoff visualization
- `confusion_matrix_k_components.png` - Confusion matrices for each k
- `classification_report_k_components.txt` - Detailed reports
- `summary.txt` - Analysis summary

## How to Run
```bash
cd q2
python main.py
```

## Expected Results
- High accuracy (>95%) even with reduced dimensions
- 10-15 components typically maintain near-original performance
- Clear tradeoff between dimensionality reduction and accuracy
