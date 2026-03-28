# Q4: Modified CNN with Second Conv2D Layer

## Objective
Modify the CNN by adding a second Conv2D layer (64 filters), train for 10 epochs, store history, and plot training accuracy and loss.

## Architecture Enhancement
```
Conv2D(32, 3×3, ReLU)
↓
MaxPooling2D(2×2)
↓
Conv2D(64, 3×3, ReLU)  ← NEW LAYER
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
- Adds second convolutional layer with 64 filters
- Trains for 10 epochs
- Stores complete training history
- Plots accuracy and loss curves

## Expected Results
- Test Accuracy: ~65-70%
- Improved feature extraction with deeper network

## Output Files
- `training_history.png` - Training curves over 10 epochs
- `training_history.npz` - Raw history data
- `results.txt` - Performance metrics and training log
- `enhanced_cnn_model.h5` - Trained model

## Usage
```bash
python main.py
```
