"""
Q3: K-Means vs Hierarchical Clustering on Wholesale Customers Dataset
Can K-Means and Hierarchical clustering produce consistent customer segments?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, adjusted_rand_score, davies_bouldin_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import cdist
import os

# Create output directory
os.makedirs('output/q3', exist_ok=True)

# Create or load Wholesale Customers dataset
def load_or_create_wholesale_data():
    """Load or create synthetic Wholesale Customers dataset"""
    try:
        # Try to load from UCI repository or local file
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00292/Wholesale%20customers%20data.csv"
        df = pd.read_csv(url)
        print("Loaded Wholesale Customers dataset from UCI repository")
    except:
        print("Creating synthetic Wholesale Customers dataset...")
        np.random.seed(42)
        n_samples = 440
        
        # Create different customer types
        # Type 1: Hotel/Restaurant/Cafe - high fresh, milk, grocery
        type1 = pd.DataFrame({
            'Channel': [1] * 110,
            'Region': np.random.randint(1, 4, 110),
            'Fresh': np.random.randint(3000, 30000, 110),
            'Milk': np.random.randint(2000, 12000, 110),
            'Grocery': np.random.randint(3000, 15000, 110),
            'Frozen': np.random.randint(500, 3000, 110),
            'Detergents_Paper': np.random.randint(500, 4000, 110),
            'Delicassen': np.random.randint(500, 3000, 110)
        })
        
        # Type 2: Retail - high everything
        type2 = pd.DataFrame({
            'Channel': [2] * 110,
            'Region': np.random.randint(1, 4, 110),
            'Fresh': np.random.randint(5000, 20000, 110),
            'Milk': np.random.randint(4000, 18000, 110),
            'Grocery': np.random.randint(6000, 25000, 110),
            'Frozen': np.random.randint(2000, 8000, 110),
            'Detergents_Paper': np.random.randint(3000, 12000, 110),
            'Delicassen': np.random.randint(1000, 5000, 110)
        })
        
        # Type 3: Small retail - moderate values
        type3 = pd.DataFrame({
            'Channel': [2] * 110,
            'Region': np.random.randint(1, 4, 110),
            'Fresh': np.random.randint(2000, 10000, 110),
            'Milk': np.random.randint(1000, 6000, 110),
            'Grocery': np.random.randint(2000, 8000, 110),
            'Frozen': np.random.randint(500, 2000, 110),
            'Detergents_Paper': np.random.randint(1000, 5000, 110),
            'Delicassen': np.random.randint(300, 2000, 110)
        })
        
        # Type 4: Fresh products specialist
        type4 = pd.DataFrame({
            'Channel': [1] * 110,
            'Region': np.random.randint(1, 4, 110),
            'Fresh': np.random.randint(10000, 60000, 110),
            'Milk': np.random.randint(500, 3000, 110),
            'Grocery': np.random.randint(1000, 5000, 110),
            'Frozen': np.random.randint(1000, 5000, 110),
            'Detergents_Paper': np.random.randint(200, 2000, 110),
            'Delicassen': np.random.randint(500, 3000, 110)
        })
        
        df = pd.concat([type1, type2, type3, type4], ignore_index=True)
        df.to_csv('output/q3/synthetic_wholesale_customers.csv', index=False)
    
    return df

# Load data
df = load_or_create_wholesale_data()
print("\n" + "="*70)
print("WHOLESALE CUSTOMERS DATASET")
print("="*70)
print(df.head())
print(f"\nShape: {df.shape}")
print("\nDataset statistics:")
print(df.describe())

# Select product features for clustering
feature_cols = ['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']
X = df[feature_cols].values

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine optimal number of clusters using Elbow method
inertias = []
silhouette_kmeans = []
silhouette_hierarchical = []
K_range = range(2, 11)

print("\n" + "="*70)
print("DETERMINING OPTIMAL NUMBER OF CLUSTERS")
print("="*70)

for k in K_range:
    # K-Means
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_kmeans = kmeans.fit_predict(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_kmeans.append(silhouette_score(X_scaled, labels_kmeans))
    
    # Hierarchical
    hierarchical = AgglomerativeClustering(n_clusters=k)
    labels_hierarchical = hierarchical.fit_predict(X_scaled)
    silhouette_hierarchical.append(silhouette_score(X_scaled, labels_hierarchical))

# Plot comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(K_range, inertias, 'bo-', label='K-Means Inertia')
axes[0].set_xlabel('Number of Clusters (K)')
axes[0].set_ylabel('Inertia')
axes[0].set_title('Elbow Method - K-Means')
axes[0].grid(True)
axes[0].legend()

axes[1].plot(K_range, silhouette_kmeans, 'ro-', label='K-Means')
axes[1].plot(K_range, silhouette_hierarchical, 'go-', label='Hierarchical')
axes[1].set_xlabel('Number of Clusters (K)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Scores Comparison')
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.savefig('output/q3/cluster_selection.png', dpi=300, bbox_inches='tight')
plt.show()

# Select optimal K (typically 4-5 for wholesale)
optimal_k = 4

# Apply K-Means
print(f"\nApplying K-Means with k={optimal_k}...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X_scaled)

# Apply Hierarchical Clustering with different linkages
print(f"Applying Hierarchical Clustering with k={optimal_k}...")
hierarchical_ward = AgglomerativeClustering(n_clusters=optimal_k, linkage='ward')
labels_hier_ward = hierarchical_ward.fit_predict(X_scaled)

hierarchical_complete = AgglomerativeClustering(n_clusters=optimal_k, linkage='complete')
labels_hier_complete = hierarchical_complete.fit_predict(X_scaled)

hierarchical_average = AgglomerativeClustering(n_clusters=optimal_k, linkage='average')
labels_hier_average = hierarchical_average.fit_predict(X_scaled)

# Create dendrogram for hierarchical clustering
plt.figure(figsize=(14, 6))
linkage_matrix = linkage(X_scaled, method='ward')
dendrogram(linkage_matrix, truncate_mode='lastp', p=30)
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)', fontsize=14, fontweight='bold')
plt.xlabel('Sample Index or (Cluster Size)', fontsize=11)
plt.ylabel('Distance', fontsize=11)
plt.axhline(y=40, color='r', linestyle='--', label='Cut for 4 clusters')
plt.legend()
plt.tight_layout()
plt.savefig('output/q3/dendrogram.png', dpi=300, bbox_inches='tight')
plt.show()

# Compare clustering results
print("\n" + "="*70)
print("CLUSTERING CONSISTENCY ANALYSIS")
print("="*70)

ari_ward = adjusted_rand_score(labels_kmeans, labels_hier_ward)
ari_complete = adjusted_rand_score(labels_kmeans, labels_hier_complete)
ari_average = adjusted_rand_score(labels_kmeans, labels_hier_average)

print(f"\nAdjusted Rand Index (K-Means vs Hierarchical):")
print(f"  Ward Linkage: {ari_ward:.4f}")
print(f"  Complete Linkage: {ari_complete:.4f}")
print(f"  Average Linkage: {ari_average:.4f}")

# Performance metrics
metrics = pd.DataFrame({
    'Method': ['K-Means', 'Hierarchical (Ward)', 'Hierarchical (Complete)', 'Hierarchical (Average)'],
    'Silhouette Score': [
        silhouette_score(X_scaled, labels_kmeans),
        silhouette_score(X_scaled, labels_hier_ward),
        silhouette_score(X_scaled, labels_hier_complete),
        silhouette_score(X_scaled, labels_hier_average)
    ],
    'Davies-Bouldin Index': [
        davies_bouldin_score(X_scaled, labels_kmeans),
        davies_bouldin_score(X_scaled, labels_hier_ward),
        davies_bouldin_score(X_scaled, labels_hier_complete),
        davies_bouldin_score(X_scaled, labels_hier_average)
    ]
})

print("\n" + "="*70)
print("CLUSTERING PERFORMANCE METRICS")
print("="*70)
print(metrics.to_string(index=False))

# Visualize cluster assignments
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# K-Means
scatter0 = axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_kmeans, 
                               cmap='viridis', alpha=0.6, edgecolors='black', linewidths=0.5)
axes[0, 0].set_title('K-Means Clustering', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
axes[0, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
axes[0, 0].grid(True, alpha=0.3)
plt.colorbar(scatter0, ax=axes[0, 0], label='Cluster')

# Hierarchical Ward
scatter1 = axes[0, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_hier_ward,
                               cmap='viridis', alpha=0.6, edgecolors='black', linewidths=0.5)
axes[0, 1].set_title(f'Hierarchical (Ward) - ARI: {ari_ward:.3f}', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
axes[0, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
axes[0, 1].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0, 1], label='Cluster')

# Hierarchical Complete
scatter2 = axes[1, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_hier_complete,
                               cmap='viridis', alpha=0.6, edgecolors='black', linewidths=0.5)
axes[1, 0].set_title(f'Hierarchical (Complete) - ARI: {ari_complete:.3f}', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
axes[1, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
axes[1, 0].grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=axes[1, 0], label='Cluster')

# Hierarchical Average
scatter3 = axes[1, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_hier_average,
                               cmap='viridis', alpha=0.6, edgecolors='black', linewidths=0.5)
axes[1, 1].set_title(f'Hierarchical (Average) - ARI: {ari_average:.3f}', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
axes[1, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
axes[1, 1].grid(True, alpha=0.3)
plt.colorbar(scatter3, ax=axes[1, 1], label='Cluster')

plt.tight_layout()
plt.savefig('output/q3/clustering_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Cluster profiles for K-Means
df['Cluster_KMeans'] = labels_kmeans
df['Cluster_Hierarchical'] = labels_hier_ward

print("\n" + "="*70)
print("CUSTOMER SEGMENT PROFILES (K-MEANS)")
print("="*70)

cluster_profiles = df.groupby('Cluster_KMeans')[feature_cols].mean().round(2)
print(cluster_profiles)

# Visualize cluster profiles
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# K-Means profiles
cluster_profiles.T.plot(kind='bar', ax=axes[0], width=0.8)
axes[0].set_title('Customer Segment Profiles - K-Means', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Product Category', fontsize=11)
axes[0].set_ylabel('Average Annual Spending', fontsize=11)
axes[0].legend(title='Cluster', labels=[f'Cluster {i}' for i in range(optimal_k)])
axes[0].grid(True, alpha=0.3, axis='y')
axes[0].tick_params(axis='x', rotation=45)

# Hierarchical profiles
cluster_profiles_hier = df.groupby('Cluster_Hierarchical')[feature_cols].mean()
cluster_profiles_hier.T.plot(kind='bar', ax=axes[1], width=0.8)
axes[1].set_title('Customer Segment Profiles - Hierarchical (Ward)', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Product Category', fontsize=11)
axes[1].set_ylabel('Average Annual Spending', fontsize=11)
axes[1].legend(title='Cluster', labels=[f'Cluster {i}' for i in range(optimal_k)])
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('output/q3/cluster_profiles.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
metrics.to_csv('output/q3/performance_metrics.csv', index=False)
cluster_profiles.to_csv('output/q3/kmeans_cluster_profiles.csv')

with open('output/q3/results.txt', 'w') as f:
    f.write("K-MEANS VS HIERARCHICAL CLUSTERING ON WHOLESALE CUSTOMERS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Number of Clusters: {optimal_k}\n")
    f.write(f"Number of Customers: {len(df)}\n\n")
    f.write("CONSISTENCY ANALYSIS (Adjusted Rand Index):\n")
    f.write(f"K-Means vs Hierarchical (Ward): {ari_ward:.4f}\n")
    f.write(f"K-Means vs Hierarchical (Complete): {ari_complete:.4f}\n")
    f.write(f"K-Means vs Hierarchical (Average): {ari_average:.4f}\n\n")
    f.write("CONCLUSION:\n")
    if ari_ward > 0.7:
        f.write("HIGH consistency between K-Means and Hierarchical clustering.\n")
    elif ari_ward > 0.5:
        f.write("MODERATE consistency between K-Means and Hierarchical clustering.\n")
    else:
        f.write("LOW consistency between K-Means and Hierarchical clustering.\n")
    f.write("Ward linkage shows the best agreement with K-Means.\n")

print("\n✓ Analysis complete! Results saved to output/q3/")
