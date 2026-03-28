"""
Q9: Use Early Stopping
- EarlyStopping (patience=3)
- Train for 25 epochs
- Print stopped epoch
- Compare final accuracy
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.callbacks import EarlyStopping
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
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(10, activation='softmax')
    ])
    return model

def train_with_early_stopping(model, x_train, y_train):
    """Train model with early stopping"""
    print("=" * 60)
    print("CNN WITH EARLY STOPPING")
    print("=" * 60)
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("\nModel Summary:")
    model.summary()
    
    # Define Early Stopping callback
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
    
    print("\n" + "=" * 60)
    print("Early Stopping Configuration:")
    print("  Monitor: val_loss")
    print("  Patience: 3 epochs")
    print("  Restore Best Weights: Yes")
    print("  Max Epochs: 25")
    print("=" * 60)
    
    print("\nTraining with Early Stopping...")
    history = model.fit(x_train, y_train,
                       epochs=25,
                       batch_size=64,
                       validation_split=0.2,
                       callbacks=[early_stopping],
                       verbose=1)
    
    return history

def analyze_early_stopping(history):
    """Analyze early stopping behavior"""
    stopped_epoch = len(history.history['loss'])
    best_epoch = stopped_epoch - 3  # patience = 3
    
    print("\n" + "=" * 60)
    print("EARLY STOPPING ANALYSIS")
    print("=" * 60)
    print(f"\nTotal epochs trained:  {stopped_epoch}")
    print(f"Best epoch (restored): {max(1, best_epoch)}")
    print(f"Epochs saved:          {25 - stopped_epoch}")
    
    if stopped_epoch < 25:
        print(f"\n✓ Early stopping triggered at epoch {stopped_epoch}")
        print(f"  Saved {25 - stopped_epoch} epochs of unnecessary training!")
    else:
        print("\n⚠ Training completed all 25 epochs (no early stop)")
    
    # Show validation loss trend
    print(f"\nValidation Loss Trend (last 5 epochs):")
    start_idx = max(0, len(history.history['val_loss']) - 5)
    for i, val_loss in enumerate(history.history['val_loss'][start_idx:], start=start_idx+1):
        marker = " ← BEST" if i == best_epoch else ""
        print(f"  Epoch {i}: {val_loss:.4f}{marker}")
    
    print("=" * 60)
    
    return stopped_epoch, best_epoch

def evaluate_and_compare(model, x_test, y_test, history):
    """Evaluate model and compare with Q8"""
    print("\n" + "=" * 60)
    print("EVALUATION & COMPARISON")
    print("=" * 60)
    
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    print(f"\nWith Early Stopping:")
    print(f"  Test Loss:     {test_loss:.4f}")
    print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"  Final Val Acc: {history.history['val_accuracy'][-1]:.4f}")
    
    # Try to load Q8 model for comparison
    q8_model_path = "../q8/output/large_filter_model.h5"
    if os.path.exists(q8_model_path):
        try:
            q8_model = keras.models.load_model(q8_model_path)
            q8_loss, q8_accuracy = q8_model.evaluate(x_test, y_test, verbose=0)
            
            print(f"\nWithout Early Stopping (Q8 - 10 epochs):")
            print(f"  Test Accuracy: {q8_accuracy:.4f}")
            
            print(f"\nComparison:")
            print(f"  Accuracy Change: {test_accuracy - q8_accuracy:+.4f}")
            
            return test_loss, test_accuracy, q8_accuracy
        except:
            pass
    
    print("\n(Q8 model not available for comparison)")
    print("=" * 60)
    
    return test_loss, test_accuracy, None

def plot_early_stopping_analysis(history, stopped_epoch, best_epoch):
    """Plot training curves with early stopping markers"""
    fig = plt.figure(figsize=(16, 5))
    
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    # Training vs Validation Accuracy
    ax1 = plt.subplot(1, 3, 1)
    ax1.plot(epochs, history.history['accuracy'], marker='o', linewidth=2, 
             color='#3498db', label='Training Accuracy')
    ax1.plot(epochs, history.history['val_accuracy'], marker='s', linewidth=2, 
             color='#2ecc71', label='Validation Accuracy')
    ax1.axvline(x=best_epoch, color='red', linestyle='--', linewidth=2, 
                label=f'Best Epoch ({best_epoch})', alpha=0.7)
    ax1.axvline(x=stopped_epoch, color='orange', linestyle=':', linewidth=2, 
                label=f'Stopped ({stopped_epoch})', alpha=0.7)
    ax1.set_title('Training vs Validation Accuracy\n(With Early Stopping)', fontsize=12, fontweight='bold')
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
    ax2.axvline(x=best_epoch, color='red', linestyle='--', linewidth=2, 
                label=f'Best Epoch ({best_epoch})', alpha=0.7)
    ax2.axvline(x=stopped_epoch, color='orange', linestyle=':', linewidth=2, 
                label=f'Stopped ({stopped_epoch})', alpha=0.7)
    ax2.set_title('Training vs Validation Loss\n(With Early Stopping)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=10)
    ax2.set_ylabel('Loss', fontsize=10)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Validation loss detail
    ax3 = plt.subplot(1, 3, 3)
    ax3.plot(epochs, history.history['val_loss'], marker='o', linewidth=3, 
             color='#9b59b6', label='Validation Loss')
    ax3.scatter([best_epoch], [history.history['val_loss'][best_epoch-1]], 
                color='red', s=200, zorder=5, label=f'Best ({history.history["val_loss"][best_epoch-1]:.4f})')
    ax3.set_title('Validation Loss Tracking\n(Early Stopping Monitor)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Epoch', fontsize=10)
    ax3.set_ylabel('Validation Loss', fontsize=10)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.suptitle(f'Early Stopping Analysis (Patience=3, Stopped at Epoch {stopped_epoch})', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'early_stopping_analysis.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/early_stopping_analysis.png")
    plt.close()

def save_results(history, test_loss, test_accuracy, stopped_epoch, best_epoch, q8_accuracy, model):
    """Save results"""
    with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
        f.write("CNN with Early Stopping Results\n")
        f.write("=" * 50 + "\n\n")
        f.write("Early Stopping Configuration:\n")
        f.write("  Monitor:             val_loss\n")
        f.write("  Patience:            3 epochs\n")
        f.write("  Max Epochs:          25\n")
        f.write("  Restore Best Weights: Yes\n\n")
        f.write(f"Training stopped at epoch: {stopped_epoch}\n")
        f.write(f"Best epoch (restored):     {best_epoch}\n")
        f.write(f"Epochs saved:              {25 - stopped_epoch}\n\n")
        f.write(f"Test Loss:                 {test_loss:.4f}\n")
        f.write(f"Test Accuracy:             {test_accuracy:.4f}\n\n")
        
        if q8_accuracy is not None:
            f.write("Comparison with Q8 (10 epochs, no early stopping):\n")
            f.write(f"  Q8 Test Accuracy:  {q8_accuracy:.4f}\n")
            f.write(f"  Q9 Test Accuracy:  {test_accuracy:.4f}\n")
            f.write(f"  Change:            {test_accuracy - q8_accuracy:+.4f}\n\n")
        
        f.write("Benefits of Early Stopping:\n")
        f.write("  - Prevents overfitting by stopping at optimal point\n")
        f.write("  - Saves computational resources\n")
        f.write("  - Automatically finds best epoch\n")
        f.write("  - Restores weights from best epoch\n")
        f.write(f"  - Saved {(25 - stopped_epoch) * 100 / 25:.1f}% of training time!\n")
    
    print(f"✓ Saved: {output_dir}/results.txt")
    
    # Save model
    model.save(os.path.join(output_dir, 'early_stopping_model.h5'))
    print(f"✓ Saved: {output_dir}/early_stopping_model.h5")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    # Create model
    model = create_cnn()
    
    # Train with early stopping
    history = train_with_early_stopping(model, x_train, y_train)
    
    # Analyze early stopping
    stopped_epoch, best_epoch = analyze_early_stopping(history)
    
    # Evaluate and compare
    test_loss, test_accuracy, q8_accuracy = evaluate_and_compare(model, x_test, y_test, history)
    
    # Plot analysis
    plot_early_stopping_analysis(history, stopped_epoch, best_epoch)
    
    # Save results
    save_results(history, test_loss, test_accuracy, stopped_epoch, best_epoch, q8_accuracy, model)
    
    print("\n" + "=" * 60)
    print("Q9 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
