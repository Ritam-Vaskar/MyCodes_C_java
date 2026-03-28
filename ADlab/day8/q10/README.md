# Q10: Generate Confusion Matrix and Display Misclassified Images

## Objective
Generate confusion matrix, classification report, and display 15 misclassified CIFAR-10 images with error analysis.

## Implementation
- Loads best model from previous questions (Q9/Q8/Q7)
- Makes predictions on test set
- Generates confusion matrix heatmap
- Creates classification report (precision/recall/F1)
- Displays 15 misclassified images with predictions
- Analyzes per-class performance

## Outputs Generated
1. **Confusion Matrix**: 10×10 heatmap showing prediction patterns
2. **Classification Report**: Detailed metrics per class
3. **Misclassified Images**: Visual examples of errors
4. **Class Accuracy Chart**: Per-class performance comparison
5. **Evaluation Summary**: Complete analysis report

## Error Analysis Features
- Most confused class pairs
- Worst/best performing classes
- Confidence scores for misclassifications
- Misclassification rate

## Expected Insights
- Cat ↔ Dog confusion (similar features)
- Automobile ↔ Truck confusion (vehicle similarity)
- Bird ↔ Airplane confusion (sky background)
- Clear visualization of model strengths/weaknesses

## Output Files
- `confusion_matrix.png` - Confusion matrix heatmap
- `classification_report.txt` - Detailed metrics
- `misclassified_images.png` - 15 error examples
- `class_accuracy.png` - Per-class performance
- `evaluation_summary.txt` - Complete summary

## Usage
```bash
python main.py
```

**Note**: Requires a trained model from Q7, Q8, or Q9.
