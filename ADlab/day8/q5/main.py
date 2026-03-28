"""
Q5: Train CNN with Validation Split
- validation_split=0.2
- Plot training vs validation accuracy
- Plot training vs validation loss
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

def create_cnn():
    """Build CNN model"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

def train_with_validation(model, x_train, y_train):
    """Train model with validation split"""
    print("=" * 60)
    print("CNN WITH VALIDATION SPLIT (20%)")
    print("=" * 60)
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("\nModel Summary:")
    model.summary()
    
    print(f"\nTraining with validation_split=0.2")
    print(f"Training samples: {int(len(x_train) * 0.8)}")
    print(f"Validation samples: {int(len(x_train) * 0.2)}")
    
    history = model.fit(x_train, y_train,
                       epochs=10,
                       batch_size=64,
                       validation_split=0.2,
                       verbose=1)
    
    return history

def evaluate_model(model, x_test, y_test):
    """Evaluate model on test set"""
    print("\n" + "=" * 60)
    print("EVALUATION")
    print("=" * 60)
    
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    print(f"\nTest Loss:     {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print("=" * 60)
    
    return test_loss, test_accuracy

def plot_training_vs_validation(history):
    """Plot training vs validation accuracy and loss"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    # Accuracy comparison
    axes[0].plot(epochs, history.history['accuracy'], marker='o', linewidth=2, 
                 color='#3498db', label='Training Accuracy')
    axes[0].plot(epochs, history.history['val_accuracy'], marker='s', linewidth=2, 
                 color='#2ecc71', label='Validation Accuracy')
    axes[0].set_title('Training vs Validation Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0, 1])
    
    # Loss comparison
    axes[1].plot(epochs, history.history['loss'], marker='o', linewidth=2, 
                 color='#e74c3c', label='Training Loss')
    axes[1].plot(epochs, history.history['val_loss'], marker='s', linewidth=2, 
                 color='#f39c12', label='Validation Loss')
    axes[1].set_title('Training vs Validation Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('CNN with Validation Split (20%)', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'train_vs_validation.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/train_vs_validation.png")
    plt.close()

def analyze_overfitting(history):
    """Analyze overfitting from training history"""
    train_acc_final = history.history['accuracy'][-1]
    val_acc_final = history.history['val_accuracy'][-1]
    gap = train_acc_final - val_acc_final
    
    print("\n" + "=" * 60)
    print("OVERFITTING ANALYSIS")
    print("=" * 60)
    print(f"Final Training Accuracy:   {train_acc_final:.4f}")
    print(f"Final Validation Accuracy: {val_acc_final:.4f}")
    print(f"Gap (Train - Val):         {gap:.4f}")
    
    if gap > 0.1:
        print("\n⚠ Significant overfitting detected (gap > 0.1)")
    elif gap > 0.05:
        print("\n⚠ Moderate overfitting (gap > 0.05)")
    else:
        print("\n✓ Minimal overfitting (gap ≤ 0.05)")
    print("=" * 60)
    
    return gap

def save_results(history, test_loss, test_accuracy, gap, model):
    """Save results and analysis"""
    with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
        f.write("CNN with Validation Split Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Validation Split: 20%\n")
        f.write(f"Training Epochs: 10\n\n")
        f.write(f"Test Loss:                 {test_loss:.4f}\n")
        f.write(f"Test Accuracy:             {test_accuracy:.4f}\n\n")
        f.write(f"Final Training Accuracy:   {history.history['accuracy'][-1]:.4f}\n")
        f.write(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}\n")
        f.write(f"Overfitting Gap:           {gap:.4f}\n\n")
        f.write("Training History:\n")
        for i in range(len(history.history['accuracy'])):
            f.write(f"  Epoch {i+1:2d}: ")
            f.write(f"Train Acc={history.history['accuracy'][i]:.4f}, ")
            f.write(f"Val Acc={history.history['val_accuracy'][i]:.4f}, ")
            f.write(f"Train Loss={history.history['loss'][i]:.4f}, ")
            f.write(f"Val Loss={history.history['val_loss'][i]:.4f}\n")
    
    print(f"✓ Saved: {output_dir}/results.txt")
    
    # Save history
    np.savez(os.path.join(output_dir, 'validation_history.npz'),
             train_acc=history.history['accuracy'],
             val_acc=history.history['val_accuracy'],
             train_loss=history.history['loss'],
             val_loss=history.history['val_loss'])
    print(f"✓ Saved: {output_dir}/validation_history.npz")
    
    # Save model
    model.save(os.path.join(output_dir, 'validation_model.h5'))
    print(f"✓ Saved: {output_dir}/validation_model.h5")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    # Create model
    model = create_cnn()
    
    # Train with validation split
    history = train_with_validation(model, x_train, y_train)
    
    # Evaluate model
    test_loss, test_accuracy = evaluate_model(model, x_test, y_test)
    
    # Plot training vs validation
    plot_training_vs_validation(history)
    
    # Analyze overfitting
    gap = analyze_overfitting(history)
    
    # Save results
    save_results(history, test_loss, test_accuracy, gap, model)
    
    print("\n" + "=" * 60)
    print("Q5 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
