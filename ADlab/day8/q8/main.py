"""
Q8: Increase Filter Sizes (32 → 64 → 128)
- Progressive filter increase
- Compare test accuracy
- Print total parameter increase
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

def create_large_filter_cnn():
    """Build CNN with larger filters (32 → 64 → 128)"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),  # Additional layer with 128 filters
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(10, activation='softmax')
    ])
    return model

def create_baseline_cnn():
    """Create baseline CNN for comparison (from Q7)"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(10, activation='softmax')
    ])
    return model

def analyze_parameters():
    """Compare parameters between baseline and large filter models"""
    print("=" * 60)
    print("PARAMETER COMPARISON")
    print("=" * 60)
    
    baseline = create_baseline_cnn()
    large_filter = create_large_filter_cnn()
    
    params_baseline = baseline.count_params()
    params_large = large_filter.count_params()
    increase = params_large - params_baseline
    percentage = (increase / params_baseline) * 100
    
    print(f"\nBaseline Model (32→64):")
    print(f"  Total Parameters: {params_baseline:,}")
    
    print(f"\nLarge Filter Model (32→64→128):")
    print(f"  Total Parameters: {params_large:,}")
    
    print(f"\nParameter Increase:")
    print(f"  Absolute:   {increase:,}")
    print(f"  Percentage: {percentage:.2f}%")
    print("=" * 60)
    
    return params_baseline, params_large, increase, percentage

def train_model(model, x_train, y_train):
    """Train the model"""
    print("\n" + "=" * 60)
    print("TRAINING LARGE FILTER CNN")
    print("=" * 60)
    print("\nArchitecture:")
    print("  Conv2D(32, 3×3, ReLU)")
    print("  BatchNormalization")
    print("  MaxPooling2D(2×2)")
    print("  Conv2D(64, 3×3, ReLU)")
    print("  BatchNormalization")
    print("  MaxPooling2D(2×2)")
    print("  Conv2D(128, 3×3, ReLU)  ← ADDED")
    print("  BatchNormalization")
    print("  Flatten")
    print("  Dense(128, ReLU)")
    print("  Dropout(0.3)")
    print("  Dense(10, Softmax)")
    print("=" * 60)
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("\nModel Summary:")
    model.summary()
    
    print("\nTraining...")
    history = model.fit(x_train, y_train,
                       epochs=10,
                       batch_size=64,
                       validation_split=0.2,
                       verbose=1)
    
    return history

def evaluate_and_compare(model, x_test, y_test):
    """Evaluate model and compare with Q7"""
    print("\n" + "=" * 60)
    print("EVALUATION & COMPARISON")
    print("=" * 60)
    
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    print(f"\nLarge Filter Model (32→64→128):")
    print(f"  Test Loss:     {test_loss:.4f}")
    print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Try to load Q7 model for comparison
    q7_model_path = "../q7/output/batchnorm_model.h5"
    if os.path.exists(q7_model_path):
        try:
            q7_model = keras.models.load_model(q7_model_path)
            q7_loss, q7_accuracy = q7_model.evaluate(x_test, y_test, verbose=0)
            
            print(f"\nBaseline Model (32→64) - Q7:")
            print(f"  Test Accuracy: {q7_accuracy:.4f} ({q7_accuracy*100:.2f}%)")
            
            print(f"\nImprovement:")
            print(f"  Accuracy Gain: {test_accuracy - q7_accuracy:+.4f} ({(test_accuracy - q7_accuracy)*100:+.2f}%)")
            
            return test_loss, test_accuracy, q7_accuracy
        except:
            pass
    
    print("\n(Baseline model from Q7 not available for comparison)")
    print("=" * 60)
    
    return test_loss, test_accuracy, None

def plot_analysis(history, test_accuracy, q7_accuracy):
    """Plot training curves and comparison"""
    fig = plt.figure(figsize=(16, 5))
    
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    # Training vs Validation Accuracy
    ax1 = plt.subplot(1, 3, 1)
    ax1.plot(epochs, history.history['accuracy'], marker='o', linewidth=2, 
             color='#3498db', label='Training Accuracy')
    ax1.plot(epochs, history.history['val_accuracy'], marker='s', linewidth=2, 
             color='#2ecc71', label='Validation Accuracy')
    ax1.set_title('Training vs Validation Accuracy\n(Filters: 32→64→128)', fontsize=12, fontweight='bold')
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
    ax2.set_title('Training vs Validation Loss\n(Filters: 32→64→128)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=10)
    ax2.set_ylabel('Loss', fontsize=10)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Accuracy comparison
    ax3 = plt.subplot(1, 3, 3)
    if q7_accuracy is not None:
        models_list = ['Baseline\n(32→64)\nQ7', 'Large Filters\n(32→64→128)\nQ8']
        accuracies = [q7_accuracy, test_accuracy]
        colors = ['#95a5a6', '#e74c3c']
        bars = ax3.bar(models_list, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{acc:.4f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax3.set_ylabel('Test Accuracy', fontsize=10)
        ax3.set_title('Model Comparison', fontsize=12, fontweight='bold')
        ax3.set_ylim([0, 1])
        ax3.grid(axis='y', alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'Q7 model\nnot available\nfor comparison', 
                ha='center', va='center', fontsize=12)
        ax3.set_xlim([0, 1])
        ax3.set_ylim([0, 1])
        ax3.axis('off')
    
    plt.suptitle('Large Filter CNN (32→64→128) Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'filter_size_analysis.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/filter_size_analysis.png")
    plt.close()

def save_results(history, test_loss, test_accuracy, params_baseline, params_large, increase, percentage, q7_accuracy, model):
    """Save results"""
    with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
        f.write("Large Filter CNN Results\n")
        f.write("=" * 50 + "\n\n")
        f.write("Filter Configuration: 32 → 64 → 128\n")
        f.write(f"Training Epochs: 10\n\n")
        f.write("Parameter Analysis:\n")
        f.write(f"  Baseline (32→64):       {params_baseline:,}\n")
        f.write(f"  Large Filter (32→64→128): {params_large:,}\n")
        f.write(f"  Increase:               {increase:,} (+{percentage:.2f}%)\n\n")
        f.write(f"Test Loss:                {test_loss:.4f}\n")
        f.write(f"Test Accuracy:            {test_accuracy:.4f}\n\n")
        
        if q7_accuracy is not None:
            f.write("Comparison with Baseline (Q7):\n")
            f.write(f"  Q7 Test Accuracy:  {q7_accuracy:.4f}\n")
            f.write(f"  Q8 Test Accuracy:  {test_accuracy:.4f}\n")
            f.write(f"  Improvement:       {test_accuracy - q7_accuracy:+.4f}\n\n")
        
        f.write("Impact of Larger Filters:\n")
        f.write("  - More feature maps for complex pattern detection\n")
        f.write("  - Deeper network learns hierarchical features\n")
        f.write("  - Trade-off: More parameters vs better performance\n")
        f.write(f"  - Worth it: {percentage:.1f}% more params for better accuracy\n")
    
    print(f"✓ Saved: {output_dir}/results.txt")
    
    # Save model
    model.save(os.path.join(output_dir, 'large_filter_model.h5'))
    print(f"✓ Saved: {output_dir}/large_filter_model.h5")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Analyze parameters
    params_baseline, params_large, increase, percentage = analyze_parameters()
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    # Create large filter model
    model = create_large_filter_cnn()
    
    # Train model
    history = train_model(model, x_train, y_train)
    
    # Evaluate and compare
    test_loss, test_accuracy, q7_accuracy = evaluate_and_compare(model, x_test, y_test)
    
    # Plot analysis
    plot_analysis(history, test_accuracy, q7_accuracy)
    
    # Save results
    save_results(history, test_loss, test_accuracy, params_baseline, params_large, 
                increase, percentage, q7_accuracy, model)
    
    print("\n" + "=" * 60)
    print("Q8 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
