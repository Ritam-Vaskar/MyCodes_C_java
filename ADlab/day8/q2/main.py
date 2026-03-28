"""
Q2: One-Hot Encoding vs Sparse Categorical
- Convert labels to one-hot encoding
- Train model using categorical_crossentropy
- Compare accuracy with sparse categorical version
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def load_data():
    """Load normalized data from Q1"""
    # Try to load from Q1's output first
    data_path = "../q1/output/cifar10_normalized.npz"
    if not os.path.exists(data_path):
        # Fallback: load and normalize
        from tensorflow.keras.datasets import cifar10
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
    else:
        data = np.load(data_path)
        x_train = data['x_train']
        y_train = data['y_train']
        x_test = data['x_test']
        y_test = data['y_test']
    
    return x_train, y_train, x_test, y_test

def create_model():
    """Create a simple CNN model"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

def train_with_onehot(x_train, y_train, x_test, y_test):
    """Train model with one-hot encoding and categorical_crossentropy"""
    print("=" * 60)
    print("MODEL 1: ONE-HOT ENCODING + CATEGORICAL_CROSSENTROPY")
    print("=" * 60)
    
    # Convert labels to one-hot encoding
    y_train_onehot = to_categorical(y_train, 10)
    y_test_onehot = to_categorical(y_test, 10)
    
    print(f"\nOriginal label shape: {y_train.shape}")
    print(f"One-hot label shape: {y_train_onehot.shape}")
    print(f"Example - Original: {y_train[0]} → One-hot: {y_train_onehot[0]}")
    
    # Create and compile model
    model1 = create_model()
    model1.compile(optimizer='adam',
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])
    
    print("\nTraining...")
    history1 = model1.fit(x_train, y_train_onehot,
                          epochs=5,
                          batch_size=64,
                          validation_split=0.1,
                          verbose=1)
    
    # Evaluate
    test_loss1, test_acc1 = model1.evaluate(x_test, y_test_onehot, verbose=0)
    print(f"\nTest Accuracy: {test_acc1:.4f}")
    
    return history1, test_acc1

def train_with_sparse(x_train, y_train, x_test, y_test):
    """Train model with sparse categorical crossentropy"""
    print("\n" + "=" * 60)
    print("MODEL 2: SPARSE CATEGORICAL_CROSSENTROPY")
    print("=" * 60)
    
    # Create and compile model
    model2 = create_model()
    model2.compile(optimizer='adam',
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    
    print("\nTraining...")
    history2 = model2.fit(x_train, y_train,
                          epochs=5,
                          batch_size=64,
                          validation_split=0.1,
                          verbose=1)
    
    # Evaluate
    test_loss2, test_acc2 = model2.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest Accuracy: {test_acc2:.4f}")
    
    return history2, test_acc2

def compare_results(acc1, acc2):
    """Compare and visualize results"""
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    print(f"One-Hot Encoding (Categorical):       {acc1:.4f}")
    print(f"Sparse Categorical:                   {acc2:.4f}")
    print(f"Difference:                           {abs(acc1 - acc2):.4f}")
    print("=" * 60)
    print("\n✓ Both approaches yield nearly identical results!")
    print("  - One-hot: More memory, explicit encoding")
    print("  - Sparse: Memory efficient, integer labels")
    
    # Visualization
    methods = ['One-Hot\n(Categorical)', 'Sparse\nCategorical']
    accuracies = [acc1, acc2]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(methods, accuracies, color=['#3498db', '#2ecc71'], alpha=0.8, edgecolor='black', linewidth=2)
    plt.ylabel('Test Accuracy', fontsize=12, fontweight='bold')
    plt.title('One-Hot vs Sparse Categorical Encoding Comparison', fontsize=14, fontweight='bold')
    plt.ylim([0, 1])
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.4f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'encoding_comparison.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/encoding_comparison.png")
    plt.close()

def save_results(acc1, acc2):
    """Save comparison results"""
    with open(os.path.join(output_dir, 'comparison_results.txt'), 'w') as f:
        f.write("One-Hot vs Sparse Categorical Comparison\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"One-Hot Encoding (Categorical):  {acc1:.4f}\n")
        f.write(f"Sparse Categorical:              {acc2:.4f}\n")
        f.write(f"Difference:                      {abs(acc1 - acc2):.4f}\n\n")
        f.write("Conclusion:\n")
        f.write("Both methods produce nearly identical results.\n")
        f.write("Sparse categorical is preferred for memory efficiency.\n")
    print(f"✓ Saved: {output_dir}/comparison_results.txt")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    # Train with one-hot encoding
    history1, acc1 = train_with_onehot(x_train, y_train, x_test, y_test)
    
    # Train with sparse categorical
    history2, acc2 = train_with_sparse(x_train, y_train, x_test, y_test)
    
    # Compare results
    compare_results(acc1, acc2)
    
    # Save results
    save_results(acc1, acc2)
    
    print("\n" + "=" * 60)
    print("Q2 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
