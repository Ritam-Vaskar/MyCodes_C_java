# AD Lab Day 7 - Implementation Summary

## Overview
Complete implementation of Neural Networks with TensorFlow/Keras and Particle Swarm Optimization (PSO) for various optimization tasks on the MNIST dataset.

## Questions Implemented

### Question 1: Basic MNIST Data Handling and Model Construction ✓
**File:** `q1.py`

**Tasks Completed:**
- ✓ Import TensorFlow, NumPy, Matplotlib
- ✓ Load MNIST dataset using `mnist.load_data()`
- ✓ Print shapes of training/test images and labels
- ✓ Display one training image with label
- ✓ Normalize pixel values to [0, 1]
- ✓ Flatten 28×28 images to 784-dimensional vectors
- ✓ Build Sequential neural network (Input: 784 → Dense: 128 ReLU → Output: 10 Softmax)
- ✓ Print model summary with parameter explanation
- ✓ Compile with Adam optimizer, sparse categorical crossentropy
- ✓ Train for 5 epochs
- ✓ Evaluate on test data

**Outputs:**
- Sample image visualization
- Training history plots
- Sample predictions
- Saved model (.h5 file)

---

### Question 2: PSO for Neural Network Weight Optimization ✓
**File:** `q2.py`

**Tasks Completed:**
- ✓ Implement complete PSO algorithm from scratch
- ✓ Build simple neural network (784 → 32 → 10)
- ✓ Encode all weights and biases into particle position vector
- ✓ Define fitness function as classification error
- ✓ Initialize swarm with 20 particles
- ✓ Update velocity and position for 30 iterations
- ✓ Train Adam baseline for comparison
- ✓ Compare PSO vs Adam accuracy
- ✓ Analyze convergence speed, computational complexity

**Key Features:**
- Custom forward pass implementation
- Softmax and ReLU from scratch
- Fitness function combining error rate and cross-entropy
- PSO with configurable inertia weight, cognitive and social parameters

**Outputs:**
- PSO convergence plots
- Adam training plots  
- Accuracy comparison charts
- Detailed results summary

---

### Question 3: Performance Analysis and Model Improvements ✓
**File:** `q3.py`

**Tasks Completed:**

**Stage 3 - Performance:**
- ✓ Train model for 10 epochs with history storage
- ✓ Plot training accuracy vs epoch
- ✓ Plot training loss vs epoch
- ✓ Add validation_split=0.2
- ✓ Plot training vs validation accuracy
- ✓ Plot training vs validation loss
- ✓ Analyze overfitting/underfitting based on plots

**Model Improvements:**
- ✓ Add Dropout layer (rate=0.2) after hidden layer
- ✓ Increase hidden neurons from 128 → 256
- ✓ Add additional hidden layer (128 → 64 → 10)
- ✓ Train with 20 epochs using EarlyStopping callback

**Analysis:**
- ✓ Generate confusion matrix for test predictions
- ✓ Compare Adam vs SGD optimizers
- ✓ Print and compare test accuracies
- ✓ Classification report with precision/recall/f1-score

**Outputs:**
- Training/validation plots
- Overfitting analysis
- Confusion matrix heatmap
- Optimizer comparison plots
- Model improvement comparison chart

---

### Question 4: PSO for Hyperparameter Optimization ✓
**File:** `q4.py`

**Tasks Completed:**
- ✓ Define hyperparameter search space:
  - Number of hidden neurons (50-300)
  - Learning rate (0.0001-0.01)
  - Batch size (32-256)
  - Dropout rate (0-0.5)
- ✓ Implement particle representation as hyperparameter vector
- ✓ Fitness function = validation accuracy
- ✓ Run PSO for 20 iterations with 10 particles
- ✓ Train model with PSO-optimized hyperparameters
- ✓ Train model with default hyperparameters
- ✓ Compare accuracies and improvements

**Key Features:**
- Multi-dimensional hyperparameter optimization
- Automatic clipping to valid ranges
- Early stopping in fitness evaluation for efficiency
- Comprehensive comparison metrics

**Outputs:**
- PSO convergence plot
- Hyperparameter comparison
- Validation accuracy comparison
- Test accuracy comparison
- Optimization results summary

---

### Question 5: PSO-based Neural Architecture Search (NAS) ✓
**File:** `q5.py`

**Tasks Completed:**
- ✓ Design architecture encoding scheme:
  - Number of hidden layers (1-3)
  - Neurons per layer (32-256 for each layer)
  - Activation function (ReLU / Tanh)
  - Dropout rate (0-0.5)
- ✓ Implement architecture decoder
- ✓ Build dynamic model from architecture specification
- ✓ Define fitness = validation accuracy
- ✓ Run PSO for 20 iterations with 15 particles
- ✓ Train best architecture found by PSO
- ✓ Train manually designed baseline (2 layers, [128, 64], ReLU)
- ✓ Compare architectures and performance

**Key Features:**
- Automatic neural architecture search
- Support for variable number of layers
- Mixed activation function search
- Architecture evolution tracking

**Outputs:**
- Architecture search convergence
- Layer evolution plot
- Validation accuracy/loss comparison
- Test accuracy comparison
- Parameter count comparison
- Architecture evolution history

---

## Project Structure

