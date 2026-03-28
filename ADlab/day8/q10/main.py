"""
Q10: Generate Confusion Matrix and Display Misclassified Images
- Confusion matrix
- Classification report
- Display 15 misclassified CIFAR-10 images
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import cifar10
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# CIFAR-10 class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

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

def load_best_model():
    """Load the best model from previous questions"""
    # Try Q9 first (with early stopping)
    model_paths = [
        "../q9/output/early_stopping_model.h5",
        "../q8/output/large_filter_model.h5",
        "../q7/output/batchnorm_model.h5"
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            print(f"Loading model from: {path}")
            return keras.models.load_model(path), path
    
    print("No pre-trained model found. Training a new model...")
    return None, None

def make_predictions(model, x_test, y_test):
    """Make predictions on test set"""
    print("\n" + "=" * 60)
    print("MAKING PREDICTIONS")
    print("=" * 60)
    
    # Get predictions
    y_pred_probs = model.predict(x_test, verbose=0)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true = y_test.flatten()
    
    # Evaluate
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    print(f"\nTest Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"Total test samples: {len(y_test)}")
    print(f"Correct predictions: {np.sum(y_pred_classes == y_true)}")
    print(f"Incorrect predictions: {np.sum(y_pred_classes != y_true)}")
    
    return y_pred_classes, y_pred_probs, y_true

def generate_confusion_matrix(y_true, y_pred):
    """Generate and plot confusion matrix"""
    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)
    
    # Generate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, 
                yticklabels=class_names,
                cbar_kws={'label': 'Count'},
                linewidths=0.5,
                linecolor='gray')
    
    plt.title('Confusion Matrix - CIFAR-10 Classification', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/confusion_matrix.png")
    plt.close()
    
    # Analyze confusion matrix
    print("\nMost Confused Pairs:")
    confusion_pairs = []
    for i in range(10):
        for j in range(10):
            if i != j and cm[i][j] > 0:
                confusion_pairs.append((cm[i][j], class_names[i], class_names[j]))
    
    confusion_pairs.sort(reverse=True)
    for count, true_class, pred_class in confusion_pairs[:5]:
        print(f"  {true_class:12} → {pred_class:12}: {count:4d} times")
    
    return cm

def generate_classification_report(y_true, y_pred):
    """Generate classification report"""
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    print("\n" + report)
    
    # Save report
    with open(os.path.join(output_dir, 'classification_report.txt'), 'w') as f:
        f.write("CIFAR-10 Classification Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(report)
    
    print(f"✓ Saved: {output_dir}/classification_report.txt")

def display_misclassified_images(x_test, y_true, y_pred, y_pred_probs):
    """Display 15 misclassified images"""
    print("\n" + "=" * 60)
    print("MISCLASSIFIED IMAGES")
    print("=" * 60)
    
    # Find misclassified images
    misclassified_indices = np.where(y_pred != y_true)[0]
    print(f"\nTotal misclassified images: {len(misclassified_indices)}")
    print(f"Misclassification rate: {len(misclassified_indices)/len(y_true)*100:.2f}%")
    
    # Select 15 random misclassified images
    np.random.seed(42)
    if len(misclassified_indices) >= 15:
        sample_indices = np.random.choice(misclassified_indices, 15, replace=False)
    else:
        sample_indices = misclassified_indices
    
    # Denormalize images for display
    x_test_original = (x_test * 255).astype('uint8')
    
    # Display images
    plt.figure(figsize=(16, 10))
    for i, idx in enumerate(sample_indices):
        plt.subplot(3, 5, i + 1)
        plt.imshow(x_test_original[idx])
        
        true_label = class_names[y_true[idx]]
        pred_label = class_names[y_pred[idx]]
        confidence = y_pred_probs[idx][y_pred[idx]] * 100
        
        title = f'True: {true_label}\nPred: {pred_label}\n({confidence:.1f}%)'
        plt.title(title, fontsize=9, color='red', fontweight='bold')
        plt.axis('off')
    
    plt.suptitle('15 Misclassified CIFAR-10 Images', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'misclassified_images.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/misclassified_images.png")
    plt.close()
    
    # Print details of sample misclassifications
    print("\nSample Misclassifications:")
    for i, idx in enumerate(sample_indices[:5], 1):
        true_label = class_names[y_true[idx]]
        pred_label = class_names[y_pred[idx]]
        confidence = y_pred_probs[idx][y_pred[idx]] * 100
        print(f"  {i}. True: {true_label:12} → Predicted: {pred_label:12} (Confidence: {confidence:.1f}%)")

def analyze_class_performance(y_true, y_pred, cm):
    """Analyze per-class performance"""
    print("\n" + "=" * 60)
    print("PER-CLASS PERFORMANCE")
    print("=" * 60)
    
    class_accuracies = []
    for i in range(10):
        total = np.sum(cm[i, :])
        correct = cm[i, i]
        accuracy = correct / total if total > 0 else 0
        class_accuracies.append((accuracy, class_names[i], correct, total))
    
    class_accuracies.sort()
    
    print("\nWorst Performing Classes:")
    for acc, name, correct, total in class_accuracies[:3]:
        print(f"  {name:12}: {acc*100:.2f}% ({correct}/{total})")
    
    print("\nBest Performing Classes:")
    for acc, name, correct, total in class_accuracies[-3:]:
        print(f"  {name:12}: {acc*100:.2f}% ({correct}/{total})")
    
    # Plot class-wise accuracy
    plt.figure(figsize=(12, 6))
    names = [name for _, name, _, _ in sorted(class_accuracies, reverse=True)]
    accs = [acc*100 for acc, _, _, _ in sorted(class_accuracies, reverse=True)]
    colors = ['#2ecc71' if acc > 70 else '#f39c12' if acc > 60 else '#e74c3c' for acc in accs]
    
    bars = plt.bar(names, accs, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    plt.axhline(y=np.mean(accs), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(accs):.1f}%')
    plt.ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    plt.title('Per-Class Accuracy', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.ylim([0, 100])
    
    # Add value labels
    for bar, acc in zip(bars, accs):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'class_accuracy.png'), dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_dir}/class_accuracy.png")
    plt.close()

def save_summary(test_accuracy, cm, model_path):
    """Save complete summary"""
    with open(os.path.join(output_dir, 'evaluation_summary.txt'), 'w') as f:
        f.write("CIFAR-10 Model Evaluation Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Model Used: {model_path if model_path else 'New model'}\n")
        f.write(f"Overall Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)\n\n")
        f.write("Files Generated:\n")
        f.write("  1. confusion_matrix.png - Full 10x10 confusion matrix\n")
        f.write("  2. classification_report.txt - Precision/Recall/F1 scores\n")
        f.write("  3. misclassified_images.png - 15 error examples\n")
        f.write("  4. class_accuracy.png - Per-class performance\n")
        f.write("  5. evaluation_summary.txt - This file\n\n")
        f.write("Analysis Complete!\n")
    
    print(f"✓ Saved: {output_dir}/evaluation_summary.txt")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    print("=" * 60)
    print("Q10: CONFUSION MATRIX & MISCLASSIFIED IMAGES")
    print("=" * 60)
    
    # Load data
    x_train, y_train, x_test, y_test = load_data()
    
    #Load best model
    model, model_path = load_best_model()
    
    if model is None:
        print("\nError: No pre-trained model found!")
        print("Please run Q7, Q8, or Q9 first to train a model.")
        return
    
    # Make predictions
    y_pred, y_pred_probs, y_true = make_predictions(model, x_test, y_test)
    
    # Generate confusion matrix
    cm = generate_confusion_matrix(y_true, y_pred)
    
    # Generate classification report
    generate_classification_report(y_true, y_pred)
    
    # Display misclassified images
    display_misclassified_images(x_test, y_true, y_pred, y_pred_probs)
    
    # Analyze class performance
    analyze_class_performance(y_true, y_pred, cm)
    
    # Save summary
    test_accuracy = np.sum(y_pred == y_true) / len(y_true)
    save_summary(test_accuracy, cm, model_path)
    
    print("\n" + "=" * 60)
    print("Q10 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nAll evaluation files saved in output/")
    print("  - Confusion Matrix")
    print("  - Classification Report")
    print("  - 15 Misclassified Images")
    print("  - Class-wise Accuracy Chart")
    print("=" * 60)

if __name__ == "__main__":
    main()
