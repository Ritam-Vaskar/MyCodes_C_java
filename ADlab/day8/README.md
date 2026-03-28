# Day 8: CNN with CIFAR-10 - Data Handling, Validation & Regularization

## Overview
Comprehensive CNN development using CIFAR-10 dataset, covering data handling, model architecture, validation strategies, and regularization techniques.

## Structure
```
day8/
├── q1/   - Data Loading & Visualization
├── q2/   - One-Hot vs Sparse Categorical
├── q3/   - Simple CNN Model
├── q4/   - Enhanced CNN with Plots
├── q5/   - Validation Split Analysis
├── q6/   - Dropout Regularization
├── q7/   - Batch Normalization
├── q8/   - Filter Size Optimization
├── q9/   - Early Stopping
├── q10/  - Confusion Matrix & Error Analysis
├── run_all.py - Execute all questions
├── requirements.txt
└── README.md
```

## Questions

### Part 1: Data Handling & Basic CNN (Q1-Q4)

**Q1: Data Loading & Visualization**
- Import TensorFlow, NumPy, Matplotlib
- Load CIFAR-10 using `cifar10.load_data()`
- Print dataset shapes
- Display 10 random images with class names
- Normalize pixel values to [0, 1]

**Q2: One-Hot vs Sparse Categorical**
- Convert labels to one-hot encoding
- Train with categorical_crossentropy
- Compare with sparse_categorical_crossentropy
- Analyze accuracy differences

**Q3: Simple CNN Model**
- Architecture: Conv2D(32, 3×3, ReLU) → MaxPool → Flatten → Dense(128) → Dense(10)
- Train for 5 epochs
- Print test accuracy

**Q4: Enhanced CNN**
- Add second Conv2D(64) layer
- Train for 10 epochs
- Store history
- Plot training accuracy and loss

### Part 2: Validation & Regularization (Q5-Q10)

**Q5: Validation Split**
- Train with validation_split=0.2
- Plot training vs validation accuracy
- Plot training vs validation loss
- Identify overfitting

**Q6: Dropout Regularization**
- Add Dropout(0.3) after Dense layer
- Compare validation accuracy with Q5
- Analyze overfitting reduction

**Q7: Batch Normalization**
- Add BatchNormalization after Conv layers
- Retrain and compare convergence speed
- Analyze training stability

**Q8: Filter Size Increase**
- Progressive filters: 32 → 64 → 128
- Compare test accuracy
- Print parameter increase
- Analyze performance vs complexity

**Q9: Early Stopping**
- Implement EarlyStopping (patience=3)
- Train for up to 25 epochs
- Print stopped epoch
- Compare final accuracy

**Q10: Model Evaluation**
- Generate confusion matrix heatmap
- Classification report (precision/recall/F1)
- Display 15 misclassified images
- Per-class performance analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run All Questions
```bash
python run_all.py
```

### Run Individual Question
```bash
cd q1
python main.py
```

## Requirements
- Python 3.8+
- TensorFlow 2.10+
- NumPy 1.23+
- Matplotlib 3.5+
- Seaborn 0.12+
- scikit-learn 1.1+

## Expected Runtime
- **CPU**: 30-60 minutes (all questions)
- **GPU**: 10-15 minutes (all questions)
- First run downloads CIFAR-10 dataset (~170MB)

## Output Structure
Each question generates:
- `output/` folder with results
- Visualization plots (PNG)
- Performance metrics (TXT)
- Trained models (H5)

## Key Learnings

### Data Handling
- Normalization improves convergence
- CIFAR-10: 50k train, 10k test, 32×32×3 images
- 10 classes: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck

### Label Encoding
- One-hot and sparse categorical yield identical results
- Sparse categorical is memory efficient
- Use sparse for large datasets

### CNN Architecture
- Deeper networks (more Conv layers) improve accuracy
- Progressive filter increase (32→64→128) captures hierarchical features
- Parameter count increases significantly with depth

### Validation Strategies
- 20% validation split sufficient for monitoring
- Gap between train/val indicates overfitting
- Validation loss plateaus signal stopping point

### Regularization Techniques
- **Dropout(0.3)**: Reduces overfitting by ~2-3%
- **BatchNormalization**: Accelerates convergence, stable training
- **Early Stopping**: Prevents unnecessary training, saves time

### Performance Expectations
- Simple CNN (Q3): ~60-65% accuracy
- Enhanced CNN (Q4): ~65-70% accuracy
- With regularization (Q6-Q7): ~70-73% accuracy
- Optimized model (Q8-Q9): ~72-75% accuracy

## Common Misclassifications
- Cat ↔ Dog (similar features)
- Automobile ↔ Truck (vehicle similarity)
- Bird ↔ Airplane (sky background)
- Deer ↔ Horse (four-legged animals)

## Best Practices Demonstrated
1. **Data Preprocessing**: Normalize to [0, 1]
2. **Architecture Design**: Progressive filter increases
3. **Training Strategy**: Validation split + early stopping
4. **Regularization**: Dropout + BatchNorm
5. **Evaluation**: Confusion matrix + error analysis

## Files Generated
Each question saves:
- Training curves (accuracy/loss plots)
- Model performance metrics
- Trained models (for subsequent questions)
- Comparison visualizations

## Tips
- Set random seeds for reproducibility
- Use GPU for 3-5x speedup
- Monitor validation loss, not training loss
- Early stopping typically stops at epoch 10-15
- Batch normalization allows higher learning rates

## Troubleshooting

**Out of Memory**
- Reduce batch size: `batch_size=32`
- Use CPU if GPU memory insufficient

**Slow Training**
- Check GPU availability: `tf.config.list_physical_devices('GPU')`
- Use smaller subset for testing

**Model Not Loading (Q10)**
- Run Q7, Q8, or Q9 first to train a model
- Q10 uses the best available model

## References
- CIFAR-10 Dataset: https://www.cs.toronto.edu/~kriz/cifar.html
- TensorFlow Documentation: https://www.tensorflow.org/
- Keras CNN Guide: https://keras.io/guides/

## Author Notes
This lab provides hands-on experience with:
- Complete CNN development workflow
- Systematic architecture improvements
- Validation and regularization techniques
- Model evaluation and error analysis
- Production-ready code structure

Perfect for understanding deep learning best practices and CNN optimization strategies.

---

**Status**: Ready to run
**Estimated Total Time**: 30-60 minutes (CPU) | 10-15 minutes (GPU)
**Difficulty**: Intermediate
