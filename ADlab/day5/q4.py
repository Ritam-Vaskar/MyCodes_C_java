"""
Q4: Gaussian Mixture Model (GMM) vs K-Means on Iris Dataset
How does GMM clustering compare with K-Means on the Iris dataset?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import (silhouette_score, adjusted_rand_score, 
                              davies_bouldin_score, homogeneity_score, 
                              completeness_score, v_measure_score)
import os

# Create output directory
os.makedirs('output/q4', exist_ok=True)

# Load Iris dataset
iris = load_iris()
X = iris.data
y_true = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print("="*70)
print("GMM VS K-MEANS CLUSTERING ON IRIS DATASET")
print("="*70)
print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"True classes: {target_names}")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine optimal number of components
n_components_range = range(2, 8)
bic_scores = []
aic_scores = []
silhouette_gmm = []
silhouette_kmeans_list = []

for n in n_components_range:
    # GMM
    gmm = GaussianMixture(n_components=n, random_state=42, n_init=10)
    gmm.fit(X_scaled)
    labels_gmm = gmm.predict(X_scaled)
    bic_scores.append(gmm.bic(X_scaled))
    aic_scores.append(gmm.aic(X_scaled))
    silhouette_gmm.append(silhouette_score(X_scaled, labels_gmm))
    
    # K-Means
    kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
    labels_kmeans = kmeans.fit_predict(X_scaled)
    silhouette_kmeans_list.append(silhouette_score(X_scaled, labels_kmeans))

# Plot model selection criteria
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(n_components_range, bic_scores, 'ro-', label='BIC')
axes[0].plot(n_components_range, aic_scores, 'bo-', label='AIC')
axes[0].set_xlabel('Number of Components')
axes[0].set_ylabel('Information Criterion')
axes[0].set_title('GMM Model Selection (Lower is Better)')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(n_components_range, silhouette_gmm, 'go-', label='GMM')
axes[1].plot(n_components_range, silhouette_kmeans_list, 'mo-', label='K-Means')
axes[1].set_xlabel('Number of Clusters/Components')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score Comparison')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('output/q4/model_selection.png', dpi=300, bbox_inches='tight')
plt.show()

# Use optimal number (3 for Iris)
optimal_k = 3

# Apply K-Means
print(f"\nApplying K-Means with k={optimal_k}...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)

# Apply GMM with different covariance types
print(f"Applying GMM with {optimal_k} components...")
gmm_full = GaussianMixture(n_components=optimal_k, covariance_type='full', 
                            random_state=42, n_init=10)
labels_gmm_full = gmm_full.fit_predict(X_scaled)
probs_gmm_full = gmm_full.predict_proba(X_scaled)

gmm_diag = GaussianMixture(n_components=optimal_k, covariance_type='diag',
                            random_state=42, n_init=10)
labels_gmm_diag = gmm_diag.fit_predict(X_scaled)

gmm_tied = GaussianMixture(n_components=optimal_k, covariance_type='tied',
                            random_state=42, n_init=10)
labels_gmm_tied = gmm_tied.fit_predict(X_scaled)

gmm_spherical = GaussianMixture(n_components=optimal_k, covariance_type='spherical',
                                 random_state=42, n_init=10)
labels_gmm_spherical = gmm_spherical.fit_predict(X_scaled)

# Calculate comprehensive metrics
methods = {
    'K-Means': labels_kmeans,
    'GMM (Full)': labels_gmm_full,
    'GMM (Diagonal)': labels_gmm_diag,
    'GMM (Tied)': labels_gmm_tied,
    'GMM (Spherical)': labels_gmm_spherical
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

# Visualization: Clustering results
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

plot_configs = [
    ('True Labels', y_true, axes[0, 0]),
    ('K-Means', labels_kmeans, axes[0, 1]),
    ('GMM (Full Covariance)', labels_gmm_full, axes[0, 2]),
    ('GMM (Diagonal)', labels_gmm_diag, axes[1, 0]),
    ('GMM (Tied)', labels_gmm_tied, axes[1, 1]),
    ('GMM (Spherical)', labels_gmm_spherical, axes[1, 2])
]

for title, labels, ax in plot_configs:
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis',
                         alpha=0.6, edgecolors='black', linewidths=0.5)
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.savefig('output/q4/clustering_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Probability visualization for GMM
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i in range(optimal_k):
    scatter = axes[i].scatter(X_pca[:, 0], X_pca[:, 1], c=probs_gmm_full[:, i],
                              cmap='RdYlGn', alpha=0.6, edgecolors='black', linewidths=0.5)
    axes[i].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
    axes[i].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
    axes[i].set_title(f'Component {i} Probability', fontsize=11, fontweight='bold')
    axes[i].grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=axes[i], label='Probability')

plt.tight_layout()
plt.savefig('output/q4/gmm_probabilities.png', dpi=300, bbox_inches='tight')
plt.show()

# Uncertainty analysis for GMM
max_probs = probs_gmm_full.max(axis=1)
uncertainty = 1 - max_probs

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Uncertainty visualization
scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=uncertainty,
                          cmap='RdYlBu_r', alpha=0.6, edgecolors='black', linewidths=0.5)
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})', fontsize=10)
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})', fontsize=10)
axes[0].set_title('GMM Prediction Uncertainty', fontsize=11, fontweight='bold')
axes[0].grid(True, alpha=0.3)
plt.colorbar(scatter, ax=axes[0], label='Uncertainty')

# Histogram of uncertainties
axes[1].hist(uncertainty, bins=30, edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Uncertainty (1 - max probability)', fontsize=10)
axes[1].set_ylabel('Frequency', fontsize=10)
axes[1].set_title('Distribution of Prediction Uncertainty', fontsize=11, fontweight='bold')
axes[1].axvline(uncertainty.mean(), color='red', linestyle='--', 
                label=f'Mean: {uncertainty.mean():.3f}')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q4/gmm_uncertainty.png', dpi=300, bbox_inches='tight')
plt.show()

# Feature space comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
feature_pairs = [(0, 1), (0, 2), (1, 3), (2, 3)]

for idx, (f1, f2) in enumerate(feature_pairs):
    ax = axes[idx // 2, idx % 2]
    
    # K-Means
    ax.scatter(X[labels_kmeans == 0, f1], X[labels_kmeans == 0, f2],
               c='red', marker='o', label='K-Means C0', alpha=0.4, s=50)
    ax.scatter(X[labels_kmeans == 1, f1], X[labels_kmeans == 1, f2],
               c='blue', marker='o', label='K-Means C1', alpha=0.4, s=50)
    ax.scatter(X[labels_kmeans == 2, f1], X[labels_kmeans == 2, f2],
               c='green', marker='o', label='K-Means C2', alpha=0.4, s=50)
    
    # GMM with ellipses would be complex, just show points differently
    ax.scatter(X[labels_gmm_full == 0, f1], X[labels_gmm_full == 0, f2],
               c='red', marker='x', label='GMM C0', alpha=0.6, s=80)
    ax.scatter(X[labels_gmm_full == 1, f1], X[labels_gmm_full == 1, f2],
               c='blue', marker='x', label='GMM C1', alpha=0.6, s=80)
    ax.scatter(X[labels_gmm_full == 2, f1], X[labels_gmm_full == 2, f2],
               c='green', marker='x', label='GMM C2', alpha=0.6, s=80)
    
    ax.set_xlabel(feature_names[f1], fontsize=10)
    ax.set_ylabel(feature_names[f2], fontsize=10)
    ax.set_title(f'{feature_names[f1]} vs {feature_names[f2]}', fontsize=11)
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q4/feature_space_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Comparison summary
print("\n" + "="*70)
print("KEY DIFFERENCES")
print("="*70)
print("\nK-Means:")
print("  - Hard clustering (each point assigned to exactly one cluster)")
print("  - Assumes spherical clusters with equal variance")
print("  - Uses distance-based assignment")
print("  - Faster computation")

print("\nGMM:")
print("  - Soft clustering (probabilistic assignments)")
print("  - Can model elliptical clusters with different shapes/sizes")
print("  - Uses probabilistic model")
print("  - Provides uncertainty estimates")
print("  - More flexible but slower")

# Save results
metrics_df.to_csv('output/q4/performance_metrics.csv', index=False)

# Save GMM parameters
gmm_params = {
    'means': gmm_full.means_,
    'covariances': gmm_full.covariances_,
    'weights': gmm_full.weights_
}

with open('output/q4/results.txt', 'w') as f:
    f.write("GMM VS K-MEANS CLUSTERING ON IRIS DATASET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Number of Clusters/Components: {optimal_k}\n")
    f.write(f"Dataset size: {len(X)}\n\n")
    f.write("PERFORMANCE METRICS:\n")
    f.write(metrics_df.to_string(index=False))
    f.write("\n\n")
    f.write("GMM BIC: {:.2f}\n".format(gmm_full.bic(X_scaled)))
    f.write("GMM AIC: {:.2f}\n".format(gmm_full.aic(X_scaled)))
    f.write("GMM Log-Likelihood: {:.2f}\n".format(gmm_full.score(X_scaled) * len(X)))
    f.write("\nAverage prediction uncertainty: {:.4f}\n".format(uncertainty.mean()))
    f.write("\nCONCLUSION:\n")
    f.write("GMM provides probabilistic cluster assignments and better handles\n")
    f.write("elliptical clusters. K-Means is faster but assumes spherical clusters.\n")
    f.write("For Iris dataset, both perform well, but GMM provides additional insights\n")
    f.write("through probability distributions and uncertainty measures.\n")

print("\n✓ Analysis complete! Results saved to output/q4/")
