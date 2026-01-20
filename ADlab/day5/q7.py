"""
Q7: DBSCAN on Two Moons Synthetic Dataset
Can DBSCAN identify irregular-shaped clusters in the Two Moons synthetic dataset?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (silhouette_score, adjusted_rand_score,
                              davies_bouldin_score, homogeneity_score)
import os

# Create output directory
os.makedirs('output/q7', exist_ok=True)

print("="*70)
print("DBSCAN ON TWO MOONS SYNTHETIC DATASET")
print("="*70)

# Generate Two Moons dataset with varying noise levels
noise_levels = [0.0, 0.05, 0.1, 0.15]
n_samples = 300

fig, axes = plt.subplots(2, 4, figsize=(18, 9))

for idx, noise in enumerate(noise_levels):
    print(f"\nTesting with noise level: {noise}")
    
    # Generate data
    X, y_true = make_moons(n_samples=n_samples, noise=noise, random_state=42)
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply DBSCAN
    dbscan = DBSCAN(eps=0.3, min_samples=5)
    labels_dbscan = dbscan.fit_predict(X_scaled)
    
    # Apply K-Means for comparison
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    labels_kmeans = kmeans.fit_predict(X_scaled)
    
    # Count clusters and noise
    n_clusters_dbscan = len(set(labels_dbscan)) - (1 if -1 in labels_dbscan else 0)
    n_noise = list(labels_dbscan).count(-1)
    
    # Calculate metrics (only if we have valid clusters)
    if n_clusters_dbscan > 0:
        ari_dbscan = adjusted_rand_score(y_true, labels_dbscan)
        if n_clusters_dbscan > 1:
            silhouette_dbscan = silhouette_score(X_scaled, labels_dbscan)
        else:
            silhouette_dbscan = -1
    else:
        ari_dbscan = -1
        silhouette_dbscan = -1
    
    ari_kmeans = adjusted_rand_score(y_true, labels_kmeans)
    silhouette_kmeans = silhouette_score(X_scaled, labels_kmeans)
    
    print(f"  DBSCAN - Clusters: {n_clusters_dbscan}, Noise: {n_noise}, ARI: {ari_dbscan:.4f}")
    print(f"  K-Means - ARI: {ari_kmeans:.4f}")
    
    # Plot DBSCAN results
    ax = axes[0, idx]
    unique_labels = set(labels_dbscan)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    
    for label, color in zip(unique_labels, colors):
        if label == -1:
            color = 'black'
            marker = 'x'
            label_name = 'Noise'
            s = 100
        else:
            marker = 'o'
            label_name = f'Cluster {label}'
            s = 50
        
        mask = labels_dbscan == label
        ax.scatter(X[mask, 0], X[mask, 1], c=[color], marker=marker, s=s,
                   label=label_name, alpha=0.6, edgecolors='black', linewidths=0.5)
    
    ax.set_title(f'DBSCAN (noise={noise})\nClusters={n_clusters_dbscan}, ARI={ari_dbscan:.3f}',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    
    # Plot K-Means results
    ax = axes[1, idx]
    for cluster in range(2):
        mask = labels_kmeans == cluster
        ax.scatter(X[mask, 0], X[mask, 1], label=f'Cluster {cluster}',
                   alpha=0.6, s=50, edgecolors='black', linewidths=0.5)
    
    # Plot K-Means centroids
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X',
               s=300, edgecolors='yellow', linewidths=2, label='Centroids')
    
    ax.set_title(f'K-Means (noise={noise})\nARI={ari_kmeans:.3f}',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q7/noise_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Detailed analysis with optimal noise level
print("\n" + "="*70)
print("DETAILED ANALYSIS (noise=0.1)")
print("="*70)

X, y_true = make_moons(n_samples=n_samples, noise=0.1, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Test different epsilon values
eps_values = [0.1, 0.2, 0.3, 0.4, 0.5]
results = []

for eps in eps_values:
    dbscan = DBSCAN(eps=eps, min_samples=5)
    labels = dbscan.fit_predict(X_scaled)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    if n_clusters > 1:
        ari = adjusted_rand_score(y_true, labels)
        silhouette = silhouette_score(X_scaled, labels)
    else:
        ari = -1
        silhouette = -1
    
    results.append({
        'eps': eps,
        'n_clusters': n_clusters,
        'n_noise': n_noise,
        'ARI': ari,
        'Silhouette': silhouette
    })

results_df = pd.DataFrame(results)
print("\nParameter Search Results:")
print(results_df.to_string(index=False))

# Visualize epsilon effect
fig, axes = plt.subplots(2, len(eps_values), figsize=(18, 7))

for idx, eps in enumerate(eps_values):
    dbscan = DBSCAN(eps=eps, min_samples=5)
    labels = dbscan.fit_predict(X_scaled)
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    # DBSCAN result
    ax = axes[0, idx]
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    
    for label, color in zip(unique_labels, colors):
        if label == -1:
            color = 'black'
            marker = 'x'
            s = 100
        else:
            marker = 'o'
            s = 50
        
        mask = labels == label
        ax.scatter(X[mask, 0], X[mask, 1], c=[color], marker=marker, s=s,
                   alpha=0.6, edgecolors='black', linewidths=0.5)
    
    ax.set_title(f'eps={eps}\nClusters={n_clusters}, Noise={n_noise}', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # True labels
    ax = axes[1, idx]
    for label in range(2):
        mask = y_true == label
        ax.scatter(X[mask, 0], X[mask, 1], label=f'Moon {label}',
                   alpha=0.6, s=50, edgecolors='black', linewidths=0.5)
    ax.set_title('True Labels', fontsize=9)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q7/epsilon_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Compare with other algorithms
print("\n" + "="*70)
print("COMPARISON WITH OTHER ALGORITHMS")
print("="*70)

from sklearn.cluster import AgglomerativeClustering, SpectralClustering

dbscan = DBSCAN(eps=0.3, min_samples=5)
labels_dbscan = dbscan.fit_predict(X_scaled)

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)

hierarchical = AgglomerativeClustering(n_clusters=2)
labels_hierarchical = hierarchical.fit_predict(X_scaled)

spectral = SpectralClustering(n_clusters=2, random_state=42, n_init=10)
labels_spectral = spectral.fit_predict(X_scaled)

methods = {
    'DBSCAN': labels_dbscan,
    'K-Means': labels_kmeans,
    'Hierarchical': labels_hierarchical,
    'Spectral': labels_spectral
}

comparison_data = []
for name, labels in methods.items():
    ari = adjusted_rand_score(y_true, labels)
    if name == 'DBSCAN':
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    else:
        n_clusters = 2
    
    if n_clusters > 1:
        silhouette = silhouette_score(X_scaled, labels)
    else:
        silhouette = -1
    
    comparison_data.append({
        'Method': name,
        'Clusters': n_clusters,
        'ARI': ari,
        'Silhouette': silhouette
    })

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# Visualize all methods
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

configs = [
    ('DBSCAN', labels_dbscan, axes[0, 0]),
    ('K-Means', labels_kmeans, axes[0, 1]),
    ('Hierarchical', labels_hierarchical, axes[1, 0]),
    ('Spectral', labels_spectral, axes[1, 1])
]

for name, labels, ax in configs:
    if name == 'DBSCAN':
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        
        for label, color in zip(unique_labels, colors):
            if label == -1:
                color = 'black'
                marker = 'x'
                s = 100
            else:
                marker = 'o'
                s = 50
            
            mask = labels == label
            ax.scatter(X[mask, 0], X[mask, 1], c=[color], marker=marker, s=s,
                       alpha=0.6, edgecolors='black', linewidths=0.5)
    else:
        for cluster in range(2):
            mask = labels == cluster
            ax.scatter(X[mask, 0], X[mask, 1], label=f'Cluster {cluster}',
                       alpha=0.6, s=50, edgecolors='black', linewidths=0.5)
        ax.legend()
    
    ari = adjusted_rand_score(y_true, labels)
    ax.set_title(f'{name} (ARI={ari:.3f})', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q7/algorithm_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Performance metrics bar chart
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(comparison_df))
width = 0.35

bars1 = ax.bar(x - width/2, comparison_df['ARI'], width, label='ARI', alpha=0.8)
bars2 = ax.bar(x + width/2, comparison_df['Silhouette'], width, label='Silhouette', alpha=0.8)

ax.set_xlabel('Clustering Method', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title('Clustering Performance on Two Moons Dataset', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(comparison_df['Method'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('output/q7/performance_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
results_df.to_csv('output/q7/epsilon_analysis.csv', index=False)
comparison_df.to_csv('output/q7/algorithm_comparison.csv', index=False)

with open('output/q7/results.txt', 'w') as f:
    f.write("DBSCAN ON TWO MOONS SYNTHETIC DATASET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Dataset Size: {n_samples}\n")
    f.write(f"Noise Level: 0.1\n\n")
    f.write("ALGORITHM COMPARISON:\n")
    f.write(comparison_df.to_string(index=False))
    f.write("\n\nCONCLUSION:\n")
    
    best_ari = comparison_df['ARI'].max()
    best_method = comparison_df.loc[comparison_df['ARI'].idxmax(), 'Method']
    
    f.write(f"Best performing method: {best_method} (ARI={best_ari:.4f})\n\n")
    
    if best_method == 'DBSCAN':
        f.write("YES, DBSCAN successfully identifies irregular-shaped clusters!\n")
    else:
        f.write("DBSCAN performs well but other methods may be competitive.\n")
    
    f.write("\nDBSCAN advantages for Two Moons dataset:\n")
    f.write("  - Can detect non-convex (crescent) shapes\n")
    f.write("  - Identifies noise points\n")
    f.write("  - No need to specify number of clusters\n")
    f.write("  - Robust to outliers\n\n")
    f.write("K-Means struggles with non-spherical clusters.\n")
    f.write("Spectral clustering can also handle complex shapes.\n")

print("\n✓ Analysis complete! Results saved to output/q7/")
