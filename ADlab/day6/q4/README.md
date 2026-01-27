# Q4: PCA Impact on Intrusion Detection - Accuracy and Latency

## Objective
Analyze how PCA-based feature reduction impacts intrusion detection accuracy and detection latency.

## Dataset
- **Synthetic Intrusion Detection** dataset
- **Features**: 40 network traffic features
- **Samples**: 50,000 network events
- **Classes**: Normal traffic vs Intrusions

## Implementation
1. Create intrusion detection dataset
2. Measure training and prediction time without PCA
3. Apply PCA with {5, 10, 20, 30} components
4. Compare timing metrics and accuracy
5. Generate confusion matrices for all configurations

## Outputs
- `timing_accuracy_results.csv` - Complete timing and accuracy data
- `performance_comparison.png` - Multi-metric comparison plots
- `accuracy_latency_tradeoff.png` - Trade-off visualization
- `confusion_matrix_*.png` - Confusion matrices for each configuration
- `summary.txt` - Performance analysis

## How to Run
```bash
cd q4
python main.py
```

## Expected Results
- Significant reduction in training and prediction time with PCA
- Minimal accuracy loss with optimal component selection
- Clear visualization of accuracy vs latency trade-off
