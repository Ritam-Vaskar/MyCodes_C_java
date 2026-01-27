# Q8: Plant Disease Classification with PCA

## Objective
Analyze how PCA impacts plant disease classification accuracy using spectral and environmental features. Compare feature importance vs PCA components and inference speed.

## Dataset
- **Synthetic Plant Disease** dataset
- **Features**: 50 spectral and environmental features
- **Samples**: 5000 plant samples
- **Classes**: 5 disease types

## Implementation
1. Create plant disease dataset with spectral features
2. Train Random Forest and analyze feature importance
3. Apply PCA with varying components {5, 10, 15, 20, 30, 40}
4. Compare accuracy and inference speed
5. Analyze feature importance vs PCA contributions

## Outputs
- `results_comparison.csv` - Complete performance metrics
- `feature_importance.csv` and `.png` - Original feature importance
- `pca_contribution_*.csv` - PCA component contributions
- `performance_comparison.png` - Multi-metric analysis
- `feature_vs_pca_importance.png` - Importance comparison
- `summary.txt` - Analysis summary

## How to Run
```bash
cd q8
python main.py
```

## Expected Results
- Faster inference with PCA (1.5-3x speedup)
- Maintained accuracy with 20-30 components
- Clear trade-off between speed and accuracy