```
day7/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── run_all.py                   # Master script to run all questions
├── q1.py                        # Basic MNIST and Model Construction
├── q2.py                        # PSO for Weight Optimization
├── q3.py                        # Performance Analysis and Improvements
├── q4.py                        # PSO for Hyperparameter Optimization
├── q5.py                        # PSO-based Neural Architecture Search
└── output/                      # All outputs organized by question
    ├── q1/
    │   ├── sample_image.png
    │   ├── training_history.png
    │   ├── sample_predictions.png
    │   └── mnist_model.h5
    ├── q2/
    │   ├── pso_vs_adam_comparison.png
    │   └── results_summary.txt
    ├── q3/
    │   ├── training_10_epochs.png
    │   ├── training_vs_validation.png
    │   ├── confusion_matrix.png
    │   ├── optimizer_comparison.png
    │   ├── improvements_comparison.png
    │   └── analysis_summary.txt
    ├── q4/
    │   ├── pso_hyperparameter_optimization.png
    │   └── optimization_results.txt
    ├── q5/
    │   ├── architecture_search_results.png
    │   └── architecture_search_results.txt
    └── execution_summary.txt
```

## Installation

```bash
cd "c:\C programing\ADlab\day7"
pip install -r requirements.txt
```

## Usage

### Run Individual Questions

```bash
python q1.py  # Basic MNIST and Model Construction
python q2.py  # PSO for Weight Optimization (takes ~5-10 minutes)
python q3.py  # Performance Analysis (takes ~10-15 minutes)
python q4.py  # PSO Hyperparameter Optimization (takes ~15-20 minutes)
python q5.py  # PSO Architecture Search (takes ~15-20 minutes)
```

### Run All Questions

```bash
python run_all.py
```

This will execute all questions sequentially and provide a comprehensive summary.

## Key Concepts Covered

### 1. Deep Learning Fundamentals
- MNIST dataset handling
- Data normalization and preprocessing
- Neural network architecture design
- Model compilation and training
- Evaluation metrics

### 2. Particle Swarm Optimization (PSO)
- Bio-inspired optimization algorithm
- Swarm intelligence concepts
- Particle position and velocity updates
- Global and personal best tracking
- Convergence analysis

### 3. Neural Network Weight Optimization
- Alternative to gradient descent
- Direct weight optimization using PSO
- Fitness function design
- Comparison with backpropagation

### 4. Hyperparameter Tuning
- Learning rate optimization
- Batch size selection
- Dropout rate tuning
- Network size optimization

### 5. Neural Architecture Search (NAS)
- Automated model design
- Architecture encoding schemes
- Multi-objective optimization
- Performance vs complexity tradeoffs

### 6. Model Evaluation and Improvement
- Training/validation curves
- Overfitting/underfitting detection
- Confusion matrix analysis
- Optimizer comparison (Adam vs SGD)
- Regularization techniques (Dropout)
- Early stopping

## Expected Results

### Q1: Basic Model
- Test Accuracy: ~97-98%
- Training Time: ~1 minute

### Q2: PSO vs Adam
- PSO Test Accuracy: ~85-90%
- Adam Test Accuracy: ~95-97%
- **Key Insight:** Adam is more efficient for neural networks, but PSO demonstrates the concept

### Q3: Model Improvements
- Baseline: ~97%
- With Dropout: ~97.5%
- With 256 Neurons: ~97.8%
- With 2 Hidden Layers: ~98%
- With Early Stopping: ~98%

### Q4: Hyperparameter Optimization
- Default Accuracy: ~97.5%
- PSO-Optimized Accuracy: ~97.8-98.2%
- Improvement: +0.3-0.7%

### Q5: Architecture Search
- Manual Baseline: ~97.8%
- PSO-Optimized: ~98-98.5%
- **Best Architecture:** Usually finds 2-3 layers with varying neuron counts

## Performance Notes

- Q1: Fast (~1-2 minutes)
- Q2: Moderate (~5-10 minutes due to 30 PSO iterations)
- Q3: Moderate (~10-15 minutes, multiple models trained)
- Q4: Slow (~15-25 minutes, hyperparameter search)
- Q5: Slow (~15-25 minutes, architecture search)

**Total Runtime:** Approximately 45-75 minutes for all questions

## Technical Highlights

### PSO Implementation Features
- Configurable swarm size and iterations
- Bounded search spaces
- Adaptive inertia weight
- Real-time convergence monitoring
- History tracking for analysis

### Neural Network Features
- Sequential API for easy model building
- Flexible architecture construction
- Multiple optimizers support (Adam, SGD)
- Dropout regularization
- Early stopping callbacks
- Comprehensive model evaluation

### Visualization Features
- Training history plots
- Convergence curves
- Confusion matrices
- Comparison charts
- Architecture evolution plots

## Dependencies

- tensorflow>=2.13.0
- numpy>=1.24.3
- matplotlib>=3.7.1
- scikit-learn>=1.3.0
- seaborn>=0.12.2
- pandas>=2.0.3

## Authors
AD Lab - Day 7 Assignment

## Conclusion

This assignment provides a comprehensive exploration of:
1. Deep learning with TensorFlow/Keras
2. Particle Swarm Optimization algorithms
3. Hyperparameter and architecture optimization
4. Model evaluation and improvement techniques

All implementations are complete, functional, and ready to execute!
