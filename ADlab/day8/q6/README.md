# Q6: Add Dropout Regularization

## Objective
Add Dropout(0.3) after Dense layer and compare validation accuracy with Q5 (without Dropout).

## Implementation
- Adds Dropout(0.3) layer after Dense(128, ReLU)
- Trains with validation split
- Compares with Q5 results
- Analyzes overfitting reduction

## Dropout Benefits
- **Prevents Overfitting**: Randomly drops 30% of neurons during training
- **Improves Generalization**: Forces network to learn robust features
- **Reduces Train-Val Gap**: Smaller gap indicates better generalization

## Expected Impact
- Slight decrease in training accuracy
- Improved validation accuracy
- Reduced overfitting gap

## Output Files
- `dropout_analysis.png` - Training curves and comparison
- `results.txt` - Performance metrics and comparison
- `dropout_model.h5` - Trained model

## Usage
```bash
python main.py
```
