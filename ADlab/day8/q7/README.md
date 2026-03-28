# Q7: Add Batch Normalization

## Objective
Add BatchNormalization after Conv layers. Retrain and compare convergence speed.

## Implementation
- Adds BatchNormalization after each Conv2D layer
- Trains with validation split
- Analyzes convergence speed (accuracy at epoch 3 vs final)
- Compares training stability

## Batch Normalization Benefits
- **Faster Convergence**: Normalizes inputs to each layer
- **Stable Training**: Reduces internal covariate shift
- **Higher Learning Rates**: Can use more aggressive optimization
- **Mild Regularization**: Small regularization effect

## Key Metrics
- **Epoch 3 Performance**: Early convergence indicator
- **Final Performance**: Overall model quality
- **Training Stability**: Smoother loss curves

## Output Files
- `batchnorm_analysis.png` - Convergence analysis plots
- `results.txt` - Performance metrics and benefits
- `batchnorm_model.h5` - Trained model

## Usage
```bash
python main.py
```
