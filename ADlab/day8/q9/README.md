# Q9: Use Early Stopping

## Objective
Use EarlyStopping (patience=3). Train for up to 25 epochs. Print stopped epoch and compare final accuracy.

## Implementation
- Implements EarlyStopping callback
- Monitors validation loss
- Patience of 3 epochs (stops if no improvement)
- Restores best weights
- Saves computational resources

## Early Stopping Configuration
- **Monitor**: val_loss
- **Patience**: 3 epochs
- **Max Epochs**: 25
- **Restore Best Weights**: Yes

## Benefits
- **Optimal Training**: Stops at best performance
- **Time Saving**: Avoids unnecessary epochs
- **Prevents Overfitting**: Stops before degradation
- **Automatic Tuning**: No manual epoch selection needed

## Expected Behavior
- Typically stops at epoch 10-15
- Saves 40-60% of training time
- Test accuracy similar or better than fixed epoch training

## Output Files
- `early_stopping_analysis.png` - Training curves with stop markers
- `results.txt` - Stopping analysis and comparison
- `early_stopping_model.h5` - Best model (restored weights)

## Usage
```bash
python main.py
```
