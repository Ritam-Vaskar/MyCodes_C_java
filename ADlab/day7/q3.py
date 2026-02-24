"""
Question 3: Performance Analysis and Model Improvements
- Train model for 10 epochs with history
- Plot training accuracy and loss
- Add validation split and analyze overfitting/underfitting
- Model improvements: Dropout, more neurons, additional layers
- Generate confusion matrix
- Compare Adam vs SGD optimizers
- Implement early stopping
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os

# Create output directory
output_dir = "output/q3"
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("QUESTION 3: PERFORMANCE ANALYSIS AND MODEL IMPROVEMENTS")
print("=" * 70)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================
print("\n1. LOADING DATA")
print("-" * 70)

# Load MNIST dataset
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize and flatten
train_images_flat = train_images.reshape(-1, 784) / 255.0
test_images_flat = test_images.reshape(-1, 784) / 255.0

print(f"Training samples: {len(train_images)}")
print(f"Test samples: {len(test_images)}")

# ============================================================================
# 2. STAGE 3 - PERFORMANCE: TRAIN FOR 10 EPOCHS
# ============================================================================
print("\n" + "=" * 70)
print("STAGE 3: PERFORMANCE ANALYSIS")
print("=" * 70)
print("\n2. TRAINING BASELINE MODEL (10 EPOCHS)")
print("-" * 70)

model_baseline = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_baseline.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_10 = model_baseline.fit(
    train_images_flat,
    train_labels,
    epochs=10,
    batch_size=32,
    verbose=1
)

# Plot training history
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy
ax1.plot(history_10.history['accuracy'], marker='o', linewidth=2, markersize=6)
ax1.set_title('Training Accuracy vs Epoch', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Accuracy', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 1])

# Loss
ax2.plot(history_10.history['loss'], marker='o', color='red', linewidth=2, markersize=6)
ax2.set_title('Training Loss vs Epoch', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Loss', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/training_10_epochs.png", dpi=300, bbox_inches='tight')
print(f"Training plots saved to: {output_dir}/training_10_epochs.png")
plt.close()

# ============================================================================
# 3. TRAINING WITH VALIDATION SPLIT
# ============================================================================
print("\n3. TRAINING WITH VALIDATION SPLIT (20%)")
print("-" * 70)

model_val = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_val.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_val = model_val.fit(
    train_images_flat,
    train_labels,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Plot training vs validation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy
ax1.plot(history_val.history['accuracy'], label='Training', marker='o', linewidth=2)
ax1.plot(history_val.history['val_accuracy'], label='Validation', marker='s', linewidth=2)
ax1.set_title('Training vs Validation Accuracy', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Accuracy', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 1])

# Loss
ax2.plot(history_val.history['loss'], label='Training', marker='o', linewidth=2)
ax2.plot(history_val.history['val_loss'], label='Validation', marker='s', linewidth=2)
ax2.set_title('Training vs Validation Loss', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Loss', fontsize=12)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/training_vs_validation.png", dpi=300, bbox_inches='tight')
print(f"Training vs validation plots saved to: {output_dir}/training_vs_validation.png")
plt.close()

# Overfitting/Underfitting Analysis
print("\n4. OVERFITTING/UNDERFITTING ANALYSIS")
print("-" * 70)
final_train_acc = history_val.history['accuracy'][-1]
final_val_acc = history_val.history['val_accuracy'][-1]
acc_gap = final_train_acc - final_val_acc

print(f"Final Training Accuracy: {final_train_acc:.4f}")
print(f"Final Validation Accuracy: {final_val_acc:.4f}")
print(f"Accuracy Gap: {acc_gap:.4f}")

if acc_gap > 0.05:
    print("[WARNING] OVERFITTING detected: Training accuracy significantly higher than validation")
    print("   Recommendations: Add dropout, regularization, or reduce model complexity")
elif final_train_acc < 0.85 and final_val_acc < 0.85:
    print("[WARNING] UNDERFITTING detected: Both accuracies are low")
    print("   Recommendations: Increase model complexity, train longer, or adjust learning rate")
else:
    print("[OK] Model appears well-fitted")

# ============================================================================
# 4. MODEL IMPROVEMENTS
# ============================================================================
print("\n" + "=" * 70)
print("MODEL IMPROVEMENTS")
print("=" * 70)

improvements = {}

# Improvement 1: Add Dropout
print("\n5. IMPROVEMENT 1: ADD DROPOUT (rate=0.2)")
print("-" * 70)

model_dropout = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

model_dropout.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_dropout = model_dropout.fit(
    train_images_flat, train_labels,
    epochs=10, batch_size=32,
    validation_split=0.2, verbose=0
)

test_loss_dropout, test_acc_dropout = model_dropout.evaluate(test_images_flat, test_labels, verbose=0)
improvements['Dropout'] = test_acc_dropout
print(f"Test Accuracy with Dropout: {test_acc_dropout:.4f} ({test_acc_dropout*100:.2f}%)")

# Improvement 2: Increase neurons (128 → 256)
print("\n6. IMPROVEMENT 2: INCREASE NEURONS (128 → 256)")
print("-" * 70)

model_256 = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(256, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_256.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_256 = model_256.fit(
    train_images_flat, train_labels,
    epochs=10, batch_size=32,
    validation_split=0.2, verbose=0
)

test_loss_256, test_acc_256 = model_256.evaluate(test_images_flat, test_labels, verbose=0)
improvements['256 Neurons'] = test_acc_256
print(f"Test Accuracy with 256 neurons: {test_acc_256:.4f} ({test_acc_256*100:.2f}%)")

# Improvement 3: Add one more hidden layer (64 neurons)
print("\n7. IMPROVEMENT 3: ADD HIDDEN LAYER (128 → 64 → 10)")
print("-" * 70)

model_2layer = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_2layer.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_2layer = model_2layer.fit(
    train_images_flat, train_labels,
    epochs=10, batch_size=32,
    validation_split=0.2, verbose=0
)

test_loss_2layer, test_acc_2layer = model_2layer.evaluate(test_images_flat, test_labels, verbose=0)
improvements['2 Hidden Layers'] = test_acc_2layer
print(f"Test Accuracy with 2 hidden layers: {test_acc_2layer:.4f} ({test_acc_2layer*100:.2f}%)")

# Improvement 4: Early Stopping
print("\n8. IMPROVEMENT 4: EARLY STOPPING (20 epochs max)")
print("-" * 70)

model_early = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

model_early.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True,
    verbose=1
)

history_early = model_early.fit(
    train_images_flat, train_labels,
    epochs=20, batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=0
)

test_loss_early, test_acc_early = model_early.evaluate(test_images_flat, test_labels, verbose=0)
improvements['Early Stopping'] = test_acc_early
print(f"Test Accuracy with Early Stopping: {test_acc_early:.4f} ({test_acc_early*100:.2f}%)")
print(f"Stopped at epoch: {len(history_early.history['loss'])}")

# ============================================================================
# 5. CONFUSION MATRIX
# ============================================================================
print("\n9. GENERATING CONFUSION MATRIX")
print("-" * 70)

# Use best model
predictions = model_dropout.predict(test_images_flat, verbose=0)
predicted_labels = np.argmax(predictions, axis=1)

# Compute confusion matrix
cm = confusion_matrix(test_labels, predicted_labels)

# Plot confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=range(10), yticklabels=range(10))
plt.title('Confusion Matrix - Test Predictions', fontsize=14, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('True Label', fontsize=12)
plt.tight_layout()
plt.savefig(f"{output_dir}/confusion_matrix.png", dpi=300, bbox_inches='tight')
print(f"Confusion matrix saved to: {output_dir}/confusion_matrix.png")
plt.close()

# Classification report
print("\nClassification Report:")
print(classification_report(test_labels, predicted_labels, 
                          target_names=[str(i) for i in range(10)]))

# ============================================================================
# 6. OPTIMIZER COMPARISON: ADAM VS SGD
# ============================================================================
print("\n10. OPTIMIZER COMPARISON: ADAM VS SGD")
print("-" * 70)

# Adam optimizer
model_adam = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_adam.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_adam = model_adam.fit(
    train_images_flat, train_labels,
    epochs=10, batch_size=32,
    validation_split=0.2, verbose=0
)

test_loss_adam, test_acc_adam = model_adam.evaluate(test_images_flat, test_labels, verbose=0)

# SGD optimizer
model_sgd = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model_sgd.compile(
    optimizer='sgd',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_sgd = model_sgd.fit(
    train_images_flat, train_labels,
    epochs=10, batch_size=32,
    validation_split=0.2, verbose=0
)

test_loss_sgd, test_acc_sgd = model_sgd.evaluate(test_images_flat, test_labels, verbose=0)

print(f"\nAdam Test Accuracy: {test_acc_adam:.4f} ({test_acc_adam*100:.2f}%)")
print(f"SGD Test Accuracy: {test_acc_sgd:.4f} ({test_acc_sgd*100:.2f}%)")
print(f"Difference: {abs(test_acc_adam - test_acc_sgd):.4f}")

if test_acc_adam > test_acc_sgd:
    print(f"[OK] Adam optimizer performs better (+{(test_acc_adam - test_acc_sgd)*100:.2f}%)")
else:
    print(f"[OK] SGD optimizer performs better (+{(test_acc_sgd - test_acc_adam)*100:.2f}%)")

# Plot optimizer comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy comparison
ax1.plot(history_adam.history['val_accuracy'], label='Adam', marker='o', linewidth=2)
ax1.plot(history_sgd.history['val_accuracy'], label='SGD', marker='s', linewidth=2)
ax1.set_title('Optimizer Comparison - Validation Accuracy', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Validation Accuracy', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Loss comparison
ax2.plot(history_adam.history['val_loss'], label='Adam', marker='o', linewidth=2)
ax2.plot(history_sgd.history['val_loss'], label='SGD', marker='s', linewidth=2)
ax2.set_title('Optimizer Comparison - Validation Loss', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Validation Loss', fontsize=12)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/optimizer_comparison.png", dpi=300, bbox_inches='tight')
print(f"\nOptimizer comparison plots saved to: {output_dir}/optimizer_comparison.png")
plt.close()

# ============================================================================
# 7. SUMMARY OF ALL IMPROVEMENTS
# ============================================================================
print("\n" + "=" * 70)
print("IMPROVEMENT SUMMARY")
print("=" * 70)

baseline_acc = model_val.evaluate(test_images_flat, test_labels, verbose=0)[1]
improvements['Baseline'] = baseline_acc

print(f"\n{'Model':<25} {'Test Accuracy':<15} {'Improvement'}")
print("-" * 70)
print(f"{'Baseline (128 neurons)':<25} {baseline_acc:.4f}        -")
print(f"{'+ Dropout (0.2)':<25} {test_acc_dropout:.4f}        {(test_acc_dropout - baseline_acc)*100:+.2f}%")
print(f"{'+ 256 Neurons':<25} {test_acc_256:.4f}        {(test_acc_256 - baseline_acc)*100:+.2f}%")
print(f"{'+ 2 Hidden Layers':<25} {test_acc_2layer:.4f}        {(test_acc_2layer - baseline_acc)*100:+.2f}%")
print(f"{'+ Early Stopping':<25} {test_acc_early:.4f}        {(test_acc_early - baseline_acc)*100:+.2f}%")

# Bar chart of improvements
fig, ax = plt.subplots(figsize=(10, 6))
models_list = ['Baseline', 'Dropout', '256 Neurons', '2 Hidden\nLayers', 'Early\nStopping']
accuracies = [baseline_acc, test_acc_dropout, test_acc_256, test_acc_2layer, test_acc_early]
colors = ['gray', 'blue', 'green', 'orange', 'red']

bars = ax.bar(models_list, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.4f}', ha='center', va='bottom', fontweight='bold')

ax.set_title('Model Improvement Comparison', fontsize=14, fontweight='bold')
ax.set_ylabel('Test Accuracy', fontsize=12)
ax.set_ylim([0.94, 0.99])
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f"{output_dir}/improvements_comparison.png", dpi=300, bbox_inches='tight')
print(f"\nImprovement comparison chart saved to: {output_dir}/improvements_comparison.png")
plt.close()

# Save summary
with open(f"{output_dir}/analysis_summary.txt", 'w') as f:
    f.write("Performance Analysis and Model Improvements Summary\n")
    f.write("=" * 70 + "\n\n")
    f.write("Overfitting/Underfitting Analysis:\n")
    f.write(f"  Final Training Accuracy: {final_train_acc:.4f}\n")
    f.write(f"  Final Validation Accuracy: {final_val_acc:.4f}\n")
    f.write(f"  Accuracy Gap: {acc_gap:.4f}\n\n")
    f.write("Model Improvements:\n")
    f.write(f"  Baseline: {baseline_acc:.4f}\n")
    f.write(f"  + Dropout: {test_acc_dropout:.4f} ({(test_acc_dropout - baseline_acc)*100:+.2f}%)\n")
    f.write(f"  + 256 Neurons: {test_acc_256:.4f} ({(test_acc_256 - baseline_acc)*100:+.2f}%)\n")
    f.write(f"  + 2 Hidden Layers: {test_acc_2layer:.4f} ({(test_acc_2layer - baseline_acc)*100:+.2f}%)\n")
    f.write(f"  + Early Stopping: {test_acc_early:.4f} ({(test_acc_early - baseline_acc)*100:+.2f}%)\n\n")
    f.write("Optimizer Comparison:\n")
    f.write(f"  Adam: {test_acc_adam:.4f}\n")
    f.write(f"  SGD: {test_acc_sgd:.4f}\n")

print(f"Analysis summary saved to: {output_dir}/analysis_summary.txt")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("[OK] Performance analysis completed")
print("[OK] Overfitting/underfitting analysis done")
print("[OK] Multiple model improvements tested")
print("[OK] Confusion matrix generated")
print("[OK] Optimizer comparison completed")
print(f"[OK] All outputs saved to: {output_dir}/")
print("=" * 70)
