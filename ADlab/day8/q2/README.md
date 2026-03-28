# Q2: One-Hot Encoding vs Sparse Categorical

## Objective
Convert labels to one-hot encoding and train the model using categorical_crossentropy. Compare accuracy with sparse categorical version.

## Implementation
- Converts labels to one-hot encoding
- Trains model with categorical_crossentropy
- Trains identical model with sparse_categorical_crossentropy
- Compares test accuracy between both approaches

## Key Findings
- Both methods produce nearly identical results
- One-hot encoding: More memory, explicit representation
- Sparse categorical: Memory efficient, uses integer labels directly

## Output Files
- `encoding_comparison.png` - Bar chart comparing accuracies
- `comparison_results.txt` - Detailed comparison results

## Usage
```bash
python main.py
```
