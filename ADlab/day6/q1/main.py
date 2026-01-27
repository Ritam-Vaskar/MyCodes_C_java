"""
Q1: Principal Component Analysis (PCA) on Wine Dataset
Objective: Reduce dimensionality using PCA and visualize the results
- Display proportion of variance captured by each principal component
- 2D Plot: Project data onto first two principal components
- 3D Plot: Project data onto first three principal components
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

def perform_pca_analysis():
    """Perform PCA on Wine dataset and visualize results"""
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Load Wine dataset
    print("Loading Wine Dataset...")
    wine = load_wine()
    X = wine.data
    y = wine.target
    target_names = wine.target_names
    feature_names = wine.feature_names
    
    print(f"Original dataset shape: {X.shape}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Number of samples: {X.shape[0]}")
    print(f"Target classes: {target_names}")
    
    # Standardize the features
    print("\nStandardizing features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform PCA with all components
    print("\nPerforming PCA...")
    pca_full = PCA()
    X_pca_full = pca_full.fit_transform(X_scaled)
    
    # Display variance explained by each component
    variance_ratio = pca_full.explained_variance_ratio_
    cumulative_variance = np.cumsum(variance_ratio)
    
    print("\n" + "="*60)
    print("VARIANCE EXPLAINED BY PRINCIPAL COMPONENTS")
    print("="*60)
    
    results_df = pd.DataFrame({
        'PC': [f'PC{i+1}' for i in range(len(variance_ratio))],
        'Variance Explained': variance_ratio,
        'Cumulative Variance': cumulative_variance
    })
    print(results_df.to_string(index=False))
    
    # Save variance results
    results_df.to_csv('output/variance_explained.csv', index=False)
    print("\nVariance results saved to output/variance_explained.csv")
    
    # Plot variance explained
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Individual variance
    ax1.bar(range(1, len(variance_ratio) + 1), variance_ratio, alpha=0.7, color='steelblue')
    ax1.set_xlabel('Principal Component', fontsize=12)
    ax1.set_ylabel('Variance Explained', fontsize=12)
    ax1.set_title('Variance Explained by Each Principal Component', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Cumulative variance
    ax2.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 
             marker='o', linestyle='-', linewidth=2, markersize=6, color='darkgreen')
    ax2.axhline(y=0.95, color='r', linestyle='--', label='95% Variance')
    ax2.set_xlabel('Number of Components', fontsize=12)
    ax2.set_ylabel('Cumulative Variance Explained', fontsize=12)
    ax2.set_title('Cumulative Variance Explained', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/variance_plot.png', dpi=300, bbox_inches='tight')
    print("Variance plot saved to output/variance_plot.png")
    plt.close()
    
    # 2D PCA Visualization
    print("\nGenerating 2D PCA visualization...")
    pca_2d = PCA(n_components=2)
    X_pca_2d = pca_2d.fit_transform(X_scaled)
    
    plt.figure(figsize=(10, 8))
    colors = ['navy', 'turquoise', 'darkorange']
    
    for i, color, target_name in zip(range(3), colors, target_names):
        plt.scatter(X_pca_2d[y == i, 0], X_pca_2d[y == i, 1], 
                   color=color, alpha=0.7, lw=2, label=target_name, s=50)
    
    plt.xlabel(f'First Principal Component ({pca_2d.explained_variance_ratio_[0]:.2%} variance)', 
              fontsize=12)
    plt.ylabel(f'Second Principal Component ({pca_2d.explained_variance_ratio_[1]:.2%} variance)', 
              fontsize=12)
    plt.title('2D PCA of Wine Dataset', fontsize=16, fontweight='bold')
    plt.legend(loc='best', shadow=True, fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/pca_2d.png', dpi=300, bbox_inches='tight')
    print("2D PCA plot saved to output/pca_2d.png")
    plt.close()
    
    # 3D PCA Visualization
    print("\nGenerating 3D PCA visualization...")
    pca_3d = PCA(n_components=3)
    X_pca_3d = pca_3d.fit_transform(X_scaled)
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    for i, color, target_name in zip(range(3), colors, target_names):
        ax.scatter(X_pca_3d[y == i, 0], X_pca_3d[y == i, 1], X_pca_3d[y == i, 2],
                  color=color, alpha=0.7, lw=2, label=target_name, s=50)
    
    ax.set_xlabel(f'PC1 ({pca_3d.explained_variance_ratio_[0]:.2%})', fontsize=11)
    ax.set_ylabel(f'PC2 ({pca_3d.explained_variance_ratio_[1]:.2%})', fontsize=11)
    ax.set_zlabel(f'PC3 ({pca_3d.explained_variance_ratio_[2]:.2%})', fontsize=11)
    ax.set_title('3D PCA of Wine Dataset', fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('output/pca_3d.png', dpi=300, bbox_inches='tight')
    print("3D PCA plot saved to output/pca_3d.png")
    plt.close()
    
    # Save PCA transformed data
    pca_2d_df = pd.DataFrame(X_pca_2d, columns=['PC1', 'PC2'])
    pca_2d_df['Class'] = [target_names[i] for i in y]
    pca_2d_df.to_csv('output/pca_2d_data.csv', index=False)
    
    pca_3d_df = pd.DataFrame(X_pca_3d, columns=['PC1', 'PC2', 'PC3'])
    pca_3d_df['Class'] = [target_names[i] for i in y]
    pca_3d_df.to_csv('output/pca_3d_data.csv', index=False)
    
    print("\nPCA transformed data saved to output/")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total variance explained by first 2 PCs: {sum(pca_2d.explained_variance_ratio_):.2%}")
    print(f"Total variance explained by first 3 PCs: {sum(pca_3d.explained_variance_ratio_):.2%}")
    print(f"Number of components needed for 95% variance: {np.argmax(cumulative_variance >= 0.95) + 1}")
    print(f"Number of components needed for 99% variance: {np.argmax(cumulative_variance >= 0.99) + 1}")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("PCA Analysis on Wine Dataset\n")
        f.write("="*60 + "\n\n")
        f.write(f"Original dimensions: {X.shape[1]}\n")
        f.write(f"Number of samples: {X.shape[0]}\n")
        f.write(f"Number of classes: {len(target_names)}\n\n")
        f.write(f"Variance explained by first 2 PCs: {sum(pca_2d.explained_variance_ratio_):.2%}\n")
        f.write(f"Variance explained by first 3 PCs: {sum(pca_3d.explained_variance_ratio_):.2%}\n")
        f.write(f"Components needed for 95% variance: {np.argmax(cumulative_variance >= 0.95) + 1}\n")
        f.write(f"Components needed for 99% variance: {np.argmax(cumulative_variance >= 0.99) + 1}\n")
    
    print("\nAll results saved successfully!")
    print("="*60)

if __name__ == "__main__":
    perform_pca_analysis()
