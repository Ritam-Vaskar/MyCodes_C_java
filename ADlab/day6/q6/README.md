# Q6: PCA Robustness with Noisy Clinical Features

## Objective
Evaluate if PCA improves classification stability and accuracy under noisy clinical feature conditions using SVM models.

## Dataset
- **Breast Cancer Wisconsin** dataset
- **Features**: 30 clinical features
- **Noise**: Synthetic Gaussian noise added at various levels

## Implementation
1. Load breast cancer dataset
2. Add synthetic noise at different levels (0.0 to 1.0)
3. Train SVM with and without PCA
4. Measure accuracy and cross-validation stability
5. Analyze robustness to noise

## Outputs
- `robustness_results.csv` - Complete results
- `accuracy_vs_noise.png` - Accuracy degradation plots
- `stability_analysis.png` - CV standard deviation analysis
- `accuracy_heatmap.png` - Method vs noise heatmap
- `degradation_analysis.png` - Baseline degradation
- `summary.txt` - Robustness analysis

## How to Run
```bash
cd q6
python main.py
```

## Expected Results
- PCA shows improved stability under noisy conditions
- Lower CV standard deviation with PCA
- Dimensionality reduction acts as noise filter
