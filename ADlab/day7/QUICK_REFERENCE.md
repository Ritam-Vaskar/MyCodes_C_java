# AD Lab Day 7 - Quick Reference Guide

## Quick Start

```bash
# Navigate to day7 folder
cd "c:\C programing\ADlab\day7"

# Install dependencies
pip install -r requirements.txt

# Run all questions
python run_all.py

# Or run individual questions
python q1.py
python q2.py
python q3.py
python q4.py
python q5.py
```

## Questions at a Glance

| Question | Topic | Runtime | Key Output |
|----------|-------|---------|------------|
| Q1 | Basic MNIST + Neural Network | ~2 min | Model with ~97% accuracy |
| Q2 | PSO Weight Optimization | ~10 min | PSO vs Adam comparison |
| Q3 | Performance Analysis | ~15 min | Confusion matrix, optimizer comparison |
| Q4 | PSO Hyperparameter Tuning | ~20 min | Optimized hyperparameters |
| Q5 | PSO Architecture Search | ~20 min | Best architecture found |

## What Each Question Does

### Q1: Foundation
- Loads MNIST dataset
- Builds basic neural network (784→128→10)
- Trains with Adam optimizer
- **Output:** Basic model achieving ~97% accuracy

### Q2: PSO vs Backpropagation
- Implements PSO from scratch
- Optimizes neural network weights without gradient descent
- Compares with traditional Adam optimizer
- **Key Insight:** Shows PSO can optimize NNs (though less efficiently than Adam)

### Q3: Model Engineering
- Analyzes overfitting/underfitting
- Tests improvements: Dropout, more neurons, extra layers
- Generates confusion matrix
- Compares Adam vs SGD
- **Output:** Best performing model configuration

### Q4: Automated Hyperparameter Tuning
- Uses PSO to find best:
  - Number of neurons (50-300)
  - Learning rate (0.0001-0.01)
  - Batch size (32-256)
  - Dropout rate (0-0.5)
- **Output:** Optimized hyperparameters beating defaults

### Q5: Automated Architecture Design
- PSO searches for best architecture:
  - Number of layers (1-3)
  - Neurons per layer (32-256)
  - Activation function (ReLU/Tanh)
  - Dropout rate
- **Output:** Automatically designed neural network

## Expected Accuracies

```
Q1 Basic Model:              97-98%
Q2 PSO-optimized weights:    85-90%
Q2 Adam baseline:            95-97%
Q3 Improved models:          97-98%
Q4 PSO hyperparameters:      97.8-98.2%
Q5 PSO architecture:         98-98.5%
```

## Output Files

All outputs are saved to `output/q{n}/` folders:

```
output/
├── q1/
│   ├── sample_image.png              # Sample MNIST digit
│   ├── training_history.png          # Training curves
│   ├── sample_predictions.png        # Model predictions
│   └── mnist_model.h5                # Saved model
├── q2/
│   ├── pso_vs_adam_comparison.png    # Comprehensive comparison
│   └── results_summary.txt           # Text results
├── q3/
│   ├── training_10_epochs.png        # 10 epoch training
│   ├── training_vs_validation.png    # Overfitting analysis
│   ├── confusion_matrix.png          # Confusion matrix heatmap
│   ├── optimizer_comparison.png      # Adam vs SGD
│   ├── improvements_comparison.png   # All improvements
│   └── analysis_summary.txt          # Text analysis
├── q4/
│   ├── pso_hyperparameter_optimization.png
│   └── optimization_results.txt
└── q5/
    ├── architecture_search_results.png
    └── architecture_search_results.txt
```

## PSO Parameters Used

### Q2: Weight Optimization
- Particles: 20
- Iterations: 30
- Parameters to optimize: ~25,000 (network weights)
- Bounds: [-1, 1]

### Q4: Hyperparameter Optimization
- Particles: 10
- Iterations: 20
- Parameters to optimize: 4 (neurons, lr, batch, dropout)
- Bounds: Variable per parameter

### Q5: Architecture Search
- Particles: 15
- Iterations: 20
- Parameters to optimize: 6 (layers, neurons×3, activation, dropout)
- Bounds: Variable per parameter

## Common Issues & Solutions

### Issue: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Issue: Slow execution
- Normal! PSO requires training many models
- Q4 and Q5 take 15-25 minutes each
- Use smaller datasets in code if needed (already optimized)

### Issue: Out of memory
- Reduce batch size in the code
- Close other applications
- Use CPU instead of GPU (automatic fallback)

### Issue: MNIST download fails
```python
# In code, data will auto-download on first run
# If it fails, check internet connection
```

## Key Code Snippets

### Load MNIST
```python
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

### Build Basic Model
```python
model = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

### PSO Update Rules
```python
velocity = w * velocity + c1 * r1 * (pbest - position) + c2 * r2 * (gbest - position)
position = position + velocity
```

## Understanding the Results

### Overfitting Indicators (Q3)
- Training accuracy >> Validation accuracy
- Training loss << Validation loss
- **Solution:** Add dropout, reduce complexity

### Underfitting Indicators (Q3)
- Both accuracies are low (<90%)
- Loss doesn't decrease much
- **Solution:** Increase model complexity, train longer

### PSO Convergence (Q2, Q4, Q5)
- Good: Smooth decrease/increase in fitness
- Bad: Oscillating or flat fitness
- **Check:** Iteration plots in output folder

## Troubleshooting

### All questions running slowly?
- Expected behavior for PSO questions (Q2, Q4, Q5)
- Consider running overnight for complete results
- Or reduce iterations in code:
  ```python
  # In q2.py, q4.py, q5.py, change:
  max_iter = 20  # from 30 or 20
  ```

### Want faster results?
Edit the code to use fewer training samples:
```python
# In q2.py, q4.py, q5.py:
train_size = 1000  # instead of 5000
```

### Need more accuracy?
Increase PSO iterations:
```python
max_iter = 50  # instead of 20-30
```

## File Organization Tips

- All Python scripts are in `day7/` folder
- All outputs automatically go to `output/q{n}/` folders
- `run_all.py` creates `output/execution_summary.txt`
- Check `IMPLEMENTATION_SUMMARY.md` for detailed documentation

## Testing Individual Components

```bash
# Test just the data loading
python -c "from tensorflow import keras; keras.datasets.mnist.load_data(); print('✓ MNIST loaded')"

# Test TensorFlow installation
python -c "import tensorflow as tf; print(f'✓ TensorFlow {tf.__version__}')"

# Test all imports
python -c "import tensorflow, numpy, matplotlib, sklearn, seaborn; print('✓ All imports work')"
```

## Next Steps After Completion

1. Review all output plots in `output/` folders
2. Read the summary files (`.txt` files)
3. Compare accuracies across different approaches
4. Experiment with different PSO parameters
5. Try other datasets (Fashion-MNIST, CIFAR-10)

## Time Budget

For a complete run of all questions:
- Minimum: 45 minutes
- Average: 60 minutes
- Maximum: 90 minutes (if system is slow)

Plan accordingly!

---

**Happy Learning! 🚀**
