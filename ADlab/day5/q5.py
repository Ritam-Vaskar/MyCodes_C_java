"""
Q5: K-Means Clustering on Digits Dataset
Using the Digits dataset, how effective is K-Means in grouping handwritten digits?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import (confusion_matrix, adjusted_rand_score, 
                              normalized_mutual_info_score, homogeneity_score,
                              completeness_score, v_measure_score, silhouette_score)
import os

# Create output directory
os.makedirs('output/q5', exist_ok=True)

# Load Digits dataset
digits = load_digits()
X = digits.data
y_true = digits.target
images = digits.images

print("="*70)
print("K-MEANS CLUSTERING ON DIGITS DATASET")
print("="*70)
print(f"\nDataset shape: {X.shape}")
print(f"Number of digits: {len(X)}")
print(f"Number of features (pixels): {X.shape[1]}")
print(f"Digit classes: {np.unique(y_true)}")

# Visualize sample digits
fig, axes = plt.subplots(2, 10, figsize=(15, 3))
for i in range(10):
    for j in range(2):
        idx = np.where(y_true == i)[0][j]
        axes[j, i].imshow(images[idx], cmap='gray')
        axes[j, i].axis('off')
        if j == 0:
            axes[j, i].set_title(f'Digit {i}', fontsize=10)

plt.suptitle('Sample Handwritten Digits', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('output/q5/sample_digits.png', dpi=300, bbox_inches='tight')
plt.show()

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine optimal number of clusters
inertias = []
silhouette_scores = []
K_range = range(2, 21)

print("\nDetermining optimal number of clusters...")
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

# Plot elbow curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(K_range, inertias, 'bo-')
ax1.axvline(x=10, color='r', linestyle='--', label='k=10 (true classes)')
ax1.set_xlabel('Number of Clusters (K)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method For Optimal K')
ax1.legend()
ax1.grid(True)

ax2.plot(K_range, silhouette_scores, 'go-')
ax2.axvline(x=10, color='r', linestyle='--', label='k=10 (true classes)')
ax2.set_xlabel('Number of Clusters (K)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score For Different K')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('output/q5/elbow_method.png', dpi=300, bbox_inches='tight')
plt.show()

# Apply K-Means with k=10 (since we have 10 digits)
optimal_k = 10
print(f"\nApplying K-Means with k={optimal_k}...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
labels_pred = kmeans.fit_predict(X_scaled)

# Calculate metrics
metrics = {
    'Adjusted Rand Index': adjusted_rand_score(y_true, labels_pred),
    'Normalized Mutual Information': normalized_mutual_info_score(y_true, labels_pred),
    'Homogeneity': homogeneity_score(y_true, labels_pred),
    'Completeness': completeness_score(y_true, labels_pred),
    'V-Measure': v_measure_score(y_true, labels_pred),
    'Silhouette Score': silhouette_score(X_scaled, labels_pred)
}

print("\n" + "="*70)
print("CLUSTERING PERFORMANCE METRICS")
print("="*70)
for metric, value in metrics.items():
    print(f"{metric:.<40} {value:.4f}")

# Create mapping from clusters to true labels (find best match)
def find_cluster_digit_mapping(true_labels, cluster_labels, n_clusters):
    """Find the best mapping from clusters to digits"""
    mapping = {}
    for cluster in range(n_clusters):
        mask = cluster_labels == cluster
        if np.sum(mask) > 0:
            # Find most common true label in this cluster
            most_common = np.bincount(true_labels[mask]).argmax()
            mapping[cluster] = most_common
    return mapping

cluster_to_digit = find_cluster_digit_mapping(y_true, labels_pred, optimal_k)
labels_mapped = np.array([cluster_to_digit.get(label, -1) for label in labels_pred])

# Confusion matrix
cm = confusion_matrix(y_true, labels_mapped)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Count'})
plt.xlabel('Predicted Digit', fontsize=12)
plt.ylabel('True Digit', fontsize=12)
plt.title('Confusion Matrix: K-Means Clustering on Digits', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/q5/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Cluster purity analysis
print("\n" + "="*70)
print("CLUSTER PURITY ANALYSIS")
print("="*70)

cluster_analysis = []
for cluster in range(optimal_k):
    mask = labels_pred == cluster
    cluster_size = np.sum(mask)
    if cluster_size > 0:
        true_labels_in_cluster = y_true[mask]
        unique, counts = np.unique(true_labels_in_cluster, return_counts=True)
        dominant_digit = unique[np.argmax(counts)]
        purity = counts.max() / cluster_size
        
        cluster_analysis.append({
            'Cluster': cluster,
            'Size': cluster_size,
            'Dominant Digit': dominant_digit,
            'Purity': purity,
            'Distribution': dict(zip(unique, counts))
        })
        
        print(f"\nCluster {cluster} (n={cluster_size}):")
        print(f"  Dominant Digit: {dominant_digit}")
        print(f"  Purity: {purity:.2%}")
        print(f"  Distribution: {dict(zip(unique, counts))}")

# Visualize cluster centroids
centroids = kmeans.cluster_centers_
centroids_original = scaler.inverse_transform(centroids)

fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for i in range(optimal_k):
    ax = axes[i // 5, i % 5]
    centroid_image = centroids_original[i].reshape(8, 8)
    im = ax.imshow(centroid_image, cmap='gray')
    ax.set_title(f'Cluster {i}\n(Digit {cluster_to_digit.get(i, "?")})', fontsize=10)
    ax.axis('off')

plt.suptitle('Cluster Centroids (Average Digit in Each Cluster)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('output/q5/cluster_centroids.png', dpi=300, bbox_inches='tight')
plt.show()

# PCA visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# True labels
scatter0 = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=y_true, cmap='tab10',
                           alpha=0.6, s=20, edgecolors='none')
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)', fontsize=11)
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)', fontsize=11)
axes[0].set_title('True Digit Labels', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)
plt.colorbar(scatter0, ax=axes[0], label='Digit', ticks=range(10))

# Predicted clusters
scatter1 = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_pred, cmap='tab10',
                           alpha=0.6, s=20, edgecolors='none')
axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)', fontsize=11)
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)', fontsize=11)
axes[1].set_title('K-Means Cluster Assignments', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[1], label='Cluster', ticks=range(10))

plt.tight_layout()
plt.savefig('output/q5/pca_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# Show correctly and incorrectly clustered examples
correct_mask = labels_mapped == y_true
incorrect_mask = ~correct_mask

accuracy = np.sum(correct_mask) / len(y_true)

print("\n" + "="*70)
print("CLUSTERING ACCURACY")
print("="*70)
print(f"Correctly clustered: {np.sum(correct_mask)} / {len(y_true)}")
print(f"Accuracy: {accuracy:.2%}")

# Visualize some misclassifications
if np.sum(incorrect_mask) > 0:
    fig, axes = plt.subplots(2, 10, figsize=(15, 3))
    incorrect_indices = np.where(incorrect_mask)[0][:20]
    
    for i, idx in enumerate(incorrect_indices):
        ax = axes[i // 10, i % 10]
        ax.imshow(images[idx], cmap='gray')
        ax.set_title(f'T:{y_true[idx]}\nP:{labels_mapped[idx]}', fontsize=8)
        ax.axis('off')
    
    plt.suptitle('Misclassified Examples (T=True, P=Predicted)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('output/q5/misclassified_examples.png', dpi=300, bbox_inches='tight')
    plt.show()

# Evaluate effectiveness for each digit
digit_effectiveness = []
for digit in range(10):
    digit_mask = y_true == digit
    digit_correct = np.sum((labels_mapped == y_true) & digit_mask)
    digit_total = np.sum(digit_mask)
    digit_accuracy = digit_correct / digit_total if digit_total > 0 else 0
    
    digit_effectiveness.append({
        'Digit': digit,
        'Total Samples': digit_total,
        'Correctly Clustered': digit_correct,
        'Accuracy': digit_accuracy
    })

effectiveness_df = pd.DataFrame(digit_effectiveness)

print("\n" + "="*70)
print("EFFECTIVENESS BY DIGIT")
print("="*70)
print(effectiveness_df.to_string(index=False))

# Plot effectiveness
plt.figure(figsize=(10, 6))
plt.bar(effectiveness_df['Digit'], effectiveness_df['Accuracy'], 
        color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel('Digit', fontsize=12)
plt.ylabel('Clustering Accuracy', fontsize=12)
plt.title('K-Means Effectiveness by Digit', fontsize=14, fontweight='bold')
plt.xticks(range(10))
plt.ylim(0, 1.0)
plt.grid(True, alpha=0.3, axis='y')
for i, v in enumerate(effectiveness_df['Accuracy']):
    plt.text(i, v + 0.02, f'{v:.2%}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('output/q5/effectiveness_by_digit.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
effectiveness_df.to_csv('output/q5/digit_effectiveness.csv', index=False)

with open('output/q5/results.txt', 'w') as f:
    f.write("K-MEANS CLUSTERING ON DIGITS DATASET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Number of Clusters: {optimal_k}\n")
    f.write(f"Dataset Size: {len(X)}\n")
    f.write(f"Number of Features: {X.shape[1]}\n\n")
    f.write("PERFORMANCE METRICS:\n")
    for metric, value in metrics.items():
        f.write(f"  {metric}: {value:.4f}\n")
    f.write(f"\nClustering Accuracy: {accuracy:.2%}\n\n")
    f.write("CONCLUSION:\n")
    if accuracy > 0.8:
        f.write("K-Means is HIGHLY effective at grouping handwritten digits.\n")
    elif accuracy > 0.6:
        f.write("K-Means is MODERATELY effective at grouping handwritten digits.\n")
    else:
        f.write("K-Means has LIMITED effectiveness at grouping handwritten digits.\n")
    f.write("\nThe algorithm can identify general patterns in digit shapes,\n")
    f.write("but may struggle with digits that have similar visual features\n")
    f.write("or significant variation in writing style.\n")

print("\n✓ Analysis complete! Results saved to output/q5/")
