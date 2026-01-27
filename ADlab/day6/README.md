# ADLab - Day 6: Principal Component Analysis (PCA) Applications

Comprehensive analysis of PCA for dimensionality reduction across 10 different machine learning applications.

## Overview

This folder contains 10 distinct PCA-based projects analyzing how dimensionality reduction impacts model performance, computational efficiency, and accuracy across various domains.

## Project Structure

```
day6/
├── q1/  - Wine Dataset PCA with 2D/3D Visualization
├── q2/  - Breast Cancer SVM with Varying PCA Components
├── q3/  - Fraud Detection with Imbalanced Dataset
├── q4/  - Intrusion Detection Timing Analysis
├── q5/  - Digit Recognition Optimal Components
├── q6/  - Noisy Clinical Features Robustness
├── q7/  - Spam Detection with TF-IDF Pipeline
├── q8/  - Plant Disease Classification
├── q9/  - Eye State Detection: SVM vs KNN
└── q10/ - Land Cover Remote Sensing
```

## Questions Summary

### Q1: Wine Dataset PCA Visualization
- **Dataset**: Wine (13 features, 178 samples, 3 classes)
- **Objective**: Visualize PCA with 2D/3D plots and variance analysis
- **Key Output**: Variance explained plots, 2D/3D projections

### Q2: Breast Cancer SVM with PCA
- **Dataset**: Breast Cancer (30 features, 569 samples)
- **Objective**: Compare SVM accuracy with k={2,5,10,15} components
- **Key Metrics**: Accuracy, Precision, Recall

### Q3: Fraud Detection PCA
- **Dataset**: Synthetic fraud (30 features, 97:3 imbalance)
- **Objective**: Maintain fraud detection with dimensionality reduction
- **Key Metrics**: ROC-AUC scores for KNN and SVM

### Q4: Intrusion Detection Latency
- **Dataset**: Synthetic intrusion (40 features, 50K samples)
- **Objective**: Analyze timing and accuracy trade-offs
- **Key Metrics**: Training/prediction time, confusion matrices

### Q5: Digit Recognition Optimization
- **Dataset**: Digits (64 features, 1797 samples)
- **Objective**: Find optimal number of components for KNN
- **Key Output**: Accuracy vs components curve

### Q6: Noisy Clinical Features
- **Dataset**: Breast Cancer with synthetic noise
- **Objective**: Test PCA robustness under noise
- **Key Metrics**: Accuracy degradation, CV stability

### Q7: Spam Detection with TF-IDF
- **Dataset**: 20 Newsgroups (5000 TF-IDF features)
- **Objective**: Reduce memory and computation cost
- **Key Metrics**: Memory usage, accuracy

### Q8: Plant Disease Classification
- **Dataset**: Synthetic plant disease (50 features)
- **Objective**: Compare feature importance vs PCA
- **Key Metrics**: Inference speed, accuracy

### Q9: Eye State Detection
- **Dataset**: Synthetic eye state (14 features)
- **Objective**: Compare SVM vs KNN with PCA
- **Key Metrics**: Accuracy, Precision, Recall, F1-Score

### Q10: Land Cover Remote Sensing
- **Dataset**: Synthetic hyperspectral (100 bands, 7 classes)
- **Objective**: Analyze band reduction impact
- **Key Metrics**: Accuracy vs band reduction trade-off

## Installation

### Install dependencies for all projects:
```bash
pip install -r requirements.txt
```

### Or install for individual projects:
```bash
cd q1
pip install -r requirements.txt
```

## Running the Projects

### Run individual projects:
```bash
cd q1
python main.py
```

### Run all projects sequentially:
```bash
python run_all.py
```

## Common Dependencies

- numpy
- pandas
- matplotlib
- scikit-learn
- seaborn

## Expected Outcomes

All projects demonstrate:
1. **Dimensionality Reduction**: 30-90% feature reduction possible
2. **Accuracy Preservation**: Most maintain >95% of original accuracy
3. **Speed Improvements**: 1.5-5x faster training/inference
4. **Memory Savings**: Up to 95% memory reduction (Q7)
5. **Robustness**: PCA often improves stability (Q6)

## Key Insights

### When PCA Works Best:
- High-dimensional data (>20 features)
- Correlated features
- Real-time applications requiring speed
- Memory-constrained environments

### Optimal Component Selection:
- 2-5 components: Quick visualization
- 10-20 components: Good balance for most tasks
- 30-50 components: Near-original performance
- Based on 95% variance retention

### Performance Trade-offs:
- **Accuracy**: Minimal loss (<5%) with proper component selection
- **Speed**: Significant gains (2-5x) with 50%+ reduction
- **Interpretability**: May be reduced but offset by visualization gains

## Visualization Outputs

Each project generates:
- Performance comparison plots
- Confusion matrices
- Trade-off analyses
- Feature importance comparisons
- Time/memory efficiency charts

## Research Applications

These implementations are suitable for:
- Academic research papers
- Machine learning course assignments
- Industry benchmark studies
- Algorithm comparison studies
- Real-world deployment planning

## Notes

- All datasets are either from sklearn or synthetically generated
- Random seeds are fixed for reproducibility
- Outputs are saved to individual `output/` directories
- All timings are system-dependent

## Author

Created for Advanced Data Analytics Lab coursework.

## License

Educational use only.
