# AD Lab Day 7: Neural Networks and Particle Swarm Optimization

## Overview
This assignment covers deep learning with TensorFlow/Keras and Particle Swarm Optimization (PSO) for neural network optimization tasks.

## Questions

### Q1: Basic MNIST Data Handling and Model Construction
- Load and explore MNIST dataset
- Normalize and flatten data
- Build and train a Sequential neural network
- Evaluate model performance

**Run:** `python q1.py`

### Q2: PSO for Neural Network Weight Optimization
- Implement Particle Swarm Optimization algorithm
- Use PSO to optimize neural network weights (instead of backpropagation)
- Compare PSO-trained vs Adam-trained models
- Analyze convergence, accuracy, and computational complexity

**Run:** `python q2.py`

### Q3: Performance Analysis and Model Improvements
- Training/validation plots (accuracy and loss)
- Overfitting/underfitting analysis
- Model improvements: Dropout, more neurons, additional layers
- Confusion matrix generation
- Optimizer comparison (Adam vs SGD)
- Early stopping implementation

**Run:** `python q3.py`

### Q4: PSO for Hyperparameter Optimization
- Use PSO to optimize:
  - Number of hidden neurons (50-300)
  - Learning rate (0.0001-0.01)
  - Batch size (32-256)
  - Dropout rate (0-0.5)
- Compare default vs PSO-optimized hyperparameters

**Run:** `python q4.py`

### Q5: PSO-based Neural Architecture Search (NAS)
- Automated architecture search using PSO
- Optimize:
  - Number of hidden layers (1-3)
  - Neurons per layer (32-256)
  - Activation functions (ReLU/Tanh)
  - Dropout rates
- Compare best architecture vs manually designed model

**Run:** `python q5.py`

## Installation

### Option 1: Automated Setup (Recommended for Windows)

```bash
python setup.py
```

Or double-click `install.bat` on Windows.

### Option 2: Manual Installation

```bash
python -m pip install tensorflow>=2.13.0
python -m pip install numpy>=1.24.3
python -m pip install matplotlib>=3.7.1
python -m pip install scikit-learn>=1.3.0
python -m pip install seaborn>=0.12.2
python -m pip install pandas>=2.0.3
```

### Option 3: Using requirements.txt

```bash
python -m pip install -r requirements.txt
```

**Note:** Use `python -m pip` instead of just `pip` if pip is not in your PATH.

## Run All Questions

```bash
python run_all.py
```

## Output Structure

```
output/
├── q1/          # Basic model outputs
├── q2/          # PSO weight optimization results
├── q3/          # Performance analysis plots
├── q4/          # Hyperparameter optimization results
└── q5/          # Architecture search results
```

## Key Concepts

1. **MNIST Dataset**: Handwritten digit classification (28×28 grayscale images)
2. **Neural Networks**: Feedforward networks with Dense layers
3. **Particle Swarm Optimization**: Bio-inspired optimization algorithm
4. **Hyperparameter Tuning**: Optimizing model configuration
5. **Neural Architecture Search**: Automated model design

## Authors
AD Lab - Day 7 Assignment
