# Q7: Spam Detection with TF-IDF and PCA

## Objective
Reduce computational cost while maintaining spam detection accuracy using TF-IDF → PCA → SVM pipeline.

## Dataset
- **20 Newsgroups** dataset (4 categories)
- **Features**: 5000 TF-IDF features from text
- **Pipeline**: Text → TF-IDF → PCA → SVM

## Implementation
1. Load newsgroups dataset as text classification proxy
2. Create TF-IDF feature vectors (5000 features)
3. Apply PCA with {50, 100, 200, 500, 1000} components
4. Train Linear SVM for classification
5. Compare memory usage and accuracy

## Outputs
- `results_comparison.csv` - Accuracy and memory metrics
- `accuracy_vs_memory.png` - Trade-off visualization
- `comprehensive_comparison.png` - Multi-metric analysis
- `classification_report_*.txt` - Detailed reports
- `summary.txt` - Performance summary

## How to Run
```bash
cd q7
python main.py
```

## Expected Results
- 80-95% memory savings with PCA
- Maintains >90% accuracy with 200-500 components
- Clear trade-off between memory and accuracy
