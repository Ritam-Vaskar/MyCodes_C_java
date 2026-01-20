"""
Q2: DBSCAN Clustering on Iris Dataset
How does DBSCAN clustering perform on the Iris dataset in detecting noise and natural clusters?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score, davies_bouldin_score
import os

# Create output directory
os.makedirs('output/q2', exist_ok=True)

# Load Iris dataset
iris = load_iris()
X = iris.data
y_true = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print("="*70)
print("DBSCAN CLUSTERING ON IRIS DATASET")
print("="*70)
print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"True classes: {target_names}")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Try different epsilon values to find optimal
epsilons = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
min_samples_range = [3, 5, 7]

results = []

for eps in epsilons:
    for min_samples in min_samples_range:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X_scaled)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        if n_clusters > 1:
            silhouette = silhouette_score(X_scaled, labels)
            ari = adjusted_rand_score(y_true, labels)
        else:
            silhouette = -1
            ari = -1
        
        results.append({
            'eps': eps,
            'min_samples': min_samples,
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'silhouette': silhouette,
            'ari': ari
        })

results_df = pd.DataFrame(results)
print("\n" + "="*70)
print("PARAMETER SEARCH RESULTS")
print("="*70)
print(results_df.to_string(index=False))

# Select best parameters based on ARI
best_params = results_df.loc[results_df['ari'].idxmax()]
print("\n" + "="*70)
print("BEST PARAMETERS")
print("="*70)
print(f"Epsilon: {best_params['eps']}")
print(f"Min Samples: {int(best_params['min_samples'])}")
print(f"Number of Clusters: {int(best_params['n_clusters'])}")
print(f"Noise Points: {int(best_params['n_noise'])}")
print(f"Silhouette Score: {best_params['silhouette']:.4f}")
print(f"Adjusted Rand Index: {best_params['ari']:.4f}")

# Apply DBSCAN with best parameters
dbscan = DBSCAN(eps=best_params['eps'], min_samples=int(best_params['min_samples']))
labels = dbscan.fit_predict(X_scaled)

# PCA for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Visualization 1: DBSCAN clustering results
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# DBSCAN clusters
unique_labels = set(labels)
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
    
    mask = labels == label
    axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1], 
                    c=[color], marker=marker, s=s, 
                    label=label_name, alpha=0.6, edgecolors='black', linewidths=0.5)

axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)', fontsize=11)
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)', fontsize=11)
axes[0].set_title('DBSCAN Clustering Results', fontsize=13, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# True labels
for i, target_name in enumerate(target_names):
    mask = y_true == i
    axes[1].scatter(X_pca[mask, 0], X_pca[mask, 1],
                    label=target_name, alpha=0.6, s=50, edgecolors='black', linewidths=0.5)

axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)', fontsize=11)
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)', fontsize=11)
axes[1].set_title('True Iris Classes', fontsize=13, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q2/dbscan_vs_true.png', dpi=300, bbox_inches='tight')
plt.show()

# Analyze noise points
noise_mask = labels == -1
noise_indices = np.where(noise_mask)[0]
print("\n" + "="*70)
print("NOISE POINT ANALYSIS")
print("="*70)
print(f"Number of noise points: {len(noise_indices)}")
print(f"Percentage of data: {len(noise_indices)/len(X)*100:.2f}%")

if len(noise_indices) > 0:
    print("\nNoise points by true class:")
    for i, target_name in enumerate(target_names):
        noise_in_class = np.sum(y_true[noise_indices] == i)
        print(f"  {target_name}: {noise_in_class} ({noise_in_class/len(noise_indices)*100:.1f}%)")

# Cluster composition analysis
print("\n" + "="*70)
print("CLUSTER COMPOSITION (True Class Distribution)")
print("="*70)

for cluster_id in sorted(set(labels)):
    if cluster_id == -1:
        continue
    
    cluster_mask = labels == cluster_id
    cluster_size = np.sum(cluster_mask)
    
    print(f"\nCluster {cluster_id} (n={cluster_size}):")
    for i, target_name in enumerate(target_names):
        count = np.sum((labels == cluster_id) & (y_true == i))
        percentage = count / cluster_size * 100
        print(f"  {target_name}: {count} ({percentage:.1f}%)")

# Visualization 2: Feature space analysis
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Plot different feature combinations
feature_pairs = [(0, 1), (0, 2), (1, 3), (2, 3)]
for idx, (f1, f2) in enumerate(feature_pairs):
    ax = axes[idx // 2, idx % 2]
    
    for label in sorted(set(labels)):
        if label == -1:
            color = 'black'
            marker = 'x'
            label_name = 'Noise'
            s = 100
        else:
            marker = 'o'
            label_name = f'Cluster {label}'
            s = 50
        
        mask = labels == label
        ax.scatter(X[mask, f1], X[mask, f2],
                   marker=marker, s=s, label=label_name, 
                   alpha=0.6, edgecolors='black', linewidths=0.5)
    
    ax.set_xlabel(feature_names[f1], fontsize=10)
    ax.set_ylabel(feature_names[f2], fontsize=10)
    ax.set_title(f'{feature_names[f1]} vs {feature_names[f2]}', fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q2/feature_space_dbscan.png', dpi=300, bbox_inches='tight')
plt.show()

# Comparison with different epsilon values
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
test_eps = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

for idx, eps in enumerate(test_eps):
    ax = axes[idx // 3, idx % 3]
    
    dbscan_test = DBSCAN(eps=eps, min_samples=5)
    labels_test = dbscan_test.fit_predict(X_scaled)
    
    unique_labels = set(labels_test)
    colors_test = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    
    for label, color in zip(unique_labels, colors_test):
        if label == -1:
            color = 'black'
            marker = 'x'
            s = 100
        else:
            marker = 'o'
            s = 50
        
        mask = labels_test == label
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                   c=[color], marker=marker, s=s, alpha=0.6)
    
    n_clusters = len(set(labels_test)) - (1 if -1 in labels_test else 0)
    n_noise = list(labels_test).count(-1)
    
    ax.set_title(f'eps={eps}, clusters={n_clusters}, noise={n_noise}', fontsize=10)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q2/epsilon_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
results_df.to_csv('output/q2/parameter_search.csv', index=False)

with open('output/q2/results.txt', 'w') as f:
    f.write("DBSCAN CLUSTERING ON IRIS DATASET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Best Epsilon: {best_params['eps']}\n")
    f.write(f"Best Min Samples: {int(best_params['min_samples'])}\n\n")
    f.write(f"Number of Clusters Found: {int(best_params['n_clusters'])}\n")
    f.write(f"Number of Noise Points: {int(best_params['n_noise'])}\n")
    f.write(f"Percentage of Noise: {int(best_params['n_noise'])/len(X)*100:.2f}%\n\n")
    f.write(f"Silhouette Score: {best_params['silhouette']:.4f}\n")
    f.write(f"Adjusted Rand Index: {best_params['ari']:.4f}\n\n")
    f.write("CONCLUSION:\n")
    f.write("DBSCAN successfully identifies natural clusters in the Iris dataset.\n")
    f.write("The algorithm can detect noise points and handle non-spherical clusters.\n")
    f.write(f"Performance depends heavily on epsilon and min_samples parameters.\n")

print("\n✓ Analysis complete! Results saved to output/q2/")
