# Q8: Increase Filter Sizes (32 → 64 → 128)

## Objective
Increase filter sizes progressively (32 → 64 → 128). Compare test accuracy and print total parameter increase.

## Implementation
- Adds third Conv2D layer with 128 filters
- Compares parameters with baseline (Q7)
- Analyzes performance vs complexity trade-off
- Evaluates accuracy improvement

## Architecture Enhancement
```
Conv2D(32) → BatchNorm → MaxPool
↓
Conv2D(64) → BatchNorm → MaxPool
↓
Conv2D(128) → BatchNorm  ← NEW LAYER
↓
Flatten → Dense(128) → Dropout → Dense(10)
```

## Analysis
- **Parameter Increase**: ~50-70% more parameters
- **Performance Gain**: Expected 2-3% accuracy improvement
- **Feature Complexity**: More filters capture richer patterns

## Expected Results
- Test Accuracy: ~72-75%
- Deeper feature extraction
- Better pattern recognition

## Output Files
- `filter_size_analysis.png` - Training curves and comparison
- `results.txt` - Parameter analysis and performance
- `large_filter_model.h5` - Trained model

## Usage
```bash
python main.py
```
