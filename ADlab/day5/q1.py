"""
Q1: K-Means Clustering on Mall Customers Dataset
Apply K-Means clustering to group customers based on purchasing patterns.
Analyze clusters to identify customer groups.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import os

# Create output directory
os.makedirs('output/q1', exist_ok=True)

# Since we may not have the actual Mall Customers dataset, let's create synthetic data
# Or try to load from a common location
def load_or_create_mall_data():
    """Load Mall Customers dataset or create synthetic data"""
    try:
        # Try to load from common locations
        df = pd.read_csv('Mall_Customers.csv')
        print("Loaded Mall Customers dataset")
    except:
        print("Creating synthetic Mall Customers dataset...")
        np.random.seed(42)
        n_samples = 200
        
        # Create customer segments
        # Segment 1: High income, high spending
        high_high = pd.DataFrame({
            'CustomerID': range(1, 51),
            'Gender': np.random.choice(['Male', 'Female'], 50),
            'Age': np.random.randint(25, 40, 50),
            'Annual Income (k$)': np.random.randint(70, 140, 50),
            'Spending Score (1-100)': np.random.randint(60, 100, 50)
        })
        
        # Segment 2: High income, low spending
        high_low = pd.DataFrame({
            'CustomerID': range(51, 101),
            'Gender': np.random.choice(['Male', 'Female'], 50),
            'Age': np.random.randint(35, 60, 50),
            'Annual Income (k$)': np.random.randint(70, 140, 50),
            'Spending Score (1-100)': np.random.randint(1, 40, 50)
        })
        
        # Segment 3: Low income, low spending
        low_low = pd.DataFrame({
            'CustomerID': range(101, 151),
            'Gender': np.random.choice(['Male', 'Female'], 50),
            'Age': np.random.randint(20, 50, 50),
            'Annual Income (k$)': np.random.randint(15, 50, 50),
            'Spending Score (1-100)': np.random.randint(1, 40, 50)
        })
        
        # Segment 4: Low income, high spending
        low_high = pd.DataFrame({
            'CustomerID': range(151, 201),
            'Gender': np.random.choice(['Male', 'Female'], 50),
            'Age': np.random.randint(18, 35, 50),
            'Annual Income (k$)': np.random.randint(15, 50, 50),
            'Spending Score (1-100)': np.random.randint(60, 100, 50)
        })
        
        df = pd.concat([high_high, high_low, low_low, low_high], ignore_index=True)
        df.to_csv('output/q1/synthetic_mall_customers.csv', index=False)
    
    return df

# Load data
df = load_or_create_mall_data()
print("\nDataset Info:")
print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nColumn names: {df.columns.tolist()}")

# Select features for clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine optimal number of clusters using Elbow method
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

# Plot Elbow curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(K_range, inertias, 'bo-')
ax1.set_xlabel('Number of Clusters (K)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method For Optimal K')
ax1.grid(True)

ax2.plot(K_range, silhouette_scores, 'ro-')
ax2.set_xlabel('Number of Clusters (K)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score For Different K')
ax2.grid(True)

plt.tight_layout()
plt.savefig('output/q1/elbow_method.png', dpi=300, bbox_inches='tight')
plt.show()

# Apply K-Means with optimal K (typically 5 for mall customers)
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Get cluster centers in original scale
cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)

# Visualization 1: 2D scatter plot with clusters
plt.figure(figsize=(12, 8))
colors = ['red', 'blue', 'green', 'orange', 'purple']

for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    plt.scatter(cluster_data['Annual Income (k$)'], 
                cluster_data['Spending Score (1-100)'],
                c=colors[i], label=f'Cluster {i}', alpha=0.6, s=50)

# Plot centroids
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1],
            c='black', marker='X', s=300, edgecolors='yellow', 
            linewidths=2, label='Centroids')

plt.xlabel('Annual Income (k$)', fontsize=12)
plt.ylabel('Spending Score (1-100)', fontsize=12)
plt.title('Customer Segments - K-Means Clustering', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('output/q1/customer_segments.png', dpi=300, bbox_inches='tight')
plt.show()

# Cluster Analysis
print("\n" + "="*70)
print("CLUSTER ANALYSIS")
print("="*70)

cluster_analysis = df.groupby('Cluster').agg({
    'Age': ['mean', 'std'],
    'Annual Income (k$)': ['mean', 'std'],
    'Spending Score (1-100)': ['mean', 'std'],
    'CustomerID': 'count'
}).round(2)

cluster_analysis.columns = ['_'.join(col).strip() for col in cluster_analysis.columns.values]
cluster_analysis.rename(columns={'CustomerID_count': 'Customer_Count'}, inplace=True)

print(cluster_analysis)

# Detailed cluster characterization
print("\n" + "="*70)
print("CUSTOMER GROUP CHARACTERIZATION")
print("="*70)

for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    avg_income = cluster_data['Annual Income (k$)'].mean()
    avg_spending = cluster_data['Spending Score (1-100)'].mean()
    count = len(cluster_data)
    
    print(f"\nCluster {i} ({count} customers):")
    print(f"  Average Annual Income: ${avg_income:.2f}k")
    print(f"  Average Spending Score: {avg_spending:.2f}/100")
    
    # Characterize the cluster
    if avg_income > 70 and avg_spending > 60:
        category = "HIGH-INCOME, HIGH-SPENDING (Premium Customers)"
        strategy = "Target with premium products and exclusive offers"
    elif avg_income > 70 and avg_spending < 40:
        category = "HIGH-INCOME, LOW-SPENDING (Careful Spenders)"
        strategy = "Focus on value propositions and quality over quantity"
    elif avg_income < 50 and avg_spending > 60:
        category = "LOW-INCOME, HIGH-SPENDING (Impulsive Buyers)"
        strategy = "Offer affordable luxury and installment plans"
    elif avg_income < 50 and avg_spending < 40:
        category = "LOW-INCOME, LOW-SPENDING (Budget Conscious)"
        strategy = "Provide budget-friendly options and discounts"
    else:
        category = "MODERATE INCOME & SPENDING (Average Customers)"
        strategy = "Maintain engagement with balanced product mix"
    
    print(f"  Category: {category}")
    print(f"  Marketing Strategy: {strategy}")

# Save cluster analysis
cluster_analysis.to_csv('output/q1/cluster_analysis.csv')

# Additional visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Distribution of customers across clusters
axes[0, 0].bar(range(optimal_k), df['Cluster'].value_counts().sort_index(), color=colors)
axes[0, 0].set_xlabel('Cluster')
axes[0, 0].set_ylabel('Number of Customers')
axes[0, 0].set_title('Customer Distribution Across Clusters')
axes[0, 0].grid(True, alpha=0.3)

# Average income by cluster
avg_income_by_cluster = df.groupby('Cluster')['Annual Income (k$)'].mean()
axes[0, 1].bar(range(optimal_k), avg_income_by_cluster, color=colors)
axes[0, 1].set_xlabel('Cluster')
axes[0, 1].set_ylabel('Average Annual Income (k$)')
axes[0, 1].set_title('Average Income by Cluster')
axes[0, 1].grid(True, alpha=0.3)

# Average spending score by cluster
avg_spending_by_cluster = df.groupby('Cluster')['Spending Score (1-100)'].mean()
axes[1, 0].bar(range(optimal_k), avg_spending_by_cluster, color=colors)
axes[1, 0].set_xlabel('Cluster')
axes[1, 0].set_ylabel('Average Spending Score')
axes[1, 0].set_title('Average Spending Score by Cluster')
axes[1, 0].grid(True, alpha=0.3)

# Age distribution by cluster
df.boxplot(column='Age', by='Cluster', ax=axes[1, 1], patch_artist=True)
axes[1, 1].set_xlabel('Cluster')
axes[1, 1].set_ylabel('Age')
axes[1, 1].set_title('Age Distribution by Cluster')
plt.suptitle('')

plt.tight_layout()
plt.savefig('output/q1/cluster_statistics.png', dpi=300, bbox_inches='tight')
plt.show()

# Performance metrics
silhouette = silhouette_score(X_scaled, df['Cluster'])
davies_bouldin = davies_bouldin_score(X_scaled, df['Cluster'])

print("\n" + "="*70)
print("CLUSTERING PERFORMANCE METRICS")
print("="*70)
print(f"Silhouette Score: {silhouette:.4f} (higher is better, range: -1 to 1)")
print(f"Davies-Bouldin Index: {davies_bouldin:.4f} (lower is better)")
print(f"Inertia: {kmeans.inertia_:.4f}")

# Save results
with open('output/q1/results.txt', 'w') as f:
    f.write("K-MEANS CLUSTERING ON MALL CUSTOMERS DATASET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Number of Clusters: {optimal_k}\n")
    f.write(f"Number of Customers: {len(df)}\n\n")
    f.write("PERFORMANCE METRICS:\n")
    f.write(f"Silhouette Score: {silhouette:.4f}\n")
    f.write(f"Davies-Bouldin Index: {davies_bouldin:.4f}\n")
    f.write(f"Inertia: {kmeans.inertia_:.4f}\n\n")
    f.write("CLUSTER CENTERS (Original Scale):\n")
    f.write(str(pd.DataFrame(cluster_centers, 
                             columns=['Annual Income (k$)', 'Spending Score (1-100)'])))

print("\n✓ Analysis complete! Results saved to output/q1/")
