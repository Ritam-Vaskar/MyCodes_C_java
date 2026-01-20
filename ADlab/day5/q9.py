"""
Q9: PSO-Optimized K-Means on Wine Dataset
Can Particle Swarm Optimization improve centroid initialization for K-Means on Wine dataset?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from pyswarm import pso
import os

os.makedirs('output/q9', exist_ok=True)

print("="*70)
print("PSO-OPTIMIZED K-MEANS ON WINE DATASET")
print("="*70)

# Load Wine dataset
wine = load_wine()
X = wine.data
y_true = wine.target
feature_names = wine.feature_names
target_names = wine.target_names

print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"Classes: {target_names}")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

n_clusters = 3
n_features = X_scaled.shape[1]

# Define objective function for PSO (minimize inertia)
def kmeans_objective(centroids):
    """Objective function: K-Means inertia"""
    centroids = centroids.reshape(n_clusters, n_features)
    
    # Assign points to nearest centroids
    distances = np.linalg.norm(X_scaled[:, np.newaxis, :] - centroids[np.newaxis, :, :], axis=2)
    labels = np.argmin(distances, axis=1)
    
    # Calculate inertia
    inertia = 0
    for i in range(n_clusters):
        cluster_points = X_scaled[labels == i]
        if len(cluster_points) > 0:
            inertia += np.sum((cluster_points - centroids[i])**2)
    
    return inertia

# Run PSO to find optimal centroids
print("\nRunning Particle Swarm Optimization...")
lb = [X_scaled.min(axis=0).tolist()] * n_clusters
ub = [X_scaled.max(axis=0).tolist()] * n_clusters
lb = np.array(lb).flatten()
ub = np.array(ub).flatten()

# PSO parameters
best_centroids, best_inertia = pso(kmeans_objective, lb, ub, 
                                    swarmsize=30, maxiter=50, debug=False)

best_centroids = best_centroids.reshape(n_clusters, n_features)

# Apply K-Means with PSO-initialized centroids
print("Applying K-Means with PSO-initialized centroids...")
kmeans_pso = KMeans(n_clusters=n_clusters, init=best_centroids, n_init=1, random_state=42)
labels_pso = kmeans_pso.fit_predict(X_scaled)

# Apply standard K-Means (random initialization)
print("Applying standard K-Means (random initialization)...")
results_random = []
for i in range(20):
    kmeans_random = KMeans(n_clusters=n_clusters, init='random', n_init=1, random_state=i)
    labels_random = kmeans_random.fit_predict(X_scaled)
    results_random.append({
        'iteration': i,
        'inertia': kmeans_random.inertia_,
        'silhouette': silhouette_score(X_scaled, labels_random),
        'ari': adjusted_rand_score(y_true, labels_random)
    })

# Apply K-Means++ initialization
print("Applying K-Means with k-means++ initialization...")
kmeans_pp = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, random_state=42)
labels_pp = kmeans_pp.fit_predict(X_scaled)

# Calculate metrics
pso_metrics = {
    'Inertia': kmeans_pso.inertia_,
    'Silhouette': silhouette_score(X_scaled, labels_pso),
    'ARI': adjusted_rand_score(y_true, labels_pso)
}

pp_metrics = {
    'Inertia': kmeans_pp.inertia_,
    'Silhouette': silhouette_score(X_scaled, labels_pp),
    'ARI': adjusted_rand_score(y_true, labels_pp)
}

random_df = pd.DataFrame(results_random)
random_metrics = {
    'Inertia': random_df['inertia'].mean(),
    'Silhouette': random_df['silhouette'].mean(),
    'ARI': random_df['ari'].mean()
}

print("\n" + "="*70)
print("PERFORMANCE COMPARISON")
print("="*70)
comparison = pd.DataFrame({
    'Metric': ['Inertia', 'Silhouette', 'ARI'],
    'PSO-Init': [pso_metrics['Inertia'], pso_metrics['Silhouette'], pso_metrics['ARI']],
    'K-Means++': [pp_metrics['Inertia'], pp_metrics['Silhouette'], pp_metrics['ARI']],
    'Random (avg)': [random_metrics['Inertia'], random_metrics['Silhouette'], random_metrics['ARI']]
})
print(comparison.to_string(index=False))

# Visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# True labels
scatter0 = axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=y_true, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[0, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 0].set_title('True Wine Classes', fontsize=11, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)
plt.colorbar(scatter0, ax=axes[0, 0])

# PSO-initialized
scatter1 = axes[0, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_pso, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[0, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 1].set_title(f'PSO-Init (ARI={pso_metrics["ARI"]:.3f})', fontsize=11, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0, 1])

# K-Means++
scatter2 = axes[1, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_pp, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[1, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[1, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[1, 0].set_title(f'K-Means++ (ARI={pp_metrics["ARI"]:.3f})', fontsize=11, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=axes[1, 0])

# Performance comparison
ax = axes[1, 1]
methods = ['PSO-Init', 'K-Means++', 'Random']
metrics = ['Inertia (scaled)', 'Silhouette', 'ARI']

# Normalize inertia to 0-1 scale for visualization
inertia_values = [pso_metrics['Inertia'], pp_metrics['Inertia'], random_metrics['Inertia']]
max_inertia = max(inertia_values)
normalized_inertia = [1 - (v / max_inertia) for v in inertia_values]

data = {
    'PSO-Init': [normalized_inertia[0], pso_metrics['Silhouette'], pso_metrics['ARI']],
    'K-Means++': [normalized_inertia[1], pp_metrics['Silhouette'], pp_metrics['ARI']],
    'Random': [normalized_inertia[2], random_metrics['Silhouette'], random_metrics['ARI']]
}

x = np.arange(len(metrics))
width = 0.25

for i, method in enumerate(methods):
    ax.bar(x + i*width, data[method], width, label=method)

ax.set_xlabel('Metric', fontsize=10)
ax.set_ylabel('Score', fontsize=10)
ax.set_title('Performance Metrics Comparison', fontsize=11, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(metrics, fontsize=9)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/q9/pso_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot random initialization convergence
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

axes[0].hist(random_df['inertia'], bins=15, edgecolor='black', alpha=0.7, color='skyblue')
axes[0].axvline(pso_metrics['Inertia'], color='red', linestyle='--', linewidth=2, label='PSO')
axes[0].axvline(pp_metrics['Inertia'], color='green', linestyle='--', linewidth=2, label='K-Means++')
axes[0].set_xlabel('Inertia', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Inertia Distribution (Random Init)', fontsize=11, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(random_df['silhouette'], bins=15, edgecolor='black', alpha=0.7, color='lightcoral')
axes[1].axvline(pso_metrics['Silhouette'], color='red', linestyle='--', linewidth=2, label='PSO')
axes[1].axvline(pp_metrics['Silhouette'], color='green', linestyle='--', linewidth=2, label='K-Means++')
axes[1].set_xlabel('Silhouette Score', fontsize=11)
axes[1].set_ylabel('Frequency', fontsize=11)
axes[1].set_title('Silhouette Distribution (Random Init)', fontsize=11, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

axes[2].hist(random_df['ari'], bins=15, edgecolor='black', alpha=0.7, color='lightgreen')
axes[2].axvline(pso_metrics['ARI'], color='red', linestyle='--', linewidth=2, label='PSO')
axes[2].axvline(pp_metrics['ARI'], color='green', linestyle='--', linewidth=2, label='K-Means++')
axes[2].set_xlabel('ARI', fontsize=11)
axes[2].set_ylabel('Frequency', fontsize=11)
axes[2].set_title('ARI Distribution (Random Init)', fontsize=11, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q9/random_init_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
comparison.to_csv('output/q9/performance_comparison.csv', index=False)

with open('output/q9/results.txt', 'w') as f:
    f.write("PSO-OPTIMIZED K-MEANS ON WINE DATASET\n")
    f.write("="*70 + "\n\n")
    f.write("PERFORMANCE METRICS:\n")
    f.write(comparison.to_string(index=False))
    f.write("\n\nCONCLUSION:\n")
    
    if pso_metrics['ARI'] > pp_metrics['ARI']:
        f.write("PSO initialization IMPROVES performance over K-Means++.\n")
    else:
        f.write("K-Means++ performs comparable to or better than PSO.\n")
    
    f.write("\nPSO can find good initial centroids but adds computational cost.\n")
    f.write("K-Means++ is often sufficient for most datasets.\n")
    f.write("PSO may be beneficial for very difficult clustering problems.\n")

print("\n✓ Analysis complete! Results saved to output/q9/")
