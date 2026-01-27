# Q10: Land Cover Classification with PCA-based Band Reduction

## Objective
Analyze how PCA-based band reduction influences land cover classification accuracy in remote sensing applications.

## Dataset
- **Synthetic Remote Sensing** dataset
- **Features**: 100 spectral bands (hyperspectral imagery)
- **Samples**: 8000 pixels
- **Classes**: 7 land cover types (Water, Forest, Urban, Agriculture, Grassland, Barren, Wetland)

## Implementation
1. Create hyperspectral remote sensing dataset
2. Train Random Forest and SVM without PCA (baseline)
3. Apply PCA with {5, 10, 20, 30, 50, 75} bands
4. Compare accuracy and computational efficiency
5. Analyze accuracy vs band reduction trade-off

## Outputs
- `results_comparison.csv` - Complete performance metrics
- `comprehensive_comparison.png` - Multi-metric analysis
- `accuracy_vs_reduction_tradeoff.png` - Trade-off visualization
- `confusion_matrix_*.png` - Confusion matrices
- `report_*.txt` - Classification reports
- `summary.txt` - Analysis summary

## How to Run
```bash
cd q10
python main.py
```

## Expected Results
- High accuracy maintained with 50-70% band reduction
- Significant speedup in training and prediction
- 20-30 principal components capture >95% variance
- Optimal for real-time remote sensing applications
