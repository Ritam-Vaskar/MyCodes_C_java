"""
Q6: Add Dropout Regularization
- Add Dropout(0.3) after Dense layer
- Compare validation accuracy with Q5
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def load_data():
    """Load normalized data"""
    data_path = "../q1/output/cifar10_normalized.npz"
    if not os.path.exists(data_path):
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

def create_cnn_with_dropout():
    """Build CNN model with Dropout"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),  # Dropout layer added
        layers.Dense(10, activation='softmax')
    ])
    return model

def train_with_dropout(model, x_train, y_train):
    """Train model with dropout"""
    print("=" * 60)
    print("CNN WITH DROPOUT(0.3) REGULARIZATION")
    print("=" * 60)
    print("\nArchitecture:")
    print("  Conv2D(32, 3×3, ReLU)")
    print("  MaxPooling2D(2×2)")
    print("  Conv2D(64, 3×3, ReLU)")
    print("  MaxPooling2D(2×2)")
    print("  Flatten")
    print("  Dense(128, ReLU)")
    print("  Dropout(0.3)  ← REGULARIZATION")
    print("  Dense(10, Softmax)")
    print("=" * 60)
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("\nModel Summary:")
    model.summary()
    
    print("\nTraining with Dropout...")
    history = model.fit(x_train, y_train,
                       epochs=10,
                       batch_size=64,
                       validation_split=0.2,
                       verbose=1)
    
    return history

def compare_with_previous():
    """Load Q5 results for comparison"""
    q5_path = "../q5/output/validation_history.npz"
    if os.path.exists(q5_path):
        q5_data = np.load(q5_path)
        q5_val_acc = q5_data['val_acc'][-1]
        return q5_val_acc
    return None

def evaluate_and_compare(model, x_test, y_test, history):
    """Evaluate model and compare with Q5"""
    print("\n" + "=" * 60)
    print("EVALUATION & COMPARISON")
    print("=" * 60)
    
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    val_acc_final = history.history['val_accuracy'][-1]
    train_acc_final = history.history['accuracy'][-1]
    gap = train_acc_final - val_acc_final
    
    print(f"\nWith Dropout(0.3):")
    print(f"  Training Accuracy:   {train_acc_final:.4f}")
    print(f"  Validation Accuracy: {val_acc_final:.4f}")
    print(f"  Test Accuracy:       {test_accuracy:.4f}")
    print(f"  Overfitting Gap:     {gap:.4f}")
    
    q5_val_acc = compare_with_previous()
    if q5_val_acc is not None:
        print(f"\nComparison with Q5 (without Dropout):")
        print(f"  Q5 Validation Accuracy:   {q5_val_acc:.4f}")
        print(f"  Q6 Validation Accuracy:   {val_acc_final:.4f}")
        print(f"  Improvement:              {val_acc_final - q5_val_acc:+.4f}")
        
        if gap < 0.05:
            print("\n✓ Dropout successfully reduced overfitting!")
        else:
            print("\n⚠ Some overfitting still present")
    
    print("=" * 60)
    
    return test_loss, test_accuracy, gap, q5_val_acc

def plot_comparison(history, q5_val_acc):
    """Plot training curves and comparison"""
    fig = plt.figure(figsize=(16, 5))
    
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    # Training vs Validation Accuracy
    ax1 = plt.subplot(1, 3, 1)
    ax1.plot(epochs, history.history['accuracy'], marker='o', linewidth=2, 
             color='#3498db', label='Training Accuracy')
    ax1.plot(epochs, history.history['val_accuracy'], marker='s', linewidth=2, 
             color='#2ecc71', label='Validation Accuracy')
    ax1.set_title('Training vs Validation Accuracy\n(With Dropout)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=10)
    ax1.set_ylabel('Accuracy', fontsize=10)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1])
    
    # Training vs Validation Loss
    ax2 = plt.subplot(1, 3, 2)
    ax2.plot(epochs, history.history['loss'], marker='o', linewidth=2, 
             color='#e74c3c', label='Training Loss')
    ax2.plot(epochs, history.history['val_loss'], marker='s', linewidth=2, 
             color='#f39c12', label='Validation Loss')
    ax2.set_title('Training vs Validation Loss\n(With Dropout)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=10)
    ax2.set_ylabel('Loss', fontsize=10)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Comparison bar chart
    ax3 = plt.subplot(1, 3, 3)
    if q5_val_acc is not None:
        methods = ['Without\nDropout\n(Q5)', 'With\nDropout(0.3)\n(Q6)']
        accuracies = [q5_val_acc, history.history['val_accuracy'][-1]]
        colors = ['#95a5a6', '#2ecc71']
        bars = ax3.bar(methods, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{acc:.4f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax3.set_ylabel('Validation Accuracy', fontsize=10)
        ax3.set_title('Dropout Impact Comparison', fontsize=12, fontweight='bold')
        ax3.set_ylim([0, 1])
        ax3.grid(axis='y', alpha=0.3)
    
    plt.suptitle('CNN with Dropout(0.3) Regularization', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dropout_analysis.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/dropout_analysis.png")
    plt.close()

def save_results(history, test_loss, test_accuracy, gap, q5_val_acc, model):
    """Save results"""
    with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
        f.write("CNN with Dropout Regularization Results\n")
        f.write("=" * 50 + "\n\n")
        f.write("Dropout Rate: 0.3 (after Dense layer)\n")
        f.write(f"Training Epochs: 10\n\n")
        f.write(f"Test Loss:                 {test_loss:.4f}\n")
        f.write(f"Test Accuracy:             {test_accuracy:.4f}\n")
        f.write(f"Final Training Accuracy:   {history.history['accuracy'][-1]:.4f}\n")
        f.write(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}\n")
        f.write(f"Overfitting Gap:           {gap:.4f}\n\n")
        
        if q5_val_acc is not None:
            f.write("Comparison with Q5 (without Dropout):\n")
            f.write(f"  Q5 Validation Accuracy: {q5_val_acc:.4f}\n")
            f.write(f"  Q6 Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}\n")
            f.write(f"  Change:                 {history.history['val_accuracy'][-1] - q5_val_acc:+.4f}\n\n")
        
        f.write("Benefits of Dropout:\n")
        f.write("  - Prevents overfitting by randomly dropping neurons\n")
        f.write("  - Forces network to learn redundant representations\n")
        f.write("  - Improves generalization to unseen data\n")
    
    print(f"✓ Saved: {output_dir}/results.txt")
    
    # Save model
    model.save(os.path.join(output_dir, 'dropout_model.h5'))
    print(f"✓ Saved: {output_dir}/dropout_model.h5")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    # Create model with dropout
    model = create_cnn_with_dropout()
    
    # Train model
    history = train_with_dropout(model, x_train, y_train)
    
    # Evaluate and compare
    test_loss, test_accuracy, gap, q5_val_acc = evaluate_and_compare(model, x_test, y_test, history)
    
    # Plot comparison
    plot_comparison(history, q5_val_acc)
    
    # Save results
    save_results(history, test_loss, test_accuracy, gap, q5_val_acc, model)
    
    print("\n" + "=" * 60)
    print("Q6 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
