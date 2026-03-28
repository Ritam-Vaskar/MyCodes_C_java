"""
Q1: Data Loading, Visualization, and Normalization
- Import TensorFlow, NumPy, Matplotlib
- Load CIFAR-10 using cifar10.load_data()
- Print shapes of train/test images and labels
- Display 10 random images with class names
- Normalize pixel values to [0,1]
"""

import tensorflow as tf
from tensorflow.keras.datasets import cifar10
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# CIFAR-10 class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

def load_and_explore_data():
    """Load CIFAR-10 dataset and print information"""
    print("=" * 60)
    print("Q1: DATA LOADING, VISUALIZATION, AND NORMALIZATION")
    print("=" * 60)
    
    # Load CIFAR-10 dataset
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    
    print("\nCIFAR-10 Dataset Information:")
    print("-" * 60)
    print(f"Training images shape: {x_train.shape}")
    print(f"Training labels shape: {y_train.shape}")
    print(f"Test images shape: {x_test.shape}")
    print(f"Test labels shape: {y_test.shape}")
    print(f"\nNumber of training samples: {x_train.shape[0]}")
    print(f"Number of test samples: {x_test.shape[0]}")
    print(f"Image dimensions: {x_train.shape[1]} x {x_train.shape[2]}")
    print(f"Number of channels: {x_train.shape[3]}")
    print(f"Pixel value range: [{x_train.min()}, {x_train.max()}]")
    print(f"\nClasses: {class_names}")
    
    return x_train, y_train, x_test, y_test

def display_random_images(x_train, y_train):
    """Display 10 random images with class names"""
    print("\n" + "-" * 60)
    print("Displaying 10 random images...")
    
    np.random.seed(42)
    random_indices = np.random.randint(0, len(x_train), 10)
    
    plt.figure(figsize=(15, 6))
    for i, idx in enumerate(random_indices):
        plt.subplot(2, 5, i + 1)
        plt.imshow(x_train[idx])
        plt.title(f"{class_names[y_train[idx][0]]}", fontsize=12, fontweight='bold')
        plt.axis('off')
    
    plt.suptitle('10 Random CIFAR-10 Images', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'random_images.png'), dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/random_images.png")
    plt.close()

def normalize_data(x_train, x_test):
    """Normalize pixel values to [0, 1]"""
    print("\n" + "-" * 60)
    print("Normalizing pixel values...")
    
    x_train_norm = x_train.astype('float32') / 255.0
    x_test_norm = x_test.astype('float32') / 255.0
    
    print(f"Original range: [{x_train.min()}, {x_train.max()}]")
    print(f"Normalized range: [{x_train_norm.min()}, {x_train_norm.max()}]")
    
    # Visualize normalization
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(x_train[0])
    axes[0].set_title(f'Original Image\nRange: {x_train[0].min()}-{x_train[0].max()}')
    axes[0].axis('off')
    
    axes[1].imshow(x_train_norm[0])
    axes[1].set_title(f'Normalized Image\nRange: {x_train_norm[0].min():.2f}-{x_train_norm[0].max():.2f}')
    axes[1].axis('off')
    
    plt.suptitle('Image Normalization Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'normalization_comparison.png'), dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/normalization_comparison.png")
    plt.close()
    
    return x_train_norm, x_test_norm

def save_normalized_data(x_train_norm, y_train, x_test_norm, y_test):
    """Save normalized data for use in other questions"""
    np.savez_compressed(
        os.path.join(output_dir, 'cifar10_normalized.npz'),
        x_train=x_train_norm,
        y_train=y_train,
        x_test=x_test_norm,
        y_test=y_test
    )
    print(f"\n✓ Saved normalized data: {output_dir}/cifar10_normalized.npz")

def main():
    print(f"TensorFlow version: {tf.__version__}\n")
    
    # Load and explore data
    x_train, y_train, x_test, y_test = load_and_explore_data()
    
    # Display random images
    display_random_images(x_train, y_train)
    
    # Normalize data
    x_train_norm, x_test_norm = normalize_data(x_train, x_test)
    
    # Save normalized data
    save_normalized_data(x_train_norm, y_train, x_test_norm, y_test)
    
    print("\n" + "=" * 60)
    print("Q1 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
