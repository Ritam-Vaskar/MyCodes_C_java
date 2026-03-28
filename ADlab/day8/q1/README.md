# Q1: Data Loading, Visualization, and Normalization

## Objective
Import TensorFlow, NumPy, and Matplotlib. Load CIFAR-10 using `cifar10.load_data()`. Print shapes of train/test images and labels. Display 10 random images with class names. Normalize pixel values to [0,1].

## Implementation
- Loads CIFAR-10 dataset
- Prints dataset shapes and information
- Displays 10 random images with labels
- Normalizes pixel values from [0, 255] to [0, 1]
- Saves normalized data for subsequent questions

## Output Files
- `random_images.png` - 10 random CIFAR-10 images
- `normalization_comparison.png` - Before/after normalization
- `cifar10_normalized.npz` - Normalized dataset

## Usage
```bash
python main.py
```
