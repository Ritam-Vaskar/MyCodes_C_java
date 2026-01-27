"""
Q5: PCA for Digit Recognition using KNN - Optimal Components Analysis
Objective: Determine how many principal components are required to retain high digit 
recognition accuracy. Reduce 784 MNIST features and plot accuracy vs number of PCs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

def evaluate_digit_recognition():
    """Evaluate digit recognition with varying PCA components"""
    
    os.makedirs('output', exist_ok=True)
    
    print("="*70)
    print("DIGIT RECOGNITION WITH PCA - OPTIMAL COMPONENTS ANALYSIS")
    print("="*70)
    
    # Load digits dataset (8x8 = 64 features, subset of MNIST)
    print("\nLoading Digits dataset...")
    digits = load_digits()
    X = digits.data
    y = digits.target
    
    print(f"Dataset shape: {X.shape}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Number of samples: {X.shape[0]}")
    print(f"Number of classes: {len(np.unique(y))}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Test WITHOUT PCA
    print("\n" + "="*70)
    print(f"EVALUATION WITHOUT PCA ({X.shape[1]} FEATURES)")
    print("="*70)
    
    knn_original = KNeighborsClassifier(n_neighbors=5)
    knn_original.fit(X_train_scaled, y_train)
    y_pred_original = knn_original.predict(X_test_scaled)
    acc_original = accuracy_score(y_test, y_pred_original)
    
    print(f"Accuracy: {acc_original:.4f}")
    
    results = [{
        'n_components': X.shape[1],
        'accuracy': acc_original,
        'variance_explained': 1.0
    }]
    
    # Test with varying PCA components
    component_range = list(range(1, 11)) + list(range(15, 65, 5))
    
    print(f"\nTesting PCA with components: {component_range}")
    print("="*70)
    
    for n_comp in component_range:
        pca = PCA(n_components=n_comp)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)
        
        variance_explained = sum(pca.explained_variance_ratio_)
        
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train_pca, y_train)
        y_pred = knn.predict(X_test_pca)
        acc = accuracy_score(y_test, y_pred)
        
        results.append({
            'n_components': n_comp,
            'accuracy': acc,
            'variance_explained': variance_explained
        })
        
        if n_comp in [5, 10, 20, 40]:
            print(f"Components: {n_comp:2d} | Accuracy: {acc:.4f} | Variance: {variance_explained:.4f}")
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df.to_csv('output/accuracy_vs_components.csv', index=False)
    
    print("\n" + "="*70)
    print("COMPLETE RESULTS")
    print("="*70)
    print(results_df.to_string(index=False))
    
    # Plot accuracy vs number of components
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    color = 'tab:blue'
    ax1.set_xlabel('Number of Principal Components', fontsize=13)
    ax1.set_ylabel('Accuracy', color=color, fontsize=13)
    ax1.plot(results_df['n_components'], results_df['accuracy'], 
            marker='o', linestyle='-', linewidth=2, markersize=6, color=color, label='Accuracy')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Add horizontal line for original accuracy
    ax1.axhline(y=acc_original, color='red', linestyle='--', 
               linewidth=2, label=f'Original ({X.shape[1]} features)', alpha=0.7)
    
    # Add horizontal line for 95% of original accuracy
    threshold_95 = 0.95 * acc_original
    ax1.axhline(y=threshold_95, color='orange', linestyle=':', 
               linewidth=2, label='95% of original', alpha=0.7)
    
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Variance Explained', color=color, fontsize=13)
    ax2.plot(results_df['n_components'], results_df['variance_explained'], 
            marker='s', linestyle='--', linewidth=2, markersize=6, color=color, label='Variance')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right', fontsize=10)
    
    plt.title('Digit Recognition: Accuracy vs Number of Principal Components', 
             fontsize=15, fontweight='bold', pad=20)
    fig.tight_layout()
    plt.savefig('output/accuracy_vs_components.png', dpi=300, bbox_inches='tight')
    print("\nAccuracy vs components plot saved!")
    plt.close()
    
    # Plot zoomed version for low components
    fig, ax = plt.subplots(figsize=(10, 6))
    
    low_comp_df = results_df[results_df['n_components'] <= 30]
    
    ax.plot(low_comp_df['n_components'], low_comp_df['accuracy'], 
           marker='o', linestyle='-', linewidth=2, markersize=8, color='steelblue')
    
    ax.axhline(y=acc_original, color='red', linestyle='--', 
              linewidth=2, label=f'Original accuracy: {acc_original:.4f}', alpha=0.7)
    ax.axhline(y=threshold_95, color='orange', linestyle=':', 
              linewidth=2, label=f'95% threshold: {threshold_95:.4f}', alpha=0.7)
    
    ax.set_xlabel('Number of Principal Components', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Digit Recognition: Accuracy (Low Component Range)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/accuracy_vs_components_zoomed.png', dpi=300, bbox_inches='tight')
    print("Zoomed accuracy plot saved!")
    plt.close()
    
    # Dimensionality reduction analysis
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Dimensionality reduction percentage
    ax = axes[0]
    reduction = 100 * (1 - results_df['n_components'] / X.shape[1])
    ax.bar(range(len(results_df)), reduction, color='skyblue', edgecolor='navy', alpha=0.7)
    ax.set_xlabel('Configuration Index', fontsize=12)
    ax.set_ylabel('Dimensionality Reduction (%)', fontsize=12)
    ax.set_title('Dimensionality Reduction Percentage', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Accuracy retention
    ax = axes[1]
    retention = 100 * results_df['accuracy'] / acc_original
    ax.bar(range(len(results_df)), retention, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
    ax.axhline(y=95, color='red', linestyle='--', linewidth=2, label='95% threshold')
    ax.set_xlabel('Configuration Index', fontsize=12)
    ax.set_ylabel('Accuracy Retention (%)', fontsize=12)
    ax.set_title('Accuracy Retention vs Original', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('output/dimensionality_analysis.png', dpi=300, bbox_inches='tight')
    print("Dimensionality analysis plot saved!")
    plt.close()
    
    # Find optimal number of components
    # Components needed for 95%, 98%, 99% accuracy retention
    threshold_98 = 0.98 * acc_original
    threshold_99 = 0.99 * acc_original
    
    n_comp_95 = results_df[results_df['accuracy'] >= threshold_95]['n_components'].min()
    n_comp_98 = results_df[results_df['accuracy'] >= threshold_98]['n_components'].min()
    n_comp_99 = results_df[results_df['accuracy'] >= threshold_99]['n_components'].min()
    
    # Components for variance thresholds
    var_threshold_90 = results_df[results_df['variance_explained'] >= 0.90]['n_components'].min()
    var_threshold_95 = results_df[results_df['variance_explained'] >= 0.95]['n_components'].min()
    var_threshold_99 = results_df[results_df['variance_explained'] >= 0.99]['n_components'].min()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY - OPTIMAL COMPONENTS ANALYSIS")
    print("="*70)
    
    print(f"\nOriginal performance ({X.shape[1]} features):")
    print(f"  Accuracy: {acc_original:.4f}")
    
    print(f"\nComponents needed for accuracy retention:")
    print(f"  95% accuracy ({threshold_95:.4f}): {n_comp_95} components")
    print(f"  98% accuracy ({threshold_98:.4f}): {n_comp_98} components")
    print(f"  99% accuracy ({threshold_99:.4f}): {n_comp_99} components")
    
    print(f"\nComponents needed for variance explained:")
    print(f"  90% variance: {var_threshold_90} components")
    print(f"  95% variance: {var_threshold_95} components")
    print(f"  99% variance: {var_threshold_99} components")
    
    print(f"\nDimensionality reduction:")
    print(f"  With {n_comp_95} components (95% accuracy): {100*(1-n_comp_95/X.shape[1]):.1f}% reduction")
    print(f"  With {n_comp_98} components (98% accuracy): {100*(1-n_comp_98/X.shape[1]):.1f}% reduction")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("Digit Recognition with PCA - Optimal Components Analysis\n")
        f.write("="*70 + "\n\n")
        f.write(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features, {len(np.unique(y))} classes\n\n")
        f.write(f"Original Performance:\n")
        f.write(f"  Features: {X.shape[1]}\n")
        f.write(f"  Accuracy: {acc_original:.4f}\n\n")
        
        f.write("Optimal Component Selection:\n")
        f.write(f"  For 95% accuracy retention: {n_comp_95} components ({100*(1-n_comp_95/X.shape[1]):.1f}% reduction)\n")
        f.write(f"  For 98% accuracy retention: {n_comp_98} components ({100*(1-n_comp_98/X.shape[1]):.1f}% reduction)\n")
        f.write(f"  For 99% accuracy retention: {n_comp_99} components ({100*(1-n_comp_99/X.shape[1]):.1f}% reduction)\n\n")
        
        f.write("Variance-based Selection:\n")
        f.write(f"  For 90% variance: {var_threshold_90} components\n")
        f.write(f"  For 95% variance: {var_threshold_95} components\n")
        f.write(f"  For 99% variance: {var_threshold_99} components\n\n")
        
        f.write("Recommendation:\n")
        f.write(f"  Use {n_comp_95}-{n_comp_98} components for optimal balance between\n")
        f.write(f"  dimensionality reduction and accuracy retention.\n")
    
    print("\nAll results saved successfully!")
    print("="*70)

if __name__ == "__main__":
    evaluate_digit_recognition()
