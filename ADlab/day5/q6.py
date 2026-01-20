"""
Q6: Spectral Clustering on Iris Dataset
How does Spectral clustering perform on the Iris dataset compared to distance-based clustering?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cluster import SpectralClustering, KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import (silhouette_score, adjusted_rand_score, davies_bouldin_score,
                              homogeneity_score, completeness_score, v_measure_score)
from sklearn.metrics.pairwise import rbf_kernel
import os

# Create output directory
os.makedirs('output/q6', exist_ok=True)

# Load Iris dataset
iris = load_iris()
X = iris.data
y_true = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print("="*70)
print("SPECTRAL CLUSTERING ON IRIS DATASET")
print("="*70)
print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"True classes: {target_names}")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply different clustering methods
n_clusters = 3

print("\nApplying clustering algorithms...")

# 1. Spectral Clustering with different affinity types
spectral_rbf = SpectralClustering(n_clusters=n_clusters, affinity='rbf', 
                                   random_state=42, n_init=10)
labels_spectral_rbf = spectral_rbf.fit_predict(X_scaled)

spectral_nearest = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors',
                                       n_neighbors=10, random_state=42, n_init=10)
labels_spectral_nearest = spectral_nearest.fit_predict(X_scaled)

# 2. K-Means (distance-based)
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)

# 3. Hierarchical (distance-based)
hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
labels_hierarchical = hierarchical.fit_predict(X_scaled)

# Calculate comprehensive metrics
methods = {
    'Spectral (RBF)': labels_spectral_rbf,
    'Spectral (K-NN)': labels_spectral_nearest,
    'K-Means': labels_kmeans,
    'Hierarchical': labels_hierarchical
}

metrics_data = []
for name, labels in methods.items():
    metrics_data.append({
        'Method': name,
        'Silhouette': silhouette_score(X_scaled, labels),
        'Davies-Bouldin': davies_bouldin_score(X_scaled, labels),
        'ARI': adjusted_rand_score(y_true, labels),
        'Homogeneity': homogeneity_score(y_true, labels),
        'Completeness': completeness_score(y_true, labels),
        'V-Measure': v_measure_score(y_true, labels)
    })

metrics_df = pd.DataFrame(metrics_data)

print("\n" + "="*70)
print("COMPREHENSIVE PERFORMANCE COMPARISON")
print("="*70)
print(metrics_df.to_string(index=False))

# PCA for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Visualization: All clustering methods
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# True labels
scatter0 = axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=y_true, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[0, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 0].set_title('True Iris Classes', fontsize=11, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)
plt.colorbar(scatter0, ax=axes[0, 0])

# Spectral RBF
scatter1 = axes[0, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_spectral_rbf, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
ari = adjusted_rand_score(y_true, labels_spectral_rbf)
axes[0, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 1].set_title(f'Spectral (RBF) - ARI: {ari:.3f}', fontsize=11, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0, 1])

# Spectral K-NN
scatter2 = axes[0, 2].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_spectral_nearest, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
ari = adjusted_rand_score(y_true, labels_spectral_nearest)
axes[0, 2].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 2].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 2].set_title(f'Spectral (K-NN) - ARI: {ari:.3f}', fontsize=11, fontweight='bold')
axes[0, 2].grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=axes[0, 2])

# K-Means
scatter3 = axes[1, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_kmeans, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
ari = adjusted_rand_score(y_true, labels_kmeans)
axes[1, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[1, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[1, 0].set_title(f'K-Means - ARI: {ari:.3f}', fontsize=11, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)
plt.colorbar(scatter3, ax=axes[1, 0])

# Hierarchical
scatter4 = axes[1, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_hierarchical, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
ari = adjusted_rand_score(y_true, labels_hierarchical)
axes[1, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[1, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[1, 1].set_title(f'Hierarchical - ARI: {ari:.3f}', fontsize=11, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)
plt.colorbar(scatter4, ax=axes[1, 1])

# Metrics comparison bar chart
ax = axes[1, 2]
metrics_to_plot = ['Silhouette', 'ARI', 'V-Measure']
x = np.arange(len(methods))
width = 0.25

for i, metric in enumerate(metrics_to_plot):
    values = metrics_df[metric].values
    ax.bar(x + i*width, values, width, label=metric)

ax.set_xlabel('Method', fontsize=10)
ax.set_ylabel('Score', fontsize=10)
ax.set_title('Performance Metrics Comparison', fontsize=11, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(metrics_df['Method'], rotation=45, ha='right', fontsize=8)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/q6/clustering_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualize affinity matrix for Spectral Clustering
from sklearn.metrics.pairwise import pairwise_kernels

affinity_rbf = rbf_kernel(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# RBF affinity matrix
im0 = axes[0].imshow(affinity_rbf, cmap='viridis', aspect='auto')
axes[0].set_title('RBF Affinity Matrix', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Sample Index', fontsize=10)
axes[0].set_ylabel('Sample Index', fontsize=10)
plt.colorbar(im0, ax=axes[0], label='Affinity')

# Sorted by true labels to see structure
sorted_idx = np.argsort(y_true)
affinity_sorted = affinity_rbf[sorted_idx][:, sorted_idx]
im1 = axes[1].imshow(affinity_sorted, cmap='viridis', aspect='auto')
axes[1].set_title('RBF Affinity Matrix (Sorted by True Labels)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Sample Index (Sorted)', fontsize=10)
axes[1].set_ylabel('Sample Index (Sorted)', fontsize=10)
plt.colorbar(im1, ax=axes[1], label='Affinity')

# Add lines to separate true classes
cumsum = np.cumsum(np.bincount(y_true))
for pos in cumsum[:-1]:
    axes[1].axhline(y=pos, color='red', linestyle='--', linewidth=1)
    axes[1].axvline(x=pos, color='red', linestyle='--', linewidth=1)

plt.tight_layout()
plt.savefig('output/q6/affinity_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Test different gamma values for RBF kernel
gamma_values = [0.1, 0.5, 1.0, 2.0, 5.0]
gamma_results = []

print("\n" + "="*70)
print("SPECTRAL CLUSTERING WITH DIFFERENT GAMMA VALUES")
print("="*70)

for gamma in gamma_values:
    spectral = SpectralClustering(n_clusters=n_clusters, affinity='rbf',
                                   gamma=gamma, random_state=42, n_init=10)
    labels = spectral.fit_predict(X_scaled)
    
    ari = adjusted_rand_score(y_true, labels)
    silhouette = silhouette_score(X_scaled, labels)
    
    gamma_results.append({
        'Gamma': gamma,
        'ARI': ari,
        'Silhouette': silhouette
    })
    print(f"Gamma={gamma:.1f} - ARI: {ari:.4f}, Silhouette: {silhouette:.4f}")

gamma_df = pd.DataFrame(gamma_results)

# Plot gamma effect
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(gamma_df['Gamma'], gamma_df['ARI'], 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Gamma', fontsize=11)
axes[0].set_ylabel('Adjusted Rand Index', fontsize=11)
axes[0].set_title('Effect of Gamma on Clustering Quality', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

axes[1].plot(gamma_df['Gamma'], gamma_df['Silhouette'], 'ro-', linewidth=2, markersize=8)
axes[1].set_xlabel('Gamma', fontsize=11)
axes[1].set_ylabel('Silhouette Score', fontsize=11)
axes[1].set_title('Effect of Gamma on Silhouette Score', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q6/gamma_effect.png', dpi=300, bbox_inches='tight')
plt.show()

# Feature space comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
feature_pairs = [(0, 1), (0, 2), (1, 3), (2, 3)]

for idx, (f1, f2) in enumerate(feature_pairs):
    ax = axes[idx // 2, idx % 2]
    
    # Plot Spectral RBF
    for cluster in range(n_clusters):
        mask = labels_spectral_rbf == cluster
        ax.scatter(X[mask, f1], X[mask, f2], label=f'Spectral C{cluster}',
                   alpha=0.5, s=50, edgecolors='black', linewidths=0.5)
    
    ax.set_xlabel(feature_names[f1], fontsize=10)
    ax.set_ylabel(feature_names[f2], fontsize=10)
    ax.set_title(f'{feature_names[f1]} vs {feature_names[f2]}', fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q6/feature_space_spectral.png', dpi=300, bbox_inches='tight')
plt.show()

# Comparative analysis
print("\n" + "="*70)
print("KEY DIFFERENCES")
print("="*70)
print("\nSpectral Clustering:")
print("  - Uses graph-based approach (affinity matrix)")
print("  - Can detect non-convex clusters")
print("  - Performs eigenvalue decomposition")
print("  - Better for complex cluster shapes")
print("  - More computationally expensive")

print("\nDistance-based Clustering (K-Means, Hierarchical):")
print("  - Uses Euclidean distance")
print("  - Assumes convex clusters")
print("  - Simpler and faster")
print("  - Works well for spherical clusters")

# Determine winner
best_spectral_ari = max(adjusted_rand_score(y_true, labels_spectral_rbf),
                        adjusted_rand_score(y_true, labels_spectral_nearest))
best_distance_ari = max(adjusted_rand_score(y_true, labels_kmeans),
                        adjusted_rand_score(y_true, labels_hierarchical))

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print(f"Best Spectral Clustering ARI: {best_spectral_ari:.4f}")
print(f"Best Distance-based ARI: {best_distance_ari:.4f}")

if best_spectral_ari > best_distance_ari:
    print("\nSpectral clustering performs BETTER on Iris dataset.")
else:
    print("\nDistance-based clustering performs BETTER on Iris dataset.")

print("\nFor Iris dataset (well-separated, roughly spherical clusters),")
print("both approaches work well. Spectral clustering may offer marginal")
print("improvements but at higher computational cost.")

# Save results
metrics_df.to_csv('output/q6/performance_metrics.csv', index=False)
gamma_df.to_csv('output/q6/gamma_analysis.csv', index=False)

with open('output/q6/results.txt', 'w') as f:
    f.write("SPECTRAL CLUSTERING ON IRIS DATASET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Number of Clusters: {n_clusters}\n")
    f.write(f"Dataset Size: {len(X)}\n\n")
    f.write("PERFORMANCE METRICS:\n")
    f.write(metrics_df.to_string(index=False))
    f.write("\n\nBest Spectral ARI: {:.4f}\n".format(best_spectral_ari))
    f.write("Best Distance-based ARI: {:.4f}\n".format(best_distance_ari))
    f.write("\nCONCLUSION:\n")
    f.write("Spectral clustering uses graph theory and can handle non-convex clusters.\n")
    f.write("For Iris dataset with well-separated spherical clusters, both spectral\n")
    f.write("and distance-based methods perform well. Spectral may offer slight\n")
    f.write("advantages but requires more computation.\n")

print("\n✓ Analysis complete! Results saved to output/q6/")
