# Q1: Principal Component Analysis (PCA) on Wine Dataset

## Objective
Reduce dimensionality using PCA and visualize the results with variance analysis.

## Dataset
- **Wine Dataset** from sklearn
- **Features**: 13 chemical properties
- **Samples**: 178 wine samples
- **Classes**: 3 wine types

## Implementation
1. Load and standardize Wine dataset
2. Perform PCA with all components
3. Display variance explained by each PC
4. Create 2D visualization (first 2 PCs)
5. Create 3D visualization (first 3 PCs)

## Outputs
- `variance_explained.csv` - Variance contribution of each PC
- `variance_plot.png` - Individual and cumulative variance plots
- `pca_2d.png` - 2D projection visualization
- `pca_3d.png` - 3D projection visualization
- `pca_2d_data.csv` - 2D transformed data
- `pca_3d_data.csv` - 3D transformed data
- `summary.txt` - Analysis summary

## How to Run
```bash
cd q1
python main.py
```

## Expected Results
- Clear separation of wine classes in 2D/3D space
- First 2-3 PCs capture majority of variance (typically >60%)
- Visualization of how dimensionality reduction preserves class structure
