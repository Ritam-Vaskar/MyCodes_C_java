"""
Q10: Fuzzy C-Means Clustering on Iris Dataset
How does Fuzzy C-Means clustering handle overlapping classes in the Iris dataset?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
import skfuzzy as fuzz
import os

os.makedirs('output/q10', exist_ok=True)

print("="*70)
print("FUZZY C-MEANS CLUSTERING ON IRIS DATASET")
print("="*70)

# Load Iris dataset
iris = load_iris()
X = iris.data
y_true = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"Classes: {target_names}")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

n_clusters = 3

# Apply Fuzzy C-Means
print("\nApplying Fuzzy C-Means...")
# Transpose data for skfuzzy (expects features x samples)
X_fuzzy = X_scaled.T

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    X_fuzzy, c=n_clusters, m=2, error=0.005, maxiter=1000, init=None
)

# Get cluster membership matrix
labels_fuzzy_hard = np.argmax(u, axis=0)
membership_matrix = u.T

# Apply K-Means for comparison
print("Applying K-Means for comparison...")
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)

# Calculate metrics
fuzzy_ari = adjusted_rand_score(y_true, labels_fuzzy_hard)
kmeans_ari = adjusted_rand_score(y_true, labels_kmeans)

fuzzy_silhouette = silhouette_score(X_scaled, labels_fuzzy_hard)
kmeans_silhouette = silhouette_score(X_scaled, labels_kmeans)

print("\n" + "="*70)
print("PERFORMANCE COMPARISON")
print("="*70)
print(f"Fuzzy C-Means:")
print(f"  ARI: {fuzzy_ari:.4f}")
print(f"  Silhouette: {fuzzy_silhouette:.4f}")
print(f"  FPC (Fuzzy Partition Coefficient): {fpc:.4f}")
print(f"\nK-Means:")
print(f"  ARI: {kmeans_ari:.4f}")
print(f"  Silhouette: {kmeans_silhouette:.4f}")

# Analyze membership degrees
print("\n" + "="*70)
print("MEMBERSHIP DEGREE ANALYSIS")
print("="*70)

# Calculate uncertainty (entropy of membership)
epsilon = 1e-10
entropy = -np.sum(membership_matrix * np.log(membership_matrix + epsilon), axis=1)
max_membership = np.max(membership_matrix, axis=1)
uncertainty = 1 - max_membership

print(f"Average max membership: {max_membership.mean():.4f}")
print(f"Average uncertainty: {uncertainty.mean():.4f}")
print(f"Average entropy: {entropy.mean():.4f}")

# PCA for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# True labels
scatter0 = axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=y_true, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[0, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 0].set_title('True Iris Classes', fontsize=11, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)
plt.colorbar(scatter0, ax=axes[0, 0])

# Fuzzy C-Means hard assignment
scatter1 = axes[0, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_fuzzy_hard, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[0, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 1].set_title(f'Fuzzy C-Means (Hard) - ARI: {fuzzy_ari:.3f}', fontsize=11, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0, 1])

# K-Means
scatter2 = axes[0, 2].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_kmeans, cmap='viridis',
                              alpha=0.6, edgecolors='black', linewidths=0.5, s=50)
axes[0, 2].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0, 2].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0, 2].set_title(f'K-Means - ARI: {kmeans_ari:.3f}', fontsize=11, fontweight='bold')
axes[0, 2].grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=axes[0, 2])

# Membership plots for each cluster
for i in range(n_clusters):
    scatter = axes[1, i].scatter(X_pca[:, 0], X_pca[:, 1], c=membership_matrix[:, i],
                                 cmap='RdYlGn', alpha=0.6, edgecolors='black', 
                                 linewidths=0.5, s=50, vmin=0, vmax=1)
    axes[1, i].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
    axes[1, i].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
    axes[1, i].set_title(f'Cluster {i} Membership', fontsize=11, fontweight='bold')
    axes[1, i].grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=axes[1, i], label='Membership Degree')

plt.tight_layout()
plt.savefig('output/q10/fuzzy_cmeans_results.png', dpi=300, bbox_inches='tight')
plt.show()

# Uncertainty visualization
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Uncertainty scatter
scatter0 = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=uncertainty,
                           cmap='RdYlBu_r', alpha=0.6, edgecolors='black',
                           linewidths=0.5, s=50)
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0].set_title('Fuzzy Clustering Uncertainty', fontsize=11, fontweight='bold')
axes[0].grid(True, alpha=0.3)
plt.colorbar(scatter0, ax=axes[0], label='Uncertainty (1 - max membership)')

# Max membership
scatter1 = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=max_membership,
                           cmap='RdYlGn', alpha=0.6, edgecolors='black',
                           linewidths=0.5, s=50, vmin=0, vmax=1)
axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[1].set_title('Maximum Membership Degree', fontsize=11, fontweight='bold')
axes[1].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[1], label='Max Membership')

# Uncertainty histogram
axes[2].hist(uncertainty, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[2].axvline(uncertainty.mean(), color='red', linestyle='--', linewidth=2,
                label=f'Mean: {uncertainty.mean():.3f}')
axes[2].set_xlabel('Uncertainty', fontsize=11)
axes[2].set_ylabel('Frequency', fontsize=11)
axes[2].set_title('Distribution of Uncertainty', fontsize=11, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q10/uncertainty_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Identify overlapping regions
high_uncertainty_mask = uncertainty > uncertainty.mean() + uncertainty.std()
overlapping_samples = X_pca[high_uncertainty_mask]

print(f"\nSamples in overlapping regions: {np.sum(high_uncertainty_mask)}")
print(f"Percentage: {np.sum(high_uncertainty_mask)/len(X)*100:.2f}%")

# Visualize overlapping regions
plt.figure(figsize=(10, 7))
plt.scatter(X_pca[~high_uncertainty_mask, 0], X_pca[~high_uncertainty_mask, 1],
            c=labels_fuzzy_hard[~high_uncertainty_mask], cmap='viridis',
            alpha=0.4, s=50, label='Clear assignment')
plt.scatter(overlapping_samples[:, 0], overlapping_samples[:, 1],
            c='red', marker='x', s=200, linewidths=3,
            label='Overlapping regions', alpha=0.8)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=11)
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=11)
plt.title('Identification of Overlapping Regions', fontsize=13, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('output/q10/overlapping_regions.png', dpi=300, bbox_inches='tight')
plt.show()

# Membership degree examples
print("\n" + "="*70)
print("SAMPLE MEMBERSHIP DEGREES")
print("="*70)

# Show some examples
sample_indices = [0, 50, 100, 75, 125]  # Examples from each class and boundary
for idx in sample_indices:
    print(f"\nSample {idx} (True class: {target_names[y_true[idx]]}):")
    print(f"  Cluster memberships: {membership_matrix[idx]}")
    print(f"  Assigned cluster: {labels_fuzzy_hard[idx]}")
    print(f"  Max membership: {max_membership[idx]:.4f}")
    print(f"  Uncertainty: {uncertainty[idx]:.4f}")

# Test different fuzziness parameters
print("\n" + "="*70)
print("EFFECT OF FUZZINESS PARAMETER (m)")
print("="*70)

fuzziness_values = [1.5, 2.0, 2.5, 3.0]
fuzziness_results = []

for m in fuzziness_values:
    cntr_m, u_m, _, _, _, _, fpc_m = fuzz.cluster.cmeans(
        X_fuzzy, c=n_clusters, m=m, error=0.005, maxiter=1000, init=None
    )
    labels_m = np.argmax(u_m, axis=0)
    ari_m = adjusted_rand_score(y_true, labels_m)
    
    membership_m = u_m.T
    max_mem_m = np.max(membership_m, axis=1)
    uncertainty_m = 1 - max_mem_m
    
    fuzziness_results.append({
        'm': m,
        'FPC': fpc_m,
        'ARI': ari_m,
        'Avg Uncertainty': uncertainty_m.mean()
    })
    print(f"m={m}: FPC={fpc_m:.4f}, ARI={ari_m:.4f}, Avg Uncertainty={uncertainty_m.mean():.4f}")

fuzziness_df = pd.DataFrame(fuzziness_results)

# Save results
comparison_df = pd.DataFrame({
    'Method': ['Fuzzy C-Means', 'K-Means'],
    'ARI': [fuzzy_ari, kmeans_ari],
    'Silhouette': [fuzzy_silhouette, kmeans_silhouette]
})
comparison_df.to_csv('output/q10/performance_comparison.csv', index=False)
fuzziness_df.to_csv('output/q10/fuzziness_analysis.csv', index=False)

with open('output/q10/results.txt', 'w') as f:
    f.write("FUZZY C-MEANS CLUSTERING ON IRIS DATASET\n")
    f.write("="*70 + "\n\n")
    f.write("PERFORMANCE METRICS:\n")
    f.write(comparison_df.to_string(index=False))
    f.write(f"\n\nFuzzy Partition Coefficient: {fpc:.4f}\n")
    f.write(f"Average Uncertainty: {uncertainty.mean():.4f}\n")
    f.write(f"Samples in overlapping regions: {np.sum(high_uncertainty_mask)} ({np.sum(high_uncertainty_mask)/len(X)*100:.2f}%)\n")
    f.write("\nCONCLUSION:\n")
    f.write("Fuzzy C-Means handles overlapping classes by providing soft membership degrees.\n")
    f.write("Unlike K-Means (hard clustering), FCM allows samples to belong to multiple clusters.\n")
    f.write("This is particularly useful for:\n")
    f.write("  - Identifying boundary/uncertain samples\n")
    f.write("  - Handling overlapping class distributions\n")
    f.write("  - Providing confidence in cluster assignments\n\n")
    f.write("For Iris dataset, Versicolor and Virginica classes have some overlap,\n")
    f.write("which Fuzzy C-Means successfully captures through membership degrees.\n")

print("\n✓ Analysis complete! Results saved to output/q10/")
