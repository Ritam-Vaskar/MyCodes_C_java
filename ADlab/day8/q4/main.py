"""
Q4: Modified CNN with Second Conv2D Layer
- Add second Conv2D layer (64 filters)
- Train for 10 epochs
- Store history
- Plot training accuracy and loss
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

def create_enhanced_cnn():
    """Build enhanced CNN with second Conv2D layer"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),  # Second Conv2D layer
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

def train_model(model, x_train, y_train):
    """Train the model for 10 epochs"""
    print("=" * 60)
    print("ENHANCED CNN MODEL (WITH SECOND CONV2D LAYER)")
    print("=" * 60)
    print("\nArchitecture:")
    print("  Conv2D(32, 3×3, ReLU)")
    print("  MaxPooling2D(2×2)")
    print("  Conv2D(64, 3×3, ReLU)  ← NEW LAYER")
    print("  MaxPooling2D(2×2)")
    print("  Flatten")
    print("  Dense(128, ReLU)")
    print("  Dense(10, Softmax)")
    print("=" * 60)
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("\nModel Summary:")
    model.summary()
    
    print("\nTraining for 10 epochs...")
    history = model.fit(x_train, y_train,
                       epochs=10,
                       batch_size=64,
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

def plot_training_history(history):
    """Plot training accuracy and loss"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    # Training Accuracy
    axes[0].plot(epochs, history.history['accuracy'], marker='o', linewidth=2, 
                 color='#3498db', label='Training Accuracy')
    axes[0].set_title('Training Accuracy over Epochs', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].set_ylim([0, 1])
    
    # Training Loss
    axes[1].plot(epochs, history.history['loss'], marker='s', linewidth=2, 
                 color='#e74c3c', label='Training Loss')
    axes[1].set_title('Training Loss over Epochs', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    plt.suptitle('Enhanced CNN - Training History (10 Epochs)', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_history.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/training_history.png")
    plt.close()

def save_results(history, test_loss, test_accuracy, model):
    """Save training history and results"""
    # Save history data
    np.savez(os.path.join(output_dir, 'training_history.npz'),
             accuracy=history.history['accuracy'],
             loss=history.history['loss'])
    print(f"✓ Saved: {output_dir}/training_history.npz")
    
    # Save results
    with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
        f.write("Enhanced CNN Model Results\n")
        f.write("=" * 50 + "\n\n")
        f.write("Architecture:\n")
        f.write("  - Conv2D(32, 3×3, ReLU)\n")
        f.write("  - MaxPooling2D(2×2)\n")
        f.write("  - Conv2D(64, 3×3, ReLU)  ← NEW\n")
        f.write("  - MaxPooling2D(2×2)\n")
        f.write("  - Flatten\n")
        f.write("  - Dense(128, ReLU)\n")
        f.write("  - Dense(10, Softmax)\n\n")
        f.write(f"Training Epochs: 10\n")
        f.write(f"Test Loss:       {test_loss:.4f}\n")
        f.write(f"Test Accuracy:   {test_accuracy:.4f} ({test_accuracy*100:.2f}%)\n")
        f.write(f"Total Parameters: {model.count_params():,}\n\n")
        f.write("Training Progress:\n")
        for i, (acc, loss) in enumerate(zip(history.history['accuracy'], history.history['loss']), 1):
            f.write(f"  Epoch {i:2d}: Accuracy={acc:.4f}, Loss={loss:.4f}\n")
    
    print(f"✓ Saved: {output_dir}/results.txt")
    
    # Save model
    model.save(os.path.join(output_dir, 'enhanced_cnn_model.h5'))
    print(f"✓ Saved: {output_dir}/enhanced_cnn_model.h5")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    # Create model
    model = create_enhanced_cnn()
    
    # Train model
    history = train_model(model, x_train, y_train)
    
    # Evaluate model
    test_loss, test_accuracy = evaluate_model(model, x_test, y_test)
    
    # Plot training history
    plot_training_history(history)
    
    # Save results
    save_results(history, test_loss, test_accuracy, model)
    
    print("\n" + "=" * 60)
    print("Q4 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
