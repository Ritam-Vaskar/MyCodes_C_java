"""
Question 1: Data Handling and Model Construction
- Import TensorFlow, NumPy, Matplotlib
- Load MNIST dataset
- Display data shapes and sample image
- Normalize and flatten data
- Build Sequential neural network
- Train and evaluate model
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
output_dir = "output/q1"
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("QUESTION 1: DATA HANDLING AND MODEL CONSTRUCTION")
print("=" * 70)

# ============================================================================
# 1. DATA HANDLING
# ============================================================================
print("\n1. LOADING MNIST DATASET")
print("-" * 70)

# Load MNIST dataset
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Print shapes
print(f"Shape of training images: {train_images.shape}")
print(f"Shape of training labels: {train_labels.shape}")
print(f"Shape of test images: {test_images.shape}")
print(f"Shape of test labels: {test_labels.shape}")

print(f"\nDataset Details:")
print(f"  - Number of training samples: {len(train_images)}")
print(f"  - Number of test samples: {len(test_images)}")
print(f"  - Image dimensions: 28 x 28 pixels")
print(f"  - Number of classes: 10 (digits 0-9)")

# Display one training image
print(f"\n2. DISPLAYING SAMPLE IMAGE")
print("-" * 70)
sample_idx = 0
sample_image = train_images[sample_idx]
sample_label = train_labels[sample_idx]

print(f"Sample image index: {sample_idx}")
print(f"Label: {sample_label}")
print(f"Image shape: {sample_image.shape}")
print(f"Pixel value range: [{sample_image.min()}, {sample_image.max()}]")

# Plot the sample image
plt.figure(figsize=(6, 6))
plt.imshow(sample_image, cmap='gray')
plt.title(f'Sample Training Image\nLabel: {sample_label}', fontsize=14, fontweight='bold')
plt.colorbar(label='Pixel Intensity')
plt.axis('off')
plt.tight_layout()
plt.savefig(f"{output_dir}/sample_image.png", dpi=300, bbox_inches='tight')
print(f"Sample image saved to: {output_dir}/sample_image.png")
plt.close()

# Normalize pixel values to [0, 1]
print(f"\n3. NORMALIZING DATA")
print("-" * 70)
train_images_normalized = train_images / 255.0
test_images_normalized = test_images / 255.0

print(f"Original pixel range: [0, 255]")
print(f"Normalized pixel range: [{train_images_normalized.min():.2f}, {train_images_normalized.max():.2f}]")

# Flatten 28x28 images to 784-dimensional vectors
print(f"\n4. FLATTENING IMAGES")
print("-" * 70)
train_images_flat = train_images_normalized.reshape(-1, 784)
test_images_flat = test_images_normalized.reshape(-1, 784)

print(f"Original shape: (28, 28)")
print(f"Flattened shape: (784,)")
print(f"Training data shape after flattening: {train_images_flat.shape}")
print(f"Test data shape after flattening: {test_images_flat.shape}")

# ============================================================================
# 2. MODEL CONSTRUCTION
# ============================================================================
print(f"\n" + "=" * 70)
print("2. MODEL CONSTRUCTION")
print("=" * 70)

# Build Sequential neural network
model = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu', name='hidden_layer'),
    layers.Dense(10, activation='softmax', name='output_layer')
])

print("\n1. MODEL ARCHITECTURE")
print("-" * 70)
model.summary()

# Explain number of parameters
print("\n2. PARAMETER CALCULATION")
print("-" * 70)
print("Layer 1 (Hidden Layer):")
print(f"  - Weights: 784 × 128 = {784 * 128:,} parameters")
print(f"  - Biases: 128 parameters")
print(f"  - Total: {784 * 128 + 128:,} parameters")

print("\nLayer 2 (Output Layer):")
print(f"  - Weights: 128 × 10 = {128 * 10:,} parameters")
print(f"  - Biases: 10 parameters")
print(f"  - Total: {128 * 10 + 10:,} parameters")

total_params = (784 * 128 + 128) + (128 * 10 + 10)
print(f"\nTotal trainable parameters: {total_params:,}")

# Compile the model
print("\n3. COMPILING MODEL")
print("-" * 70)
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("Optimizer: Adam")
print("Loss function: Sparse Categorical Crossentropy")
print("Metrics: Accuracy")

# Train the model
print("\n4. TRAINING MODEL (5 EPOCHS)")
print("-" * 70)
history = model.fit(
    train_images_flat,
    train_labels,
    epochs=5,
    batch_size=32,
    verbose=1
)

# Evaluate on test data
print("\n5. EVALUATING ON TEST DATA")
print("-" * 70)
test_loss, test_accuracy = model.evaluate(test_images_flat, test_labels, verbose=0)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Plot training history
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy plot
ax1.plot(history.history['accuracy'], marker='o', linewidth=2, markersize=8)
ax1.set_title('Training Accuracy over Epochs', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Accuracy', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 1])

# Loss plot
ax2.plot(history.history['loss'], marker='o', color='red', linewidth=2, markersize=8)
ax2.set_title('Training Loss over Epochs', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Loss', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/training_history.png", dpi=300, bbox_inches='tight')
print(f"\nTraining history plot saved to: {output_dir}/training_history.png")
plt.close()

# Make predictions on a few test samples
print("\n6. SAMPLE PREDICTIONS")
print("-" * 70)
num_samples = 5
predictions = model.predict(test_images_flat[:num_samples], verbose=0)

fig, axes = plt.subplots(1, num_samples, figsize=(15, 3))
for i in range(num_samples):
    axes[i].imshow(test_images[i], cmap='gray')
    pred_label = np.argmax(predictions[i])
    true_label = test_labels[i]
    confidence = predictions[i][pred_label] * 100
    
    color = 'green' if pred_label == true_label else 'red'
    axes[i].set_title(f'True: {true_label}\nPred: {pred_label}\n({confidence:.1f}%)', 
                      fontsize=10, color=color, fontweight='bold')
    axes[i].axis('off')

plt.suptitle('Sample Predictions', fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()
plt.savefig(f"{output_dir}/sample_predictions.png", dpi=300, bbox_inches='tight')
print(f"Sample predictions saved to: {output_dir}/sample_predictions.png")
plt.close()

# Save model
model.save(f"{output_dir}/mnist_model.h5")
print(f"\nModel saved to: {output_dir}/mnist_model.h5")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"[OK] Dataset loaded and preprocessed successfully")
print(f"[OK] Model built with {total_params:,} trainable parameters")
print(f"[OK] Model trained for 5 epochs")
print(f"[OK] Final test accuracy: {test_accuracy*100:.2f}%")
print(f"[OK] All outputs saved to: {output_dir}/")
print("=" * 70)
