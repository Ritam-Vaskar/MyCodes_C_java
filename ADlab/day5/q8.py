"""
Q8: Clustering Stability on Mall Customers Dataset
How does clustering stability vary across different sampling of the Mall Customers dataset?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
import os

os.makedirs('output/q8', exist_ok=True)

print("="*70)
print("CLUSTERING STABILITY ANALYSIS ON MALL CUSTOMERS")
print("="*70)

# Generate synthetic mall customers data
np.random.seed(42)
n_samples = 200

high_high = pd.DataFrame({
    'Annual Income (k$)': np.random.randint(70, 140, 50),
    'Spending Score (1-100)': np.random.randint(60, 100, 50)
})
high_low = pd.DataFrame({
    'Annual Income (k$)': np.random.randint(70, 140, 50),
    'Spending Score (1-100)': np.random.randint(1, 40, 50)
})
low_low = pd.DataFrame({
    'Annual Income (k$)': np.random.randint(15, 50, 50),
    'Spending Score (1-100)': np.random.randint(1, 40, 50)
})
low_high = pd.DataFrame({
    'Annual Income (k$)': np.random.randint(15, 50, 50),
    'Spending Score (1-100)': np.random.randint(60, 100, 50)
})

df = pd.concat([high_high, high_low, low_low, low_high], ignore_index=True)
X = df.values

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Baseline clustering
kmeans_base = KMeans(n_clusters=5, random_state=42, n_init=10)
labels_base = kmeans_base.fit_predict(X_scaled)

# Test stability with different sampling ratios
sampling_ratios = [0.5, 0.6, 0.7, 0.8, 0.9]
n_iterations = 30

stability_results = []

print("\nTesting stability across different sampling ratios...")
for ratio in sampling_ratios:
    ari_scores = []
    
    for iteration in range(n_iterations):
        # Sample data
        n_sample = int(len(X_scaled) * ratio)
        indices = np.random.choice(len(X_scaled), n_sample, replace=False)
        X_sample = X_scaled[indices]
        
        # Cluster sampled data
        kmeans = KMeans(n_clusters=5, random_state=iteration, n_init=10)
        labels_sample = kmeans.fit_predict(X_sample)
        
        # Get labels for all data from fitted model
        labels_full = kmeans.predict(X_scaled)
        
        # Calculate ARI with baseline
        ari = adjusted_rand_score(labels_base, labels_full)
        ari_scores.append(ari)
    
    stability_results.append({
        'Sampling Ratio': ratio,
        'Mean ARI': np.mean(ari_scores),
        'Std ARI': np.std(ari_scores),
        'Min ARI': np.min(ari_scores),
        'Max ARI': np.max(ari_scores)
    })
    print(f"Ratio {ratio:.1f}: Mean ARI = {np.mean(ari_scores):.4f} ± {np.std(ari_scores):.4f}")

stability_df = pd.DataFrame(stability_results)

# Plot stability results
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Mean ARI with error bars
axes[0].errorbar(stability_df['Sampling Ratio'], stability_df['Mean ARI'],
                 yerr=stability_df['Std ARI'], marker='o', capsize=5, linewidth=2)
axes[0].set_xlabel('Sampling Ratio', fontsize=11)
axes[0].set_ylabel('Adjusted Rand Index', fontsize=11)
axes[0].set_title('Clustering Stability vs Sampling Ratio', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Min-Max range
axes[1].fill_between(stability_df['Sampling Ratio'], 
                      stability_df['Min ARI'], 
                      stability_df['Max ARI'], 
                      alpha=0.3, label='Min-Max Range')
axes[1].plot(stability_df['Sampling Ratio'], stability_df['Mean ARI'], 
             'r-o', linewidth=2, label='Mean ARI')
axes[1].set_xlabel('Sampling Ratio', fontsize=11)
axes[1].set_ylabel('Adjusted Rand Index', fontsize=11)
axes[1].set_title('ARI Range Across Iterations', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/q8/stability_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Test stability with bootstrap resampling
print("\nBootstrap Stability Analysis (100 iterations)...")
bootstrap_ari = []

for i in range(100):
    # Bootstrap sample
    indices = np.random.choice(len(X_scaled), len(X_scaled), replace=True)
    X_bootstrap = X_scaled[indices]
    
    # Cluster
    kmeans = KMeans(n_clusters=5, random_state=i, n_init=10)
    labels_bootstrap = kmeans.fit_predict(X_bootstrap)
    
    # Predict on full data
    labels_full = kmeans.predict(X_scaled)
    
    # Calculate ARI
    ari = adjusted_rand_score(labels_base, labels_full)
    bootstrap_ari.append(ari)

print(f"Bootstrap Mean ARI: {np.mean(bootstrap_ari):.4f} ± {np.std(bootstrap_ari):.4f}")

# Visualize bootstrap distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(bootstrap_ari, bins=20, edgecolor='black', alpha=0.7)
axes[0].axvline(np.mean(bootstrap_ari), color='red', linestyle='--', linewidth=2, label='Mean')
axes[0].set_xlabel('Adjusted Rand Index', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Bootstrap ARI Distribution', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Box plot
axes[1].boxplot([bootstrap_ari], labels=['Bootstrap ARI'])
axes[1].set_ylabel('Adjusted Rand Index', fontsize=11)
axes[1].set_title('Bootstrap ARI Statistics', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/q8/bootstrap_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualize baseline clustering
plt.figure(figsize=(10, 7))
colors = ['red', 'blue', 'green', 'orange', 'purple']
for i in range(5):
    mask = labels_base == i
    plt.scatter(df.iloc[mask, 0], df.iloc[mask, 1], c=colors[i], 
                label=f'Cluster {i}', alpha=0.6, s=50)

centroids = scaler.inverse_transform(kmeans_base.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='X', 
            s=300, edgecolors='yellow', linewidths=2, label='Centroids')

plt.xlabel('Annual Income (k$)', fontsize=12)
plt.ylabel('Spending Score (1-100)', fontsize=12)
plt.title('Baseline K-Means Clustering', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('output/q8/baseline_clustering.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
stability_df.to_csv('output/q8/stability_results.csv', index=False)

with open('output/q8/results.txt', 'w') as f:
    f.write("CLUSTERING STABILITY ANALYSIS\n")
    f.write("="*70 + "\n\n")
    f.write("SAMPLING STABILITY:\n")
    f.write(stability_df.to_string(index=False))
    f.write(f"\n\nBOOTSTRAP STABILITY:\n")
    f.write(f"Mean ARI: {np.mean(bootstrap_ari):.4f}\n")
    f.write(f"Std ARI: {np.std(bootstrap_ari):.4f}\n")
    f.write(f"95% CI: [{np.percentile(bootstrap_ari, 2.5):.4f}, {np.percentile(bootstrap_ari, 97.5):.4f}]\n")
    f.write("\nCONCLUSION:\n")
    if np.mean(bootstrap_ari) > 0.8:
        f.write("HIGH stability - clustering is robust to sampling variations.\n")
    elif np.mean(bootstrap_ari) > 0.6:
        f.write("MODERATE stability - some variation across samples.\n")
    else:
        f.write("LOW stability - significant variation across samples.\n")

print("\n✓ Analysis complete! Results saved to output/q8/")
