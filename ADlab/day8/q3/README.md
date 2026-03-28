# Q3: Build Simple CNN Model

## Objective
Build a simple CNN model with Conv2D(32, 3×3, ReLU), MaxPooling2D, Flatten, Dense(128, ReLU), Dense(10, Softmax). Train for 5 epochs and print test accuracy.

## Architecture
```
Conv2D(32, 3×3, ReLU)
↓
MaxPooling2D(2×2)
↓
Flatten
↓
Dense(128, ReLU)
↓
Dense(10, Softmax)
```

## Implementation
- Creates simple CNN architecture
- Trains for 5 epochs
- Evaluates test accuracy
- Saves model and training history

## Expected Results
- Test Accuracy: ~60-65%
- Total Parameters: ~1.2M

## Output Files
- `training_history.png` - Training curves
- `results.txt` - Model performance metrics
- `simple_cnn_model.h5` - Trained model

## Usage
```bash
python main.py
```
