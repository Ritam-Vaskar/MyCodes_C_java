# Q5: PCA for Digit Recognition - Optimal Components Analysis

## Objective
Determine how many principal components are required to retain high digit recognition accuracy using KNN classifier.

## Dataset
- **Digits Dataset** from sklearn (subset of MNIST)
- **Features**: 64 features (8x8 pixel images)
- **Samples**: 1,797 digit images
- **Classes**: 10 digits (0-9)

## Implementation
1. Load digits dataset
2. Train KNN without PCA (baseline)
3. Apply PCA with varying components (1-64)
4. Plot accuracy vs number of components
5. Analyze optimal component selection

## Outputs
- `accuracy_vs_components.csv` - Complete results
- `accuracy_vs_components.png` - Main accuracy plot
- `accuracy_vs_components_zoomed.png` - Low component range
- `dimensionality_analysis.png` - Reduction and retention analysis
- `summary.txt` - Optimal components recommendation

## How to Run
```bash
cd q5
python main.py
```

## Expected Results
- Significant accuracy with just 10-15 components
- Clear visualization of accuracy plateau
- Optimal balance around 20-30 components
- 50-70% dimensionality reduction possible
