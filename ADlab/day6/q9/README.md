# Q9: Eye State Detection - SVM vs KNN with PCA

## Objective
Compare classification accuracy of SVM and KNN using original eye-feature vectors versus PCA-reduced features for eye state (open/closed) detection.

## Dataset
- **Synthetic Eye State** dataset (EEG-like features)
- **Features**: 14 eye-related feature vectors
- **Samples**: 10,000 observations
- **Classes**: Eye Open vs Eye Closed

## Implementation
1. Create eye state detection dataset
2. Train SVM and KNN without PCA (baseline)
3. Apply PCA with {2, 4, 6, 8, 10, 12} components
4. Compare accuracy, precision, recall, F1-score
5. Generate confusion matrices for all configurations

## Outputs
- `results_comparison.csv` - Complete metrics for all configurations
- `metrics_comparison.png` - Multi-metric comparison plots
- `classifier_comparison.png` - Side-by-side classifier analysis
- `performance_heatmap.png` - Performance heatmaps
- `confusion_matrix_*.png` - Confusion matrices
- `summary.txt` - Performance analysis

## How to Run
```bash
cd q9
python main.py
```

## Expected Results
- High accuracy (>90%) for both classifiers
- SVM typically outperforms KNN slightly
- 30-50% dimensionality reduction possible
- PCA maintains or improves performance
