# Q5: Train CNN with Validation Split

## Objective
Train CNN with validation_split=0.2. Plot training vs validation accuracy and loss to monitor overfitting.

## Implementation
- Trains CNN with 20% validation split
- Monitors training vs validation metrics
- Plots accuracy and loss curves
- Analyzes overfitting gap

## Key Features
- **Validation Split**: 80% training, 20% validation
- **Overfitting Detection**: Monitors gap between train/val accuracy
- **Visual Analysis**: Side-by-side comparison plots

## Expected Behavior
- Training accuracy typically higher than validation
- Gap indicates model's generalization capability
- Diverging curves suggest overfitting

## Output Files
- `train_vs_validation.png` - Comparison plots
- `validation_history.npz` - Complete training history
- `results.txt` - Detailed metrics and analysis
- `validation_model.h5` - Trained model

## Usage
```bash
python main.py
```
